import requests
import json
from app.core.config import settings
from typing import List, Dict, Any, Optional
import logging

# Configure logging to avoid exposing sensitive data
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.site_url = settings.OPENROUTER_SITE_URL
        self.site_name = settings.OPENROUTER_SITE_NAME
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "qwen/qwen-2.5-72b-instruct:free"  # Using the new OpenRouter model

    def _validate_api_key(self):
        """Validate API key without exposing it in error messages"""
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            raise Exception("OpenRouter API key not configured. Please set OPENROUTER_API_KEY in your .env file. Get your API key from https://openrouter.ai/keys")
        
        # Validate API key format (should start with sk-or-v1-)
        if not self.api_key.startswith("sk-or-v1-"):
            raise Exception("Invalid OpenRouter API key format. API key should start with 'sk-or-v1-'")

    async def chat_completion(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """
        General chat completion method for any conversation
        """
        self._validate_api_key()
        
        try:
            response = self._make_openrouter_request_with_messages(messages, model)
            return response
        except Exception as e:
            # Don't expose API key in error messages
            logger.error(f"Error in chat completion: {str(e)}")
            raise Exception(f"Error in chat completion: {str(e)}")

    async def generate_test_cases(self, input_content: str, source_type: str) -> List[Dict[str, Any]]:
        self._validate_api_key()
        
        prompt = self._build_test_case_prompt(input_content, source_type)
        
        try:
            response = self._make_openrouter_request(prompt)
            return self._parse_test_cases_response(response)
        except Exception as e:
            logger.error(f"Error generating test cases: {str(e)}")
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
            logger.error(f"Error generating automation script: {str(e)}")
            raise Exception(f"Error generating automation script: {str(e)}")

    def _make_openrouter_request_with_messages(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """
        Make request to OpenRouter API with custom messages using requests
        Follows the exact pattern provided by OpenRouter
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
        }
        
        data = {
            "model": model or self.model,
            "messages": messages
        }
        
        try:
            response = requests.post(
                url=self.base_url,
                headers=headers,
                json=data
            )
            
            return self._handle_openrouter_response(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API request failed: {str(e)}")
            raise Exception(f"OpenRouter API request failed: {str(e)}")

    def _make_openrouter_request(self, prompt: str) -> str:
        """
        Make request to OpenRouter API following the exact pattern provided
        """
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
                json=data
            )
            
            return self._handle_openrouter_response(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API request failed: {str(e)}")
            raise Exception(f"OpenRouter API request failed: {str(e)}")

    def _handle_openrouter_response(self, response: requests.Response) -> str:
        """
        Handle OpenRouter API response with proper error handling
        """
        if response.status_code == 401:
            raise Exception("OpenRouter API key is invalid or expired. Please check your API key at https://openrouter.ai/keys")
        elif response.status_code == 403:
            raise Exception("OpenRouter API access denied. Please check your account status and credits.")
        elif response.status_code == 429:
            raise Exception("OpenRouter API rate limit exceeded. Please try again later.")
        elif not response.ok:
            # Don't log the full error response to avoid exposing sensitive data
            logger.error(f"OpenRouter API request failed with status {response.status_code}")
            raise Exception(f"OpenRouter API request failed with status {response.status_code}")
        
        try:
            result = response.json()
            return result['choices'][0]['message']['content']
        except KeyError as e:
            logger.error(f"Unexpected response format from OpenRouter: {str(e)}")
            raise Exception(f"Unexpected response format from OpenRouter: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from OpenRouter: {str(e)}")
            raise Exception(f"Invalid JSON response from OpenRouter: {str(e)}")

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