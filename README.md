# Ecommerce API

A Django REST API for managing an eCommerce system, including customer management, order processing, and user account functionalities. The API provides OAuth2 authentication and supports modular endpoints for different services.

## Project Structure
![alt text](image.png)


## Prerequisites
• Python 3.x<br>
• Pip<br>
• PostgreSQL or any compatible database<br>
• [Google Account](https://console.cloud.google.com/getting-started)  <br>
• [Africa Talk SMS gateway](https://account.africastalking.com/apps/sandbox) <br>

## Setup Instructions
1. Clone the Repository:  git clone https://github.com/kevi-t/Ecommerce_API 
2. Set Up Virtual Environment: python -m venv venv
3. To activate the environment: source venv/bin/activate & On Windows use `venv\Scripts\activate`
4. Install Dependencies: pip install -r requirements.txt
5. Configure local settings add your secret keys for the Google account,Django secret and Africa Talk Sms gate way
6. Configure Environment Variables: Create a .env file in the root directory and add necessary environment variables; Google,AfricaTalking SECRET_KEY,DATABASE_URL
8. Run Migrations:  python manage.py migrate
9. Run the Development Server:  python manage.py runserver


### Test Coverage
Run the following command to execute the unit tests: python manage.py test<br>
Continuous Integration (CI): This project uses GitHub Actions for continuous integration. 
The workflow is configured to run tests on every push to the repository.

### Key Features in This `README.md`:
1. **Project Structure**: Clearly outlined, showing how the project is divided into modules.
2. **Setup Instructions**: Step-by-step guide to get the API up and running locally.
3. **API Endpoints**: Sample endpoints for the main modules (customer, order).


### Postman Collection
To simplify testing the API, you can download the provided Postman collection [Ecommerce_postman_collection]:<br>
• Customer:   <br>
    POST[/api/ecommerce/customer/register/]: Creates a new customer.<br>
    POST[/api/ecommerce/customer/login/]: Logs in a user and returns an authentication token.<br>
    PUT[/api/ecommerce/customer/update/]: update user profile (requires Bearer token).<br>
• Order:<br>     
      POST[ /api/ecommerce/order/place-order/): Creates a new order.(requires Bearer token)<br>
      GET[ /api/ecommerce/order/list/]: Fetches the list of orders. (requires Bearer token)<br>
• OpenID connect: Paste the url;http://localhost:8000/api/ecommerce/customer/oidc/login/ on the browser to sign in with Google and obtain access Token<br>

### Expected Sample Outputs
![alt text](image-1.png)   
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)
![alt text](image-5.png)
### Process flow Diagram
![ecommerce_api process flow diagram](https://github.com/user-attachments/assets/c11cec5c-5576-46d5-b984-7acebf55fb81)