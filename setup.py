from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent
with open(here / "requirements.txt") as f:
    install_requires = [r.strip() for r in f if r.strip()]

setup(
    name="etl_capstone_project",
    version="0.1.0",
    description="An ETL project for extracting, transforming, and loading data.",
    author="Theo Hutchings",
    author_email="ewright@digitalfutures.com",
    url="https://github.com/TheoHutchings908/ETL-Pipeline-Capstone",

    package_dir={"": "src"},
    packages=find_packages(where="src"),

    include_package_data=True,
    install_requires=install_requires,

    entry_points={
        "console_scripts": [
            "run-etl=scripts.run_etl:main",
            "run-tests=tests.run_tests:main",
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
