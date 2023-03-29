from domain.entitati import Client
from domain.validatori import ClientValidator
from repository.client_repo import InMemoryRepository_client
import random
import string


def string_generator(size, char=string.ascii_letters):
    return ''.join(random.choice(char) for x in range(size))


def nr_generator(size, char=string.digits):
    return ''.join(random.choice(char) for x in range(size))


def generate_nume():
    return string_generator(1).upper() + string_generator(random.randint(3, 7)).lower() + ' ' + \
           string_generator(1).upper() + string_generator(random.randint(3, 7)).lower()


def generate_CNP():
    return nr_generator(13)


class ClientService:
    """
    Responsabil de efectuarea operatiilor cerute de utilizator
    Coordoneaza operatiile necesare pentru a realiza actiunea declansata de utilizator

    """

    def __init__(self, repo, val):
        """
        Initializeaza service
        :param repo: obiectul de tip repo care ne ajuta sa gestionam lista de clienti
        :type repo: InMemoryRepository_client
        :param val: validator pentru verificarea clientilor
        :type val: ClientValidator
        """
        self.__repo = repo
        self.__validator = val

    def add_client(self, id, nume, CNP):
        """
        Adaugare client in lista de clienti
        :param id: id-ul clientului
        :type id: str
        :param nume: numele clintului
        :type nume: str
        :param CNP: CNP-ul clientului
        :type CNP: str
        :return: obiectul de tip Client creat
        :rtype: -;
        :raises: ValueError daca client nu este valid
        """

        a = Client(id, nume, CNP)

        self.__validator.validate(a)
        self.__repo.store(a)

        return a

    def get_all_clients(self):
        """
        Returneaza o lista cu toti clientii
        :return: lista de clienti
        :rtype: list of Client objects
        """
        return self.__repo.get_all_clients()

    def update_client(self, id, nume, CNP):
        """
        Modifica datele unui client
        :param id: id-ul cllientului de modificat
        :type id:str
        :param nume: numele nou al clientului
        :type nume: str
        :param CNP: descrierea noua a filmului
        :type CNP: str
        :return: clientul modificat
        :rtype: Client
        :raises: ValueError daca nu exista clientul cu id-ul dat
        """
        a = Client(id, nume, CNP)

        self.__validator.validate(a)
        return self.__repo.update(id, a)

    def find_by_id(self, id):
        """
        Cauta clientul cu id-ul dat
        :param id: id dat
        :type id: str
        :return: clientul cu identificatorul id/None daca nu exista clientul
        :rtype: Client
        """
        return self.__repo.find(id)

    def delete_by_id(self, id):
        """
        Sterge clientul dupa id
        :param id: id-ul dat
        :type id: str
        :return:
        :rtype:
        """
        return self.__repo.delete_by_id(id)

    def filter_by_CNP(self, cifra):
        """
        Selecteaza filmele care au genul dat
        :param cifra: cifra cu care sa inceapa CNP-ul
        :type cifra: str
        :return:
        :rtype:
        """
        clients = self.__repo.get_all_clients()
        clients_with_good_CNP = [client for client in clients if client.getCNP().startswith(cifra)]
        return clients_with_good_CNP

