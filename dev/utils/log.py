# Provide Logged Class
import sys
import logging

class Logged():
    def __init__(self, **kwargs):
        self.setup_logger(**kwargs)

    def setup_logger(self, silent=None, logfile=None, level=None):
        self.logger_logfile = None
        self.logger = logging.getLogger(self.__class__.__name__)
        root_logger = logging.getLogger()
        if silent not in (None, True, False):
            level = silent
            silent = False
        if silent is None:
            if level is None:
                try:
                    silent = self.logger_silent
                except AttributeError:
                    silent = True
            else:
                silent = False
        self.logger_silent = silent
        if level is None:
            try:
                level = self.logger_level
            except AttributeError:
                level = logging.INFO
        self.logger_level = level


        if len(root_logger.handlers) == 0 and len(self.logger.handlers) == 0:
            if silent:
                self.logger_handler = logging.NullHandler()
            elif logfile is not None:
                self.logger_logfile = logfile
                self.logger_handler = logging.FileHandler(logfile, 'w')
            else:
                self.logger_handler = logging.StreamHandler(sys.stdout)
            self.logger_handler.setLevel(logging.INFO)
            self.logger_handler.setFormatter(logging.Formatter('[%(asctime)s][s%(filename)s.%(funcName)s][%(levelname)s] %(message)s'))
            self.logger.addHandler(self.logger_handler)
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(level)
            self.logger_handler = None
