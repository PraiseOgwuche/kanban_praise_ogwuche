Python Kanban
===================
A simple Kanban application using Flask, SQLite, HTML and Javascript

Running locally
---------------
The application can be run with the following steps:

 1. Install required python packages:

        pip install -r requirements.txt

 __Note__: this will install packages globally, the [venv module][venv-docs]
 can be used to set up a virtual environment if you want to avoid changing the
 system packages.

 2. Run the application using `flask`:

        FLASK_APP=main.py flask run

 3. Finally connect to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in a
    web browser.
