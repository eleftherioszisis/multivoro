#include <vector>
#include <sstream>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/vector.h>

#include "voro++.hh"

#ifdef _OPENMP
    #include <omp.h>
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
    nb::ndarray<uint32_t, nb::ndim<1>> blocks,
    nb::ndarray<bool, nb::ndim<1>> periodic_boundaries,
    int n_threads) {

    // views for fast access
    const auto v_points = points.view();
    const auto v_radii = radii.view();

    const size_t n_cells = v_points.shape(0);

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
#ifdef _OPENMP
        n_threads // number of threads
#else
        1         // force 1 thread in serial case, segfault otherwise
#endif
        );

    // populate container with points
    for (int i = 0; i < n_cells; ++i) {

        const bool is_inside_container = container.point_inside(v_points(i, 0), v_points(i, 1), v_points(i, 2));
        if (!is_inside_container){
            throw nb::value_error("Points outside container walls.");
        }

        container.put(i, v_points(i, 0), v_points(i, 1), v_points(i, 2), v_radii(i));
    }

    CellVector cells(n_cells);
    std::vector<int> is_successful(n_cells, 0);

    voro::container_poly_3d::iterator it;

    # pragma omp parallel for num_threads(n_threads)
    for (it = container.begin(); it < container.end(); it++) {

        // cell from voro++ implementation with all kinds of stuff
        voro::voronoicell_neighbor_3d impl_cell;

        // find the id of the cell from its block index and block local position
        const auto cell_index = container.id[it->ijk][it->q];

        // compute voronoi cell and store wheter it's successful or not
        is_successful[cell_index] = container.compute_cell(impl_cell, it);

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

