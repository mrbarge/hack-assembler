import unittest
from hack import symboltable


class TestSymbolTable(unittest.TestCase):

    def test_get_address(self):
        s = symboltable.SymbolTable()

        a = s.get_address('SCREEN')
        self.assertEqual(a,16384)

        a = s.get_address('doesntexist')
        self.assertIsNone(a)

    def test_set_and_get_address(self):
        s = symboltable.SymbolTable()

        # verify adding new symbols works and increments the memory address
        a = s.set_and_get_address('first')
        self.assertEqual(a,16)

        a = s.set_and_get_address('second')
        self.assertEqual(a, 17)

        # now verify that they already exist in the table and return the same address
        a = s.set_and_get_address('first')
        self.assertEqual(a,16)

        a = s.set_and_get_address('second')
        self.assertEqual(a, 17)