
## 1、Package的基本概念

在 Rust 中，**`package`是`Cargo`管理项目的基本单位**。

一个`package`通常对应一个项目目录，并且项目根部有一个`Cargo.toml`文件。`Cargo.toml`是项目的配置文件，用来描述这个包的基本信息、依赖和构建配置等。

例如：

```text
hello_cargo/
├── Cargo.toml
└── src/
    └── main.rs
```

其中，`hello_cargo` 这个项目整体就是一个 `package`。

`Cargo.toml` 示例：

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
rand = "0.10.1"
```

这里的 `[package]` 描述当前包本身的信息，`[dependencies]` 描述当前包依赖哪些外部 `crate`。

日常说“创建一个 Rust 项目”，多数时候就是创建一个 Cargo package。

例如：

```shell
cargo new hello_cargo
```

这条命令会创建一个名为 `hello_cargo` 的 package。

## 2、crate的基本概念

**`crate` 是 Rust 基本编译单元**。

一个`crate`可以被编译成两类产物：

- 库`crate`：编译成库，供其他代码调用
- 二进制`crate`：编译成可执行程序

`package`和`crate`的关系是：

> 一个`package`可以包含一个或多个`crate`

不过 Cargo 对一个`package`中的`crate`有一些基本规则：

- 一个`package`最多只能有一个库`crate`
- 一个`package`可以有多个二进制`crate`
- 一个`package`至少要有一个`crate`

最常见的情况是：一个`package` 只有一个二进制 crate。

如果是二进制项目：

```text
hello_cargo/
├── Cargo.toml
└── src/
    └── main.rs
```

这里：

- `hello_cargo` 是`package`。
- `src/main.rs` 对应一个二进制`crate`。
- 编译后会生成一个可执行程序

如果是库项目：

```text
my_lib/
├── Cargo.toml
└── src/
    └── lib.rs
```

这里：

- `my_lib` 是`package`。
- `src/lib.rs` 对应一个库 crate。
- 编译产物是供其他代码使用的库。

一个`crate`中，源码通常放在`src/`目录下。除外之外，`crate`中还会带上`test/`、`examples/`、`benches`、构建脚本和配置文件等内容。

很多复杂程序不会从零开始实现所有功能，而是使用社区维护的第三方库。这些第三方库通常以`crate`的形式提供给其他项目使用，最常见的来源就是[crates.io](https://crates.io/)。

在 Cargo 项目中，只需要在`Cargo.toml`的`[dependencies]`添加第三方库即可使用：

```toml
[dependencies]
rand = "0.10.1"
```

这里的 `rand = "0.10.1"` 表示当前项目依赖 `rand` 这个第三方 `crate`。

## 3、库crate和二进制crate

库`crate`的入口通常是`src/lib.rs`。

```rust
pub fn add(left: i32, right: i32) -> i32 {
    left + right
}
```

这个 `crate` 不会直接运行，而是提供函数、类型、模块等接口，供其他代码使用。

二进制`crate`的入口通常是`src/main.rs`。

```rust
fn main() {
    println!("hello");
}
```

这个 `crate` 包含`main`函数，会被编译成可执行文件。

一个`package`也可以同时包含库`crate`和二进制`crate`（但库`crate`最多只能有一个）：

```text
my_app/
├── Cargo.toml
└── src/
    ├── lib.rs
    └── main.rs
```

这种结构中：

- `src/lib.rs` 是库`crate`。
- `src/main.rs` 是二进制`crate`。
- `main.rs` 可以调用当前`package`中库`crate`暴露的代码。

## 4、多个二进制crate

一个`package`可以包含多个二进制`crate`。

除了`src/main.rs`外，还可以在`src/bin`下放多个入口文件：

```text
my_tools/
├── Cargo.toml
└── src/
    ├── main.rs
    └── bin/
        ├── server.rs
        └── client.rs
