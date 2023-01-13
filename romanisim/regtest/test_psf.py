"""Regression tests for PSF module."""

import numpy as np
import galsim
from romanisim import psf, image, catalog


# presently assumes that it gets passed the data array...
def test_psf(rtdata, return_data=False):
    scale = 0.11  # arcsec / pixel
    filter_name = 'F158'
    pix = [50, 50]
    counts = 10000
    fluxdict = {filter_name: counts}
    im = galsim.Image(101, 101, scale=scale, xmin=0, ymin=0)
    profile = psf.make_psf(1, filter_name, webbpsf=True, chromatic=False,
                           pix=pix)
    cat = [catalog.CatalogObject(None, galsim.DeltaFunction(), fluxdict)]
    image.add_objects_to_image(im, cat, [pix[0]], [pix[1]], profile, 1,
                               filter_name=filter_name, seed=0)
    if return_data:
        return im.array

    imunc = np.sqrt(im.array)
    assert np.all(np.abs(rtdata - im.array) <= 5*imunc + 0.1)
    # PSF has not changed within 5 sigma Poisson counts + 0.1 counts
    # (don't want to trigger on PSF outskirts where the size of the PSF stamp
    # is important)
