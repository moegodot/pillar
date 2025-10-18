
set(MOEGODOT_PILLAR_VERSION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/version.txt")
message(CHECK_START "Find pillar version file")

if (EXISTS ${MOEGODOT_PILLAR_VERSION_FILE})
    message(CHECK_PASS "${MOEGODOT_PILLAR_VERSION_FILE}")
else ()
    message(CHECK_FAIL "not found")
endif ()

message(CHECK_START "Read pillar version file and set variable")
file(READ ${MOEGODOT_PILLAR_VERSION_FILE} MOEGODOT_PILLAR_VERSION_RAW)

set(MOEGODOT_PILLAR_VERSION_INVALID "[ \t\r\n]")

if (${MOEGODOT_PILLAR_VERSION_RAW} MATCHES ${MOEGODOT_PILLAR_VERSION_INVALID})
    message(CHECK_FAIL "invalid character was detected")
    message(FATAL_ERROR "Failed to set the pillar version")
else ()
    message(CHECK_PASS ${MOEGODOT_PILLAR_VERSION_RAW})
endif ()

set(MOEGODOT_PILLAR_VERSION ${MOEGODOT_PILLAR_VERSIONRAW})