```

这里会产生多个二进制`crate`：

- `src/main.rs`               ->   对应二进制名为包名，例如这里是`my_tools`
- `src/bin/server.rs`   ->   对应二进制名为`server`
- `src/bin/client.rs`   ->   对应二进制名为`client`

每个文件都需要有自己的`main`函数。

运行指定二进制：

```shell
cargo run --bin hello-cargo
cargo run --bin server
cargo run --bin client
```

初学阶段不需要频繁使用多个二进制`crate`，但要知道：一个 package 不一定只对应一个可执行程序。

## 5、依赖与依赖图

编写一个库或可执行程序，顶层程序依赖一些`crate`（如图像处理、数值计算、并行库），而依赖的这些`crate`又依赖更底层的`crate`（比如解码库、压缩库等），最底层往往还依赖系统相关的库（例如libc）以及Rust标准库std。

因此，可以将依赖分为**直接依赖**和**传递依赖**：

- 直接依赖：自己项目的`Cargo.toml`中列出的依赖
- 传递依赖：自己项目依赖的`crate`依赖的一些`crate`

所有这些依赖加起来构成了项目的**依赖图**：它告诉`Cargo`需要构建哪些依赖，以及应该按什么顺序构建（必须先把依赖编译出来，才能构建依赖它们的crate）。

示例：

编写一个掷骰子小程序，其依赖于`rand` crate。

Cargo.toml

```toml
[package]  
name = "hello_cargo"  
version = "0.1.0"  
edition = "2024"  
  
[dependencies]  
rand = "0.10.1"
```

src/main.rs

```rust
use rand::RngExt;  
  
