import subprocess
import os
from pathlib import Path
from logger_factory import LoggerFactory

logger = LoggerFactory.get_logger("runners.compileCpp")


def compile_all_cpp() -> None:
    src_cpp_dir = Path(__file__).resolve().parents[1] / "src_cpp"
    os.chdir(src_cpp_dir)

    cpp_files = list(Path(".").glob("*.cpp"))

    cpp_files_str = [str(file) for file in cpp_files]

    is_windows = os.name == "nt"
    exe_name = "sorter.exe" if is_windows else "sorter"

    compile_command_gpp = f"g++ {' '.join(cpp_files_str)} -std=c++17 -O2 -o {exe_name}"
    
    if is_windows:
        compile_command_msvc = f'cl /std:c++17 /EHsc /O2 /Fe:{exe_name} {" ".join(cpp_files_str)}'
        
        try:
            logger.info(f"Windows detected. Attempting MSVC compilation: {', '.join(cpp_files_str)}")
            subprocess.run(compile_command_msvc, check=True, shell=True)
            logger.info("MSVC compilation successful.")
        except subprocess.CalledProcessError as e:
            logger.critical("MSVC compilation failed.")
            raise e
    else:
        # Linux / MacOS defaults to g++
        try:
            logger.info(f"Unix/Linux detected. Compiling with g++: {', '.join(cpp_files_str)}")
            subprocess.run(compile_command_gpp, check=True, shell=True)
            logger.info("g++ compilation successful.")
        except subprocess.CalledProcessError as e:
            logger.critical("g++ compilation failed.")
            raise e


if __name__ == "__main__":
    compile_all_cpp()
