from setuptools import find_packages, setup

setup(
    name='comms', version='0.1.0', packages=find_packages(),
    data_files=[('share/ament_index/resource_index/packages', ['resource/comms']),
                ('share/comms', ['package.xml'])],
    install_requires=['setuptools'], tests_require=['pytest'], zip_safe=True,
    maintainer='HEAT Robotics', maintainer_email='maintainers@heatrobotics.com',
    description='Fill-in-the-blank ROS 2 tutorial', license='Apache-2.0',
    entry_points={'console_scripts': ['node = comms.node:main']},
)
