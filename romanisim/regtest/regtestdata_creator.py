"""Create data for all of the tests."""

import os
import asdf
import inspect
import importlib
import pkgutil
from romanisim import regtest


def make_data_files(outdir):
    # get modules
    modules = [x.name for x in pkgutil.iter_modules(regtest.__path__)
               if x.name.startswith('test_')]
    test_functions = dict()
    for modulename in modules:
        module = importlib.import_module(modulename,
                                         package='romanisim.regtest')
        fun0 = [x for x in inspect.getmembers(module, inspect.isfunction)
                if x[0].startswith('test_')]
        test_functions[modulename] = fun0
    out = dict()
    for modulename in test_functions:
        for funname, fun in test_functions[modulename]:
            data = fun(None, return_data=True)
            out['.'.join([modulename, funname])] = data
    for fname, data in out.items():
        af = asdf.AsdfFile()
        af.tree = dict(data=data, test=fname)
        filepath = os.path.join(outdir, fname + '.asdf')
        af.write_to(filepath)
