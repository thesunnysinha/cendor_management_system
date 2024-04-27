## API Documentation

Access the API documentation via the following links:

- [Swagger](http://localhost:8000/swagger/)
- [ReDoc](http://localhost:8000/redoc/)

## Introduction

This repository includes the API documentation for testing purposes. Below is a brief overview of the available endpoints:

- **Auth**: Used for user creation and login.
- **Vendors**: Allows CRUD operations for vendors and performance checking.
- **Purchase Orders**: Enables CRUD operations for purchase orders and acknowledgment of purchase orders.

## Create Virtual Environment and Install Dependencies

To set up your development environment, follow these steps:

1. Create a virtual environment.
2. Activate the virtual environment.
3. Navigate to the `backend` directory.
4. Install the required dependencies using `pip install -r requirements.txt`.

## Manual Setup

To manually run the project, follow these steps:

1. Make migrations with `python manage.py makemigrations`.
2. Apply migrations with `python manage.py migrate`.
3. Run the server with `python manage.py runserver 0.0.0.0:8000` (You can specify the port according to your preference).
4. If needed, you can delete `__pycache__` directories and migration files using `python manage.py deletepycachemigrations`.
5. To create a `.env` file, copy the `.envExample` file using the command `cp .envExample .env`. This will create an exact copy of `.envExample` named `.env`.


### Using the Provided Script(Linux Only)

Alternatively, you can run the server using the provided script:

1. Grant execute permission to the script with `chmod +x runserver.sh`.
2. Execute the script with `./runserver.sh`.
