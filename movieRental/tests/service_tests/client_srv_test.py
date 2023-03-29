import unittest

from domain.validatori import ClientValidator
from exceptions.exceptions import ValidationException, ClientNotFoundException
from repository.client_repo import InMemoryRepository_client
from service.client_service import ClientService


class TestCaseCategoryService(unittest.TestCase):
    def setUp(self) -> None:
        repo = InMemoryRepository_client()
        validator = ClientValidator()
        self.__client_srv = ClientService(repo, validator)

    def test_add_client(self):
        added_client = self.__client_srv.add_client('1', 'Oniga Andreea', '6935620584738')
        self.assertEqual(added_client.getNume(), 'Oniga Andreea')
        self.assertEqual(len(self.__client_srv.get_all_clients()), 1)
        self.assertRaises(ValidationException, self.__client_srv.add_client, '2', 'Marginean', '')

    def test_get_all_clients(self):
        added_client = self.__client_srv.add_client('1', 'Oniga Andreea', '6935620584738')
        self.assertEqual(len(self.__client_srv.get_all_clients()), 1)

        added_client2 = self.__client_srv.add_client('2', 'Marginean Sebastian', '5011017011825')
        self.assertEqual(len(self.__client_srv.get_all_clients()), 2)

        self.assertEqual(self.__client_srv.get_all_clients()[0].getNume(), 'Oniga Andreea')
        self.assertEqual(self.__client_srv.get_all_clients()[1].getNume(), 'Marginean Sebastian')

        updated_client = self.__client_srv.update_client('1', 'Oniga Andreea', '6935620584438')
        self.assertEqual(len(self.__client_srv.get_all_clients()), 2)

        self.assertEqual(self.__client_srv.get_all_clients()[0].getCNP(), '6935620584438')

        deleted_client = self.__client_srv.delete_by_id('2')
        self.assertEqual(len(self.__client_srv.get_all_clients()), 1)

    def test_delete_category_by_id(self):
        added_client = self.__client_srv.add_client('1', 'Oniga Andreea', '6935620584738')

        added_client2 = self.__client_srv.add_client('2', 'Marginean Sebastian', '5011017011825')
        deleted_client = self.__client_srv.delete_by_id('1')
        self.assertEqual(len(self.__client_srv.get_all_clients()), 1)

        self.assertEqual(deleted_client.getNume(), 'Oniga Andreea')
        self.assertEqual(deleted_client.getCNP(), '6935620584738')

        self.assertEqual(self.__client_srv.get_all_clients()[0].getNume(), 'Marginean Sebastian')
        self.assertRaises(ClientNotFoundException, self.__client_srv.delete_by_id, 'wrongid')

    def test_update_category(self):
        added_client = self.__client_srv.add_client('1', 'Oniga Andreea', '6935620584738')
        added_client2 = self.__client_srv.add_client('2', 'Marginean Sebastian', '5011017011825')

        updated_client = self.__client_srv.update_client('1', 'Oniga Andreea', '6935620584744')
        self.assertEqual(len(self.__client_srv.get_all_clients()), 2)

        self.assertEqual(updated_client.getNume(), 'Oniga Andreea')
        self.assertEqual(updated_client.getCNP(), '6935620584744')

        modified_client_in_list = self.__client_srv.find_by_id('1')
        unchanged_category = self.__client_srv.find_by_id('2')

        self.assertEqual(updated_client, modified_client_in_list)
        self.assertEqual(unchanged_category, added_client2)

        self.assertRaises(ValidationException, self.__client_srv.update_client, 'wrongid', 'Marginean', '')

    def test_filter_by_CNP(self):

        added_client = self.__client_srv.add_client('1', 'Oniga Andreea', '6935620584738')
        added_client2 = self.__client_srv.add_client('2', 'Marginean Sebastian', '5011017011825')
        added_client3 = self.__client_srv.add_client('3', 'Solea Andra', '9235462453672')
        added_client4 = self.__client_srv.add_client('4', 'Oniga Maria', '9224536245678')

        filtered_list = self.__client_srv.filter_by_CNP('9')
        self.assertEqual(len(filtered_list), 2)
        self.assertIsInstance(filtered_list, list)

        filtered_list = self.__client_srv.filter_by_CNP('6')
        self.assertEqual(len(filtered_list), 1)
