# Node.js 与 npm Resources

## Knowledge

- [Node.js Docs: Introduction to Node.js](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs)
  Node.js 官方入门材料。Use for: 解释 Node.js 是什么、适合什么场景、运行时与浏览器 JavaScript 的边界。
- [Node.js Docs: Event Loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)
  Node.js 官方异步模型材料。Use for: 事件循环、异步 I/O、计时器、微任务和回调顺序。
- [Node.js Docs: Discover JavaScript Timers](https://nodejs.org/en/learn/asynchronous-work/discover-javascript-timers)
  Node.js 官方 timers 入门材料。Use for: `setTimeout()`、`setInterval()` 和延迟执行的基础示例。
- [MDN: Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
  MDN Promise 参考。Use for: Promise 表示异步操作最终完成或失败的结果。
- [MDN: async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
  MDN async function 参考。Use for: `async` 函数、`await` 表达式和 Promise 关系。
- [Node.js API Docs](https://nodejs.org/api/)
  Node.js 核心模块官方参考。Use for: `fs`、`path`、`process`、`http`、`stream`、`child_process` 等模块细节。
- [Node.js Docs: CommonJS modules](https://nodejs.org/api/modules.html)
  Node.js CommonJS 官方文档。Use for: `require()`、`module.exports`、内置模块和 CommonJS 加载规则。
- [Node.js Docs: ECMAScript modules](https://nodejs.org/api/esm.html)
  Node.js ESM 官方文档。Use for: `import`、`export`、ESM 与 CommonJS 的互操作边界。
- [Node.js Docs: Packages](https://nodejs.org/api/packages.html)
  Node.js package 规则官方文档。Use for: `package.json` 的 `type` 字段、`.mjs`、`.cjs`、`.js` 解释规则。
- [Node.js Docs: File system](https://nodejs.org/api/fs.html)
  Node.js 文件系统官方文档。Use for: `node:fs`、`node:fs/promises`、文件读写和同步/异步 API 边界。
- [Node.js Docs: Path](https://nodejs.org/api/path.html)
  Node.js 路径处理官方文档。Use for: `path.join()`、`path.resolve()`、`path.dirname()` 和跨平台路径拼接。
- [Node.js Docs: Process](https://nodejs.org/api/process.html)
  Node.js process 官方文档。Use for: `process.argv`、`process.env`、`process.cwd()` 和当前进程信息。
- [npm Docs: package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)
  npm 官方 package.json 字段说明。Use for: `scripts`、`dependencies`、`devDependencies`、`bin`、`exports`、`type`。
- [npm Docs: Scripts](https://docs.npmjs.com/cli/using-npm/scripts/)
  npm 官方 scripts 机制说明。Use for: `scripts` 字段、pre/post 脚本、生命周期脚本、脚本运行目录和环境变量。
- [npm Docs: npm run-script](https://docs.npmjs.com/cli/commands/npm-run-script/)
  npm 官方 `npm run` 命令说明。Use for: 自定义脚本执行、传参、`node_modules/.bin` 自动加入 PATH、脚本运行目录。
- [npm Docs: package-lock.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json)
  npm 官方锁文件说明。Use for: 解释可复现安装、依赖树、为什么不要随意删除 lockfile。
- [npm Docs: SemVer](https://docs.npmjs.com/about-semantic-versioning)
  npm 官方语义化版本说明。Use for: 解释 `^`、`~`、主版本/次版本/修订版本。
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
  TypeScript 官方手册。Use for: 类型、接口、泛型、模块、工程配置。
- [Express Guide](https://expressjs.com/en/guide/routing.html)
  Express 官方指南。Use for: 路由、中间件、请求响应模型。
- [Fastify Documentation](https://fastify.dev/docs/latest/)
  Fastify 官方文档。Use for: 高性能 Web 服务、schema、插件系统。
- [NestJS Documentation](https://docs.nestjs.com/)
  NestJS 官方文档。Use for: 企业级模块、Controller、Provider、依赖注入。
- [Prisma Documentation](https://www.prisma.io/docs)
  Prisma 官方文档。Use for: ORM、schema、migration、类型安全查询。
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
  Web 安全高信任参考。Use for: 认证、授权、输入校验、密码存储、API 安全。
- [OpenTelemetry Docs](https://opentelemetry.io/docs/)
  可观测性官方资料。Use for: 日志、指标、链路追踪和服务诊断。

## Wisdom (Communities)

- [Node.js GitHub Discussions](https://github.com/nodejs/node/discussions)
  Node.js 官方项目社区。Use for: 运行时行为、版本变化、核心模块问题。
- [npm GitHub Discussions](https://github.com/npm/cli/discussions)
  npm CLI 官方社区。Use for: 安装、发布、lockfile、workspace 和 npm 行为讨论。
- [TypeScript Community Discord](https://www.typescriptlang.org/community/)
  TypeScript 官方社区入口。Use for: 类型建模、编译配置和实际项目问题。

## Gaps

- 需要后续补充高质量中文 Node.js 实战项目资源。
- 需要根据用户实际练习项目，补充本地代码仓库作为课程案例。
