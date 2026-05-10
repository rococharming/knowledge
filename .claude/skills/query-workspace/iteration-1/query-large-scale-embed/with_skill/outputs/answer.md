# 关于并行计算和并发编程的内容

知识库中关于并行计算和并发编程的内容主要分布在 **TestLarge** 领域，涵盖从底层系统机制到高层分布式架构的多个层面。

---

## 一、并发编程核心概念

### 1. 并发与并行

- **[[Concurrency]]** — 并发编程。现代软件工程中的重要概念，具有高效、可靠、可扩展的特点，广泛应用于企业级软件开发。标签: `#systems` `#parallel`

- **[[Parallelism]]** — 并行计算。与并发编程密切相关，同样具有高效、可靠、可扩展的特点。标签: `#systems` `#parallel`

两者在知识库中相互引用，共同构成并发/并行编程的基础概念层。

### 2. 异步编程模型

- **[[AsyncAwait]]** — 异步编程模式。标签: `#async` `#programming`
  - 相关链接: [[Coroutine]]、[[GreenThread]]

- **[[Coroutine]]** — 协程。标签: `#async` `#programming`
  - 相关链接: [[GreenThread]]、[[MemoryModel]]

- **[[GreenThread]]** — 绿色线程。标签: `#async` `#systems`
  - 相关链接: [[MemoryModel]]、[[CacheCoherence]]

这三者形成了异步编程的完整技术栈：从语言层面的 async/await 语法，到协程调度机制，再到绿色线程的实现。

---

## 二、底层系统机制

### 内存与缓存

- **[[MemoryModel]]** — 内存模型。标签: `#systems` `#memory`
  - 相关链接: [[CacheCoherence]]、[[DistributedSystems]]

- **[[CacheCoherence]]** — 缓存一致性。标签: `#systems` `#memory`
  - 相关链接: [[DistributedSystems]]、[[Consensus]]

内存模型和缓存一致性是并行计算在硬件层面的核心问题，直接影响多线程/多进程程序的正确性。

---

## 三、分布式并行

### 分布式系统基础

- **[[DistributedSystems]]** — 分布式系统。标签: `#distributed` `#systems`
  - 相关链接: [[Consensus]]、[[CAP]]

- **[[Consensus]]** — 分布式共识。标签: `#distributed` `#algorithm`
  - 相关链接: [[CAP]]、[[eventualConsistency]]

- **[[CAP]]** — CAP 定理。标签: `#distributed` `#theorem`
  - 相关链接: [[eventualConsistency]]、[[Sharding]]

- **[[eventualConsistency]]** — 最终一致性。标签: `#distributed` `#database`
  - 相关链接: [[Sharding]]、[[Replication]]

### 架构模式

- **[[Microservices]]** — 微服务架构。标签: `#architecture` `#distributed`
  - 相关链接: [[Monolith]]、[[EventDriven]]

---

## 四、数据层并行

- **[[Sharding]]** — 数据分片。标签: `#database` `#scaling`
  - 相关链接: [[Replication]]、[[Indexing]]

- **[[Replication]]** — 数据复制。标签: `#database` `#reliability`
  - 相关链接: [[Indexing]]、[[QueryOptimization]]

数据分片和数据复制是数据库层面实现并行处理和高可用的核心手段。

---

## 五、编程范式关联

- **[[OOP]]** — 面向对象编程。在相关链接中引用了 [[Concurrency]] 和 [[Parallelism]]
- **[[FunctionalProgramming]]** — 函数式编程。在相关链接中引用了 [[Concurrency]]
- **[[Rust]]** — 系统编程语言。标签含 `#systems`，与底层并发机制密切相关

---

## 知识图谱关系

```
Concurrency <-> Parallelism <-> AsyncAwait <-> Coroutine <-> GreenThread
                                                     |
MemoryModel <-> CacheCoherence <-> DistributedSystems <-> Consensus <-> CAP
                                        |                    |
                                    Microservices         eventualConsistency
                                                              |
                                                         Sharding <-> Replication
```

---

## 依据

- [[Concurrency]] — 并发编程定义
- [[Parallelism]] — 并行计算定义
- [[AsyncAwait]] — 异步编程模式
- [[Coroutine]] — 协程机制
- [[GreenThread]] — 绿色线程
- [[MemoryModel]] — 内存模型
- [[CacheCoherence]] — 缓存一致性
- [[DistributedSystems]] — 分布式系统
- [[Consensus]] — 分布式共识算法
- [[CAP]] — CAP 定理
- [[eventualConsistency]] — 最终一致性
- [[Sharding]] — 数据分片
- [[Replication]] — 数据复制
- [[Microservices]] — 微服务架构
- [[OOP]] — 面向对象编程（关联引用）
- [[FunctionalProgramming]] — 函数式编程（关联引用）
