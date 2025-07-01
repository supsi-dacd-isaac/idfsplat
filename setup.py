from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="idfsplat",
    version="0.1.0",
    author="Federico Rosato",
    author_email="federico.rosato@supsi.ch",
    description="A tool to extract available EnergyPlus Exchange API data for an IDF file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supsi-dacd-isaac/idfsplat",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas",
        "openpyxl",  # for Excel output support
        # "pyenergyplus" # greyed out to prevent pip from installing it. Need to install it manually w/ EnergyPlus
    ],
    entry_points={
        "console_scripts": [
            "idfsplat=idfsplat.splat:main",
        ],
    },
    keywords="energyplus, idf, api, energy, building",
    project_urls={
        "Bug Reports": "https://github.com/supsi-dacd-isaac/idfsplat/issues",
        "Source": "https://github.com/supsi-dacd-isaac/idfsplat",
    },
) 