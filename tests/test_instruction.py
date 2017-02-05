import unittest
from hack import instruction, symboltable


class TestInstruction(unittest.TestCase):

    def test_isAInstruction(self):
        s = symboltable.SymbolTable()
        i = instruction.Instruction('@1234',s)
        self.assertTrue(i._isAInstruction())

        i = instruction.Instruction('1234',s)
        self.assertFalse(i._isAInstruction())

        i = instruction.Instruction('1@234',s)
        self.assertFalse(i._isAInstruction())

    def test_assembleA(self):
        s = symboltable.SymbolTable()

        # test that an address is returned properly
        i = instruction.Instruction('@12',s)
        a = i.assemble()
        self.assertEqual(a,'0000000000001100')

        # test that all symboltable entries have their correct address returned
        for symbol in s.symbols:
            i = instruction.Instruction('@{0}'.format(symbol), s)
            expected_address = '{0:015b}'.format(s.get_address(symbol))
            expected_code = '0' + expected_address
            a = i.assemble()
            self.assertEqual(a,expected_code)

        # test that an as-yet-declared address gets the next available address in the table
        next_address = '{0:015b}'.format(s.next_address)
        expected_code = '0' + next_address
        i = instruction.Instruction('@doesntexist', s)
        a = i.assemble()
        self.assertEqual(a,expected_code)

    def test_assembleC(self):
        s = symboltable.SymbolTable()

        # test that an address is returned properly
        i = instruction.Instruction('M=1',s)
        a = i.assemble()
        self.assertEqual(a,'1110111111001000')

        i = instruction.Instruction('M=0',s)
        a = i.assemble()
        self.assertEqual(a,'1110101010001000')

        i = instruction.Instruction('D=M',s)
        a = i.assemble()
        self.assertEqual(a,'1111110000010000')

        i = instruction.Instruction('D=D-A',s)
        a = i.assemble()
        self.assertEqual(a,'1110010011010000')

        i = instruction.Instruction('D;JGT',s)
        a = i.assemble()
        self.assertEqual(a,'1110001100000001')

        i = instruction.Instruction('M=D+M',s)
        a = i.assemble()
        self.assertEqual(a,'1111000010001000')

        i = instruction.Instruction('M=M+1',s)
        a = i.assemble()
        self.assertEqual(a,'1111110111001000')

        i = instruction.Instruction('0;JMP',s)
        a = i.assemble()
        self.assertEqual(a,'1110101010000111')


