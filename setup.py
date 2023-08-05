from setuptools import setup, find_packages

setup(
    name="nBodyEngine",
    version="1.0.0",
    author="Federico B.",
    description="A lightweight engine to simulate the n-Body problem with Newtonian and post-Newtonian mechanics",
    packages=find_packages(),
    install_requires=[
        "numpy", "matplotlib"
    ],
)
