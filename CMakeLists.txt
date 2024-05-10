# Set the minimum CMake version and policies for highest tested version
cmake_minimum_required(VERSION 3.15...3.27)

project(
  # name of the project
  multivoro

  DESCRIPTION "Python Binding for multi-threaded voro++ library."

  # ensure there is a working c++ compiler
  LANGUAGES CXX
)

# Warn if the user invokes CMake directly
if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build-core'.
  Running it directly will almost certainly not produce the desired
  result. If you are a user trying to install this package, use the
  command below, which will install all necessary build dependencies,
  compile the package in an isolated environment, and then install it.
  =====================================================================
   $ pip install .
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ pip install nanobind scikit-build-core[pyproject]
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to rerun the above
  after editing C++ files.")
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Try to import all Python components potentially needed by nanobind
find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

# Import nanobind through CMake's find_package mechanism
find_package(nanobind CONFIG REQUIRED)

OPTION(USE_OpenMP "Use OpenMP" OFF)

if (USE_OpenMP)
  find_package(OpenMP REQUIRED)
  set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
  set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
  set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
  message(WARNING "OpenMP option is enabled. Compilation will proceed with multihreading support.")
else()
  message(WARNING "OpenMP option is disabled. Compilation will proceed without multihreading support.")
endif()

set(
    VORO_SOURCES
    ext/voro/src/cell_2d.cc
    ext/voro/src/cell_3d.cc
    ext/voro/src/common.cc
    ext/voro/src/container_2d.cc
    ext/voro/src/container_3d.cc
    ext/voro/src/container_tri.cc
    ext/voro/src/iter_2d.cc
    ext/voro/src/iter_3d.cc
    ext/voro/src/particle_list.cc
    ext/voro/src/unitcell.cc
    ext/voro/src/v_base_2d.cc
    ext/voro/src/v_base_3d.cc
    ext/voro/src/v_compute_2d.cc
    ext/voro/src/v_compute_3d.cc
    ext/voro/src/wall_2d.cc
    ext/voro/src/wall_3d.cc
    ext/voro/src/wall.cc

)
# prepend the relative path to the submodule external location of the sources
list(TRANSFORM "${VORO_SOURCES}" PREPEND "ext/voro/src/")

# We are now ready to compile the actual extension module
nanobind_add_module(
  # Name of the extension
  _multivoro

  # Target the stable ABI for Python 3.12+, which reduces
  # the number of binary wheels that must be built. This
  # does nothing on older Python versions
  STABLE_ABI

  # Source code goes here
  src/multivoro.cpp
  ${VORO_SOURCES}
)

target_include_directories(
    _multivoro
    PRIVATE
    ext/voro/src
)

if (USE_OpenMP)
  target_link_libraries(_multivoro PRIVATE ${OpenMP_CXX_FLAGS})
endif()

# Install directive for scikit-build-core
install(TARGETS _multivoro LIBRARY DESTINATION multivoro)
