import re
import subprocess
import argparse
from enum import Enum
from dataclasses import dataclass

from abc import ABCMeta, abstractmethod

#  TODO (Optionally) handle cases when files with provided filenames do not exist
#  TODO (Would be great) apply 'Chain of responsibility' pattern in the pipeline


class Filename(Enum):
    bruteforce = "brute"
    optimised = "optim"
    generator = "gen"
    testfile = "testcase.txt"
    out1 = "out1"
    out2 = "out2"


class FileType(Enum):
    py = "py"
    cpp = "cpp"
    unsupported = "@"


class CompilationError(RuntimeError):
    """ Thrown in case of non-compilable code is passed """


class CodeFile:
    def __init__(self, fname: str):
        extension = determine_ext(fname)

        self.ext: str = extension.name
        self.name: str = fname[:-len(self.ext) - 1:]


class Room:
    def __init__(self, bruteforce: str, optimised: str, generator: str):
        print(bruteforce, optimised, generator)
        self.bruteforce = CodeFile(bruteforce)
        self.optimised = CodeFile(optimised)
        self.generator = CodeFile(generator)


def determine_ext(name: str) -> FileType:
    is_valid_name = re.match(r'.*\..*', name)
    if not is_valid_name:
        return FileType.unsupported

    for ftype in FileType:
        if name[-len(ftype.name)::] == ftype.name:
            return ftype

    return FileType.unsupported


class ISrcCodeWorker(metaclass=ABCMeta):
    """ This is implementation of chain of responsibility pattern, where programming language handler is a successor.

    The Handler Interface that the Successors (Source code type handlers) should implement.
    """

    @staticmethod
    @abstractmethod
    def compile(payload: CodeFile):
        """A method to implement"""

    @staticmethod
    @abstractmethod
    def generate_tests(payload: CodeFile):
        """"""

    @staticmethod
    @abstractmethod
    def run(payload: CodeFile, out: str):
        """"""


class SrcPythonWorker(ISrcCodeWorker):
    """Python code handler"""

    @staticmethod
    def compile(payload: CodeFile):
        if payload.ext != FileType.py.name:
            return SrcCppWorker.compile(payload)

    @staticmethod
    @abstractmethod
    def generate_tests(payload: CodeFile):
        if payload.ext != FileType.py.name:
            return SrcCppWorker.generate_tests(payload)

        res = subprocess.run(["python3", f"{payload.name}.{payload.ext}"],
                             shell=False,
                             stdout=open(file=Filename.testfile.value, mode="w"),
                             stderr=subprocess.PIPE)

        if res.returncode == 0:
            return

        print(res.stderr.decode('utf-8'))
        raise RuntimeError("Generator has a Runtime Error")

    @staticmethod
    @abstractmethod
    def run(payload: CodeFile, out_name: str):
        if payload.ext != FileType.py.name:
            return SrcCppWorker.run(payload, out_name)

        res = subprocess.run(["python3", f"{payload.name}.{payload.ext}"],
                             shell=False,
                             stdout=open(file=out_name, mode="w"),
                             stdin=open(file=Filename.testfile.value, mode="r"),
                             stderr=subprocess.PIPE)

        if res.returncode == 0:
            return

        print(res.stderr.decode('utf-8'))
        raise RuntimeError(f"The {payload.name} code has Runtime Error")


class SrcCppWorker(ISrcCodeWorker):
    """C++ code handler"""

    @staticmethod
    def compile(payload: CodeFile):
        if payload.ext != FileType.cpp.name:
            return SrcUnsupportedWorker.compile(payload)


        res = subprocess.run(["g++", f"{payload.name}.{payload.ext}", "-o", f"{payload.name}"],
                             shell=False,
                             capture_output=True)

        if res.returncode == 0:
            return

        print(res.stderr.decode('utf-8'))
        raise CompilationError("Cpp solution failed to compile")

    @staticmethod
    @abstractmethod
    def generate_tests(payload: CodeFile):
        if payload.ext != FileType.cpp.name:
            return SrcUnsupportedWorker.generate_tests(payload)

        res = subprocess.run([f"./{payload.name}"],
                             shell=False,
                             stdout=open(file=Filename.testfile.value, mode="w"),
                             stderr=subprocess.PIPE)

        if res.returncode == 0:
            return

        print(res.stderr.decode('utf-8'))
        raise RuntimeError("Generator has a Runtime Error")

    @staticmethod
    @abstractmethod
    def run(payload: CodeFile, out_name: str):
        if payload.ext != FileType.cpp.name:
            return SrcUnsupportedWorker.run(payload, out_name)

        res = subprocess.run([f"./{payload.name}"],
                             shell=False,
                             stdout=open(file=out_name, mode="w"),
                             stdin=open(file=Filename.testfile.value, mode="r"),
                             stderr=subprocess.PIPE)

        if res.returncode == 0:
            return

        print(res.stderr.decode('utf-8'))
        raise RuntimeError(f"The {out_name} code has Runtime Error")


class SrcUnsupportedWorker(ISrcCodeWorker):
    """Unsupported code handler"""
    @staticmethod
    def compile(payload: CodeFile):
        raise NotImplementedError("This file type is unsupported.")

    @staticmethod
    @abstractmethod
    def generate_tests(payload: CodeFile):
        raise NotImplementedError("This file type is unsupported.")

    @staticmethod
    @abstractmethod
    def run(payload: CodeFile, out_name: str):
        raise NotImplementedError("This file type is unsupported.")


def compile_solution(code: CodeFile):
    print(code.ext)
    SrcPythonWorker.compile(code)


def generate_tests(gen_code: CodeFile) -> None:
    SrcPythonWorker.generate_tests(gen_code)


def run_solution(code: CodeFile, out_name: str):
    SrcPythonWorker.run(code, out_name)


def compare_results(fname1: str, fname2: str) -> str:
    run_res = subprocess.run(["diff", "-w", f"{fname1}", f"{fname2}"], shell=False, capture_output=True)
    if run_res.returncode == 1:
        # found a mismatch
        return run_res.stdout.decode("utf-8")
    return ""


"""
    Enabling passing filenames as arguments to the program
"""
parser = argparse.ArgumentParser(description="Please pass names of files to the program")
parser.add_argument("-b", f"--{Filename.bruteforce.name}", type=str, required=True)
parser.add_argument("-o", f"--{Filename.optimised.name}", type=str, required=True)
parser.add_argument("-g", f"--{Filename.generator.name}", type=str, required=True)


def run():
    args = parser.parse_args()

    room = Room(**vars(args))

    testing_rounds = 5
    try:
        compile_solution(room.bruteforce)
        compile_solution(room.generator)
        compile_solution(room.optimised)
    except CompilationError as CE:
        print(CE)
        exit(1)

    for i in range(1, testing_rounds + 1):
        try:
            generate_tests(room.generator)

            run_solution(room.optimised, "out_opt")
            run_solution(room.bruteforce, "out_bru")
        except RuntimeError as RE:
            print(RE)
            exit(1)

        res = compare_results("out_opt", "out_bru")

        if res == "":
            continue

        print("Divergent test:")
        testname = "testcase.txt"
        try:
            with open(testname, 'r') as file:
                content = file.read()
                print(content)

        except FileNotFoundError:
            print("Tests were not generated.")

        print(f"Finished in {i} iterations")
        return

    print(f"Run {testing_rounds} testing iterations, found no differences.")


if __name__ == "__main__":
    run()
