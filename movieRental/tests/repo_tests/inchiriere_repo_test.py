import unittest

from domain.entitati import Inchiriere
from repository.inchirieri_repo import InchirieriInMemoryRepository, InchiriereRepoFile


class TestCaseInchiriereRepoMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = InchirieriInMemoryRepository()

    def test_store(self):
        i1 = Inchiriere('1', 'Oniga Andreea', '1', 'Anne')
        i2 = Inchiriere('2', 'Oniga Maria', '1', 'Anne')
        self.repo.store(i1)
        self.assertEqual(len(self.repo.toate_inchirierile()), 1)
        self.repo.store(i2)
        self.assertEqual(len(self.repo.toate_inchirierile()), 2)

    def test_toate_inchirierile(self):
        i1 = Inchiriere('1', 'Oniga Andreea', '1', 'Anne')
        i2 = Inchiriere('2', 'Oniga Maria', '1', 'Anne')
        self.repo.store(i1)
        self.repo.store(i2)

        inchirieri = self.repo.toate_inchirierile()

        self.assertTrue(type(inchirieri) == list)
        self.assertEqual(len(inchirieri), 2)

    def test_find_client(self):
        i1 = Inchiriere('1', 'Oniga Andreea', '1', 'Anne')
        i2 = Inchiriere('2', 'Oniga Maria', '1', 'Anne')
        i3 = Inchiriere('1', 'Oniga Andreea', '3', 'King Arthur')
        self.repo.store(i1)
        self.repo.store(i2)
        self.repo.store(i3)

        self.assertIn(i1, self.repo.find_client('1'))
        self.assertIn(i3, self.repo.find_client('1'))

    def test_returnare(self):
        i1 = Inchiriere('1', 'Oniga Andreea', '1', 'Anne')
        i2 = Inchiriere('2', 'Oniga Maria', '1', 'Anne')
        i3 = Inchiriere('1', 'Oniga Andreea', '3', 'King Arthur')
        self.repo.store(i1)
        self.repo.store(i2)
        self.repo.store(i3)

        returnare = self.repo.returnare('1', '1')
        self.assertEqual(returnare, i1)
        self.assertEqual(len(self.repo.toate_inchirierile()), 2)


class TestCaseInchirieriRepoFile(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = InchiriereRepoFile('test_inchiriere_repo.txt')
        self.repo.delete_all()

    def test_store(self):
        i1 = Inchiriere('1', 'Oniga Andreea', '1', 'Anne')
        i2 = Inchiriere('2', 'Oniga Maria', '1', 'Anne')
        self.repo.store(i1)
        self.assertEqual(len(self.repo.get_all()), 1)
        self.repo.store(i2)
        self.assertEqual(len(self.repo.get_all()), 2)

    def tearDown(self) -> None:
        self.repo.delete_all()

