import unittest

from domain.entitati import Inchiriere


class TestCaseInchiriereDomain(unittest.TestCase):

    def test_create_inchiriere(self):

        inchiriere1 = Inchiriere('1', 'Oniga Andreea', '1', 'Anne')
        inchiriere2 = Inchiriere('1', 'Oniga Andreea', '2', 'King Arthur')

        self.assertEqual(inchiriere1.getIdClient(), '1')
        self.assertEqual(inchiriere1.getIdFilm(), '1')
        self.assertEqual(inchiriere1.getNumeClient(), 'Oniga Andreea')
        self.assertEqual(inchiriere2.getIdFilm(), '2')
