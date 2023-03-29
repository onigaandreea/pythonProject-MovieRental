from domain.entitati import Inchiriere, Client, Movie
from exceptions.exceptions import DuplicateIDException


class InchirieriInMemoryRepository:
    def __init__(self):
        self.__inchirieri = []

    def store(self, inchiriere):
        """
        adauga o pereche client-film in lista de inchirieri
        :param inchiriere: perechea client-film
        :return:
        """
        self.__inchirieri.append(inchiriere)

    def toate_inchirierile(self):
        """
        returneaza o lista cu toate perechile client-film
        :return:
        """
        return self.__inchirieri

    def size(self):
        """
        returneaza lungimea listei de inchirieri
        :return:
        """
        return len(self.__inchirieri)

    def update(self, inchiriere, inchiriere_noua):
        """
        actualizarea inchirierii cu inchirierea noua
        :param inchiriere: inchirierea de actualizat
        :param inchiriere_noua: inchirierea care va rezulta dupa actualizare
        :return:
        """
        inchiriere.setIdFilm(inchiriere_noua.getIdFilm())
        inchiriere.setIdClient(inchiriere_noua.getIdClient())
        inchiriere.setNumeClient(inchiriere_noua.getNumeClient())
        inchiriere.setTitlu(inchiriere_noua.getTitlu())
        return inchiriere

    def find_client(self, idclient):
        """
        Cauta inchirierile cu id clientului dat
        :param idclient: id dat
        :type idclient: str
        :return:
        :rtype:
        """
        inchirieri = []
        for inchiriere in self.__inchirieri:
            if inchiriere.getIdClient() == idclient:
                inchirieri.append(inchiriere)
        return inchirieri

    def find_movie(self, idfilm):
        """
        Cauta inchirierile cu id ul filmului dat
        :param idfilm: id dat
        :type idfilm: str
        :return:
        :rtype:
        """
        inchirieri = []
        for inchiriere in self.__inchirieri:
            if inchiriere.getIdFilm() == idfilm:
                inchirieri.append(inchiriere)
        return inchirieri

    def delete_all(self):
        """
        Sterge toate filmele din lista
        """
        self.__inchirieri.clear()

    def returnare(self, idclient, idfilm):

        for inchiriere in self.__inchirieri:
            if inchiriere.getIdClient() == idclient and inchiriere.getIdFilm() == idfilm:
                self.__inchirieri.remove(inchiriere)
                return inchiriere


class InchiriereRepoFile:
    def __init__(self, filename):
        self.__filename = filename

    def __load_from_file(self):
        """
        Incarca datele din fisier
        :return: lista cu inchirieri din fisier
        :rtype: list of Inchirieri
        """

        try:
            f = open(self.__filename, 'r')
            # f = io.open(self.__filename, mode='r', encoding='utf-8')
        except IOError:
            print('Fisiereul nu se poate deschide.')

        inchirieri = []
        lines = f.readlines()
        for line in lines:
            inchirieri_id_client, inchirieri_nume_client, inchirieri_id_film, inchirieri_titlu = \
                [token.strip() for token in line.split(';')]
            a = Inchiriere(inchirieri_id_client, inchirieri_nume_client, inchirieri_id_film, inchirieri_titlu)
            inchirieri.append(a)
        f.close()
        return inchirieri

    def __save_to_file(self, inchirieri_list):
        """
        Salveaza in fisier inchirieri date
        :param inchirieri_list: lista de inchirieri
        :type inchirieri_list: list of Inchirieri
        :return: -
        :rtype: -
        """
        with open(self.__filename, 'w') as f:
            for inchiriere in inchirieri_list:
                inchiriere_string = str(inchiriere.getIdClient()) + ';' + str(inchiriere.getNumeClient()) + ';' + str(
                    inchiriere.getIdFilm()) + ';' + str(inchiriere.getTitlu()) + '\n'
                f.write(inchiriere_string)

    def store(self, inchiriere):
        """
        Adauga o inchiriere in lista
        :param inchiriere: inchirierea de adaugat
        :type inchiriere: Inchiriere
        :return: -; lista de inchirieri se modifica prin adaugarea unei inchirieri
        :rtype: -; inchirierea este adaugat
        :raises:
        """
        all_inchirieri = self.__load_from_file()
        if inchiriere in all_inchirieri:
            raise DuplicateIDException()
        all_inchirieri.append(inchiriere)
        self.__save_to_file(all_inchirieri)

    def get_all(self):
        """
        Returneaza o lista cu toate inchirierile existente
        :rtype: list of Inchirieri
        """
        return (self.__load_from_file())

    def size(self):
        """
        Returneaza numarul de inchirieri existente
        :rtype: int
        """
        return len(self.__load_from_file())

    def delete_all(self):
        """
        Sterge toate inchirierile din lista

        """
        self.__save_to_file([])


class InchirieriRepoFileInheritance(InchirieriInMemoryRepository):
    def __init__(self, filename):
        InchirieriInMemoryRepository.__init__(self)
        self.__filename = filename
        self.__load_from_file()

    def __load_from_file(self):
        """
        Incarca datele din fisier
        :return: lista cu inchirieri din fisier
        :rtype: list of Inchirieri
        """

        try:
            f = open(self.__filename, 'r')
            # f = io.open(self.__filename, mode='r', encoding='utf-8')
        except IOError:
            print('Fisiereul nu se poate deschide.')

        lines = f.readlines()
        for line in lines:
            inchirieri_id_client, inchirieri_nume_client, inchirieri_id_film, inchirieri_titlu = \
                [token.strip() for token in line.split(';')]
            a = Inchiriere(inchirieri_id_client, inchirieri_nume_client, inchirieri_id_film, inchirieri_titlu)
            InchirieriInMemoryRepository.store(self, a)
        f.close()

    def __save_to_file(self):
        """
        Salveaza in fisier inchirierile date

        """
        inchirieri_list = InchirieriInMemoryRepository.toate_inchirierile(self)
        with open(self.__filename, 'w') as f:
            for inchiriere in inchirieri_list:
                inchiriere_string = str(inchiriere.getIdClient()) + ';' + str(inchiriere.getNumeClient()) + ';' + str(
                    inchiriere.getIdFilm()) + ';' + str(inchiriere.getTitlu()) + '\n'
                f.write(inchiriere_string)

    def store(self, inchiriere):
        """
        Adauga o inchiriere in lista
        :param inchiriere: inchirierea de adaugat
        :type inchiriere: Inchiriere
        :return: -; lista de inchirieri se modifica prin adaugarea unei inchirieri
        :rtype: -; inchirierea este adaugat
        :raises:
        """
        InchirieriInMemoryRepository.store(self, inchiriere)
        self.__save_to_file()

    def get_all(self):
        """
        Returneaza o lista cu toate inchirierile existente
        :rtype: list of Inchirieri
        """
        return InchirieriInMemoryRepository.toate_inchirierile(self)

    def size(self):
        """
        Returneaza numarul de inchirieri existente
        :rtype: int
        """
        return InchirieriInMemoryRepository.size(self)

    def delete_all(self):
        """
        Sterge toate inchirierile din lista

        """
        InchirieriInMemoryRepository.delete_all(self)
        self.__save_to_file()

