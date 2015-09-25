import modulefinder
from glob import glob
from setuptools import setup, find_packages
import py2exe
# import innosetup
from amonagent import __version__

setup(
	name='amonagent',
	version=__version__,
	description='Windows system and process information collector',
	author='Martin Rusev',
	author_email='martin@amon.cx',
	packages=find_packages(),
	service=['amonagent.service'], # Your service.py, without the .py!!!
	windows = [{'script': 'amonagent/collector.py'}],
	options={ # This is the list of options each module has, for example py2exe, but for example, PyQt or django could also contain specific options
        'py2exe': {
        'bundle_files': 1,
            'dist_dir': 'compilation', # The output folder
            'compressed': True, 
            'dll_excludes': ['MSVCP90.dll'],
            'packages':['amonagent'],
            'includes':['sys', 'glob', 'os', 'platform', 'datetime',
               'unidecode', 'psutil','amonagent', 'requests'], # All the modules you need to be included, I added packages such as PySide and psutil but also custom ones like modules and utils inside it because py2exe guesses which modules are being used by the file we want to compile, but not the imports, so if you import something inside main.py which also imports something, it might break.
        }
    }

	)
