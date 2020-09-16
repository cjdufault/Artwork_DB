from peewee import *


db = SqliteDatabase('artworks_db.sqlite')


def main():
    db.connect()
    db.create_tables([Artist, Artwork])
    
    running = True
    while running:
        menu_options = {1: all_artworks,
                        2: search_by_title,
                        3: search_by_artist,
                        4: add_artist,
                        5: add_artwork,
                        6: update_email,
                        7: update_availability,
                        8: delete_artist,
                        9: delete_artwork}
        selection = menu()
        
        # run function corresponding to selection if selection in range
        if 0 < selection < 10:
            response = menu_options[selection]()
            
            # response is (response string, returned rows)
            if response[1] != None:
                print('\n' + response[0])
                for record in response[1]:
                    print('\t' + str(record))
            else:
                print('\n' + response[0])
            print()
            
        else:
            running = False # quit if selection is 0 (or something out of range for some reason)
            

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
    rows_returned = Artwork.select()
    
    if len(rows_returned) > 0:
        return 'All artworks:', rows_returned
    else:
        return 'No artworks found.', None


def search_by_title(title=None):
    if title == None:
        title = input('Title:  ')
    
    rows_returned = Artwork.select().where(Artwork.title.contains(title))
    
    if len(rows_returned) > 0:
        return 'Search results:', rows_returned
    else:
        return 'No artworks found.', None
    
    
def search_by_artist(artist=None):
    if artist == None:
        artist = input('Artist:  ')
    
    rows_returned = Artwork.select().where(Artwork.artist.contains(artist))
    
    if len(rows_returned) > 0:
        return 'Search results:', rows_returned
    else:
        return 'No artworks found.', None
    
    
def add_artist(name=None, email=None):
    if name == None:
        name = input('Name:  ')
    if email == None:
        email = input('Email:  ')
    
    print('not implemented')
    
    
def add_artwork(artist=None, title=None, price=None, available=None):
    print('not implemented')
def update_email(artist=None, email=None):
    print('not implemented')
def update_availability(artwork=None, available=None):
    print('not implemented')
def delete_artist(artist=None):
    print('not implemented')
def delete_artwork(artwork=None):
    print('not implemented')
    

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
            
        # ex: "Jimson Weed/White Flower No. 1" by Georgia O'Keefe: Sold for $44,400,000.00
        return f'"{self.title}" by {self.artist}: {available_or_sold} for ${self.price:.2f}'
    

if __name__ == '__main__':
    main()
