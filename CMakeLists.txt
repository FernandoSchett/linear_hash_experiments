cmake_minimum_required(VERSION 3.16)

project(hash_linear_experiment LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(hash_linear_experiment
    main.cpp
    src/source/ExperimentConfig.cpp
    src/source/ExperimentRunner.cpp
    src/source/CsvWriter.cpp
    src/source/RandomKeyGenerator.cpp
    libs/source/LinearHashing.cpp
    libs/source/BucketPage.cpp
    libs/source/HashStats.cpp
)

target_include_directories(hash_linear_experiment PRIVATE
    src/include
    libs/include
)

target_compile_options(hash_linear_experiment PRIVATE
    -Wall -Wextra -Wpedantic
)
