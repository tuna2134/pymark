#include <pybind11/pybind11.h>
#include <cmark.h>
#include <iostream>

int add(int i, int j) {
    return i + j;
}

std::string convert(char *markdown) {
    char *html = cmark_markdown_to_html(markdown, strlen(markdown), 0);
    std::string result(html);
    free(html);
    return result;
}

PYBIND11_MODULE(pymark, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function that adds two numbers");
    m.def("convert", &convert, "Convert markdown to html");
}
