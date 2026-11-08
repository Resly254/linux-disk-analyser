import unittest
import tempfile

from pathlib import Path
from app import investigate_disk, get_directory_size


class DiskInvestigatorTests(unittest.TestCase):

    def test_directory_size(self):

        with tempfile.TemporaryDirectory() as temp:

            directory = Path(temp)

            test_file = directory / "test.txt"
            test_file.write_text("Hello DevOps")

            size = get_directory_size(directory)

            self.assertEqual(size, 12)

    def test_investigation(self):

        with tempfile.TemporaryDirectory() as temp:

            report = investigate_disk(temp)

            self.assertIn("usage_percentage", report)

            self.assertIn("status", report)

            self.assertIn("largest_directories", report)

    def test_invalid_directory(self):

        with self.assertRaises(ValueError):

            investigate_disk("/this/path/does/not/exist")


if __name__ == "__main__":
    unittest.main()
