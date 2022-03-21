from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Advanced Password Generator'
LONG_DESCRIPTION = 'Python package that generates passwords based on a requirements JSON input'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="password_gen", 
        version=VERSION,
        author="Max Perkhounkov",
        author_email="<mperkhounkov1@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)