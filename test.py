from dataclasses import dataclass
import os
import subprocess
import tempfile
import unittest

write_golden_files = False


@dataclass
class SampleFile:
    base: str
    input_path: str
    output_path: str


class TestEvaluator(unittest.TestCase):
    excluded_programs = {
        # Infinite programs
        "default",
        "turtle",
    }

    def sample_programs(self):
        program_dir = os.path.join(os.path.dirname(__file__), "test_programs")
        samples = []
        for filename in os.listdir(program_dir):
            base, ext = os.path.splitext(filename)

            if base in self.excluded_programs:
                continue
            if ext != ".art":
                continue

            input_path = os.path.join(program_dir, filename)
            stdout_path = os.path.join(program_dir, base + ".output")
            samples.append(SampleFile(base, input_path, stdout_path))

        return samples

    def execute(self, filename):
        eval_path = os.path.join(os.path.dirname(__file__), "main.py")
        with open(filename) as inp:
            text = inp.read()

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as src:
            src.write(text)

            # Since we're not closing the file, we need to seek back to the
            # start before we try reading it again.
            src.seek(0)

            capture = subprocess.run(
                ["python", eval_path, "--tick=0", "--no-clear", src.name],
                capture_output=True,
                text=True,
            )

        return capture.stdout

    @unittest.skipIf(write_golden_files, "writing golden files")
    def test_sample_programs(self):
        for program in self.sample_programs():
            with self.subTest(program.base):
                actual = self.execute(program.input_path)
                with open(program.output_path) as out:
                    expected = out.read()
                self.assertEqual(actual, expected)

    @unittest.skipIf(not write_golden_files, "not writing golden files")
    def test_write_golden_files(self):
        for program in self.sample_programs():
            print(program.base)
            with self.subTest(program.base):
                stdout = self.execute(program.input_path)
                with open(program.output_path, "w") as out:
                    out.write(stdout)


if __name__ == "__main__":
    unittest.main()
