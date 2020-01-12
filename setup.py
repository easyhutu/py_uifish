from setuptools import setup, find_packages

# setup(name='uifish',
#       packages=find_packages(),
#       python_requires='>=3.6',
#       entry_points={
#           'console_scripts': [
#               'uifish = uifish.__main__:main'
#           ]
#       }
#       )
setup(setup_requires=['pbr'], python_requires='>=3.6', pbr=True)