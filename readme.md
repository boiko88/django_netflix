To run the project please do the following steps:

Create a Virtual Environment:

1. To create a virtual environment, navigate to the project directory and run the following command:

python -m venv env

This will create a new virtual environment in a directory called env.

2. Activate the Virtual Environment:
To activate the virtual environment, run the following command:

On Windows:

.\env\Scripts\activate

On Linux or macOS:

source env/bin/activate

3. Install Project Dependencies:

To install project dependencies, run the following command:

pip install -r requirements.txt

This will install all the required packages listed in the requirements.txt file.

4. Database Setup:
To set up the database, configure the database settings in settings.py by modifying the DATABASES dictionary.

5. After configuring the database settings, run migrations using the following command:
python manage.py migrate

6. Running the Django Project
Run the Development Server:
To run the Django development server, navigate to the project directory and run the following command:

python manage.py runserver

This will start the development server on http://127.0.0.1:8000/.


Main functionality: 

1. ![img.png](img.png)