
问题：

1、UI Preview Runtime 是 BDB 的私有组件，还是仍对外暴露 `uipreviewer` 命令?

作为 `@blueos/bdb` 的私有运行时，只服务于 `bdb preview`。

理由：BDB 与 Preview Runtime 随同一个 npm 版本发布，天然消除版本错配。

2、