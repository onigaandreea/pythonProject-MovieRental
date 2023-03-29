import unittest

from repository.movie_repo import MovieRepoFile
from repository.client_repo import ClientRepoFile
from repository.inchirieri_repo import InchiriereRepoFile
from service.inchirieri_service import InchireriService


class TestCaseInchirieriService(unittest.TestCase):
    def setUp(self) -> None:
        inchiriere_repo = InchiriereRepoFile('test_scores_srv.txt')

        repo_movie = MovieRepoFile('test_athletes_srv.txt')
        repo_client= ClientRepoFile('test_categories_srv.txt')
        self.__inchiriere_srv = InchireriService(inchiriere_repo, repo_movie, repo_client)

    def test_add_inchiriere(self):
        self.__inchiriere_srv.add_inchiriere('1', '1')
        self.__inchiriere_srv.add_inchiriere('1', '2')
        self.__inchiriere_srv.add_inchiriere('1', '4')
        self.__inchiriere_srv.add_inchiriere('2', '2')
        self.__inchiriere_srv.add_inchiriere('3', '1')
        self.__inchiriere_srv.add_inchiriere('3', '2')

        self.assertEqual(len(self.__inchiriere_srv.toate_inchirierile()), 6)

    def tearDown(self) -> None:
        self.__score_srv.delete_all()
