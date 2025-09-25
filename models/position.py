from mongoengine import Document, StringField, BooleanField, DateField


class Position(Document):
    name = StringField(required=True, unique=True)
    deleted = BooleanField(default=False)
    deleted_at = DateField(default=None, null=True)
