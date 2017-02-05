import logging
import re


class AsmParser:

    def __init__(self, infile, logger=None):
        self._infile = infile
        self.logger = logger or logging.getLogger(__name__)

    def parse(self):
        lines = []
        with open(self._infile,'r') as s:
            for line in s:
                # strip all whitespace
                line = "".join(line.split())

                # ignore empty lines and comments
                pos = line.find('//')
                if pos >= 0:
                    line = line[0:pos]

                # if we're left with a line that's not empty, add it
                if line:
                    lines.append(line)

        return lines

    def find_token(self, line):
        p = re.compile('^\((.+)\)$')
        m = p.match(line)
        if m:
            return m.group(1)
        else:
            return None