from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from conans.tools import Version
import os


class CppwinrtRecipe(ConanFile):
    name = "cppwinrt"
    settings = "os", "compiler"
    description = "C++/WinRT is a standard C++ language projection for the Windows Runtime"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/microsoft/cppwinrt"
    license = "MIT"
    topics = ("conan", "cppwinrt")
    # TODO: Update options
    options = {"windows_sdk_version": "ANY" # Target Windows SDK version
    }

    @property
    def _dest_folder(self):
        return "%s_%s_%s" % (self.name, self.version, self.options.windows_sdk_version)

    def configure(self):
        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration("%s only supports Windows." % (self.name,))

        compiler = self.settings.get_safe("compiler")
        compiler_version = Version(self.settings.get_safe("compiler.version"))

        minimal_version = {
            "Visual Studio": "15"
        }

        if compiler in minimal_version and \
           compiler_version < minimal_version[compiler]:
            raise ConanInvalidConfiguration("%s does not support %s %s." % (self.name, compiler, compiler_version))

        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, "17")

    def source(self):
        # Change file extension: .nupkg => .zip
        filename = os.path.basename(self.conan_data["sources"][self.version]["url"])
        filename = os.path.splitext(filename)[0] + ".zip"

        tools.get(filename=filename, **self.conan_data["sources"][self.version])

    def build(self):
        cppwinrt_exe = os.path.join(self.build_folder, "bin", "cppwinrt.exe")
        command = "%s -input %s" % (cppwinrt_exe, self.options.windows_sdk_version)
        command = command + (" -output %s" % self._dest_folder)

        self.run(command)

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self.source_folder)

        self.copy(pattern="*", dst="include", src=self._dest_folder)

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.system_libs = ["windowsapp"]
