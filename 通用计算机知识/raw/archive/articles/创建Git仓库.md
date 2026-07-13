# 一、Git 仓库

`Git` 仓库，也称为版本库，英文是`repository`，简称`repo`。

一个普通目录执行`git init`之后，会生成一个隐藏目录`.git`。这个`.git`目录保存了`Git`管理仓库所需的元数据、对象数据和历史信息。正是因为有了 `.git` 目录，当前目录才成为一个 Git 仓库。

`Git` 仓库中的文件并不会自动全部进入版本控制。文件是否被 Git 追踪，取决于是否被加入过暂存区并提交到版本历史中。此外，被`.gitignore`忽略的文件或目录也不会被加入版本控制。

创建 Git 仓库通常有两种方式：

|方式|命令|适合场景|
|---|---|---|
|本地初始化仓库|`git init`|从本地目录开始创建新项目|
|克隆远程仓库|`git clone <URL>`|把已有远程仓库复制到本地|

# 二、本地初始化仓库

## 1、创建项目目录

```shell
mkdir learngit
cd learngit
```

此时 `learngit` 只是一个普通目录，还不是 Git 仓库。

## 2、初始化仓库

在项目目录中执行：

```shell
git init
```

执行后，Git 会在当前目录中初始化一个本地仓库。

可能看到类似输出：

```shell
Initialized empty Git repository in xxx/learngit/.git/
```

查看目录内容：

```shell
ls -a
```

会看到多出一个隐藏目录：

![[assets/Pasted image 20260605000953.png|400]]

`.git` 目录就是当前仓库的核心目录。

## 3、在已有内容的目录中初始化仓库

`git init` 不要求目录必须是空的。也可以在一个已经有文件的目录中执行：

```shell
git init
```

这不会删除原有文件，只是会在当前目录下创建 `.git` 目录，让 Git 开始管理这个目录。

不过，执行 `git init` 之后，目录中的已有文件不会自动进入版本历史。它们还需要经过暂存和提交：

```shell
git add
git commit
```

才会真正成为 Git 提交记录的一部分。

# 三、初始分支名称

## 1、默认初始分支

执行 `git init` 时，Git 会创建一个初始分支。

在较早的 Git 版本或某些配置中，可能会看到类似提示：

```shell
hint: Using 'master' as the name for the initial branch...
```

这表示当前仓库的初始分支名是 `master`。

现在很多项目和代码托管平台更常使用 `main` 作为默认分支名。可以提前设置以后新仓库的默认初始分支：

```shell
git config --global init.defaultBranch main
```

查看配置是否生效：

```shell
git config --global init.defaultBranch
```

如果输出：

```shell
main
```

说明以后执行 `git init` 创建的新仓库，默认初始分支会使用 `main`。

## 2、重命名当前分支

如果当前分支已经创建好，想重命名当前分支，可以执行：

```shell
git branch -m xxx
```

例如，当前分支名为`master`，想重命名为`main`：

```shell
git branch -m main
```

或者：

```shell
git branch -M main
```

如果想把指定分支 `master` 重命名为 `main`，可以写得更明确：

```shell
git branch -m master main
```

两条命令的区别是：

| 命令                          | 含义                          |
| --------------------------- | --------------------------- |
| `git branch -m main`        | 把当前所在分支重命名为 `main`          |
| `git branch -m master main` | 把名为 `master` 的分支重命名为 `main` |
如果仓库还没有推送到远程仓库，重命名本地分支比较简单。

如果仓库已经推送到远程仓库，改名后还需要处理远程分支、上游分支和远程平台的默认分支设置。这部分放到远程仓库章节再讲。


# 四、.git目录

## 1、.git目录的作用

执行 `git init` 后，当前目录下会生成 `.git` 目录。

`.git` 是 Git 仓库的核心目录，用来保存当前仓库的内部数据，例如：

| 内容     | 说明                  |
| ------ | ------------------- |
| 提交对象   | 保存提交历史相关数据          |
| 分支信息   | 保存分支引用              |
| 标签信息   | 保存标签引用              |
| 暂存区信息  | 保存 `git add` 后的索引状态 |
| `HEAD` | 记录当前所在分支或提交         |
| 仓库配置   | 保存当前仓库的本地配置         |
一般不要手动修改 `.git` 目录中的内容，否则可能导致仓库状态异常。

## 2、删除.git目录的影响

如果删除 `.git` 目录：

```shell
rm -rf .git
```

当前目录就不再是 Git 仓库。也就是说，项目文件本身还在，但 Git 版本管理信息没有了。

# 五、仓库状态检查

## 1、查看当前目录是否是 Git 仓库

