#include <nanobind/nanobind.h>
#include "voro++.hh"

namespace nb = nanobind;


NB_MODULE(_multivoro, m) {
    nb::class_<voro::container_poly_3d>(m, "ContainerPoly")
        .def(
            nb::init<
                double, // ax
                double, // bx
                double, // ay
                double, // by
                double, // az
                double, // bz
                int,    // nx
                int,    // ny
                int,    // nz
                bool,   // x_prd
                bool,   // y_prd
                bool,   // z_prd
                int,    // init_mem
                int     // nt_
            >()
        )
        .def("put", nb::overload_cast<int,double,double,double,double>(&voro::container_poly_3d::put));
}
