cmake_minimum_required(VERSION 3.5...3.26)
project(pymark)

add_compile_options(-O2)

# add cmark
add_subdirectory(extern/cmark)
set_target_properties(cmark PROPERTIES
    POSITION_INDEPENDENT_CODE ON
    BUILD_SHARED_LIBS ON
)

add_subdirectory(extern/pybind11)
pybind11_add_module(_pymark src/pymark.cpp)

target_link_libraries(_pymark PRIVATE cmark)
