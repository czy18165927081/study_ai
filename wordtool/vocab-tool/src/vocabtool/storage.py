"""词汇数据的读写与备份。"""
import csv
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def load_words(path: Path) -> dict[str, str]:
    """读词库，返回 {word: meaning}。文件缺失/空词库返回空字典。"""
    if not path.exists():
        logger.warning("词库文件不存在：%s", path)
        return {}
    word_map: dict[str, str] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for lineno, row in enumerate(csv.DictReader(f), start=2):
            word = (row.get("word") or "").strip()
            meaning = (row.get("meaning") or "").strip()
            if not word or not meaning:
                logger.warning("第 %d 行数据不完整，已跳过", lineno)
                continue
            word_map[word] = meaning
    if not word_map:
        logger.warning("词库为空或没有有效数据行：%s", path)
    return word_map


def load_wrong(path: Path) -> list[dict[str, str]]:
    """读错词本；文件不存在返回空列表。"""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_wrong(wrong_dict: dict[str, dict[str, str]], path: Path) -> None:
    """写错词本；写前先备份为 wrong.csv.bak。"""
    if path.exists():
        backup = path.with_name(path.name + ".bak")
        shutil.copy2(path, backup)
        logger.info("已备份错词本：%s", backup)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["word", "times", "time"])
        writer.writeheader()
        for r in sorted(wrong_dict.values(), key=lambda x: int(x["times"]), reverse=True):
            writer.writerow(r)
