from distutils.core import setup

setup(name='lightcontrol',
      packages=['lightcontrol'],
      version='2.0.0',
      description='REST API for controlling Raspberry PI GPIO pins',
      author='zourtney',
      author_email='zourtney@gmail.com',
      url='https://github.com/zourtney/lightcontrol',
      install_requires: ['gpiocrust']
     )