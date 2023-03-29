from domain.entitati import Movie
from exceptions.exceptions import DuplicateIDException, MovieNotFoundException


class InMemoryRepository_movie:
    """
    Clasa creata cu responsabilitatea de a gestiona
    multimea de filme
    """

    def __init__(self):

        self.__movies = []

    def __exists_id(self, id):
        for movie in self.__movies:
            if movie.getId() == id:
                return True
        return False

    def find(self, id):
        """
        Cauta filmul cu id dat
        :param id: id dat
        :type id: str
        :return: filmul cu identificator id/None daca nu exista
        :rtype: Movie
        """
        for movie in self.__movies:
            if movie.getId() == id:
                return movie
        return None

    def store(self, movie):
        """
        Adauga un film in lista
        :param movie: filmul de adaugat
        :type movie: Movie
        :return: -; lista de filme se modifica prin adaugarea filmului
        :rtype:
        :raises:
        """
        if self.__exists_id(movie.getId()):
            raise DuplicateIDException

        self.__movies.append(movie)

    def get_all_movies(self):
        """
        Returneaza o lista cu toate filmele
        :rtype: list of Movie objects
        """
        return self.__movies

    def size(self):
        """
        Returneaza numarul de filme in lista
        :rtype: int
        """
        return len(self.__movies)

    def delete_by_id(self, id):
        """
        Sterge filmul cu id-ul dat din lista de filme
        :param id: id-ul dat
        :type id: str
        :return: obiectul film sters
        :rtype: Movie
        :raises: ValueError daca nu exista film cu id dat
        """
        if not self.__exists_id(id):
            raise MovieNotFoundException

        movie = self.find(id)
        self.__movies.remove(movie)
        return movie

    def update(self, id, new_movie):
        """
        Modifica datele filmului cu identificator id
        :param id: id-ul dat
        :type id: str
        :param new_movie: filmul cu noile date
        :type new_movie: Movie
        :return: filmul modificat
        :rtype: Movie
        """
        movie = self.find(id)
        if movie is None:
            raise MovieNotFoundException
        movie.setTitlu(new_movie.getTitlu())
        movie.setDescriere(new_movie.getDescriere())
        movie.setGen(new_movie.getGen())
        return movie

    def delete_all(self):
        """
        Sterge toate filmele din lista
        """
        self.__movies.clear()

    def get_movie_by_criteria(self, filter_function):
        """
        Selecteaza elementele din lista care indeplinesc un criteriu
        :param filter_function: functia dupa care se filtreaza
        :type filter_function: function
        :return: lista de filme care indeplinesc criteriul
        :rtype: list of Movies
        """
        return [movie for movie in self.__movies if filter_function(movie)]


class MovieRepoFile:
    def __init__(self, filename):
        self.__filename = filename

    def __load_from_file(self):
        """
        Incarca datele din fisier
        :return: lista cu filme din fisier
        :rtype: list of Movies
        """

        try:
            f = open(self.__filename, 'r')
            # f = io.open(self.__filename, mode='r', encoding='utf-8')
        except IOError:
            print('Fisiereul nu se poate deschide.')

        movies = []
        lines = f.readlines()
        for line in lines:
            movie_id, movie_titlu, movie_descriere, movie_gen = [token.strip() for token in line.split(';')]
            a = Movie(movie_id, movie_titlu, movie_descriere, movie_gen)
            movies.append(a)
        f.close()
        return movies

    def __save_to_file(self, movies_list):
        """
        Salveaza in fisier filmele date
        :param movies_list: lista de filme
        :type movies_list: list of Movies
        :return: -
        :rtype: -
        """
        with open(self.__filename, 'w') as f:
            for movie in movies_list:
                movie_string = str(movie.getId()) + ';' + str(movie.getTitlu()) + ';' + str(
                    movie.getDescriere()) + ';' + str(movie.getGen()) + '\n'
                f.write(movie_string)

    def store(self, movie):
        """
        Adauga un film in lista
        :param movie: filmul de adaugat
        :type movie: Movie
        :return: -; lista de filme se modifica prin adaugarea filmului
        :rtype: -; filmul este adaugat
        :raises:
        """
        all_movies = self.__load_from_file()
        if movie in all_movies:
            raise DuplicateIDException
        all_movies.append(movie)
        self.__save_to_file(all_movies)

    def __find_index(self, movies, id):
        """
        Gaseste pozitia in lista a unui film
        :param movies: lista de filme
        :type movies: list of Movies
        :param id: id-ul dat
        :type id: str
        :return: pozitia fimului cu id in movies
        :rtype: int, >0, <size(), -1 daca filmul cu id dat nu exista
               """
        index = -1
        for i in range(len(movies)):
            if movies[i].getId() == id:
                index = i
        return index

    def update(self, id, new_movie):
        """
        Actualizeaza datele unui film
        :param id: id-ul filmului care se modifica
        :type id: id-ul dat
        :param new_movie: noul film
        :type new_movie: Movie
        :return: fimul modificat
        :rtype: Movie
        """
        all_movies = self.__load_from_file()
        index = self.__find_index(all_movies, id)
        if index == -1:
            raise MovieNotFoundException
        all_movies[index] = new_movie
        self.__save_to_file(all_movies)
        return new_movie

    def delete(self, id):
        """
        Sterge filmul cu id-ul dat din lista de filme
        :param id: id-ul dat
        :type id: str
        :return: obiectul film sters
        :rtype: Movie
        :raises:
        """
        all_movies = self.__load_from_file()
        index = self.__find_index(all_movies, id)
        if index == -1:
            raise MovieNotFoundException
        deleted_movie = all_movies.pop(index)
        self.__save_to_file(all_movies)
        return deleted_movie

    def find(self, id):
        """
        Cauta filmul cu id dat
        :param id: id dat
        :type id: str
        :return: filmul cu identificator id, None daca nu exista
        :rtype: Movie
        """
        all_movies = self.__load_from_file()
        for movie in all_movies:
            if movie.getId() == id:
                return movie
        return None

    def get_all(self):
        """
        Returneaza o lista cu toate filmele existente
        :rtype: list of Movies
        """
        return (self.__load_from_file())

    def size(self):
        """
        Returneaza numarul de filme existente
        :rtype: int
        """
        return len(self.__load_from_file())

    def delete_all(self):
        """
        Sterge toate filmele din lista

        """
        self.__save_to_file([])


