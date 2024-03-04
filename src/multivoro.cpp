#include <nanobind/nanobind.h>
#include "voro++.hh"

NB_MODULE(_multivoro, m) {
    m.def("hello", []() { return "Hello world!"; });
}
