from setuptools import setup, find_packages

setup(
    name="nBodyEngine",
    version="1.0.0",
    author="Federico B.",
    description="A lightweight engine to simulate the n-Body problem with Newtonian and post-Newtonian mechanics",
    long_description='A lightweight engine to simulate the n-Body problem with Newtonian and post-Newtonian mechanics. It can now simulate both in 2 dimensions and 3. All the simulations can be run from a json file to facilitate simulation data storage. For further documentation see https://github.com/Parsifal1916/nBodyEngine/',
    packages=find_packages(),
    install_requires=[
        "numpy", "matplotlib"
    ],
)
