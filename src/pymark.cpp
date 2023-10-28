#include <pybind11/pybind11.h>
#include <cmark.h>

std::string convert(char *markdown) {
    char *html = cmark_markdown_to_html(markdown, strlen(markdown), 0);
    std::string result(html);
    free(html);
    return result;
}

PYBIND11_MODULE(_pymark, m) {
    m.doc() = "cmark python extension library"; // optional module docstring

    m.def("convert", &convert, "Convert markdown to html");
}