fn main() {  
    let mut rng = rand::rng();  
  
    println!("dice: {}", rng.random_range(1..7));  
}
```

`[dependencies]`虽然只写了`rand`一个依赖，但`rand`又依赖一些底层crate，这些依赖构成了依赖图，Cargo会解析依赖图并自动处理。

可以执行`cargo tree`查看依赖图：

```shell
cargo tree
```

结果：
![[assets/Pasted image 20260520011515.png|500]]

依赖图能帮助理解：项目最终不是只编译自己的代码，而是要把所有相关依赖都构建出来。



# 二、Cargo构建与项目配置
## 1、Cargo与rustc的关系

`Cargo` 是 Rust 的项目管理工具，负责项目结构、依赖解析、构建流程和调用编译器。

真正执行编译工作的工具是`rustc`。

执行：

```shell
cargo build
```

大致会经历这些步骤：

1. 读取`Cargo.toml`
2. 更新依赖索引
3. 解析依赖图
4. 下载缺失的依赖源码
5. 按依赖顺序编译各个`crate`
6. 最后编译当前项目
7. 将构建产物放到 `target/` 目录下。

如果想看到更详细的构建过程，可以使用：

```shell
cargo build --verbose
```

在执行前，如果在IDE（如RustRover）中给`Cargo.toml`增加依赖后，IDE会自动更新`crates.io`索引、下载依赖源码。因此，为了观察，可以先删掉`~/.cargo/registry`目录：

```shell
rm -rf ~/.cargo/registry
```

同时，为了确保target/目录干净，先执行一次`cargo clean`：

```shell
cargo clean
```

最终`cargo build --verbose`结果如下：

![[assets/Pasted image 20260520010913.png]]

![[assets/Pasted image 20260520011146.png]]

> 注意：由于配置了镜像源，因此更新依赖索引没有直接使用官方`crates.io`索引，而是使用了`rsproxy`镜像源。

Cargo 在编译依赖时，会为依赖图中的多个 `crate` 分别调用 `rustc`。

编译库 `crate` 时，`rustc` 会生成供其他 `crate` 使用的库产物，例如 `.rlib` 文件。`.rlib` 中不仅包含已经编译出的内容，也包含编译器后续做类型检查、泛型实例化、Trait 检查等所需的元数据。

编译二进制 `crate` 时，`rustc` 会生成最终的可执行文件。

当代码中写了：

```rust
use rand::RngExt;
```

`rustc`需要知道`rand`这个外部`crate`的编译产物在哪里。Cargo 在调用 `rustc` 编译当前项目时，会通过参数把依赖 `crate` 的名字和对应产物路径告诉 `rustc`，即通过`--extern crate名=库产物路径`。

## 2、cargo build 和 cargo build --release

`cargo build`默认使用开发配置，也就是`dev`profile。

开发构建的特点是：

- 编译速度较快
- 运行性能不是最高
- 通常保留更多的调试信息，更适合开发与调试
- `debug_assert!`会生效
- 整型溢出触发检查并`panic`

`cargo build --release`使用发布配置，也就是`release`profile。

发布配置的特点有：

- 编译速度较慢
- 运行性能更高
- 优化更充分
-  `debug_assert!`默认不生效
- 整型溢出会进行二进制补码回绕

## 3、Edition

Rust 重视向后兼容，目标是让旧代码尽量能在新的Rust编译器上继续编译。

但语言本身仍然需要演进。有些新特性可能会影响旧代码的解析方式，例如新增关键字、调整路径规则等。为了解决语言演进与兼容性之间的问题，Rust引入了`Edition`。

`Edition`不是Rust编译器版本号，而是一组语言规则。每个`crate`可以在自己的`Cargo.toml`中指定自己使用的`Edition`：

```toml
[package]
edition = "2024"
```

**不同`Edition`的`crate`可以在同一个项目中相互依赖**。`Edition`主要影响当前`crate`内部代码的语法和解析规则，不影响正常的依赖使用。

Rust的`Edition`不是每年发布，而是在需要承载一批语言规则变化时才发布，常见`Edition`包括：

- Rust 2015
- Rust 2018
- Rust 2021
- Rust 2024


## 4、Edition迁移与cargo fix

如果维护旧项目，升级`Edition`时通常不建议直接手动修改`Cargo.toml`中的`edition`字段，更推荐先使用`cargo fix --edition`让`Cargo`帮你做自动迁移。

`cargo fix`的作用是：

> 根据编译器给出的可自动修复建议，直接修改源码。

它本质不是格式化工具，而是利用`rustc`的诊断信息，对一些确定可改的代码做机械化修复。

`cargo fix`用于自动修复`rustc`报告的lint警告；而`cargo fix --edition`可以用于`Edition`迁移。

`Edition`迁移时，常用流程是：

```shell
cargo fix --edition
```

这条命令会检查当前项目，并尝试把代码改成同时兼容当前 Edition 和下一个 Edition 的写法。

例如，某些旧代码可能使用了后来变成关键字的变量名。`Rust 2018`引入`async`/`await`后，如果旧代码中有名为`async`的标识符，迁移工具可能会把它改成原始标识符写法：

```rust
let r#async = 1;
```

这里的 `r#async` 表示：虽然 `async` 是关键字，但这里仍然把它当作普通标识符使用。

完成自动修复后，再修改`Cargo.toml`中的`Edition`为迁移的`Edition`版本。

然后重新检查项目：

```shell
cargo check
```

如果项目有测试，也应该继续运行：

```shell
cargo test
```

需要注意，`cargo fix --edition` 不是万能迁移工具。它只能修复编译器能够明确判断、并且能安全给出修改建议的问题。涉及业务逻辑、API 设计、依赖版本升级、行为差异确认的部分，仍然需要人工检查。


## 5、构建配置profile

`Cargo.toml`不只是写依赖的地方，也可以**配置不同构建模式下的编译行为**。

常见的`profile`包括：

```toml
[profile.dev]

[profile.release]

[profile.test]
```

- `cargo build`使用`[profile.dev]`
- `cargo build --release`使用`[profile.release]`
- `cargo test`使用`[profile.test]

有时希望在`release`构建中也保留调试信息，例如用于性能剖析或更可读的崩溃回溯。可以这样配置：

```toml
[profile.release]
debug = true
```

这样执行：

```shell
cargo build --release
```

得到的仍然是经过优化的发布构建，但会包含调试符号，更适合性能分析工具定位函数和代码位置。


# 三、模块

## 1、模块的基本概念

`crate`是 Rust 编译的基本单元，**模块（module）则是`crate`内部组织代码的方式**。

模块可以理解为：

> 给一组相关代码取一个名字，并管理这组代码的命名空间与可见性

模块中可以放很多语法项：

- 函数
- 结构体
- 枚举
- Trait
- 常量
- 静态变量
- 类型别名
- 子模块
- `use`声明

一个简单的模块声明示例：

```rust
mod shop {
    pub struct Product {
        pub name: String,
        price: u32,
    }

