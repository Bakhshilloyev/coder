import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent.adapters import detect_arch, detect_platform, describe
from agent.adapters.common.arch import is_64bit


class TestPlatformDetection(unittest.TestCase):
    def test_arch_known(self):
        arch = detect_arch()
        self.assertIn(arch, ("x64", "x86", "arm64", "armv7", "arm", "riscv64", "mips", "unknown"))

    def test_platform_family(self):
        self.assertIn(detect_platform(), ("linux", "windows", "termux"))

    def test_is_64bit_bool(self):
        self.assertIsInstance(is_64bit(), bool)

    def test_describe_has_python(self):
        info = describe()
        self.assertIn("python", info)
        self.assertIn("os", info)


if __name__ == "__main__":
    unittest.main()
