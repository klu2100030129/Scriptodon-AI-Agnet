import json
import re
from typing import Dict, Any, List

class SwaggerService:
    def parse_swagger_content(self, content: str) -> Dict[str, Any]:
        """Parse Swagger content from JSON or YAML format"""
        try:
            # Try to parse as JSON first
            return json.loads(content)
        except json.JSONDecodeError:
            # If JSON fails, try YAML
            try:
                return self._parse_yaml_simple(content)
            except Exception as e:
                raise Exception(f"Invalid YAML content: {str(e)}")
    
    def _parse_yaml_simple(self, yaml_content: str) -> Dict[str, Any]:
        """Simple YAML parser for basic Swagger files"""
        lines = yaml_content.strip().split('\n')
        result = {}
        current_key = None
        current_value = ""
        indent_level = 0
        
        for line in lines:
            line = line.rstrip()
            if not line or line.startswith('#'):
                continue
                
            # Count leading spaces for indentation
            leading_spaces = len(line) - len(line.lstrip())
            
            # Check if this is a key-value pair
            if ':' in line and not line.strip().startswith('-'):
                parts = line.split(':', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ""
                
                if value:
                    # Simple value
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.lower() in ['true', 'false']:
                        value = value.lower() == 'true'
                    elif value.isdigit():
                        value = int(value)
                    elif self._is_float(value):
                        value = float(value)
                    # Otherwise keep as string
                    
                    result[key] = value
                else:
                    # Complex value (object or array)
                    current_key = key
                    current_value = ""
                    indent_level = leading_spaces
            else:
                # This is part of a complex value
                if current_key is not None:
                    if leading_spaces > indent_level:
                        current_value += line + "\n"
                    else:
                        # End of current complex value
                        if current_value.strip():
                            result[current_key] = self._parse_yaml_simple(current_value)
                        current_key = None
                        current_value = ""
        
        # Handle any remaining complex value
        if current_key is not None and current_value.strip():
            result[current_key] = self._parse_yaml_simple(current_value)
        
        return result
    
    def _is_float(self, value: str) -> bool:
        """Check if a string can be converted to float"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def fetch_swagger_from_url(self, url: str) -> Dict[str, Any]:
        """Fetch Swagger/OpenAPI specification from URL"""
        try:
            import requests
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            content = response.text
            swagger_data = self.parse_swagger_content(content)
            
            # Validate the fetched data
            if not self.validate_swagger(swagger_data):
                raise ValueError("Invalid Swagger/OpenAPI specification")
            
            return swagger_data
        except Exception as e:
            raise Exception(f"Failed to fetch Swagger from URL: {str(e)}")

    def validate_swagger(self, swagger_data: Dict[str, Any]) -> bool:
        """Validate if the data is a valid Swagger/OpenAPI specification"""
        try:
            # Check for required fields
            if not isinstance(swagger_data, dict):
                return False
            
            # Check for OpenAPI version
            if 'openapi' in swagger_data:
                return True
            
            # Check for Swagger version
            if 'swagger' in swagger_data:
                return True
            
            # Check for info and paths (basic validation)
            if 'info' in swagger_data and 'paths' in swagger_data:
                return True
            
            return False
        except Exception:
            return False

    def extract_endpoints(self, swagger_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract endpoints from Swagger/OpenAPI specification"""
        endpoints = []
        
        try:
            paths = swagger_data.get('paths', {})
            
            for path, methods in paths.items():
                for method, details in methods.items():
                    if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                        endpoint = {
                            'path': path,
                            'method': method.upper(),
                            'summary': details.get('summary', ''),
                            'description': details.get('description', ''),
                            'parameters': details.get('parameters', []),
                            'responses': details.get('responses', {})
                        }
                        endpoints.append(endpoint)
            
            return endpoints
        except Exception:
            return []

    def generate_test_cases_from_swagger(self, swagger_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate test cases from Swagger specification"""
        endpoints = self.extract_endpoints(swagger_data)
        test_cases = []
        
        for endpoint in endpoints:
            test_case = {
                'title': f"Test {endpoint['method']} {endpoint['path']}",
                'description': endpoint.get('summary', f"Test {endpoint['method']} endpoint"),
                'steps': f"1. Send {endpoint['method']} request to {endpoint['path']}\n2. Verify response status\n3. Validate response body",
                'expected_result': f"Should return appropriate status code and response for {endpoint['method']} {endpoint['path']}"
            }
            test_cases.append(test_case) 