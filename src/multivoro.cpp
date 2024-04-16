#include <vector>
#include <iostream>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/vector.h>

#include "voro++.hh"

#ifdef _OPENMP
    #include <omp.h>     // This line won't add the library if you don't compile with -fopenmp option.
    #ifdef _MSC_VER
         // For Microsoft compiler
         #define OMP_FOR(n) __pragma(omp parallel for if(n>10)) 
    #else  // assuming "__GNUC__" is defined
         // For GCC compiler
         #define OMP_FOR(n) _Pragma("omp parallel for if(n>10)")
    #endif
#else
    #define omp_get_thread_num() 0
    #define OMP_FOR(n)
#endif


namespace nb = nanobind;

using IntVector = std::vector<int>;
using DoubleVector = std::vector<double>;

struct Cell {
    IntVector neighbors;
    IntVector face_vertices;
    DoubleVector vertices;
};

using CellVector = std::vector<Cell>;

CellVector inline compute_voronoi_3d(
    nb::ndarray<double, nb::ndim<2>> points,
    nb::ndarray<double, nb::ndim<1>> radii,
    nb::ndarray<double, nb::ndim<2>> limits,
    nb::ndarray<size_t, nb::ndim<1>> blocks,
    nb::ndarray<bool, nb::ndim<1>> periodic_boundaries
    ) {

    // views for fast access
    auto v_points = points.view();
    auto v_radii = radii.view();

    // initialize container
    voro::container_poly_3d container(
        limits(0, 0), // ax
        limits(1, 0), // bx
        limits(0, 1), // ay
        limits(1, 1), // by
        limits(0, 2), // az
        limits(1, 2), // bz
        blocks(0), // nx
        blocks(1), // ny
        blocks(2), // nz
        periodic_boundaries(0), // x_prd
        periodic_boundaries(1), // y_prd
        periodic_boundaries(2), // z_prd
        8, // init memory
        1 // number of threads
    );

    // populate container with points
    for (int i = 0; i < v_points.shape(0); ++i) {

        const bool is_inside_container = container.point_inside(v_points(i, 0), v_points(i, 1), v_points(i, 2));
        if (not is_inside_container){
            throw nb::value_error("Points outside container walls.");
        }

        container.put(i, v_points(i, 0), v_points(i, 1), v_points(i, 2), v_radii(i));
    }

    auto cells = CellVector(points.shape(0));

    voro::container_poly_3d::iterator it;
    for (it = container.begin(); it < container.end(); it++) {

        // cell from voro++ implementation with all kinds of stuff
        voro::voronoicell_neighbor_3d impl_cell;

        // compute voronoi cell
        container.compute_cell(impl_cell, it);

        // find the id of the cell from its block index and block local position
        const auto cell_index = container.id[it->ijk][it->q];

        // cell we are returning with well-behaved attributes
        auto& cell = cells[cell_index];

        // populate the return cell attributes using the voro cell methods
        impl_cell.vertices(
            v_points(cell_index, 0),
            v_points(cell_index, 1),
            v_points(cell_index, 2),
            cell.vertices
        );
        impl_cell.neighbors(cell.neighbors);
        impl_cell.face_vertices(cell.face_vertices);
    }

    return cells;
}


NB_MODULE(_multivoro, m) {

    nb::class_<Cell>(m, "Cell")
        .def(nb::init<>())
        .def(
            "get_vertices",
            [](Cell& self){
                // reshape into a 2d point array
                const size_t shape[2] = {self.vertices.size() / 3, 3};
                return nb::ndarray<nb::numpy, double>(
                    /* data = */ self.vertices.data(),
                    /* ndim = */ 2,
                    /* shape = */ shape,
                    /* owner = */ nb::handle()
                );
            }
        )
        .def(
            "get_neighbors",
            [](Cell& self){
                return nb::ndarray<nb::numpy, int>(
                    /* data = */ self.neighbors.data(),
                    /* shape = */ {self.neighbors.size()},
                    /* owner = */ nb::handle()
                );
            }
        )
        .def(
            "get_face_vertices",
            [](Cell& self){
                return nb::ndarray<nb::numpy, int>(
                    /* data = */ self.face_vertices.data(),
                    /* shape = */ {self.face_vertices.size()},
                    /* owner = */ nb::handle()
                );
            }
        );
    m.def("compute_voronoi_3d", &compute_voronoi_3d);
}

