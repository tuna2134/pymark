cmake_minimum_required(VERSION 3.5...3.26)
project(pymark)

add_compile_options(-O2)

# add cmark
add_subdirectory(extern/cmark)
link_libraries(cmark)

add_subdirectory(extern/pybind11)
pybind11_add_module(_pymark src/pymark.cpp)
