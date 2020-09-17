from peewee import *


db = SqliteDatabase('artworks_db.sqlite', pragmas={'foreign_keys': 1})


def main():
    db.connect()
    db.create_tables([Artist, Artwork])
    
    running = True
    while running:
        menu_options = {1: all_artworks,
                        2: search_by_title,
                        3: search_by_artist,
                        4: search_for_artist,
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
                for row in response[1]:
                    print('\t' + str(row))
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
        print('4. Search for an artist')
        print('5. Add an artwork')
        print('6. Update artist email')
        print('7. Update artwork availablity')
        print('8. Delete an artist')
        print('9. Delete an artwork')
        print('0. Quit')
        response = int_input('Make a selection:  ', 'Invalid selection\n')
        
        
        selection = int(response)
        if selection >= 0 and selection <= 9:
            return selection
        
        print('Invalid selection\n')
        

def all_artworks():
    rows_returned = Artwork.select().order_by(Artwork.artist)
    
    if len(rows_returned) > 0:
        return 'All artworks:', rows_returned
    else:
        return 'No artworks found', None


def search_by_title(title=None):
    if title == None:
        title = input('Title:  ')
    
    rows_returned = Artwork.select().where(Artwork.title.contains(title))
    
    if len(rows_returned) > 0:
        return 'Search results:', rows_returned
    else:
        return 'No artworks found', None
    
    
def search_by_artist(artist_name=None):
    if artist_name == None:
        artist_name = input('Artist:  ')
    
    artist = Artist.get_or_none(Artist.name == artist_name)
    artworks = artist.artworks
    
    if len(artworks) > 0:
        return 'Search results:', artworks
    else:
        return 'No artworks found', None
    
    
def search_for_artist(artist_name=None):
    if artist_name == None:
        artist_name = input('Artist:  ')
    
    rows_returned = Artist.select().where(Artist.name.contains(artist_name))
    
    if len(rows_returned) > 0:
        return 'Search results:', rows_returned
    else:
        return 'No artists found', None
    
    
def add_artist(name=None, email=None):
    if name == None:
        name = input('Artist\'s Name:  ')
    if email == None:
        email = input('Artist\'s email address:  ')
    
    try:
        artist = Artist.create(name=name, email=email)
        return f'Added {name} to database', [artist]
        
    except IntegrityError as e:
        print(e)
        return 'Failed to add artist', None
    
    
def add_artwork(artist_name=None, title=None, price=None, available=None):
    if artist_name == None:
        artist_name = input('Artist\'s name:  ')
        
    # check if artist object already exists
    artist = Artist.get_or_none(Artist.name == artist_name)
    if artist == None:
        print(f'No existing info for {artist_name}. Creating entry for {artist_name}:')
        artist = add_artist(name=artist_name)[1][0]
        
    if title == None:
        title = input('Title of artwork:  ')
    if price == None:
        price = int_input('Price: $', 'Invalid input\n')
    if available == None:
        available = yes_no('Available for sale? Yes/No:  ', 'Invalid input\n')
        
    try:
        artwork = Artwork.create(artist=artist, title=title, price=price, available=available)
        return f'Added artwork to database:', [artwork]
        
    except IntegrityError as e:
        print(e)
    
    return 'Failed to add artwork', None
    
    
def update_email(artist=None, email=None):
    print('not implemented')
def update_availability(artwork=None, available=None):
    print('not implemented')
def delete_artist(artist=None):
    print('not implemented')
def delete_artwork(artwork=None):
    print('not implemented')
    

def int_input(prompt, invalid_message):
    while True:
        response = input(prompt)

        if response.isdigit():
            return int(response)
        else:
            print(invalid_message)
            

def yes_no(prompt, invalid_message):
    while True:
        response = input(prompt)
        
        if response.lower() == 'y' or response.lower() == 'yes':
            return True
        elif response.lower() == 'n' or response.lower() == 'no':
            return False
        
        else:
            print(invalid_message)
    
    
class BaseModel(Model):
    class Meta:
        database = db


class Artist(BaseModel):
    name = CharField(unique=True)
    email = CharField()
    
    def __str__(self):
        return f'{self.name} ({self.email})'
    

class Artwork(BaseModel):
    artist = ForeignKeyField(Artist, backref='artworks') # link artwork to artist
    title = CharField()
    price = FloatField()
    available = BooleanField()
        
    def __str__(self):
        if self.available:
            available_or_sold = 'Available'
        else:
            available_or_sold = 'Sold'
            
        # ex: "Jimson Weed/White Flower No. 1" by Georgia O'Keefe: Sold for $44,400,000.00
        return f'"{self.title}" by {self.artist}: {available_or_sold} for ${self.price:.2f}'


if __name__ == '__main__':
    main()
