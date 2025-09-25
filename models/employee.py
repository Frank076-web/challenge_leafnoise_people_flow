from mongoengine import (
    BooleanField,
    DateField,
    Document,
    EmailField,
    ReferenceField,
    StringField,
    FloatField,
)

from models.position import Position


class Employee(Document):
    name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    email = EmailField(required=True, unique=True)
    position = ReferenceField(Position, required=True)
    salary = FloatField(required=True)
    admission_date = DateField(required=True)
    deleted = BooleanField(default=False)
    deleted_at = DateField(null=True, defalut=None)
