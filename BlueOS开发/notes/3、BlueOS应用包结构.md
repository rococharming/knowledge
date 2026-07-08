# 一、整体结论

BlueOS Studio 中一个应用从开发到运行，通常会经历下面几层形态：

```text
源码工程 src/
  ↓ 编译
build/<deviceType>/
  ↓ 打包
dist/<deviceType>/<debug|release>/*.rpk
  ↓ 安装/运行读取
<package>.vru
```

可以简单理解为：

- `src/`：开发者写的源码。
- `build/foldable`：按设备类型编译后的多文件中间产物。
- `.rpk`：用于分发、上传、安装的外层包。
- `.vru`：运行时更偏好的单文件资源联合包。


---

## 二、源码应用是什么

BlueOS Studio 中开发的“应用”，本质是一个源码工程。例如源码目录通常包含：

```text
src/
  manifest.json
  app.ux
  assets/
  pages/
    Demo/
      index.ux
    DemoDetail/
      index.ux
```

### 1. manifest.json

`src/manifest.json` 描述应用元信息和运行配置，例如：

```json
{
  "package": "com.blueos.launcher",
  "name": "demo",
  "versionName": "1.0.0",
  "versionCode": 1,
  "deviceTypeList": [
    "foldable"
  ],
  "config": {
    "designWidth": 466
  },
  "router": {
    "entry": "pages/Demo",
    "pages": {
      "pages/Demo": {
        "component": "index"
      },
      "pages/DemoDetail": {
        "component": "index"
      }
    }
  },
  "display": {
    "backgroundColor": "#ffffff"
  }
}
```

其中几个关键字段：

| 字段                        | 含义                                          |
| ------------------------- | ------------------------------------------- |
| `package`                 | 应用包名，安装和运行时的唯一标识                            |
| `deviceTypeList`          | 指定生成哪些设备类型的构建产物，例如 `foldable`、`watch-round` |
| `config.designWidth`      | 页面设计宽度，用于布局单位换算                             |
| `router.entry`            | 应用入口页面                                      |
| `router.pages`            | 应用内页面列表                                     |
| `display.backgroundColor` | 默认窗口/页面背景色                                  |

### 2. .ux 是什么格式

`.ux` 是 BlueOS 快应用的单文件组件源码格式，类似 Vue SFC。一个 `.ux` 文件通常包含三段：

```ux
<script>
  // 页面逻辑
</script>

<template>
  // 页面结构
</template>

<style lang="scss">
  // 页面样式
</style>
```

例如 `src/pages/Demo/index.ux`：

```ux
<script>
  import router from '@blueos.app.appmanager.router'

  export default {
    data: {
      title: '欢迎体验应用开发'
    },

    onInit() {},

    onDetailBtnClick() {
      router.push({
        uri: '/pages/DemoDetail'
      })
    }
  }
</script>

<template>
  <div class="wrapper">
    <text class="title">{{ title }}</text>
    <input
      class="btn"
      type="button"
      value="跳转到详情页"
      onclick="onDetailBtnClick"
    />
  </div>
</template>

<style lang="scss">
@import './../../assets/styles/style.scss';

.wrapper {
  .title {
    color: $black;
  }
}
</style>
```

`.ux` 是开发态格式，便于开发者把逻辑、结构、样式写在一个文件里。但设备运行时不直接解析 `.ux`，而是运行编译后的产物。

---

## 三、build/foldable 是什么

`build/foldable` 是根据 `manifest.json` 中 `deviceTypeList` 生成的设备类型构建目录。

如果 `deviceTypeList` 中有：

```json
"deviceTypeList": [
  "foldable"
]
```

编译后就会生成：

```text
build/foldable/
```

如果同时支持手表设备，也可能出现：

```text
build/watch-round/
```

### 1. build 目录是中间产物

`build/foldable` 不是最终上传包，而是编译后的多文件目录。样例结构如下：

```text
build/foldable/
  app.js
  app.js.map
  app.snapshot
  app.css.json
  manifest.json
  packageInfo.json
  assets/
    images/
      logo.png
  pages/
    Demo/
      index.js
      index.js.map
      index.snapshot
      index.template.json
      index.css.json
    DemoDetail/
      index.js
      index.js.map
      index.snapshot
      index.template.json
      index.css.json
```

### 2. 为什么源码是 .ux，build 里变成 .js 和 json

`.ux` 会被编译拆分：

```text
index.ux
  ├── <script>   -> index.js
  ├── JS 编译结果 -> index.snapshot
  ├── <template> -> index.template.json
  └── <style>    -> index.css.json
```

对应关系：

| 源码片段         | build 产物              | 用途                           |
| ------------ | --------------------- | ---------------------------- |
| `<script>`   | `index.js`            | 页面逻辑、data、生命周期、事件处理          |
| JS 编译结果       | `index.snapshot`      | JS 预编译快照/字节码类产物，用于减少运行时解析和编译成本 |
| `<template>` | `index.template.json` | UI 节点树，描述 div/text/input 等结构 |
| `<style>`    | `index.css.json`      | 编译后的样式规则                     |

