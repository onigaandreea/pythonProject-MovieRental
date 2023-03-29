import unittest

from domain.entitati import Client
from exceptions.exceptions import ClientNotFoundException, DuplicateIDException
from repository.client_repo import InMemoryRepository_client, ClientRepoFileInheritance


class TestCaseClientRepoMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = InMemoryRepository_client()

    def test_store(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.assertEqual(self.repo.size(), 1)
        self.repo.store(b)
        self.assertEqual(self.repo.size(), 2)
        self.assertEqual(self.repo.find(a.getId()), a)

        c = Client('1', 'Solea Andra', '9235462453672')
        self.assertRaises(DuplicateIDException, self.repo.store, c)

    def test_get_all(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.assertIsInstance(self.repo.get_all_clients(), list)
        self.assertEqual(len(self.repo.get_all_clients()), 1)

        self.repo.store(b)
        assert (len(self.repo.get_all_clients()) == 2)
        self.assertEqual(self.repo.get_all_clients()[0], a)
        self.assertEqual(self.repo.get_all_clients()[1], b)

        self.repo.delete_by_id('2')
        self.assertEqual(len(self.repo.get_all_clients()), 1)

    def test_get_size(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.assertEqual(self.repo.size(), 1)

        self.repo.store(b)
        self.assertEqual(self.repo.size(), 2)

        self.repo.delete_by_id('1')
        self.assertEqual(self.repo.size(), 1)

        c = Client('2', 'Rafael Nadal', '2034576856748')
        self.repo.update('2', c)
        self.assertEqual(self.repo.size(), 1)

    def test_delete_all(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.repo.store(b)
        self.assertEqual(self.repo.size(), 2)
        self.repo.delete_all()
        self.assertEqual(self.repo.size(), 0)

    def test_delete(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.repo.store(b)

        deleted_client = self.repo.delete_by_id('1')
        self.assertEqual(self.repo.size(), 1)
        self.assertEqual(deleted_client.getId(), '1')
        self.assertEqual(deleted_client.getNume(), 'Oniga Andreea')
        self.assertEqual(deleted_client.getCNP(), '9206473849647')

    def test_update(self):
        self.repo = InMemoryRepository_client()
        a = Client('1', 'Oniga Andreea', '9206473849647')
        self.repo.store(a)

        b = Client('1', 'Marginean Sebastian', '5011017011825')
        updated_client = self.repo.update('1', b)
        self.assertEqual(updated_client.getNume(), 'Marginean Sebastian')

    def test_filter_by_criteria(self):
        self.repo = InMemoryRepository_client()
        a1 = Client('1', 'Oniga Andreea', '9206473849647')
        a2 = Client('2', 'Marginean Sebastian', '5011017011825')
        a3 = Client('3', 'Solea Andra', '9235462453672')
        a4 = Client('4', 'Oniga Maria', '9224536245678')
        a5 = Client('5', 'Aloman Dumitru', '9354245682935')
        a6 = Client('6', 'Avram Daniel', '9134253679866')
        a7 = Client('7', 'Oltean Adina', '2341567234789')
        a8 = Client('8', 'Cristea Adrian', '2451367778923')
        self.repo.store(a1)
        self.repo.store(a2)
        self.repo.store(a3)
        self.repo.store(a4)
        self.repo.store(a5)
        self.repo.store(a6)
        self.repo.store(a7)
        self.repo.store(a8)

        filter_by_name = lambda x: 'Oniga' in x.getNume()
        filtered_list = self.repo.get_clients_by_criteria(filter_by_name)
        self.assertEqual(len(filtered_list), 2)
        self.assertEqual(len(self.repo.get_all_clients()), 8)

        filter_by_CNP = lambda x: x.getCNP().startswith('9')
        filtered_list = self.repo.get_clients_by_criteria(filter_by_CNP)
        assert (len(filtered_list) == 5)
        assert (self.repo.size() == 8)


class TestCaseClientRepoFile(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = ClientRepoFileInheritance('test_client_repo.txt')
        self.repo.delete_all()

    def test_store_athlete(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.assertEqual(self.repo.size(), 1)
        self.repo.store(b)
        self.assertEqual(self.repo.size(), 2)
        self.assertEqual(self.repo.find(a.getId()), a)

        c = Client('1', 'Cristina Neagu', '2034152435624')
        self.assertRaises(DuplicateIDException, self.repo.store, c)

    def test_get_all(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.assertIsInstance(self.repo.get_all(), list)
        self.assertEqual(len(self.repo.get_all()), 1)

        self.repo.store(b)
        assert (len(self.repo.get_all()) == 2)
        self.assertEqual(self.repo.get_all()[0], a)
        self.assertEqual(self.repo.get_all()[1], b)

        self.repo.delete('2')
        self.assertEqual(len(self.repo.get_all()), 1)

    def test_get_size(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.assertEqual(self.repo.size(), 1)

        self.repo.store(b)
        self.assertEqual(self.repo.size(), 2)

        self.repo.delete('1')
        self.assertEqual(self.repo.size(), 1)

        c = Client('2', 'Rafael Nadal', '2534645738456')
        self.repo.update('2', c)
        self.assertEqual(self.repo.size(), 1)

    def test_delete_all(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.repo.store(b)
        self.assertEqual(self.repo.size(), 2)
        self.repo.delete_all()
        self.assertEqual(self.repo.size(), 0)

    def test_delete(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.repo.store(a)
        self.repo.store(b)

        deleted_client = self.repo.delete('1')
        self.assertEqual(self.repo.size(), 1)
        self.assertEqual(deleted_client.getId(), '1')
        self.assertEqual(deleted_client.getNume(), 'Oniga Andreea')
        self.assertEqual(deleted_client.getCNP(), '9206473849647')
        self.assertRaises(ClientNotFoundException, self.repo.delete, 'Clientul nu a fost gasit.')

    def test_update(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        self.repo.store(a)

        b = Client('1', 'Marginean Sebastian', '5011017011825')
        updated_client = self.repo.update('1', b)
        self.assertEqual(updated_client.getNume(), 'Marginean Sebastian')

    def tearDown(self) -> None:
        self.repo.delete_all()
