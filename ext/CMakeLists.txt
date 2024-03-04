

include(GNUInstallDirs)

find_package(OpenMP)

if (OPENMP_FOUND)
  set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
  set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
  set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

set(
    VORO_HEADERS
    voro/src/cell_2d.hh
    voro/src/cell_3d.hh
    voro/src/c_info.hh
    voro/src/common.hh
    voro/src/config.hh
    voro/src/container_2d.hh
    voro/src/container_3d.hh
    voro/src/container_tri.hh
    voro/src/iter_2d.hh
    voro/src/iter_3d.hh
    voro/src/particle_list.hh
    voro/src/particle_order.hh
    voro/src/rad_option.hh
    voro/src/unitcell.hh
    voro/src/v_base_2d.hh
    voro/src/v_base_3d.hh
    voro/src/v_compute_2d.hh
    voro/src/v_compute_3d.hh
    voro/src/voro++.hh
    voro/src/wall_2d.hh
    voro/src/wall_3d.hh
    voro/src/wall.hh
    voro/src/worklist_2d.hh
    voro/src/worklist_3d.hh
)
set(
    VORO_SOURCES
    voro/src/cell_2d.cc
    voro/src/cell_3d.cc
    voro/src/common.cc
    voro/src/container_2d.cc
    voro/src/container_3d.cc
    voro/src/container_tri.cc
    voro/src/iter_2d.cc
    voro/src/iter_3d.cc
    voro/src/particle_list.cc
    voro/src/unitcell.cc
    voro/src/v_base_2d.cc
    voro/src/v_base_3d.cc
    voro/src/v_compute_2d.cc
    voro/src/v_compute_3d.cc
    voro/src/wall_2d.cc
    voro/src/wall_3d.cc
    voro/src/wall.cc
)
add_library(voro++ STATIC ${VORO_SOURCES} ${VORO_HEADERS})

target_link_libraries(voro++ PRIVATE ${OpenMP_CXX_FLAGS})

set_target_properties(
    voro++
    PROPERTIES
    PUBLIC_HEADER "${VORO_HEADERS}"
)
#message("CMAKE INSTALL DIR: ${CMAKE_INSTALL_INCLUDEDIR}")

#target_include_directories(
#    voro++
#    SYSTEM
#    PUBLIC
#    $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/voro/src>
#    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
#)
