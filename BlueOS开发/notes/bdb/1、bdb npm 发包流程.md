## 1、上游交付本次产物

拿到两类 CI 成功 Job：

- `tools_bdb`：Windows、Linux、macOS arm64、macOS x64 四个 BDB 二进制；
- `rust-ui`：macOS arm64 的完整 uipreviewer Runtime Bundle。

每个 Job 都必须有：

- 对应源码的 40 位 commit SHA；
- GitLab Job ID；
- artifact；
- 同 Job 生成的 `*.provenance.json`，其中包含 artifact 的大小和 SHA-256

## 2、创建发布版本的代码提交

在 npm 仓库，将以下五个 `package.json` 的版本改成同一个新版本，例如 `2.0.0`：

```
package.json
darwin-arm64/package.json
darwin-x64/package.json
linux-x64/package.json
win32-x64/package.json
```

同时更新根 `package.json` 的四个 `optionalDependencies`，让它们也精确指向这个版本。

## 3、准备本次 Release Inputs

先准备依赖：

```shell
npm ci
export GITBLUEOS_TOKEN='你的 GitLab Token'
```

用本次确定的五个 Job ID 生成真实清单：

```shell
node scripts/prepare-release-inputs.js \
  --version=2.0.0 \
  --tools-commit=<tools_bdb 的 40 位 commit> \
  --win-job=<Windows Job ID> \
  --linux-job=<Linux Job ID> \
  --mac-arm-job=<macOS arm64 BDB Job ID> \
  --mac-intel-job=<macOS x64 BDB Job ID> \
  --rust-commit=<rust-ui 的 40 位 commit> \
  --runtime-job=<arm64 Runtime Bundle Job ID>
```

这会生成本地文件：

```
release-inputs.local.json
```

它不应提交到 Git，也不会进入 npm 包。脚本会先确认 Job 确实属于你指定的 commit，再读取 CI 的 provenance 内容。

## 4、下载并组装真实包内容

```shell
npm run sync-binaries
```

成功后应看到五个输入都下载、校验完成。尤其检查：

```
darwin-arm64/preview-runtime/uipreviewer
darwin-arm64/preview-runtime/runtime-manifest.json
```

如果这里报错，停止发布；不要绕过 SHA-256、Job 归属或 Runtime Manifest 校验。

## 5、本地验货

```shell
npm test
npm run verify-packages
```

按顺序发布四个平台发，再发布根包`@blueos/bdb`，都使用 `staging` 标签。根包必须最后发，因为它依赖前四个同版本平台包。


## 6、做一次从 Registry  安装的真实验证

在干净目录安装刚发布的精确版本。

两条都必须成功。后者会实际执行 `npm pack`，并检查：

- 五个包版本是否一致；
- 是否误打进了测试、脚本、`.DS_Store` 等文件；
- 二进制是否保留可执行权限；
- arm64 Runtime 的每个文件是否与 Manifest 相符。

可额外查看每个包会发出的内容：

```shell
npm pack --dry-run
npm pack --dry-run ./darwin-arm64
npm pack --dry-run ./darwin-x64
npm pack --dry-run ./linux-x64
npm pack --dry-run ./win32-x64
```

## 6、发布到 staging，平台包必须在根包之前

先确认 npm 登录的是内部 Registry：

```shell
npm whoami --registry https://npm.vmic.xyz
```

然后依次发布四个平台包：

```shell
# 四个平台包先发 alpha
npm publish ./win32-x64 --tag alpha --registry https://npm.vmic.xyz
npm publish ./linux-x64 --tag alpha --registry https://npm.vmic.xyz
npm publish ./darwin-x64 --tag alpha --registry https://npm.vmic.xyz
npm publish ./darwin-arm64 --tag alpha --registry https://npm.vmic.xyz

```

确认四个都已存在且版本正确后，最后发布入口包：

```shell
# 根包最后发 alpha
npm publish . --tag alpha --registry https://npm.vmic.xyz
```

根包最后发，因为用户安装根包时，它会立即解析四个精确版本的平台依赖。

