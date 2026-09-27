from setuptools import find_packages, setup

package_name = 'simple_mover'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Farid Surya Wardana',
    maintainer_email='user@todo.todo',
    description='ROS 2 robot movement and rectangular path controller',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mover_node = simple_mover.mover_node:main',
            'rectangle_mover = simple_mover.rectangle_mover:main',
        ],
    },
)
