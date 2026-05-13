---
title: "6、crate、module、package - KM知识管理平台"
source: "https://wiki.vivo.xyz/knowledge/22886/content/201898"
author:
published:
created: 2026-05-13
description:
tags:
  - "clippings"
---
# AI摘要

## 为什么值得读

这篇文章系统地梳理了 Rust 语言中 crate、module、package 这三大核心概念，以及它们之间的关系。对于任何 Rust 开发者（尤其是刚入门或想深入理解 Rust 模块系统的读者）来说，这是一篇非常实用的参考文档。它不仅能帮你理清这些容易混淆的术语，还能让你掌握如何正确组织代码、控制可见性、导入导出模块，从而写出更清晰、更可维护的 Rust 项目。

## How（如何组织）

文章按照“基本概念 → 核心机制 → 实践建议”的顺序展开，通过大量具体的示例和清晰的结构，帮助读者逐步建立对模块系统的理解：
- **基本概念**：分别解释了 crate、package、workspace、module、path 和 item 的定义和用途。
- **Crate 与 Package**：详细说明了库 crate 和二进制 crate 的区别，以及一个 package 如何包含多个 crate（通过 Cargo.toml 和 src/ 目录布局）。
- **模块与文件布局**：介绍了模块的两种声明方式（内联模块和文件/目录模块）、模块树的构成、路径的两种形式（相对和绝对）、私有性规则、pub 关键字以及受限可见性。
- **use 关键字**：涵盖了基本导入、重命名、分组导入、通配导入和 pub use 重导出等常用技巧。

## What（核心内容）

本文的核心内容可以概括为以下几点：
1. **crate** 是 Rust 的编译单位，**package** 是发布单位，**module** 是组织代码的命名空间机制。
2. Crate 可以有两种类型：二进制 crate（可执行）和库 crate（可被其他 crate 引用）。一个 package 可以包含零个或多个二进制 crate，但最多一个库 crate。
3. 模块默认私有，通过 `pub` 关键字控制可见性。可以使用 `pub(crate)`、`pub(super)`、`pub(in path)` 实现更精细的可见性限制。
4. 使用 `use` 关键字可以将路径中的项引入当前作用域，支持 `as` 重命名、`{}` 分组导入、`*` 通配导入，以及 `pub use` 重导出来简化对外接口。
5. 最佳实践：将逻辑复杂的模块定义在库 crate 中，二进制 crate 仅用于调用库 crate 的功能，这样可以提高代码的复用性和组织性。

---

# 原始正文

## 一、基本概念

## 1、crate

crate（箱）是Rust编译器处理代码的最小单位，每次调用rustc基本都是在编译一个crate。crate可以分为库crate和二进制crate。

## 2、package

package（包）是Cargo.toml定义的发布单元，用于组织和管理多个crate。

## 3、workspace

workspace（工作区）主要用于大型项目的多包协作开发，多个包共享Cargo.lock和target/集合。

## 4、module

module（模块）是组织命名空间的机制，构成crate的树状结构，可用于控制可见性、拆分文件、整洁API。

## 5、path

path（路径）使用**::**连接的命名路径，用于定位模块/类型/函数等项的位置，分为绝对路径和相对路径。Rust中使用use关键字将路径中的项引入到当前作用域。

## 6、item

item（项）可以是模块、函数、常量、结构体、枚举、类型、trait等。

## 二、Crate和Package

## 1、Crate

一个箱（Crate）是Rust编译器处理代码的最小单位，每次调用rustc通常都是在编译一个crate。

Crate有两种类型：

二进制crate：有fn main()，被编译成可执行文件，可以运行。默认源码为src/main.rs（主二进制）或者src/bin/\*.rs（多个二进制）

库crate：没有main函数，对外暴露API，可被其他crate通过use关键字导入。默认源码文件是src/lib.rs。

Crate Root：crate的编译入口文件，如src/main.rs，src/lib/rs。Crate Root形成crate的根模块。

特点：

一个Crate可以包含多个模块

crate关键字是模块树的根，例如通过crate::开始指定路径。

