#!/usr/bin/env python

"""
runs tests
"""
import pytest
from pytest import approx
from datetime import datetime
import numpy as np

import matplotlib
matplotlib.use('Agg')

import visuamisr

nan = np.nan

expected = [('el', 90.0), ('site_name', 'PFISR'),
            ('altitude_uncor', -60993.6033013073),
            ('eTe', 129.63594726065702), ('edensity', 15259290309.927345),
            ('Ti', 503.6725620080873),
            ('Te', 322.82619480497675), ('evel', 18.310628762855757),
            ('az', 14.039999961853027), ('density', 50817843097.05468),
            ('site_code', 61), ('site_altitude', 213.0),
            ('latitude', 65.12711), ('vel', 8.94188664493076),
            ('edensity_uncor', 0.6091023076395629),
            ('babs', 5.3851112e-05), ('eTi', 208.8506600791112),
            ('site_latitude', 65.12992), ('kvec', 5.940312e-17),
            ('site_longitude', -147.47104), ('longitude', -147.47104),
            ('times', 1558371898.0),
            ('ave_times', 1558372049.5),
            ('range', 123165.7578125), ('beamcodes', 64016.0),
            ('density_uncor', 1287195133.8320925),
            ('altitude', 123378.75502083614)
           ]

expected_dict = {key:value for key, value in expected}

def test_readdata():
    lp = visuamisr.Analyze('tests/20190520.003_lp_5min-fitcal.h5')
    for key,item in lp.data.items():
        expected_item = expected_dict[key]
        try:
            single_item = item.flatten()[0]
            if isinstance(single_item,datetime):
                obtained_item = (item.flatten()[0]-datetime(1970,1,1)).total_seconds()
            else:
                obtained_item = item.flatten()[0]
        except:
            obtained_item = item

        if isinstance(expected_item,str):
            assert(expected_item == obtained_item)
        else:
            assert(expected_item == approx(obtained_item,nan_ok=True))

def test_rti():
    from matplotlib import pyplot

    lp = visuamisr.Analyze('tests/20190520.003_lp_5min-fitcal.h5')
    cmap = pyplot.get_cmap('viridis')
    lp.rti(['density','velocity'],bmnum=2,cmap=['jet',cmap],show=False)

def test_plot3dbeams():
    from datetime import datetime
    lp = visuamisr.Analyze('tests/20190520.003_lp_5min-fitcal.h5')
    lp.plot_beams3d('density',datetime(2019,5,20,17,20,6),sym_size=5,clim=[10,12],show=False)

def test_profileplot():
    from datetime import datetime
    lp = visuamisr.Analyze('tests/20190520.003_lp_5min-fitcal.h5')
    lp.profile_plot(['density','Te','Ti','velocity'],
                    datetime(2019,5,20,17,20,6),bmnum=3,
                    param_lim=[[10**10,10**12],[0,5000],[0,4000],
                               [-1000,1000]],use_range=True, show=False)

def test_polar_beam_plot():
    from datetime import datetime
    lp = visuamisr.Analyze('tests/20190520.003_lp_5min-fitcal.h5')
    lp.plot_polar_beam_pattern(min_elevation=10,show=False)

if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])