    pub fn create_product(name: &str, price: u32) -> Product {
        Product {
            name: name.to_string(),
            price,
        }
    }

    pub(crate) fn calc_discount_price(price: u32) -> u32 {
        price * 90 / 100
    }

    fn validate_price(price: u32) -> bool {
        price > 0
    }
}
```

这里：

- `Product`是公开结构体
- `Product.name` 是公开字段
- `Product.price` 是私有字段
- `create_product` 是公开函数
- `calc_discount_price` 只在当前 `crate` 内可见
- `validate_price` 是私有函数

把某个语法项标记为`pub`，通常可以称为导出该语法项。但它是否真的能被外部访问，还要看**所在模块路径是否可见**。


## 2、模块的核心作用

模块主要承担两个作用：**命名空间管理**和**可见性管理**。

命名空间管理指的是，**不同模块中可以存在同名函数或类型**。

示例：

```rust
mod shop {
    pub fn create() {
        println!("create shop item");
    }
}

mod user {
    pub fn create() {
        println!("create user");
    }
}
```

调用时通过路径区分：

```rust
fn main() {
    shop::create();
    user::create();
}
```


可见性管理指的是，**模块可以控制哪些内容允许外部访问，哪些内容只在内部使用**。

Rust 的默认规则是：

> 未标记`pub`的内容默认私有。

```rust
mod shop {
    pub fn checkout() {   // 结账
        println!("checkout");
    }

    fn check_stock() {   // 检查库存
        println!("check stock");
    }
}

fn main() {
    shop::checkout();

    // shop::check_stock(); // 错误：check_stock 是私有的
}
```

## 3、默认私有

Rust中，未标记`pub`的语法项默认是私有的。

**私有项可以在定义它的模块内部使用，也可以被其子模块访问**。

示例：

```rust
mod shop {  
  
    pub fn checkout() {  
        println!("checkout");  
    }  
  
    fn check_stock() {  
        println!("check stock");  
    }  
  
    pub mod admin {  
        pub fn run() {  
            super::check_stock();  
        }  
    }  
  
}  
  
  
fn main() {  
    shop::admin::run();  
}
```

这里的 `super::check_stock()` 表示访问父模块中的 `check_stock` 函数。`admin` 是 `shop` 的子模块，所以可以访问父模块中的私有项。

不过，模块外部无法直接访问 `shop::check_stock()`。

> 注意，shop没有声明为`pub`，但main()函数可以直接使用`shop::admin::run()`这是因为`main()`和模块`shop`也在同一个父模块里，这个父模块称为`crate root`。


## 4、pub与路径

`pub`表示某个语法项可以被外部访问，但它能不能真正被访问，**还取决于整条路径是否可见**。

示例：

```rust
mod outer {
    pub mod inner {
        pub fn hello() {
            println!("hello");
        }
    }
}

fn main() {
    outer::inner::hello();
}
```

这里 `inner` 是 `pub mod`，`hello` 也是 `pub fn`，所以可以通过 `outer::inner::hello()` 访问。

如果改成：

```rust
mod outer {
    mod inner {
        pub fn hello() {
            println!("hello");
        }
    }
}

fn main() {
    // outer::inner::hello(); // 错误：inner 是私有模块
}
```

虽然 `hello` 是 `pub`，但 `inner` 模块本身不是公开的，所以模块外部仍然无法访问。

因此，**要让某个语法项对外可见，不仅它自己要可见，它所在的路径也要可见**。

## 5、受限制的公开可见性

除了普通的`pub`，Rust还支持**更细粒度的可见性控制**，用来限制某个语法项可以被哪些模块访问。

常见形式有：

- `pub(crate)`：只在当前`crate`内可见
- `pub(super)`：只对父模块可见
- `pub(in path)`：只在指定模块路径内可见

这些写法适合表达“不是完全公开接口，但也不是当前模块私有实现”的中间状态。

### （1）pub(crate)

`pub(crate)`表示只在当前`crate`内可见。

这种可见性常用于内部共享代码：不希望暴露给外部用户，但希望当前项目的多个模块可以使用。


```rust
mod pricing {
    pub(crate) fn calc_member_price(price: u32) -> u32 {
        price * 80 / 100
    }
}

