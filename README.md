# Ecommerce API

A Django REST API for managing an eCommerce system, including customer management, order processing, and user account functionalities. The API provides OAuth2 authentication and supports modular endpoints for different services.

## Project Structure
ecommerce_api/: Main Django project settings and configurations.<br>
customer_service/: Contains logic and routes for customer-related functionality.<br>
order_service/: Contains logic and routes for managing orders.<br>
account_service/: Manages user account creation, authentication, and profile updates.<br>
manage.py: Django’s utility script for tasks like running the server, making migrations, etc.<br>
.env: Environment variables file for sensitive data such as database credentials, secret keys, and API keys.<br>

## Setup Instructions

Prerequisites
Python 3.x
Pip
Virtualenv (optional but recommended)
PostgreSQL or any compatible database
AWS CLI and Elastic Beanstalk CLI (for deployment)
1. Clone the Repository: git clone https://github.com/yourusername/ecommerce-api.git
                         cd ecommerce-api
2. Set Up Virtual Environment: python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install Dependencies: pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory and add necessary environment variables:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
5. Run Migrations
python manage.py migrate
6. Run the Development Server
python manage.py runserver
The server will be running at http://127.0.0.1:8000/.

Run the following command to execute the unit tests: python manage.py test
Test Coverage

Continuous Integration (CI): This project uses GitHub Actions for continuous integration. The workflow is configured to run tests on every push to the repository.

### Key Features in This `README.md`:
1. **Project Structure**: Clearly outlined, showing how the project is divided into services.
2. **Setup Instructions**: Step-by-step guide to get the API up and running locally.
3. **API Endpoints**: Sample endpoints for the main services (customer, order, account).
4. **Testing**: Instructions on how to run tests, with an optional section for CI using GitHub Actions.
5. **Deployment**: Detailed guide on deploying to AWS Elastic Beanstalk, including setting up environment variables.
6. **License**: Includes an MIT License section.


### Postman Collection
To simplify testing the API, you can import the provided Postman collection:
Download the Postman collection file: ecommerce-api-postman-collection.json
Open Postman, click on Import, and select the downloaded .json file.
You will now have access to all the API endpoints with pre-configured requests in Postman.<br>
Customer Service<br>
GET /api/ecommerce/customer/list/: Retrieves a list of all customers.<br>
POST /api/ecommerce/customer/create/: Creates a new customer.<br>
Order Service<br>
GET /api/ecommerce/order/list/: Retrieves a list of all orders.<br>
POST /api/ecommerce/order/create/: Creates a new order.<br>
Account Service<br>
POST /api/ecommerce/account/register/: Registers a new user account.<br>
POST /api/ecommerce/account/login/: Logs in a user and returns an authentication token.<br>

### Process flow Diagram
![ecommerce_api process flow diagram](https://github.com/user-attachments/assets/2f441884-cf62-4148-87c9-113d7c22d431)

