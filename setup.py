from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'antropi_turtlebot3_assignment'


def get_data_files():
    data_files = [
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
    ]
    for (dirpath, _, filenames) in os.walk('models'):
        if filenames:
            dest = os.path.join('share', package_name, dirpath)
            src = [os.path.join(dirpath, f) for f in filenames]
            data_files.append((dest, src))
    return data_files


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=get_data_files(),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Madeshwar Raja',
    maintainer_email='madeshrajas005@gmail.com',
    description='TurtleBot3 autonomous navigation simulation using Nav2 in Gazebo',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'navigate_to_goal = antropi_turtlebot3_assignment.navigate_to_goal:main',
        ],
    },
)
