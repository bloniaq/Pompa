import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="[pompa-pkg-bloniaq]",
    version="2.0.1",
    author="Jakub Blonski",
    author_email="j.a.blonski@outlook.com",
    description="Sewage Pumping Station model",
    url="https://github.com/bloniaq/Pompa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    python_requires='>=3.6',
)