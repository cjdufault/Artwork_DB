from peewee import *


db = SqliteDatabase('artworks_db.sqlite')


def main():
    
    

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
    
    # value of 1 indicates artwork is available, 0 indicates artwork is sold
    available = IntegerField(
        constraints=[sqlite3('CHECK available = 0 or available = 1')]
    
    class Meta:
        database = db
        
    def __str__(self):
        if self.available == 0:
            available_or_sold = 'Sold'
        else:
            available_or_sold = 'Available'
        return f'"{self.title}" by {self.artist}: {available_or_sold} for {self.price}'
    

if __name__ == '__main__'
    main()
