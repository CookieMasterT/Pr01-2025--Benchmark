import subprocess
from pathlib import Path
from logger_factory import LoggerFactory

logger = LoggerFactory.get_logger("runners.runScripts")


def run_scripts() -> None:
    open(Path(__file__).parents[1] / "results" / "measurements_cpp.txt", "w").close()
    open(Path(__file__).parents[1] / "results" / "measurements_python.txt", "w").close()

    logger.info("Running python script. (this will take a while...)")
    subprocess.run(["python", Path(__file__).resolve().parents[1] / "src_python" / "main.py"])
    logger.info("Running C++ script.")
    result = subprocess.run(
        Path(__file__).resolve().parents[1] / "src_cpp" / "sorter.exe",
        capture_output=True,
        text=True
    )

    if result.stdout:
        logger.warning(f"Subprocess Output: {result.stdout}")

    if result.stderr:
        logger.error(f"Subprocess Errors: {result.stderr}")


if __name__ == "__main__":
    run_scripts()
