from setuptools import setup

setup(
  name="localize",
  version="0.0.2",
  author='Localize',
  author_email='chris@localizejs.com',
  url='http://pypi.python.org/localize/localize-cli',
  download_url='https://github.com/localize/localize-cli',
  packages=['localize'],
  description='Command line utiltiy for Localize.',
  install_requires=[
    "requests==2.10.0",
    "colorama==0.3.1"
  ],
  entry_points={
    'console_scripts': [
      'localize = localize.localize:main',
    ]
  },
  license = "MIT",
  platforms = "Posix; MacOS X; Windows",
  classifiers = ["Development Status :: 4 - Beta",
  	"Intended Audience :: Developers",
  	"License :: OSI Approved :: MIT License",
  	"Operating System :: OS Independent",
  	"Topic :: Internet",
  	"Programming Language :: Python :: 2.7"
  ]
)