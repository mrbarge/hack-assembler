from hack import assembler
import argparse
import sys
import logging


def setup_logging(verbosity):
    """
    Setup logging with desired verbosity
    :param verbosity:
    :return:
    """
    logger = logging.getLogger(__name__)
    LOGFORMAT = '%(asctime)s | %(name)-12s %(levelname)-8s | %(message)s'
    formatter = logging.Formatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    logger.setLevel((logging.ERROR - (verbosity * 10)))
    return logger


def main(infile, outfile, logger=None):
    a = assembler.Assembler(infile,outfile,logger=logger)
    a.assemble()


if __name__ == "__main__":
    global logger

    parser = argparse.ArgumentParser(description='Assemble HACK machine code binary')
    parser.add_argument('-i','--in', dest='infile', help='Input file to assemble')
    parser.add_argument('-o','--out', dest='outfile', help='Output file to write')
    parser.add_argument("-v", "--verbose", action="count", dest="verbosity",
                        help="Verbose mode. Can be used multiple times to increase output. Use -vvv for debugging output.")
    args = parser.parse_args()

    # Validate args
    if args.infile is None or args.outfile is None:
        parser.print_help()
        sys.exit(1)

    # initialize logging
    verbosity = args.verbosity
    if args.verbosity is None or args.verbosity < 0:
        verbosity = 3
    logger = setup_logging(verbosity)

    main(args.infile, args.outfile, logger=logger)