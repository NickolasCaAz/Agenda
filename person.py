import peewee
from flask_peewee.rest import RestResource

db = peewee.SqliteDatabase('agenda.db')

class BaseModel(db.Model):
    class Meta:
        database = db
    
class Person(BaseModel):
    number = peewee.CharField(unique=False)
    email = peewee.CharField(unique=False)
    name = peewee.CharField(unique=False)
    def __str__(self):
        return self.email
# create a RestResource subclass
# class PersonResource(RestResource):
#     exclude = None



# nome = Person.create(name = "Nickolas", number = "123", email = "asdasd@gmail.com")