## 2、Crate

一个包（Package）就是一个Rust项目，基本就是一个目录。是由Cargo.toml描述的集合，用于组织和构建一个或多个crate。这个目录有：

Cargo.toml：包的配置文件（包名、版本、依赖等）

src/ 目录：默认源码目录

一个包可以包含：

至多一个library crate（库）

零个或多个binary crate（可执行程序）

最简单的包结果如下：

展开

自动换行

my\_project/

├─ Cargo.toml

└─ src/

└─ main.rs

其中的Cargo.toml如下：

展开

自动换行

\[package\]

name = "my\_project"

version = "0.1.0"

edition = "2024"

这是一个包，其中包含一个二进制crate，入口是src/main.rs。因为没有src/lib.rs，因此这个包目前没有库crate。

一个包也可以同时拥有库和多个二进制，示例如下：

展开

自动换行

my\_project/

├─ Cargo.toml

└─ src/

├─ lib.rs # 库 crate

├─ main.rs # 默认二进制 crate

└─ bin/

├─ tool1.rs # 额外二进制 crate

└─ tool2.rs

lib.rs定义库crate的公共逻辑

main.rs和bin/目录下的rs文件都是一个二进制crate，可以使用use my\_project::xxx调用库里的代码

由于包中有多个二进制crate，因此执行cargo run时，需要使用 **\--bin** 选项指定执行哪一个二进制文件。

示例：

