import subprocess
from runners.logger_factory import LoggerFactory
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent / "runners"
SCRIPTS = ["createData.py", "collectEnviromentInfo.py", "compileCpp.py", "runScripts.py", "generateReports.py"]

import sys

def run_benchmark() -> None:
    LoggerFactory.set_log_path()
    log = LoggerFactory.get_logger("run_benchmark")

    for script in SCRIPTS:
        log.info(f"Running {script}")
        try:
            subprocess.run([sys.executable, SCRIPTS_DIR / script], check=True)
        except subprocess.CalledProcessError as e:
            log.critical(f"Script {script} failed. Aborting benchmark.")
            sys.exit(1)


if __name__ == "__main__":
    run_benchmark()