这样做的原因：

1. `.ux` 适合开发者书写，不适合设备运行时直接解析。
2. JS 引擎只负责执行逻辑代码，所以 `<script>` 被编译为 `.js`。
3. `.snapshot` 是把 JS 进一步预处理后的快照/字节码类文件。运行时如果支持并命中 snapshot，可以少做 JS 源码解析、语法分析和编译，从而提升启动和页面加载速度。
4. UI 渲染引擎更适合消费结构化数据，所以 `<template>` 和 `<style>` 被编译为 JSON。
5. 编译阶段可以提前处理 SCSS、变量、mixin、事件绑定、模板表达式等。
6. 运行时读取 build 产物或 vru 内条目即可，不需要再做源码编译。

### 3. .snapshot 的作用

`.snapshot` 可以理解为 JS 文件的“预编译结果”。

以页面为例：

```text
pages/Demo/index.js        # 可读的 JS 逻辑代码
pages/Demo/index.snapshot  # index.js 对应的预编译快照/字节码类产物
```

运行时有两种可能：

```text
没有 snapshot：
  读取 index.js
    ↓
  JS 引擎解析源码
    ↓
  编译为可执行形式
    ↓
  执行页面逻辑

有 snapshot：
  读取 index.snapshot
    ↓
  JS 引擎直接加载预编译结果
    ↓
  执行页面逻辑
```

所以 `.snapshot` 的主要价值是：

- 减少运行时解析 JS 源码的成本。
- 缩短应用启动或页面加载耗时。
- 降低低性能设备上的 CPU 开销。
- 和 `.vru` 配合后，可以把 JS、模板、样式、图片、snapshot 都放进一个单文件资源包中读取。

需要注意：`.snapshot` 不是业务源码，也不是页面模板；它是给 JS 运行时使用的优化产物。开发者通常看 `.ux` 和 `.js`，运行时会优先利用 `.snapshot` 来提升加载性能。

### 4. build/manifest.json 与 src/manifest.json 的差异

`build/foldable/manifest.json` 一般来自 `src/manifest.json`，但会经过工具链标准化和补充。

例如样例中：

- 源码中 feature 是 `blueos.app.appmanager.router`
- build 后变成 `system.router`
- build manifest 额外补充了 `debug`、`distrubuteRules`、`minPlatformVersion` 等字段

所以 `build/foldable` 是“某个设备类型下，已经可以被运行时消费的多文件应用目录”。

---

## 四、rpk 是什么

`.rpk` 是打包后的分发包，通常位于：

```text
dist/<deviceType>/debug/*.rpk
dist/<deviceType>/release/*.rpk
```

例如：

```text
dist/foldable/debug/com.blueos.launcher.debug.development.1.0.0.rpk
```

### 1. rpk 是外层分发容器

实际检查样例 `.rpk`，它是 zip 包：

```text
Zip archive data
```

解包后结构类似：

```text
META-INF/
  CERT
  build.txt
logo.png
manifest.json
com.blueos.launcher.vru
```

因此 `.rpk` 的主要职责是：

- 用于开放平台上传和设备安装。
- 承载签名、证书、构建信息。
- 承载外层 `manifest.json`，用于安装解析。
- 承载应用运行资源。运行资源可以是多文件，也可以被收拢为 `.vru`。

### 2. debug 与 release

常见路径：

```text
dist/foldable/debug/
dist/foldable/release/
```

区别通常包括：

| 类型 | 特点 |
| --- | --- |
| debug | 用于开发调试，构建信息中会体现 debug 环境 |
| release | 用于正式分发，需要正式签名信息 |

BlueOS Studio 中点击“打包”时，可以选择：

- 包类型：`debug` 或 `release`
- 环境变量：`production`、`development`、`test`

环境变量用于区分接口环境或运行配置，不需要手动修改业务代码。

---

## 五、vru 是什么



`.vru` 是 BlueOS 快应用运行时使用的资源联合文件。它不是 zip，而是自定义格式。

样例 `.vru` 文件头可看到：

```text
vivo union file
```

`.vru` 可以理解成“把很多文件装进一个大文件里，并在文件开头放了一张目录表”。

比如原来 `build/foldable` 里是很多散文件：

```
app.js
manifest.json
pages/Demo/index.js
pages/Demo/index.template.json
pages/Demo/index.css.json
assets/images/logo.png
```

打成 `.vru` 后，磁盘上只剩一个大文件：

```
com.blueos.launcher.vru
```

但运行时仍然想按原来的路径读取：

```
pages/Demo/index.template.json
```

所以 `.vru` 里面必须有一张“目录表”，大概像这样：

