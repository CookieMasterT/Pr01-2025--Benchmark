import os
import shutil
from pathlib import Path
import random
from logger_factory import LoggerFactory

sizes = [100, 5_000, 10_000, 15_000]

data_dir = Path(__file__).resolve().parents[1] / "data"
logger = LoggerFactory.get_logger("runners.createData")


def createdata() -> None:
    shutil.rmtree(data_dir, ignore_errors=True)
    os.makedirs(data_dir, exist_ok=True)
    logger.info(f"Creating data files of the following sizes: [{",".join(str(_) for _ in sizes)}]")
    for size in sizes:
        array = [str(random.randint(0, 1_000)) for _ in range(size)]

        file_path = data_dir / f"{size}.csv"

        with open(file_path, "w") as f:
            f.write(";".join(array))


if __name__ == "__main__":
    createdata()
