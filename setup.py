from setuptools import setup, find_packages
from sptk import version

setup(
    name="sptk",
    version=version.__version__,
    description="Two panel serial port terminal",
    author="Alexey Ryabov",
    author_email="6006l1k@gmail.com",
    license="GPLv3",
    packages=find_packages(),
    install_requires=[
        "wxPython>=4.1",
        "pypubsub>=4.0",
        "pyserial>=3.5",
    ],
    data_files=[
        ("share/applications", ["data/ru.b00bl1k.sptk.desktop"]),
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["sptk = sptk.__main__"]},
)
