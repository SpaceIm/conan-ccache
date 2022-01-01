from conans import ConanFile, CMake, tools
import os

required_conan_version = ">=1.33.0"


class CCacheConan(ConanFile):
    name = "ccache"
    description = (
        "Ccache (or “ccache”) is a compiler cache. It speeds up recompilation "
        "by caching previous compilations and detecting when the same "
        "compilation is being done again."
    )
    license = ("GPL-3.0", "LGPL-3.0")
    topics = ("ccache", "compiler-cache", "recompilation")
    homepage = "https://ccache.dev"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "redis_storage": [True, False],
    }
    default_options = {
        "redis_storage": True,
    }

    generators = "cmake", "cmake_find_package_multi"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def export_sources(self):
        self.copy("CMakeLists.txt")
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            self.copy(patch["patch_file"])

    def requirements(self):
        self.requires("zstd/1.5.1")
        if self.options.redis_storage:
            self.requires("hiredis/1.0.2")

    def package_id(self):
        del self.info.settings.compiler

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["REDIS_STORAGE_BACKEND"] = self.options.redis_storage
        self._cmake.definitions["ENABLE_DOCUMENTATION"] = False
        self._cmake.definitions["ENABLE_TESTING"] = False
        self._cmake.configure()
        return self._cmake

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("GPL-*.txt", dst="licenses", src=self._source_subfolder)
        self.copy("LGPL-*.txt", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bin_path))
        self.env_info.PATH.append(bin_path)
