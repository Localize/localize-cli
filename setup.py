from setuptools import setup, find_packages

# read the contents of your README file
def readme():
    with open('README.rst') as f:
        return f.read()

setup(
  name="localize",
  version="1.0.7",
  author='Localize',
  author_email='support@localizejs.com',
  url='https://help.localizejs.com/docs/localize-cli',
  packages=find_packages(),
  description='Command line utiltiy for Localize.',
  long_description=readme(),
  install_requires=[
    "requests==2.21.0",
    "colorama==0.4.1",
    "pyyaml==5.3.1"
  ],
  entry_points={
    'console_scripts': [
      'localize = localize.localize:main',
    ]
  },
  license = "MIT",
  platforms = "Posix; MacOS X; Windows",
  classifiers = ["Development Status :: 5 - Production/Stable",
  	"Intended Audience :: Developers",
  	"License :: OSI Approved :: MIT License",
  	"Operating System :: OS Independent",
  	"Topic :: Internet",
  	"Programming Language :: Python :: 2.7"
  ]
)