![](https://veditor.vivo.xyz/api/v1/attachment/file/biqr0NJzUvnUlMAkjqLqvvyUfdM2TuYmY0exjcuQY0h8wfI9AkIwUuveg_V2WOet)

当我们有想给二进制crate取不同名称，或者想指定二进制crate的路径（默认路径是src/main.rs或src/bin/\*rs）等需求时，可以在Cargo.toml中显式指定库和二进制crate的名字和路径等。

展开

自动换行

\[lib\]

name = "my\_project"

\[\[bin\]\]

name = "my\_project\_main"

path = "src/main.rs"

## 三、模块与文件布局

## 1、模块的作用

如果说crate是一本书，那么module（模块）就是书里的子章节。因此，模块有点类似于其他语言的命名空间。可以在crate根文件（crate root）定义一个新模块，还可以嵌套地定义模块。模块的作用如下：

避免所有的代码堆在一个文件里，将代码分组，提高可读性和重用性

提高命名空间（防止名字冲突）

控制可见性（模块内的项默认是私有的，通过pub可公开项）

## 2、模块声明方式

使用 **mod关键字** 声明模块，声明模块主要有两种方式：内联模块和文件/目录模块。

### （1）内联模块

直接在根crate文件或者模块文件里使用mod + 模块名 + {}的方式声明内联模块。

示例：

展开

自动换行

mod utils {

pub fn greet() {

println("Hello");

}

}

注：pub关键字用于greet函数对外可见

### （2）文件/目录模块

另一种方式是使用新文件定义模块。在当前的crate根文件或其他模块文件中仅仅声明模块。

示例：

展开

自动换行

mod utils;

例如，在当前根文件如main.rs中声明mod utils后，编译器回去找同级目录的utils.rs文件或者utils/mod.rs文件（旧版），然后将找到的文件中代码在此处声明的mod utils处展开。

进一步地，还可以进一步在utils.rs或utils/mod.rs中声明子模块：

展开

自动换行

mod greet;

此时，编译器回去找utils/greet.rs或utils/greet/mod.rs（旧版），以此类推。

🔉

Tips

Rust 2018+同时支持foo.rs和foo/mod.rs两种布局，但更推荐现在使用新式foo.rs布局。

在mod声明一个模块时，Rust编译器默认按照约定去当前目录寻找foo.rs或foo/mod.rs文件，来确定模块的代码来源。但有时候可能文件名和模块名不对应，但希望将该文件名作为模块的源码。此时可以在mod foo;前加上#\[path\]属性：

展开

自动换行

#\[path = "xxx.rs"\]

mod tricky;

但注意指定的路径是相对路径，例如在main.rs中定义mod tricky;时，此时的路径path是相对main.rs所在的目录而言的。

## 3、模块树

crate root（main.rs或lib.rs）称为根模块，其下是子模块、孙模块...。

例如，创建一个名为backyard的二进制crate，这里的main.rs就是模块树的根。而garden.rs为根模块下的子模块garden。在garden目录下的vegetables.rs是graden模块的子模块vegetables，也就是根模块的孙模块。

![](https://veditor.vivo.xyz/api/v1/attachment/file/BaElEpKgyHcBXiuEx4TkyxKSlvbFcqsaTKG3gLpA2DXUEs5vwWGMbTk9B3yFhRCT)

作为示例，编写一个餐厅功能的库crate。为了演示模块组织，仅仅定义函数的签名但函数体留空。

首先，创建一个restaurant的库crate：

展开

自动换行

cargo new restaurant --lib

然后在src/lib.rs中定义如下的模块和函数签名：

展开

自动换行

// 前台模块

mod front\_of\_house {

// 迎宾模块

mod hosting {

fn add\_to\_waitlist() {}

fn seat\_at\_table() {}

}

// 服务模块

mod serving {

fn take\_order() {}

fn serve\_order() {}

fn take\_payment() {}

}

}

整个模块树的树状结构如下：

展开

自动换行

crate

└── front\_of\_house

├── hosting

│ ├── add\_to\_waitlist()

│ └── seat\_at\_table()

└── serving

├── take\_order()

├── serve\_order()

└── take\_payment()

其中，front\_of\_house是根crate模块的子模块，而hosting和serving则是front\_of\_house的子模块。hosting和serving又称为兄弟模块。

## 4、路径

定义模块和模块中的项，其他地方需要使用将它们引入作用域并使用它们，此时需要指示从何处查找某个模块和项，这就需要路径了。

路径有两种形式：绝对路径和相对路径。绝对路径和相对路径都是由一个或多个双冒号::分隔的标识符。

### （1）相对路径

相对路径使用三种方式来表示相对方向：

不带前缀（默认从当前模块查找）

展开

自动换行

use my\_module::foo;

使用self（明确表示当前模块）

展开

自动换行

use self::my\_module::foo;

使用super（父模块）

展开

自动换行

use super::utils::helper;

从上一级模块导入utils::helper。使用super相对路径常常在测试模块中看到，后续介绍测试时会有一个认识。

### （2）绝对路径

绝对路径以crate或外部包名开头。

对于外部crate代码，是以外部crate名开头

示例：

展开

自动换行

serde::Serialize

对于当前crate的代码，是以字面值 **crate** 开头

示例：

展开

自动换行

crate::net::http:Client

仍然使用前面的restaurant库，这里简化一下模块以及项的层级，并添加一个新函数eat\_at\_restaurant()来演示如何使用绝对路径和相对路径。

展开

自动换行

// 前台模块

mod front\_of\_house {

// 迎宾模块

mod hosting {

fn add\_to\_waitlist() {}

}

}

fn eat\_at\_restaurant() {

// 绝对路径

crate::front\_of\_house::hosting::add\_to\_waitlist();

// 相对路径

self::front\_of\_house::hosting::add\_to\_waitlist();

}

但注意，此时的代码会报错，说hosting是私有的。

![](https://veditor.vivo.xyz/api/v1/attachment/file/0CLDujS9JPgJYaZEaH21VRwb_ZhU_Qul3nq8imcWWluRVfgs2SdRvWlsIpTt3UPw)

这涉及到模块内部的私有性规则，副父模块不能访问子模块的私有项。

## 5、模块内部私有性

模块内定义的项（函数、结构体、枚举等）默认对模块外部不可见。

模块父子可见性规则：

子模块可以访问父模块的私有项（可通过super指定路径）

父模块不能访问子模块的私有项

可以通过 **pub关键字** 使得模块或模块内部的项对外可见。

会到上例，这里加上pub关键字：

展开

自动换行

// 前台模块

mod front\_of\_house {

// 迎宾模块

pub mod hosting {

pub fn add\_to\_waitlist() {}

}

}

fn eat\_at\_restaurant() {

// 绝对路径

crate::front\_of\_house::hosting::add\_to\_waitlist();

// 相对路径

self::front\_of\_house::hosting::add\_to\_waitlist();

}

编译成功。

这里需要注意front\_of\_house没有加pub关键字，是因为eat\_at\_restaurant()和front\_of\_house属于兄弟关系，因此可以访问。

## 6、pub与受限可见性

### （1）pub关键字

上面已经对pub关键字有了一定认识。事实上，在Rust中，所有的项默认都是私有的，只能在当前模块的内部访问。如果想让外部模块访问，就需要使用pub关键字。pub关键字让项对其父模块可见，常用与公共API的导出。

### （2）受限可见性

受限可见性（Restricted Visibility）是指不是所有人都能访问，而是限制在一定范围内。使用pub(...)来限制可见性。

pub(crate)

作用：整个crate内部可见，但crate外部不可见。

用途：库内部模块之间相互访问，但不暴露给外部使用者。

示例：

展开

自动换行

mod inner {

pub(crate) fn helper() { }

}

pub fn api() {

// 在crate内部可以访问

inner::helper();

}

但如果是别的项目依赖这个crate：

展开

自动换行

// 外部项目

my\_crate::inner::helper();

就会编译报错。实际上可以在该package在创建一个src/main.rs（二进制crate）验证一下，发现二进制crate也访问不了helper()函数。

pub(super)

作用：只对父模块可见

用途：允许父模块调用，但不让更外层或兄弟模块使用。

pub(in path)

作用：只对指定路径（祖先模块）及其子模块可见

用途：更细粒度控制API可见性

示例：

展开

自动换行

mod net {

pub mod http {

pub(in crate::net) fn only\_for\_net() {

}

}

fn use\_http() {

http::only\_for\_net();

}

}

pub(in crate::net)表示对net模块及其子模块都可见。

### （3）结构体和枚举的可见性细节

结构体

对于结构体，其本身公开后，字段仍然默认私有。如果需要字段公开，需要给对应字段也加上pub。

枚举

对于枚举，其本身公开后，对应的变体也一并公开。

## 7、use

通过路径可以使用某个项，而use关键字提供了一个快捷方式，可以将路径引入当前作用域，然后就可以在当前作用域的任何地方使用更简短的名字了。

### （1）基本导入

示例：

展开

自动换行

use crate::net::http::Client; // 导入Client到当前作用域

// 等价于let c = crate::net::http::Client::new();

let c = Client::new();

### （2）重命名

使用 use... as... 可以重命名路径。

示例：

展开

自动换行

use std::io::Result as IoResult;

### （3）分组导入

通过{}可以导入多个项，每个项用逗号,隔开。

示例：

展开

自动换行

use std::{fmt, io};

use std::collections::{HashMap, HashSet};

use crate::net::{self, http::Client};

注意，\`self\`关键字表示将模块本身一并导入，上述第三条等价于：

展开

自动换行

use crate::net;

use crate::net::http::Client;

### （4）通配（glob）导入

使用通配符\*可以将模块内的所有公共项导入，但这种方式要谨慎使用，因为可能引入命名冲突。

示例：

展开

自动换行

use std::cmp::\*;

### （5）pub use重导出

当模块的层次较深，外部引用该模块的公共项时的路径就比较长，此时在模块中可以使用pub use重导出，将内部的实现结构隐藏，对外提供简洁路径。

示例：

展开

自动换行

pub mod net {

pub mod http {

pub struct Client;

}

}

pub use net::http::Client; // 此时，外部crate就可以直接使用\`my\_crate::Client\`

## 四、二进制crate和库crate的最佳实践

包可以同时包含一个二进制crate（src/main.rs）和一个库crate（src/lib.rs）。二进制crate只保留生成可执行文件的代码，调用库crate的功能。库crate可以被共享，可以被其他项目使用。

将模块树定义在库crate中，通过包名路径访问公有项。在二进制crate中，使用库crate提供的公有项。