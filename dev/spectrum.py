from pathlib import Path
import logging
from astropy.io import fits
import numpy as np
from utils.log import Logged
from utils.load import read_from_fits

# from fit import FIT

class Spectrum(Logged):
    # Object for running spectrum analysis

    def __init__(self, *args, silent=False, **kwargs) -> None:
        self.silent = silent
        self.setup_logger(silent=self.silent, **kwargs)
        self._setup(*args, **kwargs)

    # read FITS file
    def _setup(self, pathname, source, *args, **kwargs):
        pathname = Path(pathname)
        self.filename = pathname.name
        if (pathname.suffix in ['.fits', 'fit']) or (pathname.suffix=='.gz' and pathname.stem.endswith(('fit', 'fits'))):
            self.logger.info('Loading FITS file: %s'%self.filename)
            self._read_fits(pathname, source, *args, **kwargs)
            self.logger.info('Loading suceed!')
        else:
            raise Exception('Selected file "%s" is not in FITS format!' %(pathname))      
    
    def _read_fits(self, pathname, source, *args, hdr=False, **kwargs):
        tmp_fits = read_from_fits(pathname, source, *args, **kwargs)
        self.flux = tmp_fits.flux
        self.error = tmp_fits.error
        self.wavelength = tmp_fits.wavelength
        if hdr:
            self.header = tmp_fits.header

