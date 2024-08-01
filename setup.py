from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="repo2txt",
    version="0.0.3",
    author="Blaise",
    author_email="blaie@applio.org",
    description="A tool to clone GitHub repositories, document their directory structure, and extract file contents into a text file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "click",
        "wget"
    ],
    entry_points={
        "console_scripts": [
            "repo2txt=repo2txt.cli:cli",
        ],
    },
    url="https://github.com/blaise-tk/repo2txt",
    keywords=[
        "GitHub",
        "repository",
        "ai",
        "clone",
        "directory structure",
        "file extraction",
        "documentation",
        "CLI tool",
    ],
    classifiers=[
        "Development Status :: Release",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
    ],
)
