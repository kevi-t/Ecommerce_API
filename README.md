# Ecommerce API

A Django REST API for managing an eCommerce system, including customer management, order processing, and user account functionalities. The API provides OAuth2 authentication and supports modular endpoints for different services.

## Project Structure
![alt text](assets/structure.png)

## Technologies used
* [Django](https://www.djangoproject.com/): A Python web framework
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs

## Prerequisites
* [Python 3.x](https://www.python.org/downloads/)
* [Pip](https://pip.pypa.io/en/stable/installation/)
* [PostgreSQL](https://www.postgresql.org/download/)or any compatible database
* [Google Account](https://console.cloud.google.com/getting-started)  
* [Africa Talk SMS gateway](https://account.africastalking.com/apps/sandbox) 

## Setup Instructions
1. Clone the Repository:                                                                                                                                                          
    ```bash
        $ git clone https://github.com/kevi-t/Ecommerce_API 
    ```
2. Set Up Virtual Environment:                                                                                                                                                                                  
    ```bash
        $ python -m venv venv 
    ```
3. To activate the environment: source venv/bin/activate & On Windows use                                                                                                                                        
    ```bash
        $ venv\Scripts\activate
    ```
4. Install Dependencies:                                                                                                                                                                             
    ```bash
        $ pip install -r requirements.txt
    ```
5. Configure local settings add your secret keys for the Google account,Django secret and Africa Talk Sms gate way
6. Configure Environment Variables: Create a .env file in the root directory and add necessary environment variables; Google,AfricaTalking SECRET_KEY,DATABASE_URL
7. Prepare the local PostgreSQL database. The database user from `DATABASE_URL` must be able to create tables in the `public` schema before Django can run migrations.
    ```bash
        $ sudo -u postgres psql -d ecommerce_db
    ```
    ```sql
        ALTER DATABASE ecommerce_db OWNER TO ecommerce_user;
        ALTER SCHEMA public OWNER TO ecommerce_user;
        GRANT USAGE, CREATE ON SCHEMA public TO ecommerce_user;
    ```
8. Run Migrations:                                                                                                                                                                                              
    ```bash
        $ python manage.py migrate
    ```
9. Run the Development Server:                                                                                                                                                                            
    ```bash
        $ python manage.py runserver
    ```
### Test Coverage
Run the following command to execute the unit tests: python manage.py test<br>
Continuous Integration (CI): This project uses GitHub Actions for continuous integration. 
The workflow is configured to run tests on every push to the repository.

### Code Quality
This project uses Ruff for Python linting and formatting. Ruff follows the
standard PEP 8 spacing rules, including two blank lines between top-level
classes/functions and one blank line between methods inside a class.

Install development tools:
```bash
pip install -r requirements-dev.txt
```

Run linting:
```bash
ruff check .
```

Run formatting:
```bash
ruff format .
```

Enable automatic checks before each commit:
```bash
pre-commit install
```

Run all pre-commit checks manually:
```bash
pre-commit run --all-files
```

### Key Features in This `README.md`:
1. **Project Structure**: Clearly outlined, showing how the project is divided into modules.
2. **Setup Instructions**: Step-by-step guide to get the API up and running locally.
3. **API Endpoints**: Sample endpoints for the main modules (customer, order).


### Testing the API on Postman
To simplify testing the API, you can download and import the provided Postman collection:
* [Ecommerce Local_postman_collection](https://github.com/kevi-t/Ecommerce_API/blob/master/assets/Ecommerce.postman_collection.json)
* [Ecommerce Production_postman_collection](https://github.com/kevi-t/Ecommerce_API/blob/master/assets/Ecommerce%20Production.postman_collection.json)<br>

Endpoints descriptions:
* Customer:
   ```bash
    POST[/api/ecommerce/customer/register/]: Creates a new customer.
    POST[/api/ecommerce/customer/login/]: Logs in a user and returns an authentication token.
    PUT[/api/ecommerce/customer/update/]: update user profile (requires Bearer token).
   ```

* Order:
   ```bash   
      POST[/api/ecommerce/order/place-order/]: Creates a new order.(requires Bearer token)
      GET[/api/ecommerce/order/list/]: Fetches the list of orders. (requires Bearer token)
   ```
* OpenID connect/Google Sigin: paste on a browser to obtain the access Token
   ```bash  
      http://localhost:8000/api/ecommerce/customer/oidc/login/
      https://ecommerce-api-alpha-dun.vercel.app/api/ecommerce/customer/oidc/login/
   ```
### Expected Sample Outputs
#### Register Endpoint
![alt text](assets/image-1.png)   
#### Login Endpoint
![alt text](assets/image-2.png)
#### Place order Endpoint
![alt text](assets/image-3.png)
#### Order List Endpoint
![alt text](assets/image-4.png)
#### OpenID connect endpoint
![alt text](assets/image-5.png)

### Process flow Diagram
![ecommerce_api process flow diagram](https://github.com/user-attachments/assets/c11cec5c-5576-46d5-b984-7acebf55fb81)

### Deployment
* [Vercel](https://vercel.com/): Deployment of my Django App
* [Railway](https://railway.com/): Deployment of my Postgre database service

### Resources
* [Django docs](https://docs.djangoproject.com/): Django documentation 
