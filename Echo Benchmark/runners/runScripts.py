import subprocess
from pathlib import Path
from logger_factory import LoggerFactory
import sys
import os

import sys
import os

logger = LoggerFactory.get_logger("runners.runScripts")


def run_scripts() -> None:
    open(Path(__file__).parents[1] / "results" / "measurements_cpp.txt", "w").close()
    open(Path(__file__).parents[1] / "results" / "measurements_python.txt", "w").close()
    logger.info("Running python script. (this will take a while...)")
    subprocess.run([sys.executable, Path(__file__).resolve().parents[1] / "src_python" / "main.py"])
    logger.info("Running C++ scripts.")
    for opt_level in ["O0", "O2"]:
        exe_name = f"sorter_{opt_level}.exe" if os.name == "nt" else f"sorter_{opt_level}"
        
        logger.info(f"Running C++ script optimized with {opt_level}.")
        result = subprocess.run(
            [Path(__file__).resolve().parents[1] / "src_cpp" / exe_name, opt_level],
            capture_output=True,
            text=True
        )

        if result.stdout:
            logger.warning(f"Subprocess Output ({opt_level}): {result.stdout}")

        if result.stderr:
            logger.error(f"Subprocess Errors ({opt_level}): {result.stderr}")


if __name__ == "__main__":
    run_scripts()
