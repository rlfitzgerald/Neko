import logging
import sys

class phasesymFormatter(logging.Formatter):
    #setup special formats
    FORMATS = {logging.DEBUG :"DEBUG: %(module)s: %(lineno)d: %(message)s",
               logging.WARNING : "WARNING: %(message)s",
               logging.ERROR : "ERROR: %(message)s",
               logging.INFO : "%(message)s",
               'DEFAULT' : "%(levelname)s: %(message)s"}

    #override the logging.Formatter format function so inject custom format
    #then use the underlying logging.Formatter object to print log as normal
    #using the custom format
    def format(self, record):
        self._fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        return logging.Formatter.format(self, record)
    
def setupLogger(name, outfile=None):

    #create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #create console handler and set level to info
    handler_stdout = logging.StreamHandler(sys.stdout)
    handler_stdout.setLevel(logging.INFO)

    #create formatter and set it to only print messages with no other formatting
    formatter = logging.Formatter("%(message)s")

    #add formatter to handler
    handler_stdout.setFormatter(phasesymFormatter())
    
    #add handler to logger
    logger.addHandler(handler_stdout)

    #do the same if a file is specified
    if outfile is not None:
        handler_file = logging.FileHandler(outfile, mode='w')
        handler_file.setLevel(logging.DEBUG)
        handler_file.setFormatter(formatter)
        logger.addHandler(handler_file)

    return logger
