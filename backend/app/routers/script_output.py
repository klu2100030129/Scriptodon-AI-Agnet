from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import tempfile

from app.core.database import get_db
from app.schemas.script import ScriptCreate, ScriptResponse
from app.services.ai_service import AIService
from app.services.test_execution_service import TestExecutionService
from app.models.input_source import InputSource
from app.models.test_case import TestCase
from app.models.script import Script, ScriptType
from app.core.config import settings

router = APIRouter()
ai_service = AIService()
test_execution_service = TestExecutionService()

@router.post("/generate/{input_source_id}")
async def generate_automation_script(
    input_source_id: int,
    script_type: str = "playwright_python",
    db: Session = Depends(get_db)
):
    """Generate automation script from test cases"""
    try:
        # Get input source
        input_source = db.query(InputSource).filter(InputSource.id == input_source_id).first()
        if not input_source:
            raise HTTPException(status_code=404, detail="Input source not found")
        
        # Get test cases
        test_cases = db.query(TestCase).filter(TestCase.input_source_id == input_source_id).all()
        if not test_cases:
            raise HTTPException(
                status_code=404, 
                detail="No test cases found for this input source. Please generate test cases first before creating a script."
            )
        
        # Convert test cases to dict format
        test_cases_data = []
        for test_case in test_cases:
            test_cases_data.append({
                'title': test_case.title,
                'description': test_case.description,
                'steps': test_case.steps,
                'expected_result': test_case.expected_result
            })
        
        # Generate script using AI
        script_content = await ai_service.generate_automation_script(test_cases_data, script_type)
        
        # Determine script type enum
        if script_type == "playwright_python":
            script_type_enum = ScriptType.PLAYWRIGHT_PYTHON
        elif script_type == "playwright_selenium":
            script_type_enum = ScriptType.PLAYWRIGHT_SELENIUM
        else:
            script_type_enum = ScriptType.PLAYWRIGHT_PYTHON
        
        # Save script to database
        script = Script(
            name=f"Automation Script - {input_source.name}",
            script_type=script_type_enum,
            content=script_content,
            input_source_id=input_source_id
        )
        
        db.add(script)
        db.commit()
        db.refresh(script)
        
        # Save script to file
        import os
        from datetime import datetime
        
        # Create scripts directory if it doesn't exist
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in input_source.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        filename = f"{safe_name}_{timestamp}.py"
        file_path = os.path.join(scripts_dir, filename)
        
        # Write script content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Update script with file path
        script.file_path = file_path
        db.commit()
        
        return {
            "message": "Automation script generated successfully",
            "script_id": script.id,
            "script_name": script.name,
            "script_type": script.script_type.value,
            "file_path": file_path
        }
    except Exception as e:
        error_message = str(e)
        if "OpenRouter API key not configured" in error_message:
            raise HTTPException(
                status_code=500, 
                detail="AI service not configured. Please set OPENROUTER_API_KEY in your .env file. Get your API key from https://openrouter.ai/keys"
            )
        elif "No test cases found" in error_message:
            raise HTTPException(
                status_code=404,
                detail="No test cases found for this input source. Please generate test cases first before creating a script."
            )
        elif "OpenRouter API key is invalid" in error_message:
            raise HTTPException(
                status_code=500,
                detail="OpenRouter API key is invalid or expired. Please check your API key at https://openrouter.ai/keys"
            )
        else:
            raise HTTPException(status_code=500, detail=f"Failed to generate script: {error_message}")

@router.post("/execute/{script_id}")
async def execute_automation_script(
    script_id: int,
    db: Session = Depends(get_db)
):
    """Execute an automation script with automatic dependency installation and HTML report generation"""
    try:
        # Get script
        script = db.query(Script).filter(Script.id == script_id).first()
        if not script:
            raise HTTPException(status_code=404, detail="Script not found")
        
        # Debug script content
        print(f"Script ID: {script_id}")
        print(f"Script content type: {type(script.content)}")
        print(f"Script content length: {len(script.content) if script.content else 0}")
        print(f"Script type: {script.script_type.value}")
        print(f"Script file path: {script.file_path if hasattr(script, 'file_path') else None}")
        
        # Execute script with dependency installation and HTML report generation
        execution_result = await test_execution_service.run_automation_script_with_dependencies(
            script.content, 
            script.script_type.value,
            script.file_path if hasattr(script, 'file_path') else None,
            script_id
        )
        
        return {
            "script_id": script_id,
            "execution_result": execution_result,
            "html_report_path": execution_result.get("html_report_path")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scripts/{input_source_id}")
async def get_scripts(
    input_source_id: int,
    db: Session = Depends(get_db)
):
    """Get all scripts for an input source"""
    scripts = db.query(Script).filter(Script.input_source_id == input_source_id).all()
    return [
        {
            "id": script.id,
            "name": script.name,
            "script_type": script.script_type.value,
            "created_at": script.created_at.isoformat() if script.created_at else None,
            "download_url": f"/api/script-output/download/{script.id}"
        }
        for script in scripts
    ]

@router.get("/download/{script_id}")
async def download_script(
    script_id: int,
    db: Session = Depends(get_db)
):
    """Download a script as a file"""
    try:
        script = db.query(Script).filter(Script.id == script_id).first()
        if not script:
            raise HTTPException(status_code=404, detail="Script not found")
        
        # Determine file extension
        if script.script_type == ScriptType.PLAYWRIGHT_PYTHON:
            file_extension = "py"
        elif script.script_type == ScriptType.PLAYWRIGHT_SELENIUM:
            file_extension = "py"
        else:
            file_extension = "py"
        
        # Create filename (sanitize for safe download)
        safe_filename = "".join(c for c in script.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_filename = safe_filename.replace(' ', '_')
        filename = f"{safe_filename}.{file_extension}"
        
        # Create temporary file with UTF-8 encoding
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{file_extension}', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(script.content)
            temp_file_path = temp_file.name
        
        return FileResponse(
            path=temp_file_path,
            filename=filename,
            media_type='text/plain; charset=utf-8'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/scripts/{script_id}")
async def delete_script(
    script_id: int,
    db: Session = Depends(get_db)
):
    """Delete a specific script"""
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    db.delete(script)
    db.commit()
    return {"message": "Script deleted successfully"}

@router.get("/reports/{script_id}")
async def get_html_report(
    script_id: int,
    db: Session = Depends(get_db)
):
    """Get HTML report for a script execution"""
    try:
        import os
        import glob
        
        # Find the latest report for this script
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")
        report_pattern = os.path.join(reports_dir, f"test_report_{script_id}_*.html")
        report_files = glob.glob(report_pattern)
        
        if not report_files:
            raise HTTPException(status_code=404, detail="No HTML report found for this script")
        
        # Get the most recent report
        latest_report = max(report_files, key=os.path.getctime)
        
        return FileResponse(
            path=latest_report,
            media_type='text/html',
            filename=f"test_report_{script_id}.html"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 