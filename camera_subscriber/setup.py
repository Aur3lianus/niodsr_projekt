from setuptools import find_packages, setup

package_name = 'camera_subscriber'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            ['launch/launch_file.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Karol Dworczyński',
    maintainer_email='karoldworczynski03@gmail.com',
    description='Turtlebot movement controlled by ArUco marker detection',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera_node = camera_subscriber.camera_node:main',
            'robot_mover = camera_subscriber.robot_mover:main',
        ],
    },
)
