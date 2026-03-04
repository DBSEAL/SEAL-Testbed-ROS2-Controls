from setuptools import find_packages, setup

import os
from glob import glob

package_name = 'lattepanda_telemetry'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    zip_safe=True,
    maintainer='seal',
    maintainer_email='seal@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
		'lattepanda_metrics_sub = lattepanda_telemetry.lattepanda_metrics_sub:main'
        ],
    },
)
