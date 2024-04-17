# import unittest
# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LoginTest(TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.base_url = "http://localhost:8000"
#         self.driver.maximize_window()
#         self.driver.implicitly_wait(10)

#     def test_successful_login(self):
#         self.driver.get(self.base_url + '/login')
#         # Check if the login page is loaded successfully
#         expected_title = 'Paws and Tails - Pet Care Website Template'
#         self.assertEqual(expected_title, self.driver.title)
#         # Locate username, password fields, and submit button
#         username = self.driver.find_element(By.NAME, 'username')
#         password = self.driver.find_element(By.NAME, 'password')
#         submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
#         # Enter valid credentials
#         username.send_keys("Cherry")
#         password.send_keys("cherry123@")
#         # Submit the form
#         submit_button.click()
#         # Wait until the URL changes (indicating successful login)
#         WebDriverWait(self.driver, 10).until(EC.url_changes)
#         # Check if login is successful (you can add additional checks here)
#         self.assertTrue("user_index" in self.driver.current_url)

#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()




# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import time
# import unittest

# class NavigationTest(TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.base_url = "http://127.0.0.1:8000"
#         self.driver.maximize_window()
#         self.driver.implicitly_wait(10)
#         self.wait = WebDriverWait(self.driver, 20)  # Increase the timeout
    
#     def wait_for_element(self, by, value):
#         try:
#             return self.wait.until(EC.presence_of_element_located((by, value)))
#         except TimeoutException:
#             return None

#     def wait_for_header(self, header_text):
#         try:
#             self.wait.until(EC.presence_of_element_located((By.XPATH, f'//h1[contains(text(), "{header_text}")]')))
#         except TimeoutException:
#             return None

#     def test_add_staff(self):
#         # Navigate directly to the login page
#         self.driver.get(self.base_url + '/login')
        
#         # Perform login
#         username_input = self.driver.find_element(By.NAME, 'username')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
#         username_input.send_keys("sree")
#         password_input.send_keys("Sree123@")
#         login_button.click()
        
#         # Wait for the dashboard page to load
#         self.wait_for_header("Dashboard")

#         # Navigate to the "Staffs" page
#         try:
#             staffs_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="nav-option option3"]//a')))
#             staffs_link.click()
#         except TimeoutException:
#             self.fail("Timed out waiting for 'Staffs' link to be clickable")
        
#         # Wait for the "Add Staff" page to load
#         self.wait_for_header("ADD STAFF")

#         # Fill in staff details
#         full_name_input = self.driver.find_element(By.NAME, 'full_name')
#         username_input = self.driver.find_element(By.NAME, 'username')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         email_input = self.driver.find_element(By.NAME, 'email')
#         add_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
#         full_name_input.send_keys("Sreehari")
#         username_input.send_keys("aniiiii")
#         password_input.send_keys("Sreehari123@")
#         email_input.send_keys("sreehari@gmail.com")
        
#         # Submit the form
#         add_button.click()

#         # Wait for the staffs page to load (you might need to adjust the header accordingly)
#         self.wait_for_header("Staffs")
        
#         # Assert that the staff has been added successfully

#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()


# from django.test import TestCase
# from django.urls import reverse
# from models import Service  # Import your Service model

# class AddServiceTestCase(TestCase):
#     def setUp(self):
#         # Create a test user (if necessary) and log in
#         self.client.login(username='testuser', password='password')

#     def test_add_service(self):
#         # Navigate to the add service page
#         add_service_url = reverse('add_service')  # Update with your URL name
#         response = self.client.get(add_service_url)
#         self.assertEqual(response.status_code, 200)

#         # Submit the form to add a new service
#         new_service_data = {
#             'name': 'Test Service',
#             'description': 'Test Description',
#             'price': 100.00,
#             'is_available': True,
#         }
#         response = self.client.post(add_service_url, new_service_data)
        
#         # Check that the service was added successfully
#         self.assertEqual(response.status_code, 302)  # 302 indicates a redirect after successful form submission
#         # Optionally, you can check if the service was added to the database
#         self.assertTrue(Service.objects.filter(name='Test Service').exists())

#         # Check that the user is redirected to the service details page
#         self.assertRedirects(response, reverse('service_details'))  # Update with your URL name for the service details page



from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class NavigationTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_navigation(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Send a GET request to the dashboard page
        dashboard_response = self.client.get(reverse('dashboard_page_url_name'))
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(dashboard_response.status_code, 200)

        # Send a GET request to the add boarding page
        add_boarding_response = self.client.get(reverse('add_boarding_page_url_name'))

        # Check if the user is redirected to the login page (assuming authentication is required to access the add boarding page)
        self.assertEqual(add_boarding_response.status_code, 302)
        
        # Check if the user is redirected to the correct login page
        self.assertRedirects(add_boarding_response, reverse('login_page_url_name'))
```
