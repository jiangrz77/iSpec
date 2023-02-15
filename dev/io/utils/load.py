import os
import numpy as np
from astropy.io import fits
from pathlib import Path

class read_from_fits():
    # Object for reading from FITS files

    source_lsit = list('lamost')
    shape_dict = {
        'lamost': {
            'flux': 0, 'inverse variance': 1, 'wavelength': 2, 'andmask':3, 'ormask': 4, 
        },
    }

    def __init__(self, pathname, source, *args, **kargs) -> None:
        self.source = source.lower()
        self.pathname = Path(pathname)
        if self.source.__contains__('lamost'):
            self._read_from_lamost()
            
    def _read_from_lamost(self):
        self.data_type = self.shape_dict['lamost']
        if os.path.exists(self.pathname):
            with fits.open(self.pathname) as hdul:
                self.header = hdul[0].header
                data = np.array(hdul[0].data)
                self.flux = data[self.data_type['flux']]
                self.wavelength = data[self.data_type['wavelength']]
                self.inv_variance = data[self.data_type['inverse variance']]
                self.error = np.divide(1, self.inv_variance, out=np.full_like(self.inv_variance,np.nan), where=self.inv_variance!=0)
        else:
            raise Exception('No such file or directory: %s'%self.pathname)
        