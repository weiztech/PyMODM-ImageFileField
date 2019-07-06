from setuptools import setup

setup(name='PYMODM-IMAGEFILEFIELD',
      version='1.0',
      description='ImageFileField for PyMODM module',
      url='https://github.com/weiztech/PyMODM-ImageFileField',
      author='Jensen',
      author_email='weiztech@gmail.com',
      license='MIT',
      packages=['imagefilefield'],
      install_requires=[
          'pymodm>=0.4.1',
          'opencv-python>=3.4.0.12'
      ],
      keywords='ImageFileField PyMODM-ImageFileField',
      zip_safe=False)
