<!-- @format -->

# Shortlink API

This project is a backend API for creating and managing shortlinks using FastAPI. It provides endpoints for creating, retrieving, updating, and deleting shortlinks, as well as redirecting to the original URLs.

## Features

-   Create shortlinks for given URLs
-   Retrieve a list of shortlinks with pagination
-   Update existing shortlinks
-   Delete shortlinks
-   Redirect to the original URL using the shortlink
-   Database connection and management using SQLAlchemy and Alembic
-   Custom exception handling

## Project Structure

    .
    ├── alembic/            # Database migrations directory
    ├── configs/            # Configuration files
    ├── dependencies/       # Dependency injection and database connection
    ├── models/             # Database models
    ├── repositories/       # Data access layer
    ├── routers/            # API route definitions
    │ ├── endpoints/        # Specific endpoint routes
    ├── schemas/            # Pydantic models for request and response validation
    ├── services/           # Business logic and service layer
    ├── utils/              # Utility functions and helpers
    ├── .env.example        # Example environment configuration file
    ├── .gitignore          # Git ignore file
    ├── main.py             # Main application entry point
    ├── requirements.txt    # Project dependencies
    └── README.md

## Getting Started

### Prerequisites

-   Python 3.10+
-   PostgreSQL

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/rinaltair/shortlink-api.git
    cd shortlink-api
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file based on the `.env.example` file and update the database configuration:

    ```sh
    cp .env.example .env
    ```

### Database Setup

1. Initialize the Alembic migrations:

    ```sh
    alembic init alembic
    ```

2. Create a new migration:

    ```sh
    alembic revision --autogenerate -m "Initial migration"
    ```

3. Apply the migration:

    ```sh
    alembic upgrade head
    ```

### Running the Application

1. Start the FastAPI application:

    ```sh
    uvicorn main:app --reload
    ```

2. Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the API documentation.
