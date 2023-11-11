from mongoengine import connect


def connect_db():
    connection = connect('task',host='mongodb://localhost:27017/')

    return connection
