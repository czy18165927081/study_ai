"""命令行入口。"""
import argparse
import logging
import os
from pathlib import Path

from .quiz import quiz
from .storage import load_words, load_wrong

logger = logging.getLogger(__name__)

BASE = Path(__file__).resolve().parents[2]  # -> vocab-tool/（数据文件所在目录）
WRONG = BASE / "wrong.csv"


def report(wrong_rows: list[dict[str, str]], top: int = 5) -> None:
    """打印错词 TOP N。"""
    if not wrong_rows:
        print("还没有错词记录")
        return
    for r in wrong_rows[:top]:
        print(f"{r['word']}  错 {r['times']} 次  最近 {r['time']}")


def main() -> None:
    os.makedirs(BASE / "logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        filename=BASE / "logs" / "app.log",
        filemode="a",
        encoding="utf-8",
    )

    parser = argparse.ArgumentParser(description="命令行背单词工具")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--book", default=str(BASE / "vocab.csv"))
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    word_map = load_words(Path(args.book))
    if not word_map:
        return
    wrong_rows = load_wrong(WRONG)

    if args.report:
        report(wrong_rows)
        return

    quiz(word_map, wrong_rows, args.count, WRONG)


if __name__ == "__main__":
    main()
