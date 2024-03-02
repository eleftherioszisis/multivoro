#include <nanobind/nanobind.h>


NB_MODULE(_multivoro, m) {
    m.def("hello", []() { return "Hello world!"; });
}
