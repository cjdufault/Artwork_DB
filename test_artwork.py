from peewee import *
from artwork import *
import unittest


class TestArtwork(unittest.TestCase):
    
    def test_all_artworks(self):
        clear_db()
        populate_db()
        
        expected_message = 'All artworks:'
        expected_rows_returned = 4
        response = all_artworks()
        
        assert response[0] == expected_message
        assert len(response[1]) == expected_rows_returned
        
    def test_all_artworks_empty_db(self):
        clear_db()
        
        expected_message = 'No artworks found'
        response = all_artworks()
        
        assert response[0] == expected_message
        self.assertIsNone(response[1])
        
    def test_all_artists(self):
        clear_db()
        populate_db()
        
        expected_message = 'All artists:'
        expected_rows_returned = 2
        response = all_artists()
        
        assert response[0] == expected_message
        assert len(response[1]) == expected_rows_returned
        
    def test_all_artists_empty_db(self):
        clear_db()
        
        expected_message = 'No artists found'
        response = all_artists()
        
        assert response[0] == expected_message
        self.assertIsNone(response[1])
        
    def test_search_by_title(self):
        clear_db()
        populate_db()
        
        expected_message = 'Search results:'
        expected_rows_returned = 1
        response = search_by_title(title='lilies')
        
        assert response[0] == expected_message
        assert len(response[1]) == expected_rows_returned
        
    def test_search_by_title_not_found(self):
        clear_db()
        
        expected_message = 'No artworks found'
        response = search_by_title(title='The Persistence of Memory')
        
        assert response[0] == expected_message
        self.assertIsNone(response[1])
        
    def test_search_by_artist(self):
        clear_db()
        populate_db()
        
        expected_message = 'Search results:'
        expected_rows_returned = 2
        response = search_by_title(artist_name='Claude Monet')
        
        assert response[0] == expected_message
        assert len(response[1]) == expected_rows_returned
        
    def test_search_by_artist_not_found(self):
        clear_db()
        
        expected_message = 'No artworks found'
        response = search_by_title(artist_name='Michelangelo Merisi da Caravaggio')
        
        assert response[0] == expected_message
        self.assertIsNone(response[1])
        


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
