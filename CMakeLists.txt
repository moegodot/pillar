# CMakeList.txt : CMake project for pillar, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 4.0)

include("${CMAKE_CURRENT_SOURCE_DIR}/cmake/version.cmake")

project ("moegodot_pillar" VERSION "${MOEGODOT_PILLAR_VERSION}" LANGUAGES CXX)

function(initiate_moegodot_pillar_target target_name)
    set_property(TARGET ${target_name} PROPERTY CXX_STANDARD 23)
endfunction()

function(moegodot_pillar_add_subdir curdir)
    file(GLOB children RELATIVE ${curdir} "${curdir}/*")
    foreach (child ${children})
        if(IS_DIRECTORY ${curdir}/${child})
            add_subdirectory("${curdir}/${child}")
        endif ()
    endforeach ()
endfunction()

moegodot_pillar_add_subdir("${CMAKE_CURRENT_SOURCE_DIR}/src")
moegodot_pillar_add_subdir("${CMAKE_CURRENT_SOURCE_DIR}/lib")
