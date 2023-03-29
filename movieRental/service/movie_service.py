import random
import string

from domain.entitati import Movie
from domain.validatori import MovieValidator
from repository.movie_repo import InMemoryRepository_movie


def string_generator(size, char=string.ascii_letters):
    return ''.join(random.choice(char) for x in range(size))


def generate_title():
    return string_generator(1).upper() + string_generator(random.randint(3, 7)).lower()


def generate_description():
    return string_generator(1).upper() + string_generator(random.randint(3, 7)).lower()


class MovieService:
    """
    Responsabil de efectuarea operatiilor cerute de utilizator
    Coordoneaza operatiile necesare pentru a realiza actiunea declansata de utilizator

    """
    def __init__(self, repo, val):
        """
        Initializeaza service
        :param repo: obiectul de tip repo care ne ajuta sa gestionam lista de filme
        :type repo: InMemoryRepository_movie
        :param val: validator pentru verificarea filmelor
        :type val: MovieValidator
        """
        self.__repo = repo
        self.__validator = val

    def add_movie(self, id, titlu, descriere, gen):
        """
        Adaugare film in lista de filme
        :param id: id-ul filmului
        :type id: str
        :param titlu: titlul filmului
        :type titlu: str
        :param descriere: descrierea filmului
        :type descriere: str
        :param gen: genul filmului
        :type gen: str
        :return: obiectul de tip Movie creat
        :rtype: -;
        :raises: ValueError daca filmul nu este valid
        """

        a = Movie(id, titlu, descriere, gen)

        self.__validator.validate(a)
        self.__repo.store(a)

        return a

    def get_all_movies(self):
        """
        Returneaza o lista cu toate filmele
        :return: lista de filme
        :rtype: list of Movie objects
        """
        return self.__repo.get_all_movies()

    def update_movie(self, id, titlu, descriere, gen):
        """
        Modifica datele unui film
        :param id: id-ul filmului de modificat
        :type id:str
        :param titlu: titlul nou al filmului
        :type titlu: str
        :param descriere: descrierea noua a filmului
        :type descriere: str
        :param gen: genul filmului
        :type gen: str
        :return: filmul modificat
        :rtype: Movie
        :raises: ValueError daca nu exista filmul cu id-ul dat
        """
        a = Movie(id, titlu, descriere, gen)

        self.__validator.validate(a)
        return self.__repo.update(id, a)

    def find_by_id(self, id):
        """
        Cauta filmul cu id-ul dat
        :param id: id dat
        :type id: str
        :return: filmul cu identificatorul id/None daca nu exista filmul
        :rtype: Movie
        """
        return self.__repo.find(id)

    def delete_by_id(self, id):
        """
        Sterge filmele dupa id
        :param id: id-ul dat
        :type id: str
        :return:
        :rtype:
        """
        return self.__repo.delete_by_id(id)

    def filter_by_genre(self, gen):
        """
        Selecteaza filmele care au genul dat
        :param gen: genul cu care se compara
        :type gen: str
        :return:
        :rtype:
        """
        movies = self.__repo.get_all_movies()
        movies_with_good_genre = [movie for movie in movies if gen in movie.getGen()]
        return movies_with_good_genre

