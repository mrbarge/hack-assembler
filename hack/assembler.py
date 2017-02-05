from hack import symboltable, asmparser, instruction
import logging

class Assembler:

    def __init__(self, infile, outfile, logger=None):
        self.infile = infile
        self.outfile = outfile
        self.logger = logger or logging.getLogger(__name__)
        self.symboltable = symboltable.SymbolTable(logger=self.logger)
        self.parser = asmparser.AsmParser(infile, logger=self.logger)

    def _first_pass(self, code):
        """
        Parses through code to assign addresses to labels
        :param code:
        :return:
        """
        code_line = 0
        for line in code:
            t = self.parser.find_token(line)
            if t:
                self.symboltable.add_symbol_address(t,code_line)
            else:
                code_line += 1

    def _second_pass(self, code):
        """
        Transforms the supplied code listing into HACK machine code lines, returned as a ordered list of
        string-ified binary instructions.
        :param code: code to assemble
        :return: list of machine code instructions
        """
        machinecode = []
        for line in code:
            # skip labels
            if self.parser.find_token(line):
                continue
            i = instruction.Instruction(line, self.symboltable, logger=self.logger)
            c = i.assemble()
            machinecode.append(c)
        return machinecode


    def assemble(self):
        """
        Perform the machine code conversion.
        :return:
        """
        lines = self.parser.parse()
        self._first_pass(lines)
        code = self._second_pass(lines)
        with open(self.outfile, 'w') as o:
            for l in code:
                o.write(l + '\n')
        self.symboltable.print_table()

