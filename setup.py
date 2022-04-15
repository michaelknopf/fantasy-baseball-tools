from setuptools import setup, find_packages

setup(
    name="sabr",
    packages=find_packages(where="src", exclude=["tests"]),
    package_dir={'': "src"},
    # setup_requires=["setuptools-pipfile"],
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
)
