"""
Script templates for generating automation scripts
"""

PLAYWRIGHT_PYTHON_TEMPLATE = '''
import pytest
import time

class TestAutomation:
    """Test automation class for generated test cases"""
    
{test_cases}

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''

PLAYWRIGHT_SELENIUM_TEMPLATE = '''
import pytest
import time

class TestAutomation:
    """Test automation class for generated test cases"""
    
{test_cases}

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''

def generate_test_case_method(test_case, script_type="playwright_python"):
    """Generate a test case method based on the test case data"""
    
    title = test_case.get('title', 'Test Case')
    description = test_case.get('description', '')
    steps = test_case.get('steps', '')
    expected_result = test_case.get('expected_result', '')
    
    # Clean up the method name
    method_name = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
    method_name = method_name.replace(' ', '_').lower()
    method_name = f"test_{method_name}"
    
    if script_type == "playwright_python":
        return f'''
    def {method_name}(self):
        """{title}
        
        Description: {description}
        Steps: {steps}
        Expected Result: {expected_result}
        """
        try:
            # TODO: Implement test steps based on the description
            # This is a placeholder implementation
            print(f"Running test: {title}")
            print(f"Description: {description}")
            print(f"Steps: {steps}")
            print(f"Expected Result: {expected_result}")
            
            # Add your test implementation here
            # Example:
            # from playwright.sync_api import sync_playwright
            # with sync_playwright() as p:
            #     browser = p.chromium.launch()
            #     page = browser.new_page()
            #     page.goto("https://example.com")
            #     page.click("button")
            #     assert page.text_content("h1") == "Expected Text"
            #     browser.close()
            
            # For now, just simulate the test
            import time
            time.sleep(0.1)  # Simulate test execution time
            assert True, "Test passed - implement actual test logic"
            
        except Exception as e:
            pytest.fail(f"Test failed: {{str(e)}}")
'''
    else:  # playwright_selenium
        return f'''
    def {method_name}(self):
        """{title}
        
        Description: {description}
        Steps: {steps}
        Expected Result: {expected_result}
        """
        try:
            # TODO: Implement test steps based on the description
            # This is a placeholder implementation
            print(f"Running test: {{title}}")
            print(f"Description: {{description}}")
            print(f"Steps: {{steps}}")
            print(f"Expected Result: {{expected_result}}")
            
            # Add your test implementation here
            # Example:
            # from selenium import webdriver
            # from selenium.webdriver.common.by import By
            # driver = webdriver.Chrome()
            # driver.get("https://example.com")
            # driver.find_element(By.ID, "button").click()
            # assert driver.find_element(By.TAG_NAME, "h1").text == "Expected Text"
            # driver.quit()
            
            # For now, just simulate the test
            import time
            time.sleep(0.1)  # Simulate test execution time
            assert True, "Test passed - implement actual test logic"
            
        except Exception as e:
            pytest.fail(f"Test failed: {{str(e)}}")
'''

def generate_script_content(test_cases, script_type="playwright_python"):
    """Generate complete script content from test cases"""
    
    if script_type == "playwright_python":
        template = PLAYWRIGHT_PYTHON_TEMPLATE
    else:
        template = PLAYWRIGHT_SELENIUM_TEMPLATE
    
    # Generate test case methods
    test_case_methods = []
    for test_case in test_cases:
        test_case_methods.append(generate_test_case_method(test_case, script_type))
    
    # Combine template with test cases
    script_content = template.format(test_cases="\n".join(test_case_methods))
    
    return script_content 