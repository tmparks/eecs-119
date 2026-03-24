cmake_minimum_required(VERSION 3.31) # Ubuntu 25.10 provides 3.31
project(eecs-119 LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON) # Required by clang-tidy
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
add_compile_options(
    -Wall
    -Wextra
    -Wpedantic
)

add_executable(lab01a lab01a.cpp)
add_executable(lab01b lab01b.cpp)
add_executable(lab01c lab01c.cpp)
add_executable(lab02a lab02a.cpp)
add_executable(lab02b lab02b.cpp)
add_executable(lab03a lab03a.cpp)
add_executable(lab03b lab03b.cpp)
add_executable(lab04 lab04.cpp)
add_executable(lab05 lab05.cpp)
add_executable(lab06a lab06a.cpp)
add_executable(lab06b lab06b.cpp)
add_executable(lab06c lab06c.cpp)
add_executable(lab07 lab07.cpp)
add_executable(lab08 lab08.cpp)

add_custom_target(
    check COMMAND run-clang-tidy -quiet -p ${CMAKE_CURRENT_BINARY_DIR}
)
