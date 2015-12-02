import os
from setuptools import setup


setup(
    name = "smart_house",
    version = "0.0.1",
    author = "Marian Horban",
    author_email = "horbanmarian@gmail.com",
    description = ("Makes house smarter."),
    license = "Apache",
    keywords = "smart house",
    url = "http://packages.python.org/none",
    packages=['smart_house', 'tests'],
    long_description=open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    classifiers=[
        "Development Status :: 1 - Alpha",
    ],
)
