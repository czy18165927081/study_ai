# 命令行背单词工具（vocabtool）

一个用 Python 编写的命令行背单词小工具：随机抽词考中文释义，答错的词自动记入错词本，下次优先重考。项目已完成工程化改造，支持 `python -m` 运行、结构化日志、友好异常处理与类型检查。

- 运行环境：Python 3.9+
- 运行依赖：无第三方库
- 开发依赖：mypy（可选，用于类型检查）

## 功能特性

- 随机抽词测验，默认 10 题，题数可配置。
- 优先重考错词本中答错次数多的单词，再随机补足新词。
- 自动记录错词：累计答错次数（`times`）并更新最近答错时间（`time`）。
- 判分时忽略大小写与首尾空格，避免格式差异导致的误判。
- `--report` 模式查看错词 TOP5，不触发测验。
- 写错词本前自动备份为 `wrong.csv.bak`，防止数据丢失。
- 词库缺失、空词库、坏行等异常均记录日志并优雅退出，不崩溃。

## 快速开始

在项目根目录（`vocab-tool/`）执行：

```bash
# 1. 安装为可编辑包（首次或代码变动后）
pip install -e .

# 2. 开始测验（默认 10 题）
python -m vocabtool --count 10

# 3. 查看错词榜
python -m vocabtool --report
```

终端交互示例：

```
$ python -m vocabtool --count 3
annual 的中文意思是？ 年度的
✓ 正确
artificial 的中文意思是？ 人工的
✗ 答错了，正确答案是：人造的
```

## 命令行参数

| 参数         | 类型   | 默认值                | 说明               |
| ---------- | ---- | ------------------ | ---------------- |
| `--count`  | int  | `10`               | 本次测验的题目数量        |
| `--book`   | str  | `<项目目录>/vocab.csv` | 词库文件路径           |
| `--report` | flag | 关闭                 | 仅打印错词 TOP5，不进入测验 |

用法示例：

```bash
python -m vocabtool --count 5                    # 考 5 题
python -m vocabtool --book ./my_words.csv        # 使用自定义词库
python -m vocabtool --report                     # 查看错词 TOP5
```

## 数据文件

**词库 `vocab.csv`**：两列，首行为表头，UTF-8 编码（兼容 BOM）。

```csv
word,meaning
abandon,放弃
able,能够的
absolute,绝对的
```

**错词本 `wrong.csv`**：三列，首次答错后自动生成。

```csv
word,times,time
annual,1,2026-11-18 14:18:15
artificial,2,2026-11-18 22:03:28
```

- `times`：累计答错次数，决定重考优先级。
- `time`：最近一次答错时间。

文件按 `times` 降序写入。每次写盘前先复制为 `wrong.csv.bak`。

## 项目结构

```
vocab-tool/
├── pyproject.toml           # 包元数据，支持 pip install -e .
├── run.py                   # 兼容入口（推荐用 python -m vocabtool）

├── vocab.csv                # 词库（word,meaning）
├── wrong.csv                # 错词本（word,times,time）
├── .gitignore               # 忽略缓存、日志与备份文件
├── logs/
│   └── app.log              # 运行日志（INFO/WARNING）
└── src/
    └── vocabtool/
        ├── __init__.py      # 包标识与版本号
        ├── __main__.py      # python -m 入口
        ├── storage.py       # 词库/错词本读写、备份
        ├── quiz.py          # 出题、判分、错词记录
        └── cli.py           # 参数解析与入口
```

## 模块职责

| 模块            | 主要函数                                       | 职责               |
| ------------- | ------------------------------------------ | ---------------- |
| `storage.py`  | `load_words` / `load_wrong` / `save_wrong` | 数据读写、异常提示、备份     |
| `quiz.py`     | `quiz` / `record_wrong`                    | 抽词、判分、错词累计       |
| `cli.py`      | `main` / `report`                          | 参数解析、日志配置、错词榜展示  |
| `__main__.py` | —                                          | 转发到 `cli.main()` |

依赖方向严格单向：`cli → quiz → storage`，无循环导入。

## 健壮性与日志

异常场景统一记录到 `logs/app.log`，不中断程序：

- 词库文件不存在：`WARNING`，本次无题目，正常退出。
- 词库为空或无有效行：`WARNING`，正常退出。
- CSV 坏行（缺字段）：带行号记 `WARNING`，跳过该行。
- 写错词本失败等 IO 异常：`ERROR`。

正常运行时记录 `INFO`：本次题数、答对数、错词数、正确率，以及错词本备份路径。

题目与判分结果仍输出到终端，运行信息收口到 logging，两者不混用。

## 开发检查

```bash
pip install mypy
mypy src/
# 预期：Success: no issues found in 5 source files
```

所有关键函数均带类型注解，数据文件路径通过 `Path(__file__).resolve().parents[2]` 定位，因此从任意工作目录运行都能正确找到数据文件。

## 兼容旧入口

W2 的单脚本入口 `run.py` 保留为兼容转发层，功能与 `python -m vocabtool` 一致：

```bash
python run.py --count 10
python run.py --report
```

推荐统一使用 `python -m vocabtool`。
