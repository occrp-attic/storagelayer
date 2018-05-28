from setuptools import setup, find_packages


setup(
    name='storagelayer',
    version='0.4.2',
    description="Content-addressable storage for aleph and memorious",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='storage files s3',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/alephdata/storagelayer',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'six',
        'cryptography',
        'boto3 >= 1.4.6',
        'normality >= 0.5.12'
    ],
    tests_require=[
        'coverage',
        'moto'
    ],
    test_suite='test',
    entry_points={
    }
)
