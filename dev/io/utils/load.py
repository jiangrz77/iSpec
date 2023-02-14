import os
import numpy as np
from astropy.io import fits
from pathlib import Path

class read_from_fits():
    # Object for reading from FITS files

    source_lsit = list('lamost')
    dtype_dict = {
          'lamost': np.dtype([('flux', 'f'), ('inverse variance', 'f'), ('wavelength', 'f'), ('andmask', 'f'), ('ormask', 'f')])
    }

    def __init__(self, pathname, source, *args, **kargs) -> None:
        self.source = source.lower()
        self.pathname = Path(pathname)
        if self.source.__contains__('lamost'):
            self._read_from_lamost()
            
    def _read_from_lamost(self):
        self.data_type = self.dtype_dict['lamost']
        if os.path.exists(self.pathname):
            with fits.open(self.pathname) as hdul:
                self.header = hdul[0].header
                self.data = np.array(hdul[0].data, dtype=self.data_type)
                self.flux = self.data['flux']
                self.wavelength = self.data['wavelength']
        else:
            raise Exception('No such file or directory: %s'%self.pathname)
        