from setuptools import setup, find_packages
 
setup(
    name='rheclib',
    version='0.1.1',
    description='Grab bag django app',
    author='Robert Eanes',
    author_email='django@robsinbox.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)