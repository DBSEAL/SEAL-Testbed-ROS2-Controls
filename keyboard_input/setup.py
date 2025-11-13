from setuptools import find_packages, setup

package_name = 'keyboard_input'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Nick Dolton',
    maintainer_email='mailtheseal@gmail.com',
    description='A ROS2 package that tracks keyboard inputs and publishes them',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'keyboard_publisher = keyboard_input.controller_node:main'
        ],
    },
)
