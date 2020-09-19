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
        
        self.assertEqual(response[0], expected_message)
        self.assertEqual(len(response[1]), expected_rows_returned)
        
    # try to get all artworks from an empty db
    def test_all_artworks_empty_db(self):
        clear_db()
        
        expected_message = 'No artworks found'
        response = all_artworks()
        
        self.assertEqual(response[0], expected_message)
        self.assertIsNone(response[1])
        
    # get all artists from db
    def test_all_artists(self):
        clear_db()
        populate_db()
        
        expected_message = 'All artists:'
        expected_rows_returned = 2
        response = all_artists()
        
        self.assertEqual(response[0], expected_message)
        self.assertEqual(len(response[1]), expected_rows_returned)
        
    # try to get all artists from an empty db
    def test_all_artists_empty_db(self):
        clear_db()
        
        expected_message = 'No artists found'
        response = all_artists()
        
        self.assertEqual(response[0], expected_message)
        self.assertIsNone(response[1])
        
    # search for an artwork whose title contains a string
    def test_search_by_title(self):
        clear_db()
        populate_db()
        
        expected_message = 'Search results:'
        expected_rows_returned = 1
        response = search_by_title(title='lilies')
        
        self.assertEqual(response[0], expected_message)
        self.assertEqual(len(response[1]), expected_rows_returned)
        
    # search by title for an artwork not in db
    def test_search_by_title_not_found(self):
        clear_db()
        
        expected_message = 'No artworks found'
        response = search_by_title(title='The Persistence of Memory')
        
        self.assertEqual(response[0], expected_message)
        self.assertIsNone(response[1])
        
    # search for all art by an artist
    def test_search_by_artist(self):
        clear_db()
        populate_db()
        
        expected_message = 'Search results:'
        expected_rows_returned = 2
        response = search_by_artist(artist_name='Claude Monet')
        
        self.assertEqual(response[0], expected_message)
        self.assertEqual(len(response[1]), expected_rows_returned)
        
    # search by artist w/ an artist not in db
    def test_search_by_artist_artist_not_in_db(self):
        clear_db()
        
        expected_message = 'Artist not found'
        response = search_by_artist(artist_name='Michelangelo Merisi da Caravaggio')
        
        self.assertEqual(response[0], expected_message)
        self.assertIsNone(response[1])
    
    # search by artist for an artist w/ no artworks
    def test_search_by_artist_artist_has_no_art(self):
        clear_db()
        degas = Artist(name='Edgar Degas', email='degas_in_detank@aol.com')
        degas.save()
        
        expected_message = 'No artworks found'
        response = search_by_artist(artist_name='Edgar Degas')
        
        self.assertEqual(response[0], expected_message)
        self.assertIsNone(response[1])
        
    # add an artist to db
    def test_add_artist(self):
        clear_db()
        
        expected_message = 'Added Hokusai to database:'
        hokusai_str = 'Hokusai (makinwaves@yubinbutsu.jp)'
        expected_rows_from_db_query = 1
        response = add_artist(name='Hokusai', email='makinwaves@yubinbutsu.jp')
        db_query = Artist.select().where(Artist.name == 'Hokusai')
        
        self.assertEqual(expected_message, response[0])
        self.assertEqual(hokusai_str, str(response[1][0]))  # test artist string is returned
        self.assertEqual(len(db_query), expected_rows_from_db_query)
        
    
    # add duplicate artist; user has no way of doing this directly, but it's good to test
    def test_add_artist_duplicate(self):
        clear_db()
        populate_db()
        
        expected_message = 'Failed to add artist'
        expected_rows_from_db_query = 1
        response = add_artist(name='Frida Kahlo', email='freeds1907@correo.mx')
        db_query = Artist.select().where(Artist.name == 'Frida Kahlo')
        
        self.assertEqual(expected_message, response[0])
        self.assertIsNone = (response[1])
        self.assertEqual(len(db_query), expected_rows_from_db_query)


def populate_db():
    frida = Artist(name='Frida Kahlo', email='freeds1907@correo.mx')
    claude = Artist(name='Claude Monet', email='ocmoney@poste.fr')
    frida.save()
    claude.save()
    
    roots = Artwork(artist=frida, title='Roots', price=5616000, available=False)
    self_portrait = Artwork(artist=frida, title='Self Portrait with Curly Hair', price=1351500, available=False)
    lilies = Artwork(artist=claude, title='Water Lilies', price=54000000, available=False)
    haystacks = Artwork(artist=claude, title='Haystacks', price=110700000, available=False)
    roots.save()
    self_portrait.save()
    lilies.save()
    haystacks.save()
    

def clear_db():
    Artwork.delete().execute()
    Artist.delete().execute()


if __name__ == '__main__':
    db.connect()
    db.create_tables([Artist, Artwork])
    unittest.main()
    clear_db()
    db.close()