fn main() {
    let price = pricing::calc_member_price(100);
    println!("{price}");
}
```

`calc_member_price` 可以在当前 `crate` 内使用。但如果这个项目作为库被其他项目依赖，外部项目不能调用它。


### （2）pub(super)

`pub(super)`表示只对父模块可见。

示例：

```rust
mod shop {
    pub mod order {
        pub(super) fn normalize_order_id(id: &str) -> String {
            id.trim().to_uppercase()
        }
    }

    pub fn test() {
        let id = order::normalize_order_id(" ab-123 ");
        println!("{id}");
    }
}

fn main() {
    shop::test();

    // shop::order::normalize_order_id(" ab-123 "); // 错误
}
```

这里 `normalize_order_id` 对父模块 `shop` 可见，但对 `shop` 外部不可见。

`pub(super)` 适合表达：这个函数是给父模块协调内部逻辑用的，不是对外接口。


### （3）pub(in path)

`pub(in path)`可以把可见性限制在指定模块路径，是更细粒度的可见性控制。

示例：

```rust
mod shop {
    pub mod order {
        pub mod internal {
            pub(in crate::shop::order) struct OrderId(String);

            pub(in crate::shop::order) fn create_order_id(raw: &str) -> OrderId {
                OrderId(raw.trim().to_uppercase())
            }
        }

        pub fn demo() {
            let _id = internal::create_order_id(" x001 ");
            println!("order id created");
        }
    }

    pub fn test() {
        // order::internal::create_order_id(" x001 "); // 错误
    }
}
```

这里 `OrderId` 和 `create_order_id` 只在 `crate::shop::order` 这个模块范围内可见。`shop` 模块本身无法直接访问它们。

这种写法不如 `pub`、`pub(crate)`、`pub(super)` 常见，但在大型项目中可以用来精确控制内部接口边界。


## 6、嵌套模块

模块可以嵌套，也就是在模块中继续定义子模块。

示例：

```rust
mod shop {
    pub mod product {
        pub fn list() {
            println!("product list");
        }
    }

    pub mod order {
        pub fn create() {
            println!("create order");
        }
    }

    pub mod user {
        pub fn login() {
            println!("user login");
        }
    }
}

fn main() {
    shop::product::list();
    shop::order::create();
    shop::user::login();
}
```

这种结构适合按领域划分代码，例如：

- `shop::product`
- `shop::order`
- `shop::user`

嵌套模块让代码层级更清楚，也让命名空间更明确。


# 四、模块的分文件编写

## 1、独立文件模块

前面的例子都是把模块直接写在当前文件中，例如

```rust
mod shop {
	
	pub fn run() {
		println!("shop is running");
	}
}

fn main() {  
	shop::run();  
}
```

实际项目中，模块通常会拆到单独文件里。

例如 `main.rs` 里写：

```rust
mod shop;

fn main() {
    shop::run();
}
```

它表示：声明一个名为`shop`的模块，模块内容不写在当前文件中，而是让编译器去对应文件中查找。

最简单的文件结构是：

```text
src/
├── main.rs
└── shop.rs
```

`src/main.rs`：

```rust
mod shop;

fn main() {
    shop::run();
}
```

`src/shop.rs`

```rust
pub fn run() {
    println!("shop is running");
}
```

注意，`shop.rs` 里面不需要再写 `mod shop { ... }`。这个文件本身就是 `shop` 模块的内容。

## 2、目录模块

当模块变很大时，通常会继续拆分子模块。

一种常见结构是：

```text
src/
├── main.rs
└── shop/
    ├── mod.rs
    ├── product.rs
    ├── order.rs
    └── user.rs
