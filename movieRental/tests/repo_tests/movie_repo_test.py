import unittest

from domain.entitati import Movie
from exceptions.exceptions import MovieNotFoundException, DuplicateIDException
from repository.movie_repo import InMemoryRepository_movie, MovieRepoFileInheritance


class TestCaseMovieRepoMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = InMemoryRepository_movie()

    def test_store(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')

        self.repo.store(m)

        self.assertEqual(self.repo.size(), 1)

        self.repo.store(n)
        self.assertEqual(self.repo.size(), 2)
        self.assertEqual(self.repo.find(m.getId()), m)
        c = Movie('1', 'No Time to Die', 'very good', 'Actiune, Thriller')
        self.assertRaises(DuplicateIDException, self.repo.store, c)

    def test_get_all(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')
        self.repo.store(m)
        self.assertIsInstance(self.repo.get_all_movies(), list)
        self.assertEqual(len(self.repo.get_all_movies()), 1)

        self.repo.store(n)

        self.assertEqual(len(self.repo.get_all_movies()), 2)
        self.assertEqual(self.repo.get_all_movies()[0], m)
        self.assertEqual(self.repo.get_all_movies()[1], n)

        self.repo.delete_by_id('2')
        self.assertEqual(len(self.repo.get_all_movies()), 1)

    def test_get_size(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')
        self.repo.store(m)
        self.assertEqual(self.repo.size(), 1)
        self.repo.store(n)
        self.assertEqual(self.repo.size(), 2)
        self.repo.delete_by_id('1')
        self.assertEqual(self.repo.size(), 1)

        c = Movie('1', 'No Time to Die', 'very good', 'Actiune, Thriller')
        self.repo.update('2', c)
        self.assertEqual(self.repo.size(), 1)

    def test_delete_all(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')
        self.repo.store(m)
        self.repo.store(n)
        self.assertEqual(self.repo.size(), 2)
        self.repo.delete_all()
        self.assertEqual(self.repo.size(), 0)

    def test_delete(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')
        self.repo.store(m)
        self.repo.store(n)

        deleted_movie = self.repo.delete_by_id('1')
        self.assertEqual(self.repo.size(), 1)
        self.assertEqual(deleted_movie, m)
        self.assertRaises(MovieNotFoundException, self.repo.delete_by_id, 'some_id')

    def test_update(self):

        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        self.repo.store(m)

        n = Movie('1', 'Yes day', 'funny', 'Family')

        updated_movie = self.repo.update('1', n)
        self.assertEqual(updated_movie.getTitlu(), 'Yes day')
        self.assertEqual(updated_movie.getDescriere(), 'funny')
        self.assertRaises(MovieNotFoundException, self.repo.update, '7', n)


class TestCaseMovieRepoFile(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = MovieRepoFileInheritance('test_movie_repo.txt')
        self.repo.delete_all()

    def test_store(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')

        self.repo.store(m)

        self.assertEqual(self.repo.size(), 1)

        self.repo.store(n)
        self.assertEqual(self.repo.size(), 2)
        self.assertEqual(self.repo.find(m.getId()), m)
        c = Movie('1', 'No Time to Die', 'very good', 'Actiune, Thriller')
        self.assertRaises(DuplicateIDException, self.repo.store, c)

    def test_get_all(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')
        self.repo.store(m)
        self.assertIsInstance(self.repo.get_all_movies(), list)
        self.assertEqual(len(self.repo.get_all_movies()), 1)

        self.repo.store(n)

        self.assertEqual(len(self.repo.get_all_movies()), 2)
        self.assertEqual(self.repo.get_all_movies()[0], m)
        self.assertEqual(self.repo.get_all_movies()[1], n)

        self.repo.delete_by_id('2')
        self.assertEqual(len(self.repo.get_all_movies()), 1)

    def test_get_size(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')
        self.repo.store(m)
        self.assertEqual(self.repo.size(), 1)
        self.repo.store(n)
        self.assertEqual(self.repo.size(), 2)
        self.repo.delete_by_id('1')
        self.assertEqual(self.repo.size(), 1)

        c = Movie('1', 'No Time to Die', 'very good', 'Actiune, Thriller')
        self.repo.update('2', c)
        self.assertEqual(self.repo.size(), 1)

    def test_delete_all(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')
        self.repo.store(m)
        self.repo.store(n)
        self.assertEqual(self.repo.size(), 2)
        self.repo.delete_all()
        self.assertEqual(self.repo.size(), 0)

    def test_delete(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        n = Movie('2', 'Yes day', 'funny', 'Family')
        self.repo.store(m)
        self.repo.store(n)

        deleted_movie = self.repo.delete_by_id('1')
        self.assertEqual(self.repo.size(), 1)
        self.assertEqual(deleted_movie, m)
        self.assertRaises(MovieNotFoundException, self.repo.delete_by_id, 'some_id')

    def test_update(self):
        m = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
        self.repo.store(m)

        n = Movie('1', 'Yes day', 'funny', 'Family')

        updated_movie = self.repo.update('1', n)
        self.assertEqual(updated_movie.getTitlu(), 'Yes day')
        self.assertEqual(updated_movie.getDescriere(), 'funny')
        self.assertRaises(MovieNotFoundException, self.repo.update, '7', n)

    def tearDown(self) -> None:
        self.repo.delete_all()