class MovieRepoFileInheritance(InMemoryRepository_movie):
    def __init__(self, filename):
        InMemoryRepository_movie.__init__(self)
        self.__filename = filename
        self.__load_from_file()

    def __load_from_file(self):
        """
        Incarca datele din fisier
        :return: lista cu filme din fisier
        :rtype: list of Movies
        """

        try:
            f = open(self.__filename, 'r')
            # f = io.open(self.__filename, mode='r', encoding='utf-8')
        except IOError:
            print('Fisiereul nu se poate deschide.')

        movies = []
        lines = f.readlines()
        for line in lines:
            movie_id, movie_titlu, movie_descriere, movie_gen = [token.strip() for token in line.split(';')]
            a = Movie(movie_id, movie_titlu, movie_descriere, movie_gen)
            InMemoryRepository_movie.store(self, a)
        f.close()

    def __save_to_file(self):
        """
        Salveaza in fisier filmele date

        """
        movies_list = InMemoryRepository_movie.get_all_movies(self)
        with open(self.__filename, 'w') as f:
            for movie in movies_list:
                movie_string = str(movie.getId()) + ';' + str(movie.getTitlu()) + ';' + str(
                    movie.getDescriere()) + ';' + str(movie.getGen()) + '\n'
                f.write(movie_string)

    def store(self, movie):
        """
        Adauga un film in lista
        :param movie: filmul de adaugat
        :type movie: Movie
        :return: -; lista de filme se modifica prin adaugarea filmului
        :rtype: -; filmul este adaugat
        :raises:
        """

        InMemoryRepository_movie.store(self, movie)
        self.__save_to_file()

    def update(self, id, new_movie):
        """
        Actualizeaza datele unui film
        :param id: id-ul filmului care se modifica
        :type id: id-ul dat
        :param new_movie: noul film
        :type new_movie: Movie
        :return: fimul modificat
        :rtype: Movie
        """
        InMemoryRepository_movie.update(self, id, new_movie)
        self.__save_to_file()
        return new_movie

    def delete(self, id):
        """
        Sterge filmul cu id-ul dat din lista de filme
        :param id: id-ul dat
        :type id: str
        :return: obiectul film sters
        :rtype: Movie
        :raises:
        """
        deleted_movie = InMemoryRepository_movie.delete_by_id(self, id)
        self.__save_to_file()
        return deleted_movie

    def find(self, id):
        """
        Cauta filmul cu id dat
        :param id: id dat
        :type id: str
        :return: filmul cu identificator id, None daca nu exista
        :rtype: Movie
        """
        return InMemoryRepository_movie.find(self, id)

    def get_all(self):
        """
        Returneaza o lista cu toate filmele existente
        :rtype: list of Movies
        """
        return InMemoryRepository_movie.get_all_movies(self)

    def size(self):
        """
        Returneaza numarul de filme existente
        :rtype: int
        """
        return InMemoryRepository_movie.size(self)

    def delete_all(self):
        """
        Sterge toate filmele din lista

        """
        InMemoryRepository_movie.delete_all(self)
        self.__save_to_file()


def setup_test_repo():

    a1 = Movie('1', 'Reminiscence', 'nice', 'SF, Romantic, Thriller')
    a2 = Movie('2', 'Yes day', 'funny', 'Family')
    a3 = Movie('3', 'No Time to Die', 'very good', 'Actiune, Thriller')
    a4 = Movie('4', 'Dune', 'very good', 'SF')
    a5 = Movie('5', 'Eternals', 'good', 'Actiune, SF')
    a6 = Movie('6', 'House of Gucci', 'well but not great', 'Thriller')
    a7 = Movie('7', 'Breathe', 'amazing', 'Romantic')
    a8 = Movie('8', 'Side effects', 'great', 'Drama')

    test_repo = InMemoryRepository_movie()
    test_repo.store(a1)
    test_repo.store(a2)
    test_repo.store(a3)
    test_repo.store(a4)
    test_repo.store(a5)
    test_repo.store(a6)
    test_repo.store(a7)
    test_repo.store(a8)
    return test_repo


def test_filter_by_criteria():
    test_repo = setup_test_repo()

    filter_by_actiune = lambda x: 'Actiune' in x.getGen()
    filtered_list = test_repo.get_movie_by_criteria(filter_by_actiune)
    assert (len(filtered_list) == 2)
    assert (test_repo.size() == 8)

    filter_by_title = lambda x: x.getTitlu() == 'Reminiscence'
    filtered_list = test_repo.get_movie_by_criteria(filter_by_title)
    assert (len(filtered_list) == 1)
    assert (test_repo.size() == 8)

    filter_by_description = lambda x: x.getDescriere() == 'very good'
    filtered_list = test_repo.get_movie_by_criteria(filter_by_description)
    assert (len(filtered_list) == 2)
    assert (test_repo.size() == 8)


test_filter_by_criteria()