```

`src/main.rs`：

```rust
mod shop;  
  
fn main() {  
  
    shop::product::list();  
    shop::order::create();  
    shop::user::login();  
}
```

`src/shop/mod.rs`：

```rust
pub mod product;
pub mod order;
pub mod user;
```

`src/shop/product.rs`：

```rust
pub fn list() {
    println!("product list");
}
```

`src/shop/order.rs`：

```rust
pub fn create() {  
    println!("create order");  
}
```

`src/shop/user.rs`：

```rust
pub fn login() {  
    println!("login user");  
}
```


## 3、现代模块文件组织

除了`mod.rs`方式，Rust还支持更现代的模块文件组织方式：

```text
src/
├── main.rs
├── shop.rs
└── shop/
    ├── product.rs
    └── order.rs
```

`src/main.rs`：

```rust
mod shop;

fn main() {
    shop::start();
}
```

`src/shop.rs`：

```rust
pub mod product;
pub mod order;

pub fn start() {
    println!("shop start");
    product::list_products();
    order::create_order();
}
```

`src/shop/product.rs`：

```rust
pub struct Product {
    pub name: String,
    price: u32,
}

pub fn list_products() {
    println!("product list: milk, chocolate, strawberry");
}

pub(crate) fn default_price() -> u32 {
    100
}
```

`src/shop/order.rs`：

```rust
pub fn create_order() {
    println!("create order");

    let price = super::product::default_price();
    println!("default price: {}", price);
}
```

这里：

- `shop.rs` 是 `shop` 模块的入口
- `shop/product.rs` 是 `shop::product` 子模块
- `shop/order.rs` 是 `shop::order` 子模块
- `super::product::default_price()` 表示从 `order` 的父模块 `shop` 中访问 `product` 子模块


# 五、路径与导入

## 1、路径的基本概念

Rust 使用路径定位某个语法项的位置。

模块可以嵌套。不同模块中也可能有同名项，所以Rust需要通过路径明确指定要访问的是哪个函数、类型或模块。

路径使用`::`分隔。

例如：

```rust
std::mem::swap
```

它表示：`std`模块中的`mem`子模块中的`swap`函数。

使用示例：

```rust
fn main() {
    let mut a = 1;
    let mut b = 2;

    std::mem::swap(&mut a, &mut b);

    println!("a = {}, b = {}", a, b);
}
```

**完整路径的优点是来源清楚，缺点是路径较长时会让代码变得啰嗦**。

## 2、use导入名字

`use`可以把某个路径引入当前作用域，让后续代码使用更短的名字。

示例：

```rust
use std::mem;

fn main() {
    let mut a = 1;
    let mut b = 2;

    mem::swap(&mut a, &mut b);

    println!("a = {}, b = {}", a, b);
}

```

这里的 `use std::mem;` 表示把 `std::mem` 这个模块名引入当前作用域。之后就可以写 `mem::swap`，而不必每次都写 `std::mem::swap`。

`use`不会复制代码，也不会把定义搬到当前文件。它只是让当前作用域多了一个可用名字。

也可以直接导入具体函数：

```rust
use std::mem::swap;

fn main() {
    let mut a = 1;
    let mut b = 2;

    swap(&mut a, &mut b);

    println!("a = {}, b = {}", a, b);
}
```

一般来说，Rust 代码常见风格是：

- **类型、Trait、模块通常导入到当前作用域**
- **函数可以保留模块前缀，让来源更清楚**

例如 `HashMap` 常直接导入：

```rust
use std::collections::HashMap;

fn main() {
    let mut scores = HashMap::new();
    scores.insert("Tom", 90);
    scores.insert("Alice", 85);
}
```

而 `std::mem::swap` 这类函数，有时保留 `mem::swap` 会更清晰。

## 3、use的作用范围

`use`可以放在**模块级别**，也可以放在**代码块级别**。

放在模块级别时，当前模块后续代码都可以使用：

```rust
use std::collections::HashMap;

