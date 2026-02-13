from __future__ import annotations
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


class LoggerFactory:
    _configured: bool = False
    _format: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    _datefmt: str = "%Y-%m-%d %H-%M-%S"

    _root_level: int = logging.INFO
    _log_to_console: bool = True
    _log_to_file: bool = True
    _log_dir: Path = Path("./logs")
    _default_log_file: str = "app.log"

    @classmethod
    def set_log_path(cls) -> None:
        now = datetime.now()
        now_formatted = now.strftime(cls._datefmt)

        log_filename = f"benchmark {now_formatted}.log"

        current_log_path = cls._log_dir / "current_log.txt"
        with open(current_log_path, "w", encoding="utf-8") as f:
            f.write(log_filename)

    @classmethod
    def configure_once(cls) -> None:
        if cls._configured:
            return

        logging.getLogger().setLevel(cls._root_level)
        cls._configured = True

    @classmethod
    def _get_log_filename(cls) -> str:
        current_log_path = cls._log_dir / "current_log.txt"

        if current_log_path.exists():
            content = current_log_path.read_text(encoding="utf-8").strip()
            if content:
                return content

        return cls._default_log_file

    @classmethod
    def get_logger(cls, name: str, *, level: Optional[str] = None) -> logging.Logger:
        cls.configure_once()

        logger = logging.getLogger(name)

        if level is not None:
            logger.setLevel(getattr(logging, level.upper(), logger.level))

        formatter = logging.Formatter(cls._format, cls._datefmt)
        handlers_added = False

        if cls._log_to_console:
            if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)
                handlers_added = True

        if cls._log_to_file:
            log_dir = cls._log_dir
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file_name = cls._get_log_filename()
            log_file = log_dir / log_file_name

            if not any(
                isinstance(h, logging.FileHandler)
                and Path(h.baseFilename) == log_file
                for h in logger.handlers
            ):
                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
                handlers_added = True

        if handlers_added:
            logger.propagate = False

        return logger
