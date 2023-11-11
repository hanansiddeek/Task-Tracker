# Task-Tracker
Build a RESTful API using FastAPI that allows users to manage tasks with advanced features. Tasks and their details will be stored in a MongoDB database and implement error handling, request handling, and logging.

first need to creat an enviornment file in project 
    python -m venv venv 
    venv Scripts .\activate 

install Fast API
    pip install 'FastAPI[all]'

Run the FastAPI application:
    uvicorn main:tasks_api --reload
Replace main with the actual name of your Python file if it's different.

Access the API at http://127.0.0.1:8000 in your browser or use tools like curl.

Tasks/
|-- main.py
|-- utils/
|   |-- logger.py
|-- routes/
|   |-- tasks.py
|-- database/
|   |-- connection.py
|-- models/
|   |--mongo
|   |   |--task.py
|-- |--request
|   |   |--task.py
|-- main.py
|-- app.log
|-- README.md

main.py: Main FastAPI application file.
utils/logger.py: Logging configuration and logger setup.
routes/tasks.py: Router for task-related endpoints.
request/tasks.py: Define the structure of data sent in requests and validate that data.
mongo/tasks.py: Represents the structure of documents that will be stored in a MongoDB collection.
database/conection.py: Configuration file for MongoDB connection settings.