fn main() {
    let mut scores = HashMap::new();
    scores.insert("Tom", 90);
}
```

放在代码块内部时，只在当前代码块内有效：

```rust
fn sort_pair(mut a: i32, mut b: i32) -> (i32, i32) {
    use std::mem;

    if a > b {
        mem::swap(&mut a, &mut b);
    }

    (a, b)
}
```

小范围 `use` 适合临时使用某个名字，避免污染整个模块作用域。


## 4、合并导入

Rust 支持把同一路径下的多个名字一起导入。

```rust
use std::collections::{ HashMap, HashSet };
```

也可以同时导入模块本身和模块中的某个成员：

```rust
use std::fs::{self, File};
```

`self`表示模块本身。

这等价于：

```rust
use std::fs;
use std::fs::File;
```

通配导入`*`可以导入某个模块公开的所有名字：

```rust
use std::io::prelude::*;
```

通配导入可以减少重复书写，但也容易让名字来源不清楚，甚至造成命名冲突。建议只在常见的 prelude 场景或小范围代码中使用。


## 5、as重命名

如果导入的名字太长，或者两个名字冲突，可以使用 `as` 重命名。

```rust
use std::fmt::Result as FmtResult;
use std::io::Result as IoResult;
```

这样可以同时使用两个不同模块中的 `Result` 类型别名。


## 6、导入名字不会被子模块继承

每个模块都有自己的名字作用域。父模块中的 `use` 不会自动继承到子模块中。

```rust
mod parent {
    pub struct User {
        pub name: String,
    }

    use std::mem;

    pub mod child {
        pub fn func(a: &mut i32, b: &mut i32) {
            let user = User {
                name: String::from("Tom"),
            };

            mem::swap(a, b);
        }
    }
}
```

在 `child` 模块中，`User` 和 `mem` 都找不到。因为它们只在 `parent` 模块的作用域中可见，不会自动进入 `child` 模块。

可以这样修正：

```rust
mod parent {
    pub struct User {
        pub name: String,
    }

    pub mod child {
        use std::mem;

        pub fn func(a: &mut i32, b: &mut i32) {
            let user = super::User {
                name: String::from("Tom"),
            };

            mem::swap(a, b);

            println!("{}", user.name);
        }
    }
}
```

这里：

- `super::User` 表示从父模块 `parent` 中访问 `User`
- `use std::mem;` 写在 `child` 模块内部，所以 `child` 可以使用 `mem::swap`

这条规则很重要：模块之间不是共享一个大作用域，每个模块都有自己的名字空间。


## 7、标准库预导入

每个模块都有自己的名字作用域，父模块中的`use`不会自动继承到子模块中。不过，这个作用域并不在完全空白的。Rust会自动做两件事：

**第一，标准库`std`会自动链接到项目中，因此可以直接写完整路径**：

```rust
fn main() {
    let mut a = 1;
    let mut b = 2;

    std::mem::swap(&mut a, &mut b);
}
```

**第二，Rust 会自动导入标准库库预导入模块中的常见名字**。可以近似理解为，每个模块开头都默认带有这一句：

```rust
use std::prelude::v1::*;
```

所以很多常用类型和 Trait 不需要手动导入，例如：

```rust
let numbers: Vec<i32> = Vec::new();
let option: Option<i32> = Some(2);
let result: Result<i32, String> = Ok(1);
```

这里的`Vec`、`Option`、`Some`、`Result`以及`Ok`等名字可以直接使用，就是因为它们来自标准库预导入。

需要注意，`prelude` 只是一个约定名称。**标准库中的 `std::prelude::v1` 会被 Rust 自动导入，但其他库即使提供了名为 `prelude` 的模块，也不会自动导入**。

例如，某些库可能提供：

```rust
use some_crate::prelude::*;
```

这种写法表示把该库认为最常用的一组名字一次性导入当前作用域。它需要用户手动写出，Rust 不会自动帮你导入。








## 8、特殊路径名
### （1）self路径

 `self`表示当前模块。

```rust
mod account {
    pub enum Role {
        Admin,
        User,
        Guest,
    }

