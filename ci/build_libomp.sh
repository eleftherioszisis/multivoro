#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BUILD_DIR=${DIR}/libs_build

git clone --depth 1 --branch llvmorg-11.1.0 https://github.com/llvm/llvm-project
pushd llvm-project/openmp
mkdir build
cd build
cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_INSTALL_PREFIX="${BUILD_DIR}" -DCMAKE_MACOSX_RPATH="${BUILD_DIR}/lib" ..
make
make install

popd
rm -rf llvm-project
