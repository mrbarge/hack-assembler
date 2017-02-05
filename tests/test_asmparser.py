import unittest
from hack import asmparser


class TestAsmParser(unittest.TestCase):

    def test_find_token(self):
        a = asmparser.AsmParser('none')

        t = a.find_token('(test)')
        self.assertEquals(t,'test')

        t = a.find_token('test')
        self.assertIsNone(t)

        t = a.find_token(' (test)')
        self.assertIsNone(t)

        t = a.find_token('(test.two)')
        self.assertEquals(t,'test.two')

    def test_parse(self):
        a = asmparser.AsmParser('test.asm')
        l = a.parse()
        expected_list = ['@R0', 'D=M', '@R1', 'D=D-M', '@OUTPUT_FIRST', 'D;JGT', '@R1', 'D=M', '@OUTPUT_D', '0;JMP',
                         '(OUTPUT_FIRST)', '@R0', 'D=M', '(OUTPUT_D)', '@R2', 'M=D', '(INFINITE_LOOP)', '@INFINITE_LOOP', '0;JMP']
        self.assertListEqual(l,expected_list)

