# run.py v0.5 —— 健壮版(周五最终形态)
import csv
import random
import argparse
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent          # 修复④:数据文件相对脚本目录定位
VOCAB = BASE / "vocab.csv"
WRONG = BASE / "wrong.csv"


def load_words(path):
    """读词库,返回 {word: meaning};空词库直接提示退出"""
    word_map = {}
    with open(path, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            word_map[row["word"].strip()] = row["meaning"].strip()
    if not word_map:                   # 修复①:空文件检查
        print(f"词库为空或没有数据行:{path}")
        raise SystemExit(1)
    return word_map


def load_wrong(path):
    """读错词;文件不存在返回空列表"""
    if not path.exists():              # 修复②:文件不存在 → 当空
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def record_wrong(word, wrong_dict, now):
    if word in wrong_dict:
        wrong_dict[word]["times"] = str(int(wrong_dict[word]["times"]) + 1)
        wrong_dict[word]["time"] = now
    else:
        wrong_dict[word] = {"word": word, "times": "1", "time": now}


def save_wrong(wrong_dict, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["word", "times", "time"])
        writer.writeheader()
        for r in sorted(wrong_dict.values(), key=lambda x: int(x["times"]), reverse=True):
            writer.writerow(r)


def report(wrong_rows, top=5):
    if not wrong_rows:
        print("还没有错词记录")
        return
    for r in wrong_rows[:top]:
        print(f"{r['word']}  错 {r['times']} 次  最近 {r['time']}")


def quiz(word_map, wrong_rows, count, wrong_path):
    wrong_rows.sort(key=lambda r: int(r["times"]), reverse=True)
    quiz_words = [r["word"] for r in wrong_rows if r["word"] in word_map][:count]
    rest = [w for w in word_map if w not in quiz_words]
    random.shuffle(rest)
    quiz_words += rest[: count - len(quiz_words)]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wrong_dict = {r["word"]: r for r in wrong_rows}
    correct = 0
    for word in quiz_words:
        answer = input(f"{word} 的中文意思是？")
        # 修复③:大小写 + 首尾空格统一归一化后再比较
        if answer.strip().lower() == word_map[word].strip().lower():
            correct += 1
            print("✓ 正确")
        else:
            print(f"✗ 答错了,正确答案是:{word_map[word]}")
            record_wrong(word, wrong_dict, now)

    save_wrong(wrong_dict, wrong_path)
    total = len(quiz_words)
    print(f"\n本次共 {total} 题,答对 {correct} 题,正确率 {correct / total * 100:.0f}%")


def main():
    parser = argparse.ArgumentParser(description="命令行背单词工具")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--book", default=str(VOCAB))
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    word_map = load_words(Path(args.book))
    wrong_rows = load_wrong(WRONG)

    if args.report:
        report(wrong_rows)
        return

    quiz(word_map, wrong_rows, args.count, WRONG)


if __name__ == "__main__":
    main()