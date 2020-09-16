from peewee import *


db = SqliteDatabase('artworks_db.sqlite')


def main():
    db.connect()
    db.create_tables([Artist, Artwork])
    
    menu_options = {
        1: all_artworks,
        2: search_by_title,
        3: search_by_artist,
        4: add_artist,
        5: add_artwork,
        6: update_email,
        7: update_availability,
        8: delete_artist,
        9: delete_artwork
        }
    selection = menu()
    

def menu():
    while True:
        print('1. View all artworks')
        print('2. Search artworks by title')
        print('3. Search artworks by artist')
        print('4. Add an artist')
        print('5. Add an artwork')
        print('6. Update artist email')
        print('7. Update artwork availablity')
        print('8. Delete an artist')
        print('9. Delete an artwork')
        print('0. Quit')
        response = input('Make a selection:  ')
        
        if response.isdigit():
            selection = int(response)
            if selection >= 0 and selection <= 9:
                return selection
        
        print('Invalid selection\n')
        

def all_artworks():
def search_by_title():
def search_by_artist():
def add_artist():
def add_artwork():
def update_email():
def update_availability():
def delete_artist():
def delete_artwork():

class Artist(Model):
    name = CharField(unique=True)
    email = CharField()
    
    class Meta:
        database = db
    
    def __str__(self):
        return f'{self.name} ({self.email})'

class Artwork(Model):
    artist = ForeignKeyField(Artist, backref='artworks') # link artwork to artist
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
