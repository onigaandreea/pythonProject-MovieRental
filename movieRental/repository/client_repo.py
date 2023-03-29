from domain.entitati import Client
from exceptions.exceptions import ClientNotFoundException, DuplicateIDException


class InMemoryRepository_client:
    """
    Clasa creata cu responsabilitatea de a gestiona
    multimea de clienti
    """

    def __init__(self):

        self.__clients = []

    def __exists_id(self, id):
        for client in self.__clients:
            if client.getId() == id:
                return True
        return False

    def find(self, id):
        """
        Cauta clientul cu id dat
        :param id: id dat
        :type id: str
        :return: clientul cu identificator id/None daca nu exista
        :rtype: Client
        """
        for client in self.__clients:
            if client.getId() == id:
                return client
        return None

    def store(self, client):
        """
        Adauga un client in lista
        :param client: clientul de adaugat
        :type client: Client
        :return: -; lista de filme se modifica prin adaugarea filmului
        :rtype:
        :raises:
        """
        if client.getId() in map(lambda x: x.getId(), self.__clients):
            raise DuplicateIDException
        self.__clients.append(client)

    def get_all_clients(self):
        """
        Returneaza o lista cu toti clientii
        :rtype: list of Client objects
        """
        return self.__clients

    def size(self):
        """
        Returneaza numarul de clienti din lista
        :rtype: int
        """
        return len(self.__clients)

    def delete_by_id(self, id):
        """
        Sterge clientul cu id-ul dat din lista de clienti
        :param id: id-ul dat
        :type id: str
        :return: obiectul client sters
        :rtype: Client
        :raises: ValueError daca nu exista clientul cu id dat
        """
        if not self.__exists_id(id):
            raise ClientNotFoundException

        client = self.find(id)
        self.__clients.remove(client)
        return client

    def update(self, id, new_client):
        """
        Modifica datele clientului cu identificator id
        :param id: id-ul dat
        :type id: str
        :param new_client: clientul cu noile date
        :type new_client: Client
        :return: clientul modificat
        :rtype: Client
        """
        client = self.find(id)
        if client is None:
            raise ValueError('Nu exista client cu acest id.')
        client.setNume(new_client.getNume())
        client.setCNP(new_client.getCNP())
        return client

    def delete_all(self):
        """
        Sterge toti clientii din lista
        """
        self.__clients.clear()

    def get_clients_by_criteria(self, filter_function):
        """
        Selecteaza elementele din lista care indeplinesc un criteriu
        :param filter_function: functia dupa care se filtreaza
        :type filter_function: function
        :return: lista de clienti care indeplinesc criteriul
        :rtype: list of Clients
        """
        return [client for client in self.__clients if filter_function(client)]


class ClientRepoFile:
    def __init__(self, filename):
        self.__filename = filename

    def __load_from_file(self):
        """
        Incarca datele din fisier
        :return: lista cu clienti din fisier
        :rtype: list of Client
        """

        try:
            f = open(self.__filename, 'r')
            # f = io.open(self.__filename, mode='r', encoding='utf-8')
        except IOError:
            print('Fisiereul nu se poate deschide.')

        clients = []
        lines = f.readlines()
        for line in lines:
            client_id, client_name, client_CNP = [token.strip() for token in line.split(';')]
            a = Client(client_id, client_name, client_CNP)
            clients.append(a)
        f.close()
        return clients

    def __save_to_file(self, clients_list):
        """
        Salveaza in fisier clientii dati
        :param clients_list: lista de clienti
        :type clients_list: list of Clients
        :return: -
        :rtype: -
        """
        with open(self.__filename, 'w') as f:
            for client in clients_list:
                client_string = str(client.getId()) + ';' + str(client.getNume()) + ';' + str(
                    client.getCNP()) + '\n'
                f.write(client_string)

    def store(self, client):
        """
        Adauga client in lista
        :param client: clientul de adaugat
        :type client: Client
        :return: -; lista de clieti se modifica prin adaugarea clientului
        :rtype: -; clientul este adaugat
        :raises:ValueError daca exista deja un client cu id-ul dat
        """
        all_clients = self.__load_from_file()
        if client in all_clients:
            raise DuplicateIDException()
        all_clients.append(client)
        self.__save_to_file(all_clients)

    def __find_index(self, clients, id):
        """
        Gaseste pozitia in lista a unui client
        :param clients: lista de clienti
        :type clients: list of Clients
        :param id: id-ul dat
        :type id: str
        :return: pozitia clientului cu id in clients
        :rtype: int, >0, <size(), -1 daca clientul cu id dat nu exista
               """
        index = -1
        for i in range(len(clients)):
            if clients[i].getId() == id:
                index = i
        return index

    def update(self, id, new_client):
        """
        Actualizeaza datele unui client
        :param id: id-ul clientului care se modifica
        :type id: id-ul dat
        :param new_client: noul client
        :type new_client: Client
        :return: clientul modificat
        :rtype: Client
        """
        all_clients = self.__load_from_file()
        index = self.__find_index(all_clients, id)
        if index == -1:
            raise ClientNotFoundException()
        all_clients[index] = new_client
        self.__save_to_file(all_clients)
        return new_client

    def delete(self, id):
        """
        Sterge clientul cu id-ul dat din lista de clienti
        :param id: id-ul dat
        :type id: str
        :return: obiectul client sters
        :rtype: Client
        :raises:
        """
        all_clients = self.__load_from_file()
        index = self.__find_index(all_clients, id)
        if index == -1:
            raise ClientNotFoundException
        deleted_client = all_clients.pop(index)
        self.__save_to_file(all_clients)
        return deleted_client

    def find(self, id):
        """
        Cauta clientul cu id dat
        :param id: id dat
        :type id: str
        :return: clientul cu identificator id, None daca nu exista
        :rtype: Client
        """
        all_clients = self.__load_from_file()
        for client in all_clients:
            if client.getId() == id:
                return client
        return None

    def get_all(self):
        """
        Returneaza o lista cu toti clientii existenti
        :rtype: list of Clients
        """
        return (self.__load_from_file())

    def size(self):
        """
        Returneaza numarul de clienti existenti
        :rtype: int
        """
        return len(self.__load_from_file())

    def delete_all(self):
        """
        Sterge toti clientii din lista

        """
        self.__save_to_file([])