    pub fn print_role(role: self::Role) {
        match role {
            self::Role::Admin => println!("Admin"),
            self::Role::User => println!("User"),
            self::Role::Guest => println!("Guest"),
        }
    }
}
```

这里的 `self::Role` 表示当前模块 `account` 中的 `Role`。很多时候可以直接写 `Role`，但 `self::Role` 会更明确地表达：这个名字来自当前模块。

### （2）super路径

`super` 表示父模块。

```rust
mod account {
    pub struct User {
        pub name: String,
    }

    pub mod auth {
        use super::User;

        pub fn login(user: &User) {
            println!("login: {}", user.name);
        }
    }
}
```

这里 `auth` 是 `account` 的子模块，`super::User` 表示到父模块 `account` 中查找 `User`。

`super` 常用于子模块访问父模块中的类型、函数或兄弟模块。

### （3）crate路径

`crate` 表示当前 `crate` 的根模块。

例如项目结构如下：

```text
src/
├── main.rs
└── account.rs
```

`src/main.rs`：

```rust
mod account;

use crate::account::User;

fn main() {
    let user = User {
        name: String::from("Tom"),
    };

    println!("{}", user.name);
}
```

`src/account.rs`：

```rust
pub struct User {
    pub name: String,
}
```

`crate::account::User` 表示从当前 `crate` 根部开始，进入 `account` 模块，再找到 `User`。

相对路径依赖当前位置，绝对路径从 `crate` 根部开始。项目变复杂后，`crate::...` 的写法通常更稳定。

## 9、外部crate与本地模块重名

如果外部`crate`与本地模块重名，需要明确区分路径来源。

假设项目依赖了外部 `image` crate，同时自己也定义了本地 `image` 模块：

```rust
mod image {
	pub struct Sampler;
}
```

使用当前 `crate` 内的模块，可以写：

```rust
use crate::image::Sampler;
```

也可以在合适位置写：

```rust
use self::image::Sampler;
```

如果要使用外部 `image` crate 中的 `Sampler`，可以使用以 `::` 开头的路径：

```rust
use ::image::Sampler;
```

`::image` 表示从外部 crate 根开始查找，而不是当前模块中的 `image`。

这种情况不算特别常见，但当本地模块名和依赖名相同时，需要知道如何消除歧义。


## 10、pub use 重导出

`use`可以把某个路径引入当前作用域，让当前模块内部可以用更短的名字访问它。

如果`use`前面加上了`pub`，就变成了`pub use`。**它不仅把名字引入当前作用域，还会把这个名字作为当前模块的公开项重新导出**。这称为重导出。

例如，项目结构如下：

```text
src/
├── lib.rs
└── plant_structures/
    ├── mod.rs
    ├── leaves.rs
    └── roots.rs
```

`plant_structures/leaves.rs`：

```rust
pub struct Leaf;
```

`plant_structures/roots.rs`：

```rust
pub struct Root;
```

`plant_structures/mod.rs`：

```rust
pub mod leaves;
pub mod roots;

pub use self::leaves::Leaf;
pub use self::roots::Root;
```

这里的：

```rust
pub use self::leaves::Leaf;
pub use self::roots::Root;
```

表示把 `plant_structures::leaves::Leaf` 和 `plant_structures::roots::Root` 重新导出到 `plant_structures` 模块下。

因此，外部既可以使用原始路径：

```rust
plant_structures::leaves::Leaf  
plant_structures::roots::Root
```

也可以使用更短的重导出路径：

```rust
plant_structures::Leaf
plant_structures::Root
```

`pub use` 不会复制类型，也不会创建新的类型。`plant_structures::Leaf` 只是 `plant_structures::leaves::Leaf` 的公开别名。

重导出常用于整理库的公共 API。库内部可以按文件和模块拆得很细，但对外暴露时，可以提供更简洁、更稳定的访问路径。

标准库预导入也可以理解为通过一组 `pub use` 把常用类型、Trait 和函数集中导出，然后再由编译器自动导入到每个模块中。