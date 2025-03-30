# Ecommerce API

A Django REST API for managing an eCommerce system, including customer management, order processing, and user account functionalities. The API provides OAuth2 authentication and supports modular endpoints for different services.

## Project Structure
• ecommerce_rest_api/: Main Django project settings and configurations.<br>
• customer_service/: Contains logic and routes for customer-related functionality.<br>
• order_service/: Contains logic and routes for managing orders.<br>
• account_service/: Manages user account creation, authentication, and profile updates.<br>
• manage.py: Django’s utility script for tasks like running the server, making migrations, etc.<br>
• .env: Environment variables file for sensitive data such as database credentials, secret keys, and API keys.<br>

## Prerequisites
• Python 3.x<br>
• Pip<br>
• Virtualenv (optional but recommended)<br>
• PostgreSQL or any compatible database<br>
• Google Account <br>
• Africa Talk SMS gateway<br>

## Setup Instructions
1. Clone the Repository:  git clone https://github.com/yourusername/ecommerce-api.git then: cd ecommerce-api
2. Set Up Virtual Environment: python -m venv venv
3. To activate the environment: source venv/bin/activate & On Windows use `venv\Scripts\activate`
4. Install Dependencies: pip install -r requirements.txt
5. Configure locally on settings add your secret keys for the Openid connect account(Google:https://console.cloud.google.com/getting-started) and Africa Talk Sms gate way:https://account.africastalking.com/apps/sandbox
6. Configure Environment Variables: Create a .env file in the root directory and add necessary environment variables; SECRET_KEY=your_secret_key, DEBUG=True, DATABASE_URL=your_database_url
8. Run Migrations:  python manage.py migrate
9. Run the Development Server:  python manage.py runserver
The server will be running at http://127.0.0.1:8000/.

### Test Coverage
Run the following command to execute the unit tests: python manage.py test
Continuous Integration (CI): This project uses GitHub Actions for continuous integration. The workflow is configured to run tests on every push to the repository.

### Key Features in This `README.md`:
1. **Project Structure**: Clearly outlined, showing how the project is divided into services.
2. **Setup Instructions**: Step-by-step guide to get the API up and running locally.
3. **API Endpoints**: Sample endpoints for the main services (customer, order, account).


### Postman Collection
To simplify testing the API, you can import the provided Postman collection: Clone the repository and import the postman collection file: ecommerce-api-postman-collection.json
Open Postman, click on Import, and select the downloaded .json file.
You will now have access to all the API endpoints with pre-configured requests in Postman.<br>
• Customer Service:    POST[ /api/ecommerce/customer/register/): Creates a new customer.<br>
• Order Service:      POST[ /api/ecommerce/order/place-order/): Creates a new order.<br>
• Account Service:    POST /api/ecommerce/account/login/: Logs in a user and returns an authentication token.<br>

### Process flow Diagram
![ecommerce_api process flow diagram](https://github.com/user-attachments/assets/c11cec5c-5576-46d5-b984-7acebf55fb81)
