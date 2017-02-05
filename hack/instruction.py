import logging
import re


class Instruction:

    DEST = {
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'
    }

    JUMP = {
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }

    COMP = {
        '0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'A': '110000',
        '!D': '001101',
        '!A': '110001',
        '-D': '001111',
        '-A': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D-A': '010011',
        'A-D': '000111',
        'D&A': '000000',
        'D|A': '010101',
        'M': '110000',
        '!M': '110001',
        '-M': '110011',
        'M+1': '110111',
        'M-1': '110010',
        'D+M': '000010',
        'D-M': '010011',
        'M-D': '000111',
        'D&M': '000000',
        'D|M': '010101'
    }

    def __init__(self, instruction, symboltable, logger=None):
        self.instruction = instruction
        self.symboltable = symboltable
        self.logger = logger or logging.getLogger(__name__)

    def _isAInstruction(self):
        """
        Test whether the supplied code is an A-Instruction
        :return: True if an A-Instruction, False otherwise (implies C-Instruction)
        """
        return self.instruction.startswith('@')

    def _isLabelInstruction(self):
        return self.instruction.startswith('(') and self.instruction.endswith(')')

    def _assembleA(self):
        # grab everything after the A-prefix
        v = self.instruction.lstrip('@')

        # test if the a-instruction is an address
        if v.isdigit():
            return '0' + '{0:015b}'.format(int(v))

        # get the address from the symbol table
        address = self.symboltable.set_and_get_address(v)
        return '0' + '{0:015b}'.format(int(address))

    def _assembleC(self):
        m = re.match('^(.+=)?(.+?)(;.+)?$',self.instruction)
        if not m or (not m.group(1) and not m.group(3)):
            self.logger.error('Invalid C-instruction format: {0}'.format(self.instruction))
            return None
        dest = m.group(1)
        comp = m.group(2)
        jump = m.group(3)

        # tidy up fields because I'm a lazy regex writer
        if dest:
            dest = dest.rstrip('=')
        if jump:
            jump = jump.lstrip(';')

        # build up the machine code
        code_prefix = '111'

        # determine if a = 0 or 1
        pos = comp.find('M')
        if pos >= 0:
            code_a = '1'
        else:
            code_a = '0'

        if comp and comp not in self.COMP:
            self.logger.error('Invalid comp: {0}'.format(comp))
            return None
        code_comp = self.COMP[comp]

        if dest:
            if dest not in self.DEST:
                self.logger.error('Invalid dest: {0}'.format(dest))
                return None
            code_dest = self.DEST[dest]
        else:
            code_dest = '000'

        if jump:
            if jump not in self.JUMP:
                self.logger.error('Invalid jump: {0}'.format(jump))
                return None
            code_jump = self.JUMP[jump]
        else:
            code_jump = '000'

        return code_prefix + code_a + code_comp + code_dest + code_jump

    def assemble(self):
        if self._isAInstruction():
            return self._assembleA()
        else:
            return self._assembleC()


