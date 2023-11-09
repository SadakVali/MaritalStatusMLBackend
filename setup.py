# imports from the packages
from typing import List
from setuptools import find_packages, setup 

# initialization of constants
HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str)->List[str]:
    """
    this funtions will return the list of required libraries
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
    requirements = [req.replace("\n", "") for req in requirements]
    if HYPHEN_E_DOT in requirements: requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name = "MaritalStatusMLBackend", 
    version = "0.0.1",
    author = "Sadiq Vali", 
    author_email = "rebirth4vali@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt"),
)
