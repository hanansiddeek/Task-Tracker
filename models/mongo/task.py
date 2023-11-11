from mongoengine import Document, StringField, DateTimeField


class MongoTasks(Document):
    meta = {'collection': 'tasks'}

    task_name = StringField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
    status = StringField(required=True, default="Assigned")
    description = StringField(required=False)
