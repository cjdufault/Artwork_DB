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
    Artwork.delete()
    Artist.delete()


if __name__ == '__main__':
    db.connect()
    db.create_tables([Artist, Artwork])
    unittest.main()