class ClientRepoFileInheritance(InMemoryRepository_client):
    def __init__(self, filename):
        InMemoryRepository_client.__init__(self)
        self.__filename = filename
        self.__load_from_file()

    def __load_from_file(self):
        """
        Incarca datele din fisier
        :return: lista cu clienti din fisier
        :rtype: list of Client
        """

        try:
            f = open(self.__filename, 'r')
            # f = io.open(self.__filename, mode='r', encoding='utf-8')
        except IOError:
            print('Fisiereul nu se poate deschide.')

        lines = f.readlines()
        for line in lines:
            client_id, client_name, client_CNP = [token.strip() for token in line.split(';')]
            a = Client(client_id, client_name, client_CNP)
            InMemoryRepository_client.store(self, a)
        f.close()

    def __save_to_file(self):
        """
        Salveaza in fisier clientii dati

        """
        clients_list = InMemoryRepository_client.get_all_clients(self)
        with open(self.__filename, 'w') as f:
            for client in clients_list:
                client_string = str(client.getId()) + ';' + str(client.getNume()) + ';' + str(
                    client.getCNP()) + '\n'
                f.write(client_string)

    def store(self, client):
        """
        Adauga client in lista
        :param client: clientul de adaugat
        :type client: Client
        :return: -; lista de clieti se modifica prin adaugarea clientului
        :rtype: -; clientul este adaugat
        :raises:ValueError daca exista deja un client cu id-ul dat
        """
        InMemoryRepository_client.store(self, client)
        self.__save_to_file()

    def update(self, id, new_client):
        """
        Actualizeaza datele unui client
        :param id: id-ul clientului care se modifica
        :type id: id-ul dat
        :param new_client: noul client
        :type new_client: Client
        :return: clientul modificat
        :rtype: Client
        """
        InMemoryRepository_client.update(self, id, new_client)
        self.__save_to_file()
        return new_client

    def delete(self, id):
        """
        Sterge clientul cu id-ul dat din lista de clienti
        :param id: id-ul dat
        :type id: str
        :return: obiectul client sters
        :rtype: Client
        :raises:
        """
        deleted_client = InMemoryRepository_client.delete_by_id(self, id)
        self.__save_to_file()
        return deleted_client

    def find(self, id):
        """
        Cauta clientul cu id dat
        :param id: id dat
        :type id: str
        :return: clientul cu identificator id, None daca nu exista
        :rtype: Client
        """
        return InMemoryRepository_client.find(self, id)

    def get_all(self):
        """
        Returneaza o lista cu toti clientii existenti
        :rtype: list of Clients
        """
        return InMemoryRepository_client.get_all_clients(self)

    def size(self):
        """
        Returneaza numarul de clienti existenti
        :rtype: int
        """
        return InMemoryRepository_client.size(self)

    def delete_all(self):
        """
        Sterge toti cllientii din lista

        """
        InMemoryRepository_client.delete_all(self)
        self.__save_to_file()
