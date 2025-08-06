from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.input_source import InputSource
from app.models.test_case import TestCase
from app.models.test_run import TestRun

router = APIRouter()

def generate_html_report(test_cases, input_source, report_type="test_cases"):
    """Generate HTML report for test cases or test runs"""
    
    # Count statuses
    total_tests = len(test_cases)
    passed_tests = len([tc for tc in test_cases if tc.status.value == 'passed'])
    failed_tests = len([tc for tc in test_cases if tc.status.value == 'failed'])
    pending_tests = len([tc for tc in test_cases if tc.status.value == 'pending'])
    
    # Calculate success rate
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - {input_source.name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background-color: #f8f9fa;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            font-size: 2em;
            font-weight: 600;
        }}
        .summary-card p {{
            margin: 0;
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .total {{ color: #495057; }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .pending {{ color: #ffc107; }}
        .success-rate {{ color: #17a2b8; }}
        .test-cases {{
            padding: 30px;
        }}
        .test-case {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow: hidden;
        }}
        .test-case-header {{
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: between;
            align-items: center;
        }}
        .test-case-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #495057;
            margin: 0;
        }}
        .status-badge {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .status-passed {{
            background-color: #d4edda;
            color: #155724;
        }}
        .status-failed {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .status-pending {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .test-case-body {{
            padding: 20px;
        }}
        .test-case-section {{
            margin-bottom: 15px;
        }}
        .test-case-section h4 {{
            margin: 0 0 8px 0;
            color: #495057;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .test-case-section p {{
            margin: 0;
            color: #6c757d;
            line-height: 1.6;
        }}
        .steps {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            white-space: pre-line;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .test-case-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Test Report</h1>
            <p>{input_source.name} - {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3 class="total">{total_tests}</h3>
                <p>Total Tests</p>
            </div>
            <div class="summary-card">
                <h3 class="passed">{passed_tests}</h3>
                <p>Passed</p>
            </div>
            <div class="summary-card">
                <h3 class="failed">{failed_tests}</h3>
                <p>Failed</p>
            </div>
            <div class="summary-card">
                <h3 class="pending">{pending_tests}</h3>
                <p>Pending</p>
            </div>
            <div class="summary-card">
                <h3 class="success-rate">{success_rate:.1f}%</h3>
                <p>Success Rate</p>
            </div>
        </div>
        
        <div class="test-cases">
            <h2>Test Cases</h2>
"""
    
    for test_case in test_cases:
        status_class = f"status-{test_case.status.value}"
        status_text = test_case.status.value.upper()
        
        html_content += f"""
            <div class="test-case">
                <div class="test-case-header">
                    <h3 class="test-case-title">{test_case.title}</h3>
                    <span class="status-badge {status_class}">{status_text}</span>
                </div>
                <div class="test-case-body">
                    <div class="test-case-section">
                        <h4>Description</h4>
                        <p>{test_case.description or 'No description provided'}</p>
                    </div>
                    <div class="test-case-section">
                        <h4>Steps</h4>
                        <div class="steps">{test_case.steps}</div>
                    </div>
                    <div class="test-case-section">
                        <h4>Created</h4>
                        <p>{test_case.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>Generated by Scriptodon Test Automation Platform</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

@router.get("/test-cases/{input_source_id}/html")
async def export_test_cases_html(
    input_source_id: int,
    db: Session = Depends(get_db)
):
    """Export test cases to HTML format"""
    try:
        # Get input source
        input_source = db.query(InputSource).filter(InputSource.id == input_source_id).first()
        if not input_source:
            raise HTTPException(status_code=404, detail="Input source not found")
        
        # Get test cases
        test_cases = db.query(TestCase).filter(TestCase.input_source_id == input_source_id).all()
        
        if not test_cases:
            raise HTTPException(status_code=404, detail="No test cases found")
        
        # Generate HTML content
        html_content = generate_html_report(test_cases, input_source, "test_cases")
        
        return {
            "filename": f"test_report_{input_source.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            "content": html_content,
            "total_test_cases": len(test_cases)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_test_runs_html_report(test_runs, input_source):
    """Generate HTML report for test runs"""
    
    total_runs = len(test_runs)
    total_tests = sum(run.total_tests for run in test_runs)
    total_passed = sum(run.passed_tests for run in test_runs)
    total_failed = sum(run.failed_tests for run in test_runs)
    avg_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Runs Report - {input_source.name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background-color: #f8f9fa;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            font-size: 2em;
            font-weight: 600;
        }}
        .summary-card p {{
            margin: 0;
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .total {{ color: #495057; }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .success-rate {{ color: #17a2b8; }}
        .test-runs {{
            padding: 30px;
        }}
        .test-run {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow: hidden;
        }}
        .test-run-header {{
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: between;
            align-items: center;
        }}
        .test-run-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #495057;
            margin: 0;
        }}
        .test-run-body {{
            padding: 20px;
        }}
        .test-run-section {{
            margin-bottom: 15px;
        }}
        .test-run-section h4 {{
            margin: 0 0 8px 0;
            color: #495057;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .test-run-section p {{
            margin: 0;
            color: #6c757d;
            line-height: 1.6;
        }}
        .progress-bar {{
            width: 100%;
            height: 20px;
            background-color: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .test-run-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Test Runs Report</h1>
            <p>{input_source.name} - {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3 class="total">{total_runs}</h3>
                <p>Total Runs</p>
            </div>
            <div class="summary-card">
                <h3 class="total">{total_tests}</h3>
                <p>Total Tests</p>
            </div>
            <div class="summary-card">
                <h3 class="passed">{total_passed}</h3>
                <p>Passed</p>
            </div>
            <div class="summary-card">
                <h3 class="failed">{total_failed}</h3>
                <p>Failed</p>
            </div>
            <div class="summary-card">
                <h3 class="success-rate">{avg_success_rate:.1f}%</h3>
                <p>Avg Success Rate</p>
            </div>
        </div>
        
        <div class="test-runs">
            <h2>Test Runs</h2>
"""
    
    for test_run in test_runs:
        success_rate = (test_run.passed_tests / test_run.total_tests * 100) if test_run.total_tests > 0 else 0
        
        html_content += f"""
            <div class="test-run">
                <div class="test-run-header">
                    <h3 class="test-run-title">{test_run.name}</h3>
                    <span class="status-badge status-{test_run.status.lower()}">{test_run.status.upper()}</span>
                </div>
                <div class="test-run-body">
                    <div class="test-run-section">
                        <h4>Test Results</h4>
                        <p>Total: {test_run.total_tests} | Passed: {test_run.passed_tests} | Failed: {test_run.failed_tests}</p>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {success_rate}%"></div>
                        </div>
                        <p>Success Rate: {success_rate:.1f}%</p>
                    </div>
                    <div class="test-run-section">
                        <h4>Started</h4>
                        <p>{test_run.started_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>Generated by Scriptodon Test Automation Platform</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

@router.get("/test-runs/{input_source_id}/html")
async def export_test_runs_html(
    input_source_id: int,
    db: Session = Depends(get_db)
):
    """Export test runs to HTML format"""
    try:
        # Get input source
        input_source = db.query(InputSource).filter(InputSource.id == input_source_id).first()
        if not input_source:
            raise HTTPException(status_code=404, detail="Input source not found")
        
        # Get test runs
        test_runs = db.query(TestRun).filter(TestRun.input_source_id == input_source_id).all()
        
        if not test_runs:
            raise HTTPException(status_code=404, detail="No test runs found")
        
        # Generate HTML content
        html_content = generate_test_runs_html_report(test_runs, input_source)
        
        return {
            "filename": f"test_runs_report_{input_source.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            "content": html_content,
            "total_test_runs": len(test_runs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/manual-test-cases/{input_source_id}")
async def get_manual_test_cases(
    input_source_id: int,
    db: Session = Depends(get_db)
):
    """Get test cases formatted for manual testing"""
    try:
        # Get input source
        input_source = db.query(InputSource).filter(InputSource.id == input_source_id).first()
        if not input_source:
            raise HTTPException(status_code=404, detail="Input source not found")
        
        # Get test cases
        test_cases = db.query(TestCase).filter(TestCase.input_source_id == input_source_id).all()
        
        # Format for manual testing
        manual_test_cases = []
        for test_case in test_cases:
            manual_test_cases.append({
                'id': test_case.id,
                'title': test_case.title,
                'description': test_case.description,
                'steps': test_case.steps.split('\n') if test_case.steps else [],
                'expected_result': test_case.expected_result,
                'status': test_case.status.value,
                'is_automated': test_case.is_automated
            })
        
        return {
            "input_source": {
                "id": input_source.id,
                "name": input_source.name,
                "source_type": input_source.source_type.value
            },
            "test_cases": manual_test_cases,
            "total_count": len(manual_test_cases)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-test-case-status/{test_case_id}")
async def update_test_case_status(
    test_case_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update test case status for manual testing"""
    try:
        test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
        if not test_case:
            raise HTTPException(status_code=404, detail="Test case not found")
        
        # Validate status
        valid_statuses = ['pending', 'passed', 'failed', 'running']
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        # Update status
        test_case.status = status
        db.commit()
        db.refresh(test_case)
        
        return {
            "message": f"Test case status updated to {status}",
            "test_case_id": test_case_id,
            "new_status": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 