"""出题、判分、错词记录。"""
import logging
import random
from datetime import datetime
from pathlib import Path

from .storage import save_wrong

logger = logging.getLogger(__name__)


def record_wrong(word: str, wrong_dict: dict[str, dict[str, str]], now: str) -> None:
    """记录一次答错：已存在则次数 +1 并更新时间，否则新增。"""
    if word in wrong_dict:
        wrong_dict[word]["times"] = str(int(wrong_dict[word]["times"]) + 1)
        wrong_dict[word]["time"] = now
    else:
        wrong_dict[word] = {"word": word, "times": "1", "time": now}


def quiz(
    word_map: dict[str, str],
    wrong_rows: list[dict[str, str]],
    count: int,
    wrong_path: Path,
) -> None:
    """优先重考错词，再随机补足；判分并记录错词。"""
    wrong_rows.sort(key=lambda r: int(r["times"]), reverse=True)
    quiz_words = [r["word"] for r in wrong_rows if r["word"] in word_map][:count]
    rest = [w for w in word_map if w not in quiz_words]
    random.shuffle(rest)
    quiz_words += rest[: count - len(quiz_words)]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wrong_dict = {r["word"]: r for r in wrong_rows}
    correct = 0
    wrong_this_round = 0
    for word in quiz_words:
        answer = input(f"{word} 的中文意思是？")
        if answer.strip().lower() == word_map[word].strip().lower():
            correct += 1
            print("✓ 正确")
        else:
            wrong_this_round += 1
            print(f"✗ 答错了，正确答案是：{word_map[word]}")
            record_wrong(word, wrong_dict, now)

    save_wrong(wrong_dict, wrong_path)
    total = len(quiz_words)
    logger.info(
        "本次共 %d 题，答对 %d 题，错词数 %d，正确率 %.0f%%",
        total,
        correct,
        wrong_this_round,
        correct / total * 100 if total else 0,
    )
