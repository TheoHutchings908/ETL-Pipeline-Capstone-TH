from pathlib import Path
import logging
# using AI assistant 


def setup_logger(name: str,
                 log_file: str,
                 level: int = logging.DEBUG,
                 base_path: Path | str = None) -> logging.Logger:
    if base_path:
        project_root = Path(base_path).resolve()
    else:
        project_root = Path(__file__).resolve().parents[2]
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        fh = logging.FileHandler(log_dir / log_file, encoding="utf-8")
        fh.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger


def log_extract_success(logger: logging.Logger,
                        data_type: str,
                        shape: tuple[int, int],
                        execution_time: float,
                        expected_rate: float) -> None:
    logger.setLevel(logging.INFO)
    logger.info(f"Data extraction successful for {data_type}!")
    logger.info(f"Extracted {shape[0]} rows and {shape[1]} columns")
    logger.info(f"Execution time: {execution_time:.3f} seconds")
    per_row = execution_time / shape[0]
    if per_row <= expected_rate:
        logger.info(f"Execution time per row: {per_row:.6f} seconds")
    else:
        logger.setLevel(logging.WARNING)
        logger.warning(f"Execution time per row ({per_row:.6f}s) exceeds expected rate of {expected_rate:.6f}s")
