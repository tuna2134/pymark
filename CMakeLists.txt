cmake_minimum_required(VERSION 3.5...3.26)
project(pymark)

# add cmark
add_subdirectory(extern/cmark)
link_libraries(cmark)

add_subdirectory(extern/pybind11)
pybind11_add_module(pymark src/pymark.cpp)