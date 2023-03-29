import unittest

from domain.validatori import MovieValidator
from exceptions.exceptions import ValidationException, MovieNotFoundException
from repository.movie_repo import InMemoryRepository_movie
from service.movie_service import MovieService


class TestCaseAthleteService(unittest.TestCase):
    def setUp(self) -> None:
        repo = InMemoryRepository_movie()
        validator = MovieValidator()
        self.__movie_srv = MovieService(repo, validator)

    def test_add_movie(self):
        added_movie = self.__movie_srv.add_movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        self.assertEqual(added_movie.getId(), '1')
        self.assertEqual(len(self.__movie_srv.get_all_movies()), 1)
        self.assertRaises(ValidationException, self.__movie_srv.add_movie, '2', '', 'hfdg', '')

    def test_get_all(self):
        added_movie = self.__movie_srv.add_movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        self.assertEqual(len(self.__movie_srv.get_all_movies()), 1)

        added_movie2 = self.__movie_srv.add_movie('2', 'Yes day', 'funny', 'Family')
        self.assertEqual(len(self.__movie_srv.get_all_movies()), 2)

        self.assertEqual(self.__movie_srv.get_all_movies()[0].getTitlu(), 'Reminiscence')
        self.assertEqual(self.__movie_srv.get_all_movies()[1].getTitlu(), 'Yes day')

        updated_movie = self.__movie_srv.update_movie('1', 'Reminiscence', 'nice', 'SF')
        self.assertEqual(len(self.__movie_srv.get_all_movies()), 2)

        self.assertEqual(self.__movie_srv.get_all_movies()[0].getTitlu(), 'Reminiscence')

        deleted_movie = self.__movie_srv.delete_by_id('2')
        self.assertEqual(len(self.__movie_srv.get_all_movies()), 1)
        self.assertEqual(self.__movie_srv.get_all_movies()[0].getTitlu(), 'Reminiscence')

    def test_delete_movie_by_id(self):
        added_movie = self.__movie_srv.add_movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        added_movie2 = self.__movie_srv.add_movie('2', 'Yes day', 'funny', 'Family')

        deleted_movie = self.__movie_srv.delete_by_id('1')
        self.assertEqual(len(self.__movie_srv.get_all_movies()), 1)

        self.assertEqual(deleted_movie.getTitlu(), 'Reminiscence')
        self.assertEqual(deleted_movie.getDescriere(), 'nice')

        self.assertEqual(self.__movie_srv.get_all_movies()[0].getTitlu(), 'Yes day')
        self.assertRaises(MovieNotFoundException, self.__movie_srv.delete_by_id, 'wrongid')

    def test_update_movie(self):
        added_movie = self.__movie_srv.add_movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        added_movie2 = self.__movie_srv.add_movie('2', 'Yes day', 'funny', 'Family')

        updated_movie = self.__movie_srv.update_movie('1', 'Reminiscence', 'nice', 'SF')
        self.assertEqual(len(self.__movie_srv.get_all_movies()), 2)

        self.assertEqual(updated_movie.getTitlu(), 'Reminiscence')
        self.assertEqual(updated_movie.getGen(), 'SF')

        modified_movie_in_list = self.__movie_srv.find_by_id('1')
        unchanged_movie = self.__movie_srv.find_by_id('2')

        self.assertEqual(updated_movie, modified_movie_in_list)
        self.assertEqual(unchanged_movie, added_movie2)

        self.assertRaises(ValidationException, self.__movie_srv.update_movie, 'wrongid', '', '', 'yusgfeiu')

    def test_filter_by_genre(self):

        added_movie = self.__movie_srv.add_movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        added_movie2 = self.__movie_srv.add_movie('2', 'Yes day', 'funny', 'Family')
        added_movie3 = self.__movie_srv.add_movie('3', 'No Time to Die', 'very good', 'Actiune, Thriller')
        added_movie4 = self.__movie_srv.add_movie('4', 'Dune', 'very good', 'SF')

        filtered_list = self.__movie_srv.filter_by_genre('SF')
        self.assertEqual(len(filtered_list), 2)

        filtered_list = self.__movie_srv.filter_by_genre('Actiune')
        self.assertEqual(len(filtered_list), 1)

        filtered_list = self.__movie_srv.filter_by_genre('Romantic')
        self.assertEqual(len(filtered_list), 1)

        filtered_list = self.__movie_srv.filter_by_genre('Comedie')
        self.assertEqual(len(filtered_list), 0)

