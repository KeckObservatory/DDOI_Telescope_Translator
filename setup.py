from setuptools import setup, find_packages

# Get some values from the setup.cfg

NAME = 'ddoi_telescope_translator'
VERSION = '0.1.1'
RELEASE = 'dev' not in VERSION
AUTHOR = "Lucas Fuhrman"
AUTHOR_EMAIL = "lfuhrman@keck.hawaii.edu"
LICENSE = "3-clause BSD"
DESCRIPTION = "The Base Telescope Translator Module"

scripts = []

# Define entry points for command-line scripts
entry_points = {
    'console_scripts': [
        "translator = ddoitranslatormodule.cli_interface:main",
    ]
    }

setup(name=NAME,
      provides=NAME,
      version=VERSION,
      license=LICENSE,
      description=DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      packages=find_packages(),
      package_dir={"": "."},
      package_data={'ddoi_telescope_translator': ['ddoi_configurations/*.ini']},
      scripts=scripts,
      entry_points=entry_points,
      install_requires=[],
      python_requires=">=3.6"
      )