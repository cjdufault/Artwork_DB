from peewee import *
from artwork import *
import unittest


class TestArtwork(unittest.TestCase):
    
    # get all artworks in db
    def test_all_artworks(self):
        clear_db()
        populate_db()
        
        expected_message = 'All artworks:'
        expected_rows_returned = 4
        response = all_artworks()
        
        self.assertEqual(response[0], expected_message, 'Failed: all_artworks returned the wrong status message')
        self.assertEqual(len(response[1]), expected_rows_returned,
                         'Failed: all_artworks returned the wrong number of rows')
        
    # try to get all artworks from an empty db
    def test_all_artworks_empty_db(self):
        clear_db()
        
        expected_message = 'No artworks found'
        response = all_artworks()
        
        self.assertEqual(response[0], expected_message, 'Failed: all_artworks returned the wrong status message')
        self.assertIsNone(response[1], 'Failed: all_artworks returned rows from the db when it shouldn\'t have')
        
    # get all artists from db
    def test_all_artists(self):
        clear_db()
        populate_db()
        
        expected_message = 'All artists:'
        expected_rows_returned = 2
        response = all_artists()
        
        self.assertEqual(response[0], expected_message, 'Failed: all_artists returned the wrong status message')
        self.assertEqual(len(response[1]), expected_rows_returned,
                         'Failed: all_artists returned the wrong number of rows')
        
    # try to get all artists from an empty db
    def test_all_artists_empty_db(self):
        clear_db()
        
        expected_message = 'No artists found'
        response = all_artists()
        
        self.assertEqual(response[0], expected_message, 'Failed: all_artists returned the wrong status message')
        self.assertIsNone(response[1], 'Failed: all_artists returned rows from the db when it shouldn\'t have')
        
    # search for an artwork whose title contains a string
    def test_search_by_title(self):
        clear_db()
        populate_db()
        
        expected_message = 'Search results:'
        expected_rows_returned = 1
        response = search_by_title(title='lilies')
        
        self.assertEqual(response[0], expected_message, 'Failed: search_by_title returned the wrong status message')
        self.assertEqual(len(response[1]), expected_rows_returned,
                         'Failed: search_by_title returned the wrong number of rows')
        
    # search by title for an artwork not in db
    def test_search_by_title_not_in_db(self):
        clear_db()
        
        expected_message = 'No artworks found'
        response = search_by_title(title='The Persistence of Memory')
        
        self.assertEqual(response[0], expected_message, 'Failed: search_by_title returned the wrong status message')
        self.assertIsNone(response[1],
                          'Failed: search_by_title returned rows from the db when it shouldn\'t have')
        
    # search for all art by an artist
    def test_search_by_artist(self):
        clear_db()
        populate_db()
        
        expected_message = 'Search results:'
        expected_rows_returned = 2
        response = search_by_artist(artist_name='Claude Monet')
        
        self.assertEqual(response[0], expected_message, 'Failed: search_by_artist returned the wrong status message')
        self.assertEqual(len(response[1]), expected_rows_returned,
                         'Failed: search_by_artist returned the wrong number of rows')
        
    # search by artist w/ an artist not in db
    def test_search_by_artist_not_in_db(self):
        clear_db()
        
        expected_message = 'Artist not found'
        response = search_by_artist(artist_name='Michelangelo Merisi da Caravaggio')
        
        self.assertEqual(response[0], expected_message,
                         'Failed: search_by_artist returned the wrong status message')
        self.assertIsNone(response[1],
                          'Failed: search_by_artist returned rows from the db when it shouldn\'t have')
    
    # search by artist for an artist w/ no artworks
    def test_search_by_artist_no_art(self):
        clear_db()
        degas = Artist(name='Edgar Degas', email='degas_in_detank@aol.com')
        degas.save()
        
        expected_message = 'No artworks found'
        response = search_by_artist(artist_name='Edgar Degas')
        
        self.assertEqual(response[0], expected_message,
                         'Failed: search_by_artist returned the wrong status message')
        self.assertIsNone(response[1],
                          'Failed: search_by_artist returned rows from the db when it shouldn\'t have')
        
    # search for available art by an artist
    def test_available_by_artist(self):
        clear_db()
        populate_db()
        
        expected_message = 'Available artworks:'
        expected_rows_returned = 1
        response = available_by_artist(artist_name='Frida Kahlo')
        
        self.assertEqual(response[0], expected_message, 'Failed: available_by_artist returned the wrong status message')
        self.assertEqual(len(response[1]), expected_rows_returned,
                         'Failed: available_by_artist returned the wrong number of rows')
        
    # add an artist to db
    def test_add_artist(self):
        clear_db()
        
        expected_message = 'Added Hokusai to database:'
        expected_rows_returned = 1
        expected_rows_from_db_query = 1
        response = add_artist(name='Hokusai', email='makinwaves@yubinbutsu.jp')
        db_query = Artist.select().where(Artist.name == 'Hokusai')
        
        self.assertEqual(expected_message, response[0], 'Failed: add_artist returned the wrong status message')
        self.assertEqual(expected_rows_from_db_query, len(response[1]),
                         'Failed: add_artist returned the wrong number of rows')  
        self.assertEqual(len(db_query), expected_rows_from_db_query,
                         'Failed: add_artist did\'nt add artist to database correctly')
        
    
    # add duplicate artist; user has no way of doing this directly, but it's good to test
    def test_add_artist_duplicate(self):
        clear_db()
        populate_db()
        
        expected_message = 'Failed to add artist'
        expected_rows_from_db_query = 1
        response = add_artist(name='Frida Kahlo', email='frida2@correo.mx')
        db_query = Artist.select().where(Artist.name == 'Frida Kahlo')
        
        self.assertEqual(expected_message, response[0], 'Failed: add_artist returned the wrong status message')
        self.assertIsNone = (response[1], 'Failed add_artist returned rows when it shouldn\'t have')
        self.assertEqual(len(db_query), expected_rows_from_db_query, 'Failed: add_artist added duplicate artist')
        
    # add an artwork to db
    def test_add_artwork(self):
        clear_db()
        populate_db()
        
        expected_message = 'Added artwork to database:'
        expected_rows_from_db_query = 1
        expected_rows_returned = 1
        response = add_artwork(artist_name='Frida Kahlo', title='Self-Portrait with Thorn Necklace and Hummingbird',
                               price=15000000, available=True)
        db_query = Artwork.select().where(Artwork.title == 'Self-Portrait with Thorn Necklace and Hummingbird')
        
        self.assertEqual(expected_message, response[0], 'Failed: add_artwork returned the wrong status message')
        self.assertEqual(expected_rows_returned, len(response[1]),
                         'Failed: add_artwork returned the wrong number of rows')
        self.assertEqual(expected_rows_from_db_query, len(db_query),
                         'Failed: add_artwork did\'nt add artwork to database correctly')
        
    # adding an artwork with a duplicate title shouldn't work
    def test_add_artwork_duplicate(self):
        clear_db()
        populate_db()
        
        expected_message = 'Failed to add artwork'
        expected_rows_from_db_query = 1
        response = add_artwork(artist_name='Claude Monet', title='Haystacks',
                               price=15000000, available=True)
        db_query = Artwork.select().where(Artwork.title == 'Haystacks')
        
        self.assertEqual(expected_message, response[0], 'Failed: add_artwork returned the wrong status message')
        self.assertIsNone(response[1], 'Failed: add_artwork returned rows when it shouldn\'t have')
        self.assertEqual(expected_rows_from_db_query, len(db_query), 'Failed: add_artwork added duplicate artist')
        
    # change an artist's email address
    def test_update_email(self):
        clear_db()
        populate_db()
        
        new_email = 'fridas.new.email@hotmail.com'
        update_email(artist_name='Frida Kahlo', email=new_email)
        db_query = Artist.select().where(Artist.email == new_email)
        
        self.assertEqual(len(db_query), 1, 'Failed: update_email didn\'t update the email correctly')
        
    # change email for an artist not in db
    def test_update_email_not_in_db(self):
        clear_db()
        
        expected_message = 'No artist named Vincent Van Gogh'
        expected_rows_from_db_query = 0
        response = update_email(artist_name='Vincent Van Gogh', email='vinnie_goes@post.nl')
        db_query = Artist.select().where(Artist.email == 'vinnie_goes@post.nl')
        
        self.assertEqual(expected_message, response[0], 'Failed: update_email returned the wrong status message')
        self.assertEqual(expected_rows_from_db_query, len(db_query), 
                         'Failed: update_email updated an email address when the specified artist wasn\'t in db')
    
    # change availability of an artwork
    def test_update_availability(self):
        clear_db()
        populate_db()
        
        update_availability(title='Roots', available=True)
        db_query = Artwork.select().where(Artwork.title == 'Roots' and Artwork.available)
        
        self.assertEqual(len(db_query), 1, 'Failed: update_availability didn\'t update availability correctly')
        
    # change availability of artwork not in db
    def test_update_availability_not_in_db(self):
        clear_db()
        
        expected_message = 'No artwork titled "The Broken Column"'
        expected_rows_from_db_query = 0
        response = update_availability(title='The Broken Column', available=True)
        
        self.assertEqual(expected_message, response[0], 'Failed: update_availability returned the wrong message')
        
    # delete artist and all their work
    def test_delete_artist(self):
        clear_db()
        populate_db()
        
        delete_artist(artist_name='Claude Monet', override_warning=True)
        artist_query = Artist.select().where(Artist.name == 'Claude Monet')
        artwork_query = Artwork.select().where(Artwork.artist.name == 'Claude Monet')
        
        self.assertEqual(len(artist_query), 0, 'Failed: delete_artist didn\'t delete artist correctly')
        self.assertEqual(len(artwork_query), 0, 'Failed: delete_artist didn\'t all of the artist\'s artworks')
    
    # delete artist not in db
    def test_delete_artist_not_in_db(self):
        clear_db()
        
        expected_message = 'Artist not found'
        response = delete_artist(artist_name='Rembrandt', override_warning=True)
        
        self.assertEqual(expected_message, response[0], 'Failed: delete_artist returned the wrong status message')
    
    # delete an Artwork
    def test_delete_artwork(self):
        clear_db()
        populate_db()
        
        delete_artwork(artist_name='Claude Monet', title='Water Lilies', override_warning=True)
        db_query = Artwork.select().where(Artwork.title == 'Water Lilies')
        
        self.assertEqual(len(db_query), 0, 'Failed: delete_artwork didn\'t delete the artwork')
        
    # try to delete artwork not in db
    def test_delete_artwork_not_in_db(self):
        clear_db()
        
        expected_message = 'Artwork not found'
        response = delete_artwork(artist_name='Frida Kahlo', title='Memory, the Heart', override_warning=True)
        
        self.assertEqual(expected_message, response[0], 'Failed: delete_artwork returned the wrong status message')


# fill db with known values
def populate_db():
    frida = Artist(name='Frida Kahlo', email='freeds1907@correo.mx')
    claude = Artist(name='Claude Monet', email='ocmoney@poste.fr')
    frida.save()
    claude.save()
    
    roots = Artwork(artist=frida, title='Roots', price=5616000, available=True)
    self_portrait = Artwork(artist=frida, title='Self Portrait with Curly Hair', price=1351500, available=False)
    lilies = Artwork(artist=claude, title='Water Lilies', price=54000000, available=False)
    haystacks = Artwork(artist=claude, title='Haystacks', price=110700000, available=False)
    roots.save()
    self_portrait.save()
    lilies.save()
    haystacks.save()
    

# clear all tables in db
def clear_db():
    Artwork.delete().execute()
    Artist.delete().execute()


if __name__ == '__main__':
    db.connect()
    db.create_tables([Artist, Artwork])
    unittest.main()
    db.close()
