import os
import sys
import platform
import subprocess
from pathlib import Path
from logger_factory import LoggerFactory

logger = LoggerFactory.get_logger("runners.collectEnviromentInfo")

def get_ram_info():
    try:
        import psutil
        ram = psutil.virtual_memory()
        return f"{ram.total / (1024**3):.2f} GB"
    except ImportError:
        return "Unknown (psutil not installed)"

def get_compiler_version():
    try:
        result = subprocess.run(["g++", "--version"], capture_output=True, text=True, check=True)
        # return the first line of the output
        return result.stdout.split('\n')[0].strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            result = subprocess.run(["cl"], capture_output=True, text=True)
            return result.stderr.split('\n')[0].strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "Unknown (g++ or cl not found)"

def collect_info():
    compiler_version = get_compiler_version()
    
    flags = "/O2 /EHsc /std:c++17" if "Unknown" not in compiler_version and os.name == "nt" else "-O2 -std=c++17"

    info = {
        "OS": f"{platform.system()} {platform.release()}",
        "Architecture": platform.machine(),
        "CPU": platform.processor(),
        "CPU Cores": os.cpu_count(),
        "RAM": get_ram_info(),
        "Python Version": sys.version.split('\n')[0],
        "C++ Compiler": compiler_version,
        "Compilation Flags": flags
    }
    
    results_dir = Path(__file__).resolve().parents[1] / "results"
    results_dir.mkdir(exist_ok=True)
    
    out_file = results_dir / "env_info.txt"
    logger.info(f"Collecting environment info to {out_file}")
    
    with open(out_file, "w") as f:
        for k, v in info.items():
            f.write(f"{k}: {v}\n")

if __name__ == "__main__":
    collect_info()
