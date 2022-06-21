################################################################################
# Set minimum required version of cmake, project name and compile options
################################################################################
cmake_minimum_required(VERSION 3.5)
project(turtlebot3_manipulation_gazebo)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

if(MSVC)
  add_compile_definitions(_USE_MATH_DEFINES)
endif()


################################################################################
# Find catkin packages and libraries for catkin and system dependencies
################################################################################
find_package(ament_cmake REQUIRED)
find_package(gazebo REQUIRED)
find_package(gazebo_ros_pkgs REQUIRED)

################################################################################
# Build
################################################################################
link_directories(
  ${GAZEBO_LIBRARY_DIRS}
)

include_directories(
  include
  ${GAZEBO_INCLUDE_DIRS}
)

################################################################################
# Install
################################################################################
install(TARGETS ${EXEC_NAME}
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY config launch models worlds
DESTINATION share/${PROJECT_NAME}/
)

install(DIRECTORY include/
  DESTINATION include/
)

################################################################################
# Macro for ament package
################################################################################
ament_export_include_directories(include)
ament_export_dependencies(gazebo_ros_pkgs)
ament_package()
