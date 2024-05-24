# Installation
1. Create a virtualenv
    ```
    virtualenv venv
    ```

2. Activate virtualenv
    Run following command in windows terminal (PowerShell)
    ```
    .\venv\Scripts\activate
    ```

3. Create a database (through pgadmin)

4. Change the database credentials in `.env` file

5. Install required packages
    ```
    pip install -r requirements.txt
    ```
6. Migrate database changes
    ```
    python manage.py migrate
    ```

7. Create a super user
    ```
    python manage.py createsuperuser
    ```

8. Run the application
    ```
    python manage.py runserver
    ```