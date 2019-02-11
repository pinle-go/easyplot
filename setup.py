from distutils.core import setup
import codecs
import os
import glob

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

with codecs.open(os.path.join(here, 'CHANGELOG.txt'), encoding='utf-8') as f:
    changelog = f.read()
    version = changelog.split('\n')[0].strip()

setup(name='EasyPlot',
      version='1.0.1',
      description='A matplotlib wrapper for fast and easy generation of reusable plots',
      author='Sudeep Mandal',
      author_email='sudeepmandal@gmail.com',
      url='https://github.com/HamsterHuey/easyplot',
      packages=['easyplot'],
      data_files = [('', ['LICENSE.txt']),
                    ('', ['DESCRIPTION.rst']),
                    ('', ['README.md']),
                    ('', ['README.html']),
                    ('', ['CHANGELOG.txt']),
                    ('images', glob.glob('images/*.png')),
                    ('docs', glob.glob('docs/*.ipynb')),
                   ],
      install_requires = ['matplotlib'],
      license='MIT',
      platforms='any',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Other Audience',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
      ],
      long_description = long_description,
      keywords='matplotlib wrapper plot easyplot',
    )
