# Alembic

Generic single-database configuration with an async dbapi.

## Commads

1. Initiate the alembic

    ```sh
    alembic init alembic
    ```

2. Apply New or Changes Model

    Generate a new migrations

    ```sh
    alembic revision --autogenerate -m "your_message_here"
    ```

    Apply new migrations to Database

    ```sh
    alembic upgrade
    ```

3. Rollback migrations

    Rollback the last migrations

    ```sh
    alembic downgrade -1
    ```

    Rollback to specific migrations

    ```sh
    alembic downgrade <revision_id>
    ```

    Rollback all the migrations

    ```sh
    alembic downgrade base
    ```

4. Check history

    ```sh
    alembic history
    ```
