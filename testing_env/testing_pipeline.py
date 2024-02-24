import re
import subprocess
import argparse
import enum

#  TODO (Optionally) handle cases when files with provided filenames do not exist
#  TODO (Would be great) apply 'Chain of responsibility' pattern in the pipeline


class Filename(enum.Enum):
    bruteforce = "brute"
    optimised = "optim"
    generator = "gen"


class CompilationError(RuntimeError):
    """ Thrown in case of non-compilable code is passed """


class CodeFile:
    def __init__(self, fname):
        extension = determine_ext(fname)

        if extension == FileType.unsupported:
            raise NotImplementedError("This file type is unsupported.")

        self.ext: str = extension.name
        self.name: str = fname[:-len(self.ext) - 1:]


class Room:
    def __init__(self, **kwargs):
        self.bruteforce = CodeFile(kwargs[Filename.bruteforce.name])
        self.optim = CodeFile(kwargs[Filename.optimised.name])
        self.gen = CodeFile(kwargs[Filename.generator.name])


class FileType(enum.Enum):
    py = "py"
    cpp = "cpp"
    unsupported = "@"


def determine_ext(name: str) -> FileType:
    is_valid_name = re.match(r'.*\..*', name)
    if not is_valid_name:
        return FileType.unsupported

    for ftype in FileType:
        if name[-len(ftype.name)::] == ftype.name:
            return ftype

    return FileType.unsupported


def compile_solution(code: CodeFile) -> None:
    if code.ext == FileType.py.name:
        # no need to compile python code
        return

    if code.ext == FileType.cpp.name:
        res = subprocess.run(["g++", f"{code.name}.{code.ext}", "-o", f"{code.name}"],
                             shell=False,
                             capture_output=True)

    if res.returncode != 0:
        print(res.stderr.decode('utf-8'))
        raise CompilationError("Cpp solution failed to compile")


def generate_tests(gen_code: CodeFile) -> None:
    gen_name, gen_ext = gen_code.name, gen_code.ext
    test_name: str = "testcase.txt"

    if gen_ext == FileType.py.name:
        res = subprocess.run(["python3", f"{gen_name}.{gen_ext}"],
                             shell=False,
                             stdout=open(file=test_name, mode="w"),
                             stderr=subprocess.PIPE)

    if gen_ext == FileType.cpp.name:
        res = subprocess.run([f"./{gen_name}"],
                             shell=False,
                             stdout=open(file=test_name, mode="w"),
                             stderr=subprocess.PIPE)

    if res.returncode != 0:
        print(res.stderr.decode('utf-8'))
        raise RuntimeError("Generator has a Runtime Error")


def run_solution(code: CodeFile, out_name: str):
    test_name = "testcase.txt"
    if code.ext == FileType.py.name:
        res = subprocess.run(["python3", f"{code.name}.{code.ext}"],
                             shell=False,
                             stdout=open(file=out_name, mode="w"),
                             stdin=open(file=test_name, mode="r"),
                             stderr=subprocess.PIPE)

    if code.ext == FileType.cpp.name:
        res = subprocess.run([f"./{code.name}"],
                             shell=False,
                             stdout=open(file=out_name, mode="w"),
                             stdin=open(file=test_name, mode="r"),
                             stderr=subprocess.PIPE)

    if res.returncode != 0:
        print(res.stderr.decode('utf-8'))
        raise RuntimeError(f"The {out_name} code has Runtime Error")


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
    room: Room
    try:
        room = Room(**vars(args))
    except NotImplementedError as NE:
        print(NE)
        exit(1)

    testing_rounds = 5

    try:
        compile_solution(room.bruteforce)
        compile_solution(room.gen)
        compile_solution(room.optim)
    except CompilationError as CE:
        print(CE)
        exit(1)

    for i in range(1, testing_rounds + 1):
        try:
            generate_tests(room.gen)

            run_solution(room.optim, "out_opt")
            run_solution(room.bruteforce, "out_bru")
        except RuntimeError as RE:
            print(RE)
            exit(1)

        res = compare_results("out_opt", "out_bru")

        if res != "":
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
