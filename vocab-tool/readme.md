# 命令行背单词工具

一个用 Python 写的小工具:随机抽词考中文释义,答错自动记入错词本,下次优先重考。

## 文件结构

- run.py —— 主程序
- vocab.csv —— 词库(word,meaning)
- wrong.csv —— 错词本(word,times,time),首次答错后自动生成

## 环境

Python 3(无需第三方库)

## 使用方法

随机考 10 题(默认):
    python run.py --count 10

指定词库:
    python run.py --book vocab.csv

只看错词 TOP5:
    python run.py --report
