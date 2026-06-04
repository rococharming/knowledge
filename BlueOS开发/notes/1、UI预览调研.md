
前端框架：

对应仓库：system_core_app_fwk_ui_frontend

指责：负责把开发者写的代码翻译成渲染引擎能理解的指令。

例如，开发者写：

```text
<template>
  <text>Hello World</text>
</template>
```

通过 JS 框架编译翻译，渲染引擎收到：创建一个 Text 组件，内容是 'Hello World'，位置在 x=100, y=200。

整体流程总结：

1. 开发者写快应用代码
2. 打包成 .rpk 文件
3. 手表/手机打开快应用
4. frontend（JS框架）解析代码，生成指令
5. ui（渲染引擎）收到指令，执行 Measure -> Layout -> Paint
6. 用户在屏幕上看到界面
7. 用户点击按钮 -> 事件传回 JS 框架 -> 更新页面 -> 回到步骤4


单独的 ui_element 仓库：有些组件太复杂了，不能只靠渲染引擎来管。
