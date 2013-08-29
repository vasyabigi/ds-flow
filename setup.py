from setuptools import setup

setup(
    name='dsflow',
    version='0.1',
    author='Vasyl Stanislavchuk',
    author_email='vasyl.stanislavchuk@djangostars.com',
    entry_points={
        'console_scripts':
            ['flow = dsflow.flow:main', ]
    },
    packages=['dsflow'],
    url='https://github.com/vasyabigi/ds-flow',
    license='BSD',
    description='Add easy workflow for git/github branching system',
    long_description=open('README.md').read(),
    install_requires=[
        'fabric',
        'docopt',
        'requests'
    ],
    classifiers=[
        'Development Status :: Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: BSD',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python'
    ]
)
