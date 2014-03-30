from distutils.core import setup
import webtimer
setup(name='webtimer',
    version=webtimer.__version__,
    description='Measures download times of web page resources.',
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    url='https://github.com/chrisspen/webtimer',
    license='LGPL License',
    py_modules=['webtimer'],
    scripts=['webtimer.py'],
    install_requires=['fake-useragent>=0.0.5'],
    classifiers = [
        "Programming Language :: Python",
        #"Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
    ],
    platforms=['OS Independent'],
)