from setuptools import setup

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(
    name="discrete-event-simulation",
    version="0.1.0",
    description="Framework for making discrete event simulations",
    long_description=long_description,
    author="Alexander Grooff",
    author_email="alexandergrooff@gmail.com",
    url="https://github.com/AlexanderGrooff/discrete-event-simulation",
    packages=["simulation"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
