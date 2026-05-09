# 一、概述

`OAuth`可以理解成一种**授权别人代你做事，但不把密码告诉别人**。

它解决的核心问题是：

> 我想让一个应用访问我另一个平台上的某些数据或能力，但我不想把那个平台的账号和密码告诉该应用。

例如，你使用某个笔记软件，想让它读取你的 Google Drive 文件。

危险的做法是：

> 笔记软件让你输入 Google 的账号和密码。

这很危险，因为会泄漏自己的信息，同时可能执行很多非法操作。

`OAuth` 的做法时：

1. 笔记软件跳转到 Google 登录页面
2. 你在 Google 页面登录
3. Google 问你：是否允许这个笔记软件读取你的 Google Drive 文件
4. 你点击允许
5. Google 给笔记软件一个访问凭证
6. 笔记软件用这个凭证访问你的部分 Google Drive 数据

整个过程并没有将账号和密码给笔记软件，笔记软件拿到的是一个`Access Token`，也就是访问令牌。

# 二、OAuth 核心角色

`OAuth`里通常有四个角色：

- `Resource Owner`：资源拥有者，也就是你。比如你的 GitHub 仓库、Google Drive 文件、Notion页面等。
- `Client`：客户端/第三方应用，就是想访问你资源的应用。比如一个AI Agent工具想要读取你的 GitHub issue。
- `Authorization Server`：授权服务器，负责验证你是谁，并询问你是否同意授权，例如 Google 登录与授权页面，GitHub OAuth 授权页面。它的职责是确认你本人登录了，问你是否允许第三方应用访问某些权限，发放访问令牌。
- `Resource Server`：资源服务器，即真正存放资源的服务器。例如 Google Drive API、GitHub API。第三方应用最终会拿着访问令牌请求这些 API。

# 三、Access Token

`Access Token` 可以理解为一张临时通信证，它通常有几个特点：

1. 有权限范围

比如只能读取仓库信息、读取读取用户头像和邮箱等。

 2. 有过期时间

Access Token 通常不是永久有效的。有些 token 可能几小时后过期，有些可能更长。过期后，应用需要重新获取，或者用 Refresh Token 刷新。

3. 可以撤销

你可以在 Google、GitHub、Notion 等平台的授权管理页面，把某个第三方应用的权限撤销。撤销之后，这个应用手里的 token 就不能继续用了。