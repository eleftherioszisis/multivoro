#include <nanobind/nanobind.h>
#include "voro++.hh"

namespace nb = nanobind;

NB_MODULE(_multivoro, m) {
    nb::class_<voro::container_base_3d>(m, "container_base_3d")
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
                int,    // ps_
                int     // nt_
            >()
        );
}
