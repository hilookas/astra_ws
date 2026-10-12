cmake_minimum_required(VERSION 3.8)
project(aharobot_sim_bringup)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch maps models rviz worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
