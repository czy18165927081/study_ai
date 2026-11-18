# 命令行背单词工具

一个用 Python 写的小工具：随机抽词考中文释义，答错自动记入错词本，下次优先重考。

## 文件结构

```
vocab-tool/
├── pyproject.toml           # 包元数据，支持 pip install -e .
├── run.py                   # 兼容入口（推荐用 python -m vocabtool）
├── vocab.csv                # 词库（word,meaning）
├── wrong.csv                # 错词本（word,times,time）
├── logs/
│   └── app.log              # 运行日志（INFO/WARNING）
└── src/
    └── vocabtool/
        ├── __init__.py      # 包标识
        ├── __main__.py      # python -m 入口
        ├── storage.py       # 词库/错词本读写、备份
        ├── quiz.py          # 出题、判分、错词记录
        └── cli.py           # 参数解析与入口
```

## 环境

Python 3.9+；运行无需第三方库。开发检查需 `pip install mypy`。

## 安装

在项目根目录执行：

    pip install -e .

## 使用方法

随机考 10 题（默认）：

    python -m vocabtool --count 10

指定词库：

    python -m vocabtool --book vocab.csv

只看错词 TOP5：

    python -m vocabtool --report

旧入口仍可用：`python run.py --count 10`

## 健壮性

- 词库缺失、空词库、坏行：记录 WARNING 并跳过，不崩溃。
- 每次写错词本前自动备份为 `wrong.csv.bak`。
- 运行信息输出到 `logs/app.log`；题目交互仍走终端输出。
