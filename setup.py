from setuptools import setup
from multicolor_captcha_generator.constants import VERSION
from os import path

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='multicolor_captcha_generator',
      version=VERSION,
      description='multicolor captcha generator',
      long_description=readme(),
      url='https://github.com/crossnox/multicolor_captcha_generator',
      author='CrossNox',
      package_data={
        'multicolor_captcha_generator': [path.join('fonts', 'freefont-20120503', '*.ttf')],
      },
      #include_package_data=True,
      packages=['multicolor_captcha_generator'],
      scripts=[path.join('script', 'multicolor_captcha')],
      install_requires=['Pillow'],
      classifiers=[
          'Programming Language :: Python :: 3'
      ]
      )
