from peewee import *


db = SqliteDatabase('artworks_db.sqlite')


def main():
    db.connect()
    db.create_tables([Artist, Artwork])
    

class Artist(Model):
    name = CharField(unique=True)
    email = CharField()
    
    class Meta:
        database = db
    
    def __str__(self):
        return f'{self.name} ({self.email})'

class Artwork(Model):
    artist = CharField()    # foreign key
    title = CharField()
    price = FloatField()
    available = BooleanField()
    
    class Meta:
        database = db
        
    def __str__(self):
        if self.available:
            available_or_sold = 'Available'
        else:
            available_or_sold = 'Sold'
            
        return f'"{self.title}" by {self.artist}: {available_or_sold} for {self.price}'
    

if __name__ == '__main__':
    main()
