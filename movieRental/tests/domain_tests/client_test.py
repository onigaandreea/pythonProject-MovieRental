import unittest

from domain.entitati import Client
from domain.validatori import ClientValidator


class TestCaseClientDomain(unittest.TestCase):

    def setUp(self) -> None:
        self.__validator = ClientValidator()

    def test_create_client(self):
        c = Client('1', 'Oniga Andreea', '9206473849647')

        self.assertTrue(c.getId(), '1')
        self.assertTrue(c.getNume(), 'Oniga Andreea')
        self.assertTrue(c.getCNP(), '9206473849647')

        c.setId('1')
        c.setNume('Oniga Simona')
        c.setCNP('9206473848847')

        self.assertTrue(c.getId(), '1')
        self.assertTrue(c.getNume(), 'Oniga Simona')
        self.assertTrue(c.getCNP(), '9206473848847')

    def test_equal_client(self):
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('1', 'Marginean Sebastian', '5011017011825')

        self.assertEqual(a, b)

        c = Client('2', 'Marginean Sebastian', '5011017011825')

        self.assertNotEqual(a, c)

    def test_validate_client(self):
        validator = ClientValidator()
        a = Client('1', 'Oniga Andreea', '9206473849647')
        b = Client('2', 'Marginean Sebastian', '5011017011825')
        self.__validator.validate(a)
        self.__validator.validate(b)

        c = Client('0', 'Marginean', '50110170118')
        self.assertRaises(ValueError, self.__validator.validate, c)

        b1 = Client('-16', '', '')
        self.assertRaises(ValueError, self.__validator.validate, b1)

