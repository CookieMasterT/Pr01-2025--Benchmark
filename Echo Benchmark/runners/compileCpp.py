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

    flags_to_compile = {
        "O0": {"gpp": "-O0", "msvc": "/Od"},
        "O2": {"gpp": "-O2", "msvc": "/O2"}
    }

    vcvars_setup = ""
    if is_windows:
        vswhere_path = Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "Microsoft Visual Studio" / "Installer" / "vswhere.exe"
        if vswhere_path.exists():
            try:
                result = subprocess.run(
                    [str(vswhere_path), "-latest", "-products", "*", "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64", "-property", "installationPath"],
                    capture_output=True, text=True, check=True
                )
                vs_path = result.stdout.strip()
                if vs_path:
                    vcvars64_path = Path(vs_path) / "VC" / "Auxiliary" / "Build" / "vcvars64.bat"
                    if vcvars64_path.exists():
                        vcvars_setup = f'call "{vcvars64_path}" && '
            except Exception as e:
                logger.warning(f"Failed to find MSVC via vswhere: {e}")

    for opt_level, flags in flags_to_compile.items():
        exe_name = f"sorter_{opt_level}.exe" if is_windows else f"sorter_{opt_level}"
        
        compile_command_gpp = f"g++ {' '.join(cpp_files_str)} -std=c++17 {flags['gpp']} -o {exe_name}"
        compile_command_msvc = f'{vcvars_setup}cl /std:c++17 /EHsc {flags["msvc"]} /Fe:{exe_name} {" ".join(cpp_files_str)}'
        
        if is_windows:
            try:
                logger.info(f"Windows detected. Attempting MSVC compilation with {opt_level}: {', '.join(cpp_files_str)}")
                subprocess.run(compile_command_msvc, check=True, shell=True)
                logger.info(f"MSVC compilation {opt_level} successful.")
            except subprocess.CalledProcessError as e:
                logger.critical(f"MSVC compilation {opt_level} failed.")
                raise e
        else:
            try:
                logger.info(f"Unix/Linux detected. Compiling with g++ {opt_level}: {', '.join(cpp_files_str)}")
                subprocess.run(compile_command_gpp, check=True, shell=True)
                logger.info(f"g++ compilation {opt_level} successful.")
            except subprocess.CalledProcessError as e:
                logger.critical(f"g++ compilation {opt_level} failed.")
                raise e


if __name__ == "__main__":
    compile_all_cpp()
