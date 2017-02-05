import logging


class SymbolTable:

    def __init__(self, logger=None):
        self.next_address = 16
        self.symbols = {}

        # Add pre-defined symbols
        for i in range(0,16):
            self.symbols["R" + str(i)] = i
        self.symbols["SP"] = 0
        self.symbols["LCL"] = 1
        self.symbols["ARG"] = 2
        self.symbols["THIS"] = 3
        self.symbols["THAT"] = 4
        self.symbols["SCREEN"] = 16384
        self.symbols["KBD"] = 24576

        self.logger = logger or logging.getLogger(__name__)


    def get_address(self, symbol):
        """
        Returns the address associated with the symbol. If the symbol does not already exist,
        None is returned.
        :param symbol:
        :return:
        """
        if symbol not in self.symbols:
            return None
        else:
            return self.symbols[symbol]

    def add_symbol_address(self, symbol, address):
        self.symbols[symbol] = address

    def set_and_get_address(self, symbol):
        """
        Returns the address associated with the symbol. If the symbol does not already exist,
        an entry in the symbol table is allocated for it and returned
        :param symbol: symbol to look up
        :return:
        """
        if symbol not in self.symbols:
            self.symbols[symbol] = self.next_address
            self.next_address += 1

        return self.symbols[symbol]


    def print_table(self):
        """
        Print the table to the SymbolTable's logger
        :return:
        """
        for symbol in self.symbols:
            self.logger.info("{0:<7}: {1}".format(symbol,self.symbols[symbol]))


