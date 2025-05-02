from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="etl_capstone_project",
    version="0.1.0",
    description=("An ETL project for extracting, transforming, and loading data."),
    author="Theo Hutchings",
    author_email="ewright@digitalfutures.com",
    url="https://github.com/TheoHutchings908/ETL-Pipeline-Capstone",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "run_etl=scripts.run_etl:main",
            "run_tests=tests.run_tests:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)