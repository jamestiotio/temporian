load("@pybind11_bazel//:build_defs.bzl", "pybind_extension", "pybind_library")

package(
    default_visibility = ["//visibility:public"],
    licenses = ["notice"],
)

pybind_library(
    name = "since_last",
    srcs = ["since_last.cc"],
    hdrs = ["since_last.h"],
)

pybind_library(
    name = "window",
    srcs = ["window.cc"],
    hdrs = ["window.h"],
)

pybind_library(
    name = "resample",
    srcs = ["resample.cc"],
    hdrs = ["resample.h"],
)

pybind_library(
    name = "join",
    srcs = ["join.cc"],
    hdrs = ["join.h"],
)

pybind_extension(
    name = "operators_cc",
    srcs = ["pyinit.cc"],
    deps = [
        ":resample",
        ":since_last",
        ":window",
        ":join",
    ],
)

py_library(
    name = "operators_cc",
    data = [":operators_cc.so"],
)