|文件路径|在 vru 文件中的起始位置 offset|内容长度 len|
|---|---|---|
|`manifest.json`|1024|665|
|`app.js`|1689|520|
|`app.snapshot`|2209|700|
|`pages/Demo/index.js`|2909|1800|
|`pages/Demo/index.template.json`|4709|900|
|`pages/Demo/index.css.json`|5609|600|
|`pages/Demo/index.snapshot`|6209|800|
|`assets/images/logo.png`|7009|1659|

样例 `com.blueos.launcher.vru` 内部包含：

```text
app.js
app.js.map
app.snapshot
assets/images/logo.png
manifest.json
packageInfo.json
pages/Demo/index.css.json
pages/Demo/index.js
pages/Demo/index.js.map
pages/Demo/index.snapshot
pages/Demo/index.template.json
pages/DemoDetail/index.css.json
pages/DemoDetail/index.js
pages/DemoDetail/index.js.map
pages/DemoDetail/index.snapshot
pages/DemoDetail/index.template.json
```

这里的 `.snapshot` 和 `.js` 是同一段逻辑的两种运行形态：

- `.js`：源码级 JS，便于调试、回退和兼容。
- `.snapshot`：JS 的预编译结果，运行时加载更快。

`.vru` 会把 `.js`、`.snapshot`、`.template.json`、`.css.json`、图片等资源一起合并进去。运行时按逻辑路径读取资源时，如果要加载页面逻辑，可能读取 `pages/Demo/index.snapshot`；如果要构建 UI 树，则读取 `pages/Demo/index.template.json`；如果要应用样式，则读取 `pages/Demo/index.css.json`。


### 2. 为什么手表更需要 vru

手表设备通常有两个限制：

1. 文件句柄数量有限。
2. 大量小文件随机读取性能差。

如果运行时直接读取多文件目录，每个页面、样式、模板、图片、snapshot 都可能触发文件打开和读取。

如果运行时统一读取 `.vru`：

- 文件数量显著减少。
- 句柄占用更可控。
- 可以缓存 `.vru` 文件句柄和索引表。
- 运行时读取路径稳定：逻辑上仍然按文件路径读，物理上从 `.vru` 取。

---

## 六、安装与运行时读取链路

### 1. 安装 rpk

PMS 安装 `.rpk` 的流程大致是：

```text
install(rpk_path)
  ↓
检查 rpk 文件是否存在
  ↓
创建 install_tmp 临时目录
  ↓
校验 rpk 签名
  ↓
解压 rpk 到临时目录
  ↓
查找 .vru
  ↓
读取 manifest
  ↓
校验版本、证书、平台能力
  ↓
停止旧应用
  ↓
移动临时目录到安装目录
  ↓
更新应用数据库
```

关键代码路径：

```text
system/core/app_fwk/pkgmgr/src/installer/installer_manager.rs
```

安装过程中会查找 `.vru`：

```rust
let vru_file_path = AppArchiveUtil::find_package_vru_file(&self.extract_tmp_path_);
```

如果不是 native app 且没有 `.vru`，当前代码会把它标记为 quickapp 散文件模式：

```rust
if !item.is_native_app() && vru_file_path.is_none() {
    item.inner.quickapp_ = 1;
}
```

这说明 `.vru` 是否存在会影响运行时模式。

### 2. 预置应用扫描

预置路径扫描中也有类似逻辑：

```rust
app_item.inner.quickapp_ = if Self::find_package_vru_file(&entry_path).is_none() {
    1
} else {
    0
};
```

也就是说：

- 包目录内有 `.vru`：按 vru 资源形态处理。
- 包目录内没有 `.vru`：按 quickapp 多文件形态处理。

这也是之前无 `.vru` 时出现 `fitScreen`、默认 titlebar 等表现差异的根源。

### 3. 运行时读取资源

UI 运行时读取资源时，会进入：

```text
system/core/app_fwk/ui/common/file_utils/file_ops.rs
```

核心调用：

```rust
VruManager::get_instance().read_file(file, false)
```

`VruManager` 会根据逻辑路径解析出：

```text
install_dir
package
item_path
```

然后拼出：

```text
<install_dir>/<package>/<package>.vru
```

如果 `.vru` 存在，就从 `.vru` 中读取对应条目；如果 `.vru` 不存在，则退回普通文件读取。

---

## 七、rpk 与 vru 的关系

两者不是同一个层次：

| 对象 | 定位 | 是否 zip | 主要使用阶段 |
| --- | --- | --- | --- |
| `.rpk` | 分发/安装包 | 是，外层 zip | 上传、签名校验、安装 |
| `.vru` | 运行资源联合包 | 否，自定义 union file | 运行时资源读取 |

`.rpk` 可以包含 `.vru`。

`.vru` 可以理解为 `.rpk` 内部的运行资源主体。
