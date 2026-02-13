import subprocess
import os
from pathlib import Path
from logger_factory import LoggerFactory

logger = LoggerFactory.get_logger("runners.compileCpp")


def compile_all_cpp() -> None:
    os.chdir("src_cpp")

    cpp_files = list(Path(".").glob("*.cpp"))

    cpp_files_str = [str(file) for file in cpp_files]

    compile_command = [
        "g++",
        *cpp_files_str,
        "-std=c++17",
        "-O2",
        "-o",
        "sorter.exe"
    ]

    try:
        logger.info(f"Compiling files: {", ".join(cpp_files_str)}")
        subprocess.run(compile_command, check=True)
    except subprocess.CalledProcessError as e:
        logger.critical("Compilation failed")
        raise e


if __name__ == "__main__":
    compile_all_cpp()
