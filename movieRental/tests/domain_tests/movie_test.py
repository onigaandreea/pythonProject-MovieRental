import unittest

from domain.entitati import Movie
from domain.validatori import MovieValidator


class TestCaseMovieDomain(unittest.TestCase):

    def setUp(self) -> None:
        self.__validator = MovieValidator()

    def test_create_movie(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        self.assertEqual(m.getId(), '1')
        self.assertEqual(m.getTitlu(), 'Reminiscence')
        self.assertEqual(m.getDescriere(), 'nice')
        self.assertEqual(m.getGen(), 'SF, Romantic, Thriller')

        m.setId('1')
        m.setTitlu('Reminiscence')
        m.setDescriere('great')
        m.setGen('SF, Romantic')

        self.assertEqual(m.getId(), '1')
        self.assertEqual(m.getTitlu(), 'Reminiscence')
        self.assertEqual(m.getDescriere(), 'great')
        self.assertEqual(m.getGen(), 'SF, Romantic')

    def test_equal_movie(self):
        a = Movie('1', 'Reminiscence ', 'nice', 'SF, Romantic, Thriller')
        b = Movie('1', 'No Time to Die', 'very good', 'Actiune, Thriller')

        self.assertEqual(a, b)

        c = Movie('2', 'No Time to Die', 'very good', 'Actiune, Thriller')
        self.assertNotEqual(a, c)

    def test_validate_movie(self):
        validator = MovieValidator()
        a = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        c = Movie('2', 'No Time to Die', 'very good', 'Actiune, Thriller')
        self.__validator.validate(a)
        self.__validator.validate(c)

        b = Movie('0', '', 'nice', 'Justitiar')
        self.assertRaises(ValueError, self.__validator.validate, b)

        b1 = Movie('-16', '', '', '')
        self.assertRaises(ValueError, self.__validator.validate, b1)

