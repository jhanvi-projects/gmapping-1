import os

from glob import glob

from setuptools import find_packages
from setuptools import setup


package_name = 'gmapping_demo'


setup(

    name=package_name,

    version='0.0.0',

    packages=find_packages(
        exclude=['test']
    ),

    data_files=[

        (
            'share/ament_index/'
            'resource_index/packages',

            [
                'resource/'
                + package_name
            ]
        ),

        (
            'share/'
            + package_name,

            [
                'package.xml'
            ]
        ),

        (

            os.path.join(
                'share',
                package_name,
                'launch'
            ),

            glob(
                'launch/*.launch.py'
            )

        ),

        (

            os.path.join(
                'share',
                package_name,
                'config'
            ),

            glob(
                'config/*.yaml'
            )

        ),

        (

            os.path.join(
                'share',
                package_name,
                'rviz'
            ),

            glob(
                'rviz/*.rviz'
            )

        ),

    ],

    install_requires=[
        'setuptools'
    ],

    zip_safe=True,

    description=
        'RPLIDAR GMapping demonstration',

    license='Apache-2.0',

    entry_points={
        'console_scripts': [],
    },
)
