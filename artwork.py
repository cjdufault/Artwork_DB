from peewee import *


db = SqliteDatabase('artworks_db.sqlite', pragmas={'foreign_keys': 1})


def main():
    db.connect()
    db.create_tables([Artist, Artwork])
    
    running = True
    while running:
        menu_options = {1: all_artworks,
                        2: all_artists,
                        3: search_by_title,
                        4: search_by_artist,
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
        print('2. View all artists')
        print('3. Search artworks by title')
        print('4. Search artworks by artist')
        print('5. Add an artwork')
        print('6. Update artist email')
        print('7. Update artwork availablity')
        print('8. Delete an artist')
        print('9. Delete artwork')
        print('0. Quit')
        response = int_input('Make a selection:  ', 'Invalid selection\n')
        
        selection = int(response)
        if selection >= 0 and selection <= 9:
            return selection
        
        print('Invalid selection\n')
        

def all_artworks():
    rows_returned = Artwork.select().order_by(Artwork.artist.name)
    
    if len(rows_returned) > 0:
        return 'All artworks:', rows_returned
    else:
        return 'No artworks found', None
    

def all_artists():
    rows_returned = Artist.select().order_by(Artist.name)
    
    if len(rows_returned) > 0:
        return 'All artists:', rows_returned
    else:
        return 'No artists found', None


def search_by_title(title=None):
    if title == None or type(title) != str:
        title = input('Title:  ')
    
    rows_returned = Artwork.select().where(Artwork.title.contains(title))
    
    if len(rows_returned) > 0:
        return 'Search results:', rows_returned
    else:
        return 'No artworks found', None
    
    
def search_by_artist(artist_name=None):
    if artist_name == None or type(artist_name) != str:
        artist_name = input('Artist:  ')
    
    artist = Artist.get_or_none(Artist.name == artist_name)
    if artist != None:
        artworks = artist.artworks
    
        if len(artworks) > 0:
            return 'Search results:', artworks
        else:
            return 'No artworks found', None
    else:
        return 'Artist not found', None
    
    
def add_artist(name=None, email=None):
    if name == None or type(name) != str:
        name = input('Artist\'s Name:  ')
    if email == None or type(email) != str:
        email = input('Artist\'s email address:  ')
    
    try:
        artist = Artist.create(name=name, email=email)
        return f'Added {name} to database:', [artist]
        
    except IntegrityError as e:
        print(e)
        return 'Failed to add artist', None
    
    
def add_artwork(artist_name=None, title=None, price=None, available=None):
    if artist_name == None or type(artist_name) != str:
        artist_name = input('Artist\'s name:  ')
        
    # check if artist object already exists
    artist = Artist.get_or_none(Artist.name == artist_name)
    if artist == None:
        print(f'No existing info for {artist_name}. Creating entry for {artist_name}:')
        artist = add_artist(name=artist_name)[1][0]
        
    if title == None or type(title) != str:
        title = input('Title of artwork:  ')
    if price == None or type(price) != int:
        price = int_input('Price: $', 'Invalid input\n')
    if available == None or type(available) != bool:
        available = yes_no('Available for sale? Yes/No:  ', 'Invalid input\n')
        
    try:
        artwork = Artwork.create(artist=artist, title=title, price=price, available=available)
        return f'Added artwork to database:', [artwork]
        
    except IntegrityError as e:
        print(e)
    
    return 'Failed to add artwork', None
    
    
def update_email(artist_name=None, email=None):
    if artist_name == None or type(artist_name) != str:
        artist_name = input('Artist\'s Name:  ')
    if email == None or type(email) != str:
        email = input('Artist\'s email address:  ')
        
    artist = Artist.get_or_none(Artist.name == artist_name)
    if artist != None:
        artist.email = email
        artist.save()
        
        return f'Updated {artist_name}\'s email address to {email}', None
    
    else:
        return f'No artist named {artist_name}', None
    
    
def update_availability(title=None, available=None):
    if title == None or type(title) != str:
        title = input('Title of artwork:  ')
    if available == None or type(available) != bool:
        available = yes_no('Available for sale? Yes/No:  ', 'Invalid input\n')
    
    artwork = Artwork.get_or_none(Artwork.title == title)
    if artwork != None:
        artwork.available = available
        artwork.save()
        if available:
            available_or_sold = 'Available'
        else:
            available_or_sold = 'Sold'
            
        return f'Updated availablity of "{title}" to {available_or_sold}', None
    
    else:
        return f'No artwork titled {title}', None
    
    
def delete_artist(artist_name=None):
    if artist_name == None or type(artist_name) != str:
        artist_name = input('Artist\'s name:  ')
        
    artist = Artist.get_or_none(Artist.name == artist_name)
    if artist != None:
        confirm = yes_no('WARNING: this will delete all artworks by this artist as well. Proceed? Yes/No:  ',
                         'Invalid input\n')
        
        if confirm:
            Artwork.delete().where(Artwork.artist == artist).execute()
            Artist.delete().where(Artist.name == artist_name).execute()
            
            return f'Deleted {artist_name} and of their artworks', None
        
        return 'Canceled deletion', None
    
    else:
        return 'Artist not found', None
    
    
def delete_artwork(artist_name=None, title=None):
    if title == None or type(title) != str:
        title = input('Title of artwork:  ')
    
    matching_titles = Artwork.select().where(Artwork.title == title)
    
    if len(matching_titles) > 0:
        
        deleted_art = []
        for artwork in matching_titles:
            confirm = yes_no(f'Would you like to delete "{artwork.title}" by {artwork.artist.name}? Yes/No:  ',
                            'Invalid input\n')
            
            if confirm:
                deleted_art.append(artwork)
                Artwork.delete().where(Artwork.artwork_id == artwork.artwork_id).execute()
                            
        return 'Deleted:', deleted_art
        
    else:
        return 'Artwork not found', None
    

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
    artist_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    email = CharField()
    
    def __str__(self):
        return f'{self.name} ({self.email})'
    

class Artwork(BaseModel):
    artwork_id = IntegerField(primary_key=True)
    artist = ForeignKeyField(Artist, backref='artworks') # link artwork to artist
    title = CharField()
    price = IntegerField()
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
