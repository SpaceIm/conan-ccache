from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_C_COMPILER_LAUNCHER"] = "ccache"
        cmake.definitions["CMAKE_CXX_COMPILER_LAUNCHER"] = "ccache"
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            self.run("ccache --version", run_environment=True)
            bin_path = os.path.join("bin", "test_package")
            self.run(bin_path, run_environment=True)