可以使用：

```shell
git status
```

如果当前目录是 Git 仓库，会看到类似输出：

```text
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

这表示当前目录已经是 Git 仓库，但还没有提交记录。

如果当前目录不是 Git 仓库，可能会看到：

```text
fatal: not a git repository (or any of the parent directories): .git
```

这表示 Git 在当前目录以及上级目录中没有找到 `.git` 目录。

## 2、Git 会向上查找.git目录

在 Git 仓库的子目录中执行 `git status`，也能正常工作。

例如目录结构如下：

```shell
learngit/
  ├── .git/
  └── src/
      └── main.rs
```

即使当前位于 `src` 目录中：

```shell
cd src
git status
```

Git 也会向上级目录查找 `.git`，找到 `learngit/.git` 后，就知道当前仍然处于 `learngit` 这个仓库中。

这也是为什么错误信息中会出现：

```shell
or any of the parent directories
```

它表示 Git 不只检查当前目录，也会检查上级目录。


# 六、.gitignore文件

## 1、忽略文件的作用

项目中经常会有一些不适合提交到仓库的文件，例如：

|文件类型|示例|
|---|---|
|编译产物|`target/`、`dist/`、`build/`|
|依赖目录|`node_modules/`|
|日志文件|`*.log`|
|临时文件|`.DS_Store`|
|本地环境配置|`.env`|
这些文件或目录可以写入 `.gitignore`。

```gitignore
.DS_Store
*.log
target/
node_modules/
.env
```

被 `.gitignore` 匹配的文件，默认不会出现在 `git status` 的未跟踪文件列表中，也不会被普通的 `git add .` 加入暂存区。

## 2、.gitignore只影响未跟踪文件

`.gitignore` 主要影响尚未被 Git 跟踪的文件。

如果某个文件已经被 Git 跟踪，之后再把它写入 `.gitignore`，Git 仍然会继续跟踪它的变化。

例如：

config.json 已经被提交过
  ↓
后来把 config.json 写入 .gitignore
  ↓
Git 仍然会继续跟踪 config.json 的修改

这是因为 `.gitignore` 不是取消跟踪规则，而是**忽略未跟踪文件的规则**。

如果要让一个已经被跟踪的文件停止被 Git 跟踪，需要从索引中移除它：

```shell
git rm --cached config.json
```

这条命令会让 Git 不再跟踪 `config.json`，但保留工作区中的文件本身。


# 七、克隆远程仓库

## 1、克隆仓库

除了在本地执行 `git init` 创建仓库，也可以把一个已经存在的远程仓库复制到本地。

使用：

```shell
git clone <远程仓库URL>
```

例如：

```shell
git clone https://github.com/user/repo.git
```

执行后，Git 会在当前目录下创建一个名为 `repo` 的目录，并把远程仓库复制到本地。

克隆完成后进入仓库目录：

```shell
cd repo
```

查看状态：

```shell
git status
```


## 2、git clone做了哪些事

执行 `git clone` 时，Git 会自动完成多步操作：

1. 创建本地目录（默认使用远程仓库名作为目录名）
2. 下载项目文件（获取远程仓库中的文件内容）
3. 下载提交历史（获取远程仓库已有提交记录）
4. 初始化.git（在本地创建完整 Git 仓库）
5. 获取分支和标签（保存远程分支、标签等引用信息）
6. 添加远程别名（默认添加名为 `origin` 的远程仓库别名）

所以 `git clone` 不是简单下载代码压缩包，它会把远程仓库的 Git 历史和仓库信息一并复制到本地。


## 3、自定义克隆目录名

默认情况下，Git 会使用远程仓库名作为本地目录名。

例如：

```shell
git clone https://github.com/user/repo.git
```

会生成：

```
repo/
```

如果想指定本地目录名，可以在 URL 后面追加目录名：


```shell
git clone https://github.com/user/repo.git my-project
```

这样会生成：

```
my-project/
```

## 4、查看远程仓库地址

克隆完成后，可以查看当前仓库关联的远程地址：

```shell
git remote -v
```

输出类似：

```shell
origin  https://github.com/user/repo.git (fetch)
origin  https://github.com/user/repo.git (push)
```

其中：

| 内容       | 说明              |
| -------- | --------------- |
| `origin` | 远程仓库的默认别名       |
| `fetch`  | 从远程仓库获取数据时使用的地址 |
| `push`   | 向远程仓库推送数据时使用的地址 |
这里只需要先知道：`origin` 是 Git 给克隆来源设置的默认远程仓库名称。后续学习远程仓库时，再详细展开 `origin`、`fetch`、`pull`、`push` 的关系。