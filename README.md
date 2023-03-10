Kanban - A Python Application
===================
A simple Kanban application using Flask, SQLite, HTML and Javascript.
This application can create tasks, assign them to different progreeses (To-do, doing or done) on the schedule board, delete completed tasks, modify existing tasks etc.

An improvement on the app is the ability to create users and have different users with different kanban.

Running locally
---------------
The application can be run with the following steps:

 1. Create a virtual environment
 
        python3 -m venv venv
       
 2. Activate the virtual environment
 
     On mac:
     
        source venv/bin/activate
        
     On windows:
     
        venv\Scripts\activate.bat
        
 3. Install required python packages:

        pip install -r requirements.txt

 4. Run the application:

        python3 app.py

 5. Finally connect to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in a
    web browser.
    
    
**App description and walkthrough of functionality can be found here**: https://www.loom.com/share/be1e96fd05f043838834eae6c8d8ba62 
