#!/usr/bin/env python3
#
# Copyright 2022 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Darby Lim

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

import xacro


TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')

    world_file_name = 'empty_worlds/' + TURTLEBOT3_MODEL + '.model'
    world = os.path.join(get_package_share_directory('turtlebot3_manipulation_gazebo'),
                         'worlds', world_file_name)
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_manipulation_gazebo'), 'launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    urdf_file_name = 'turtlebot3_manipulation.urdf.xacro'
    print('urdf_file_name : {}'.format(urdf_file_name))
    urdf = os.path.join(
        get_package_share_directory('turtlebot3_manipulation_description'),
        'urdf',
        urdf_file_name)

    doc = xacro.parse(open(urdf))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml()}

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
            )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'turtlebot3_manipulation'],
                    output='screen')

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    
    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'start',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'start',
             'joint_trajectory_controller'],
        output='screen'
    )

    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_state_controller],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_joint_trajectory_controller],
            )
        ),
        gazebo,
        node_robot_state_publisher,
        spawn_entity,

        # DeclareLaunchArgument(
        #     'use_sim_time',
        #     default_value='false',
        #     description='Use simulation (Gazebo) clock if true'),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        #     ),
        #     launch_arguments={'world': world}.items(),
        # ),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        #     ),
        # ),

        # ExecuteProcess(
        #     cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
        #     output='screen'),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([launch_file_dir, '/robot_state_publisher.launch.py']),
        #     launch_arguments={'use_sim_time': use_sim_time}.items(),
        # ),

        # Node(
        #     package='robot_state_publisher',
        #     executable='robot_state_publisher',
        #     name='robot_state_publisher',
        #     output='screen',
        #     parameters=[{'use_sim_time': use_sim_time}],
        #     arguments=[urdf]),

        # Node(
        #     package='controller_manager',
        #     executable='controller_manager',
        #     name='joint_state_controller_spawner',
        #     output='screen',
        #     arguments=[{'respawn': 'false'}]),
    ])
