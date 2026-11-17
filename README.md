# Git 学习笔记 · py-toolkit

> M1 W1 产出。主线：GeekHour《一小时 Git》+ Pro Git 中文第 1–2 章。
> 目标：跨过"会敲命令"到"讲得清原理"那道坎。

---

## 一、三区模型（最核心）

Git 的所有操作，本质都是文件在三个区域之间流动。

| 区域 | 英文 | 位置 | 作用 |
|---|---|---|---|
| 工作区 | Working Directory | 你看到的文件夹 | 直接编辑文件 |
| 暂存区 | Staging Area / Index | `.git/index` | 挑出本次要提交的改动 |
| 本地仓库 | Repository | `.git/objects` | 存放永久提交快照 |

流转方向：

```
工作区 --git add--> 暂存区 --git commit--> 本地仓库 --git push--> 远程仓库
   ^                   ^                    ^
   |--git restore------|                    |
                       |--git restore --staged
                                            |--git pull / clone
```

**为什么要暂存区**：可以一次改 5 个文件，只提交其中 2 个。没有它，每次改动都必须全量提交。

## 二、文件的四种状态

- **untracked（未跟踪）**：新文件，Git 从未见过。显示 `??`
- **modified（已修改）**：跟踪过的文件被改了，但没 `add`
- **staged（已暂存）**：`add` 过，等待 `commit`
- **committed（已提交）**：已存入本地仓库

查看命令：
```bash
git status        # 完整状态
git status -s     # 简写：?? 未跟踪 / M 修改 / A 新增暂存
```

## 三、四板斧（从零建库到推送）

```bash
# 1. 初始化
git init
# 2. 配置身份（首次必做，全局生效）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
# 3. 提交
git add <file>            # 或 git add . 提交全部
git commit -m "说明这次改了什么"
# 4. 推送
git remote add origin <仓库地址>     # 首次关联远程
git push -u origin main             # -u 记住上游，以后直接 git push
```

**commit 与 push 的区别**（高频面试题）：
- `commit` 把改动存入**本地仓库**，断网也能做，别人看不到。
- `push` 把本地提交**上传到远程仓库**，别人才能看到。
- 顺序：先有 commit，才有东西可 push。

## 四、分支（branch 解决什么）

**一句话**：分支让你可以开一条独立的工作线改东西，不污染主线。

```
main:     A --- B --- C ----------- M (合并点)
                   \             /
feat/readme:        D --- E -----
```

- `HEAD`：指向当前所在分支的指针。切换分支 = 移动 HEAD。
- `git switch -c feat/readme`：新建并切到分支（`-c` = create）
- `git switch main`：切回主线
- `git merge feat/readme`：把 feat 的改动合并进当前分支

**合并的两种方式**：
- **快进（fast-forward）**：main 没有新提交，直接把指针前移，无合并节点。
- **三方合并**：两边都改过，Git 生成一个新合并提交。

**为什么不用裸 Chain / 为什么不直接在 main 上改**：分支提供隔离——改动出错可丢弃整条分支，主线始终可用。

## 五、回滚与恢复

| 场景 | 命令 | 作用 |
|---|---|---|
| 改坏了工作区文件，想还原 | `git restore <file>` | 用暂存区/仓库版本覆盖工作区 |
| 已 add，想撤回到未暂存 | `git restore --staged <file>` | 从暂存区移回工作区 |
| 改了最近一次 commit 的说明 | `git commit --amend` | 改写最后一次提交 |
| 完全回退到某个提交 | `git reset --hard <commit>` | 危险：丢弃之后所有改动 |

**存档点理解**：commit 是存档。周三故意改坏 `hello.py` 后用 `git restore` 救回，靠的就是上一次 commit 里的完好版本。

## 六、远程协作

```bash
git clone <地址>          # 第一次把远程仓库整个搬到本地
git remote -v             # 查看已关联的远程
git pull                  # 拉取远程并合并到本地（= fetch + merge）
git push                  # 推送本地提交到远程
```

**HTTPS 推送注意**：GitHub 已不接受账号密码，需生成 Personal Access Token（PAT）填入。

## 七、.gitignore

告诉 Git 哪些文件**永不纳入版本控制**。

当前 py-toolkit 的配置：
```
__pycache__/    # Python 编译缓存，可随时重建，提交只会制造噪音
.env            # 放密钥/密码，提交会泄露凭据
```

**坑**：只对**未跟踪**文件生效。文件已被跟踪后再写进 .gitignore 无效，需：
```bash
git rm -r --cached __pycache__
```

推送前自查密钥：`git log -p | grep sk-`

## 八、命令速查

| 命令 | 作用 |
|---|---|
| `git init` | 初始化仓库 |
| `git status` | 查看状态 |
| `git add .` | 全部改动放入暂存区 |
| `git add -N <file>` | 登记新文件意图，使 `git diff` 可见（不实际暂存） |
| `git commit -m "..."` | 提交 |
| `git log --oneline` | 单行历史 |
| `git log --oneline --graph --all` | 分支拓扑图 |
| `git diff` | 查看未暂存的改动 |
| `git switch -c <name>` | 新建并切换分支 |
| `git merge <branch>` | 合并分支 |
| `git restore <file>` | 丢弃工作区改动 |
| `git push -u origin main` | 首次推送并设置上游 |

## 九、自测题（M1 考卷节选）

1. 工作区 / 暂存区 / 仓库区分别是什么，文件怎么在三者间流动？
2. branch 解决了什么问题？HEAD 是什么？
3. commit 与 push 的区别？
4. 快进合并与三方合并的区别？
5. 新文件 `git diff` 为什么没输出？怎么让它显示？
6. 15 分钟内从零建库 → 提交 → 推送（不查资料）。

---

状态：M1 W1 学习中 · 持续更新
