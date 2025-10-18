import os.path

import moegodot_build_utilities as util
import moegodot_build_utilities.detector as detector
import subprocess
import argparse
import shutil
import logging

util.setup()

log = logging.getLogger(__file__)
info = detector.SystemInformation(__file__)

cmake = info.use_tool("cmake", ">=3.31.0")
ninja = info.use_tool("ninja")
git = info.use_tool("git")

root_dir = info.root_dir
library_dir = f"{root_dir}/3rd_library"
library_build_dir = f"{library_dir}/build"
library_install_dir = f"{library_dir}/install"

def get_source_dir_of(libname):
    return f"{library_dir}/{libname}/"
def get_build_dir_of(libname):
    return f"{library_build_dir}/{libname}/"
def get_install_dir_of(libname):
    return f"{library_install_dir}/{libname}/"

def cmake_build_and_install(build_dir, config="Release"):
    subprocess.run([cmake,"--build", build_dir,"--config", config],check=True)
    subprocess.run([cmake,"--install", build_dir,"--config", config],check=True)
def force_rmtree(tree):
    tree = os.path.abspath(tree)
    shutil.rmtree(tree,ignore_errors=True)

def build_cmake_library(libname, args):
    source_dir = get_source_dir_of(libname)
    build_dir = get_build_dir_of(libname)
    install_dir = get_install_dir_of(libname)
    cmake_config_prefix = [cmake,
                           "-S", source_dir,
                            "-B", build_dir,
                           "-G","Ninja",
                            "-DCMAKE_BUILD_TYPE=Release",
                            f"-DCMAKE_INSTALL_PREFIX={install_dir}",
                            f"-DCMAKE_MAKE_PROGRAM={ninja}"
                            "-Wno-dev"]
    info.enter(source_dir)
    subprocess.run(cmake_config_prefix + args,
                   check=True)
    cmake_build_and_install(build_dir)
    del source_dir
    del build_dir
    del install_dir
    info.enter(root_dir)
    
def operate_cmake_library(lib, clean,build_and_install):
    libname,args = lib()
    
    if clean:
        force_rmtree(get_build_dir_of(libname))
        force_rmtree(get_install_dir_of(libname))
    
    if build_and_install:
        build_cmake_library(libname, args)

def zlib():
    return ("zlib",  
    ["-DZLIB_ENABLE_TESTS=OFF",
           "-DZLIB_COMPAT=ON",
           "-DWITH_GTEST=OFF"])

def bzip2():
    return ("zlib",
                        ["-DENABLE_WERROR=OFF",
                         "-DENABLE_DEBUG=OFF",
                         "-DENABLE_APP=OFF",
                         "-DENABLE_DOCS=OFF",
                         "-DENABLE_EXAMPLES=OFF",
                         "-DENABLE_LIB_ONLY=ON",
                         "-DENABLE_STATIC_LIB=ON",
                         "-DENABLE_SHARED_LIB=ON"])

def libpng():
    return ("libpng",
                        ["-DPNG_TESTS=OFF",
                         "-DPNG_EXECUTABLES=OFF",
                         "-DPNG_BUILD_ZLIB=OFF",
                         "-DPNG_HARDWARE_OPTIMIZATIONS=ON",
                         f"-DZLIB_ROOT={get_install_dir_of("zlib")}/",
                         f"-DPNG_TOOLS=OFF"])
    
parser = argparse.ArgumentParser(
    prog="duce's toolset",
    description='Manage the building and other chores of Pillar Project.',
    epilog='我们不但善于破坏一个旧世界,我们还将善于建设一个新世界.')
