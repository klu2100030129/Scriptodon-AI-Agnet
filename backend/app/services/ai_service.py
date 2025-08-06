import requests
import json
from app.core.config import settings
from typing import List, Dict, Any
import asyncio

class AIService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.site_url = settings.OPENROUTER_SITE_URL
        self.site_name = settings.OPENROUTER_SITE_NAME
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "qwen/qwen-2.5-72b-instruct:free"  # Using the new OpenRouter model

    async def generate_test_cases(self, input_content: str, source_type: str) -> List[Dict[str, Any]]:
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            raise Exception("OpenRouter API key not configured. Please set OPENROUTER_API_KEY in your .env file. Get your API key from https://openrouter.ai/keys")
        
        prompt = self._build_test_case_prompt(input_content, source_type)
        
        try:
            response = await self._make_openrouter_request(prompt)
            return self._parse_test_cases_response(response)
        except Exception as e:
            raise Exception(f"Error generating test cases: {str(e)}")

    async def generate_automation_script(self, test_cases: List[Dict], script_type: str) -> str:
        """Generate automation script using templates"""
        try:
            # Import the script templates
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from script_templates import generate_script_content
            
            # Generate script using templates
            script_content = generate_script_content(test_cases, script_type)
            return script_content
        except Exception as e:
            raise Exception(f"Error generating automation script: {str(e)}")

    async def _make_openrouter_request(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                url=self.base_url,
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 401:
                raise Exception("OpenRouter API key is invalid or expired. Please check your API key at https://openrouter.ai/keys")
            elif response.status_code == 403:
                raise Exception("OpenRouter API access denied. Please check your account status and credits.")
            elif response.status_code == 429:
                raise Exception("OpenRouter API rate limit exceeded. Please try again later.")
            elif not response.ok:
                raise Exception(f"OpenRouter API request failed with status {response.status_code}: {response.text}")
            
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API request failed: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected response format from OpenRouter: {str(e)}")

    def _build_test_case_prompt(self, input_content: str, source_type: str) -> str:
        base_prompt = f"""
        Generate comprehensive test cases based on the following {source_type} input.
        Return the response as a JSON array with the following structure:
        [
            {{
                "title": "Test case title",
                "description": "Test case description",
                "steps": "Step 1. Do this\\nStep 2. Do that\\nStep 3. Verify this",
                "expected_result": "Expected outcome"
            }}
        ]
        
        Input content:
        {input_content}
        """
        return base_prompt

    def _build_script_prompt(self, test_cases: List[Dict], script_type: str) -> str:
        test_cases_text = json.dumps(test_cases, indent=2)
        
        if script_type == "playwright_python":
            framework = "Playwright with Python"
        elif script_type == "playwright_selenium":
            framework = "Playwright with Selenium"
        else:
            framework = "Playwright with Python"
        
        prompt = f"""
        Generate an automation script using {framework} based on the following test cases.
        The script should be complete and executable.
        
        Test cases:
        {test_cases_text}
        
        Generate a complete Python script that can run these test cases.
        """
        return prompt

    def _parse_test_cases_response(self, response_text: str) -> List[Dict[str, Any]]:
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: return a simple test case
                return [{
                    "title": "Generated Test Case",
                    "description": "Test case generated from input",
                    "steps": "1. Execute the test\n2. Verify results",
                    "expected_result": "Test should pass"
                }]
        except json.JSONDecodeError:
            # Fallback: return a simple test case
            return [{
                "title": "Generated Test Case",
                "description": "Test case generated from input",
                "steps": "1. Execute the test\n2. Verify results",
                "expected_result": "Test should pass"
            }] 