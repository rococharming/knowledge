# 一、变量

## 1、变量的定义

在Rust中，使用 **let关键字** 定义变量。

示例：

```rust
// 定义一个变量 a
// 没有显式指定类型时，整数默认推断为 i32

let a = 10;
```

Rust 支持类型推导，但也可以显式指定变量类型，这称为**类型注解**。

示例：

```rust
// 显式指定变量a的类型为 u32（无符号 32 位整数）

let a: u32 = 10;
```

**如果定义了某个变量但实际没有使用，编译器会给出警告**：

![[Image 20.png|500]]

可以在变量名前加上下划线 `_`，告诉编译器这个变量是故意不使用的：

```rust
let _a: u32 = 10;
```

使用 **as关键字** 可以进行显式类型转换。

示例：

```rust
// 字面值 3.14 是 f64 ( 64 位浮点数)

// 使用 as 将其转换为 i32 

let a = 3.14 as i32;

println!("a = {}", a);

```

结果：

![[Image 21.png]]

这里的 `3.14` 被转换为 `i32` 后，小数部分会被截断，因此结果是 `3`。

## 2、变量命名规范

Rust中的变量名和函数名一般采用**蛇形命名法**（`Snake Case`），即：

- 所有字母小写
- 多个单词之间使用下划线 `_` 分隔。

示例：

```rust
let hello_world = "Hello, world";
```

后续会介绍的[[6、结构体|结构体]]、[[7、枚举|枚举]]、[[10、泛型和特征|Trait]] 等类型名，则通常采用**帕斯卡命名法**（`Pascal Case`），即每个单词首字母大写，单词之间不使用下划线。

示例：

```
struct UserInfo {}  
  
enum MessageType {}  
  
trait Readable {}
```

# 二、变量与不可变性

## 1、不可变性

Rust 中的变量默认是不可变的，也就是`immutable`。

示例：

```rust
fn main() {
    let a = 10;
    a = 20; // 错误：不能修改不可变变量
}
```

编译报错：`cannot assign twice to immutable variable`，即不可以对一个不可变变量赋值两次：

![[Image 22.png]]

Rust 的这种默认不可变设计，有助于减少意外修改变量带来的问题，也是 Rust 安全性设计的一部分。

## 2、mut关键字

如果希望变量可以被修改，需要使用`mut`关键字声明为可变变量。

示例：

```rust
let mut a = 10; // a可变
a = 20;
println!("a = {}", a);
```

这里的`a`使用了`mut`修饰，因此可以重新赋值。

# 三、变量遮蔽

**变量遮蔽**（shadowing），指的是**声明一个与已有变量同名的新变量**。新变量会覆盖旧变量，使得在当前作用域中访问这个名字时，访问到的是新变量。

示例：

```rust
fn main() {
    let x = 5;

    println!("x = {}", x); // 5

    let x = x + 1;   // 变量遮蔽

    println!("x = {}", x); // 6

    {
        let x = x * 2;  // 变量遮蔽

        println!("x = {}", x); // 当前作用域内 x 为 12
    }

    println!("x = {}", x); // 外层作用域 x 仍为 6
}
```

注意：`let x = x + 1`与`let x = x * 2`不是给旧的`x`重新赋值，而是创建了一个**新的变量**，并遮蔽了旧的`x`。
结果：

![[Image 23.png]]

变量遮蔽的常见用途之一是**复用变量名**：

示例：
```rust
fn main() {
    let spaces = "   ";  // &str 

    let spaces = spaces.len();  // usize

    println!("{}", spaces);
}
```

这里第一个 `spaces` 是字符串切片 `&str`，第二个 `spaces` 是 `usize` 类型的长度值。通过变量遮蔽，可以避免写成 `spaces_str`、`spaces_count` 之类较繁琐的名字。

变量遮蔽也可以改变变量的可变性，严格来说，并不是改变原变量的可变性，而是创建与原变量同值的新变量，但新变量可变。

示例：
```rust
let a = 1;

let mut a = a; // 现在新的变量a是可变的

a = 2;
```

这里第二个 `a` 是一个新的可变变量，它遮蔽了前面的不可变变量 `a`。

> 变量遮蔽的本质是创建了一个新的变量绑定，只是这个新变量与原变量同名。它不是对原变量重新赋值。


# 四、const常量与static变量

## 1、const常量

Rust使用 `const` 关键字定义**编译期常量**。

示例：

```rust
const SRCONDS_IN_HOUR: usize = 3_600;

const SECONDS_IN_DAY: usize = 24 * SECONDS_IN_HOUR;
```

`const`常量有几个特点：

- 必须**显式指定类型**
- 值必须是**编译期可计算的常量表达式**
- 常量名通常使用**全大写字母**，单词之间用下划线分割
- 不能被重新赋值
- 可以定义在模块级、函数内或更内层的块中

示例：

```rust
fn main() {  
	const MAX_POINTS: u32 = 100;  
  
	println!("{}", MAX_POINTS);  
}
```

`const` 更像是一个编译期符号，而不是一个运行时固定分配的变量。编译器通常会把 `const` 的值直接内联到使用处，因此它不保证在运行时一定有一个固定的内存地址。

还需要注意：

```rust
const NUM: i32 = 1;
const NUM: i32 = 2; // 错误：同一作用域内不能重复定义同名 const
```

同一作用域中不能重复定义同名 `const`。

## 2、static变量

`static`变量具有**固定内存地址**，并且在**程序的整个运行期间都存在**。它通过`static`关键字定义，**默认不可变**。

示例：

```rust
static NUM: i32 = 100;  
  
fn main() {  
	println!("{}", NUM);  
}
```

`static`特点：

- 必须**显式指定类型**
- 具有静态存储期
- 在整个程序中通常只有一个实例，对它的引用会指向同一个固定地址
- 默认不可变

和`const`不同，`static`不会被简单内联。它代表的是一个实际存在的静态存储位置。

`static`也可以定义为可变的：

```rust
static mut NUM: i32 = 100;
```

但是，`static mut` 很危险。因为它是全局可变状态，多个线程同时访问和修改时可能产生数据竞争，从而导致内存安全问题。

因此，读取或修改 `static mut` 都必须放在 `unsafe` 块中，有关`unsafe`详细见不安全的Rust。^unsafe

示例：

```rust
static mut NUM: i32 = 100;

fn main() {
    unsafe {
        NUM += 1;

        let value = NUM;

        println!("NUM: {}", value);
    }
}
```

这里先把 `NUM` 的值读取到局部变量 `value` 中，再打印 `value`。

因为直接打印`NUM`的值，在新版`Edition 2024`会报错：

```rust
static mut NUM: i32 = 100;  
  
fn main() {  
    unsafe {  
        println!("{}", NUM);  
    }  
}
```

![[Pasted image 20260512105425.png|400]]

这是因为对于`println!("{}", NUM)`，会在内部创建对`NUM`的共享引用，类似`&NUM`，而`Edition 2024`默认禁止对`static mut`创建共享引用。

如果只是全局整数计数器，不建议用 `static mut`，建议用原子类型或者使用 `Mutex`、`RwLock` 等同步原语。

> 需要注意：
> `unsafe`块并不是“让代码更安全”，而是告诉编译器：这部分代码的安全性由程序员自己负责。编译器会放宽部分检查，但不会保证`unsafe`代码块中的代码一定安全。

# 五、基本数据类型

Rust的基本数据类型两大类：

**标量类型：** 单个值，包括整型、浮点型、布尔型、字符型。

**复合类型：** 多个值组成的整体。Rust原生支持的符合类型主要有：数组和元组。

## 1、标量类型

### （1）整型

#### 1）整型类型

整型表示没有小数部分的数字。Rust 内置整型如下：

| 长度      | 有符号     | 无符号     |
| ------- | ------- | ------- |
| 8-bit   | `i8`    | `u8`    |
| 16-bit  | `i16`   | `u16`   |
| 32-bit  | `i32`   | `u32`   |
| 64-bit  | `i64`   | `u64`   |
| 128-bit | `i128`  | `u128`  |
| 架构相关    | `isize` | `usize` |
其中：

其中：

- `i` 表示 signed integer，也就是有符号整数；
- `u` 表示 unsigned integer，也就是无符号整数；
- `isize` 和 `usize` 的大小与平台架构相关，32 位平台上是 32 位，64 位平台上是 64 位；
- Rust 中数组、切片等集合的索引通常使用 `usize`。

默认情况下，整型字面量会被推断为 `i32`。

示例：

```rust
let a = 1; // 默认推断为 i32
```

也可以显式指定类型：

```rust
let a: u32 = 10;    // 显示指定为 u32 类型
```

或者使用类型后缀：

```
let a = 10u32;      // 显示指定为 u32 类型
```

整型字面量可以使用下划线 `_` 提高可读性：

```
let a = 1_000_000;
let b = 10_u32;
```

整型字面量也可以使用不同进制表示：

```rust
let a = 1_000;       // 十进制
let b = 0xffff_ffff; // 十六进制
let c = 0o12;        // 八进制
let d = 0b1110_0011; // 二进制
```

Rust 还为 `u8` 类型提供了**字节字符字面量**。

示例：

```rust
let a = b'A'; // a 的类型是 u8
```

这里的 `b'A'` 表示 ASCII 字符 `A` 对应的单字节值。如果不加 `b` 前缀：

```rust
let c = 'A';
```

那么 `c` 的类型是 `char`，而不是 `u8`。

需要注意：

> 字节字符字面量只能表示单个 ASCII 字符或字节转义，不能直接写非 ASCII Unicode 字符。


#### 2）整数溢出

整数类型都有固定的取值范围。例如：

- `u8`的范围是`0..=255`
- `i8`的范围是`-128..=127`

如果在编译期就能确定某个整数值超出了类型范围，编译器会直接报错。

但很多时候，溢出发生在运行时计算过程中。Rust 对运行时整数溢出的默认行为和**构建模式**有关：

- **调试构建**：检查整型溢出，溢出时触发 `panic`；
- **发布构建**：默认使用二进制补码回绕语义，也就是`warpping`。

不同构建模式的溢出行为不同，为了让溢出行为更明确，Rust提供了几类常用方法：
##### i）检查算法（checked方法）

`checked_xxx`会返回`Option<T>`：

- 没有溢出，返回`Some(value)`
- 发生溢出，返回`None`

> `Option<T>`是Rust常用枚举类型，表示有值还是无值。

示例：

```rust
fn main() {
    let a: u8 = 254;

    println!("{:?}", a.checked_add(1)); // Some(255)
    println!("{:?}", a.checked_add(2)); // None
}
```

![[Pasted image 20260512112850.png]]

检查算法适用于“宁可显式失败，也不要错误结果”的安全计算场景。

##### ii）回绕算法（wrapping方法）

`wrapping_xxx`会在发生溢出时强制按补码规则回绕。

示例：

```rust
fn main() {  
    let a: u8 = 254;  
    println!("{:?}", a.wrapping_add(1));  
    println!("{:?}", a.wrapping_add(2));  
}
```

![[Pasted image 20260512112943.png]]

回绕算法适合明确需要模运算的场景，例如哈希、加密、循环计数等。

##### iii）饱和算法（saturating方法）

`saturating_xxx`在发生溢出时，将结果 **钳制（clamp）到类型边界** ，不会回绕。

示例：

```rust
fn main() {
    let a: u8 = 254;

    println!("{}", a.saturating_add(1)); // 255
    println!("{}", a.saturating_add(2)); // 255
}
```

![[Pasted image 20260512113109.png]]

饱和算法适合音视频、图像处理、计数上限等不希望回绕的场景。
##### iv）溢出算法（overflowing方法）

`overflowing_xxx`会返回一个二元组`(result, overflowed)`，其中`result`是结果值，而`overflowed`是布尔类型的值，表示是否发生溢出（溢出为true，否则为false）。

示例：

```rust
fn main() {
    let a: u8 = 254;

    println!("{:?}", a.overflowing_add(1)); // (255, false)
    println!("{:?}", a.overflowing_add(2)); // (0, true)
}
```

![[Pasted image 20260512113323.png]]

溢出算法适用于既想得到结果、又想知道是否发生溢出的场景。

### （2）浮点型

Rust 提供两种浮点类型：

- `f32`：32 位单精度浮点数；
- `f64`：64 位双精度浮点数。

它们大致对应 C / C++ 中的 `float` 和 `double`，并遵循 IEEE 754 浮点标准。

浮点数字面量通常由整数部分、浮点部分、指数部分以及类型后缀组成，如下图所示：

![[Image 24.png|200]]

其中浮点部分、指数部分、类型后缀都是可选的。但要让它识别为浮点数字面量，一般需要满足下面任一条件：

- 带小数点（如2.、3.14）
- 带指数（如1e-3、12E+99）
- 使用浮点后缀（如5f32）

> `5.` 是有效的浮点数字面量。

示例：

```rust
let x = 2.0; // 默认推断为 f64  
let y: f32 = 3.14;
```

**如果没有显式指定类型，浮点数字面量默认推断为 `f64`。

`f32` 和 `f64` 不仅表示普通小数，还支持 IEEE 754 浮点标准中的一些特殊值，例如：

```rust
let a = f32::INFINITY;           // 正无穷大
let b = f64::NEG_INFINITY;       // 负无穷大
let c = f64::NAN;                // Not a Number，非数值
```

这些特殊值常见于浮点计算中的异常或边界情况。

例如，正数除以 `0.0` 可能得到正无穷大：

```rust
fn main() {
    let x = 1.0 / 0.0;

    println!("{}", x); // inf
}
```

`NAN` 表示“不是一个有效数字”，常见于无意义的数学运算，例如：

```rust
fn main() {
    let x = f64::NAN;

    println!("{}", x); // NaN
}
```

需要特别注意：`NAN` 有一个比较反直觉的特性，它不等于任何值，包括它自己。

```rust
fn main() {
    let x = f64::NAN;

    println!("{}", x == x); // false
}
```

因此，判断一个浮点数是否为 `NaN`，不能使用 `==`，而应该使用 `is_nan()` 方法：

```rust
fn main() {
    let x = f64::NAN;

    println!("{}", x.is_nan()); // true
}
```

除了 `INFINITY`、`NEG_INFINITY` 和 `NAN`，`f32` / `f64` 还提供了一些与取值范围相关的关联常量，例如：

```rust
fn main() {
    println!("{}", f64::MAX); // f64 能表示的最大有限值
    println!("{}", f64::MIN); // f64 能表示的最小有限值，也就是最负的有限值
}
```

这里需要注意，`f64::MIN` 不是“最接近 0 的正数”，而是 `f64` 能表示的**最小有限值**，也就是一个非常大的负数。

如果要表示最小的正正规数，可以使用`f64::MIN_POSITIVE`。

> 新代码中，推荐使用原生类型上的关联常量，例如：`f32::INFINITY`，而不是旧式入口：`std::f32::INFINITY`。

数学常量则放在 `std::f32::consts` 和 `std::f64::consts` 模块中，例如圆周率 `PI`、自然常数 `E` 等。

```rust
fn main() {
    let pi = std::f64::consts::PI;
    let e = std::f64::consts::E;

    println!("pi = {}", pi);
    println!("e = {}", e);
}
```

### （3）布尔类型

Rust的布尔类型是`bool`，只有两个取值：

- `true`
- `false`

示例：

```rust
let x = 1 < 2;   // true

let y: bool = false;
```

**Rust 不会像 C / C++ 那样把整数、指针等隐式转换为布尔值**。

错误示例：

```rust
let x = 1;

if x {
    println!("true");
}
```

正确写法：

```rust
let x = 1;

if x != 0 {
    println!("true");
}
```

Rust 允许将 `bool` 使用 `as` 转换为整数：

```rust
let a = true as i32;  // 1
let b = false as i32; // 0
```

但不允许把整数直接转换为 `bool`：

```rust
let x = 1 as bool;   // 错误
```

虽然布尔值理论上只需要 1 bit，但 Rust 中 `bool` 的大小是**1 字节**。

### （4）字符类型

Rust中`char`类型占 **4** 个字节，表示一个Unicode标量值 。因此，无论是英文字母、汉字，表情符号等，都可以用`char`类型表示。字符字面值使用单引号 **' '** 括起来。

示例：

```rust
fn main() {
    let c = 'z';

    let z: char = '中';

    let smile = '😊';
}
```

Rust 中的 `char` 表示单个 Unicode 标量值，而 `String` 和 `&str` 使用 UTF-8 字节序列存储文本，即 `String` 和`&str`的内部表示的是UTF-8编码的字节数组。因此，Rust 不允许直接用整数下标访问字符串中的第 n 个字符。

例如，下面这种写法是错误的：

```rust
let s = "hello";
let c = s[0]; // 错误
```

因为 UTF-8 字符的字节长度不固定，按下标取字符并不是简单的 O(1) 操作。

## 2、size_of 和 size_of_val




**size_of和size_of_val都是const fn（常量函数），这意味着它们可在编译期求值** 。其中 size_of::<T>() 对给定类型 T 的结果通常是编译期已知的，而 size_of_val 在遇到 DST（动态大小类型）时会依赖运行时的元数据计算实际大小。

**std::mem::size_of::<T>()返回类型T所占内存大小（字节数）** ，T的类型必须是实现了Sized特征的类型，关于特征后续会详细介绍。

示例：

```rust
fn main() {

println!("{}", size_of::<i32>()); // 4

println!("{}", size_of::<char>()); // 4

println!("{}", size_of::<bool>()); // 1

}
```
**std::mem::size_of_val::<T:?Sized>(val: &T)** 返回的是val所借用的那个值（即*val）在内存中占用的字节数，而不是引用&T本身的大小。

若T: Sized，结果等同于size_of::<T>()

若T是DST（如str、[T]、trait object），则&T是胖指针，携带长度或vtable等元数据。size_of_val会利用这些元数据在运行时计算*val的实际大小。

若想获得引用/指针本身的大小，应使用size_of::<&T>()，或者对引用再取一次引用：size_of_val(&val)

示例：
```rust
let x: i32 = 5;

println!("{}", size_of_val(&x)); // 获取x所占内存的大小 4

let s: &str = "hello";

// s本身引用，且&str是胖指针，实际得到的大小就是str字符串内容的UTF-8字节数

println!("{}", size_of_val(s)); // 5

// 获取&str这个胖指针的字节数 64位平台，胖指针就是16字节

println!("{}", size_of_val(&s)); // 16
```

## 3、复合类型

### （1）数组

数组中的每一个元素类型必须相同。数组一旦定义，长度必须固定，不能增减（长度是类型的一部分）。

定义数组使用 **[]** ，将数组的值写到[]中并用,隔开。

数组的类型为 **[元素类型;元素个数]** ，例如[u32;5]是包含5个u32类型值的数组。

示例：

```rust
let arr1 = [1, 2, 3, 4, 5]; // [i32; 5]

let arr2: [f64; 3] = [1.0, 2.0, 3.0]; // [f64; 3]

let arr3 = [10; 3]; // 快捷写法，定义一个长度为3，值都为10的数组

println!("arr1: {:?}", arr1);

println!("arr2: {:?}", arr2);

println!("arr3: {:?}", arr3);
```
结果：

![[Image 25.png]]

**注意：对于println!格式化输出，{}、{:?}、{:#?}分别表示不同的含义**

<table><colgroup><col> <col> <col></colgroup><tbody><tr><th colspan="1" rowspan="1"><p>写法</p></th><th colspan="1" rowspan="1"><p>Trait要求</p></th><th colspan="1" rowspan="1"><p>用途</p></th></tr><tr><td colspan="1" rowspan="1"><p>{}</p></td><td colspan="1" rowspan="1"><p>Display</p></td><td colspan="1" rowspan="1"><p>用户友好，常规输出</p></td></tr><tr><td colspan="1" rowspan="1"><p>{:?}</p></td><td colspan="1" rowspan="1"><p>Debug</p></td><td colspan="1" rowspan="1"><p>开发调试，快速查看</p></td></tr><tr><td colspan="1" rowspan="1"><p>{:#?}</p></td><td colspan="1" rowspan="1"><p>Debug</p></td><td colspan="1" rowspan="1"><p>开发调试，美化(多行缩进）输出</p></td></tr></tbody></table>

有关Trait的概念后续介绍，这里需要知道：打印数组通常用{:?}，因为数组没有实现Display trait。

在后面介绍结构体时，可以直观比较{:?}和{:#?}的区别。一般来说，{:#?}会多行输出结构体的每一个字段且加上缩进，而{:?}则是单行输出。

访问数组元素时，通过 **索引值** 来访问。数组索引值可以是变量。

示例：
```rust
fn main() {

let arr = [1, 2, 3, 4, 5];

let first = arr[0];

let second = arr[1];

println!("first: {}", first);

println!("second: {}", second);

}
```
**注意：索引值不能大于等于数组长度**

若代码中出现明显超出范围的索引（例如常量索引），编译器在编译期间就会报错。

若索引在运行时才确定（例如用户输入），当索引超出范围会触发运行时检查，程序会panic。
### （2）元组

不同于数组，元组中的每个元素可以是不同类型。元组一旦定义，长度同样固定不可变。

定义元组使用 **()** ，并将不同的值用,分隔。

元组的类型为 **(元素类型1，元素类型2，...)** ，例如(u32, f64)。

示例：

```rust
let tup1 = (10, 3.14); // (i32, f64)

let tup2: (bool, char) = (true, 'A');

println!("tup1: {:?}", tup1);

println!("tup2: {:?}", tup2);
```
结果：

![[Image 26.png]]

访问元组元素通过**.索引** 的方式进行，但这里的索引必须是编译期常量（如.0、.1）。

示例：
```rust
fn main() {

let tup = (10, 3.14);

println!("{}, {}", tup.0, tup.1);

}
```
此外，还可以使用 **模式匹配解构元组** 。

示例：
```rust
fn main() {

let tup = (10, 3.14);

let (x, y) = tup; // 模式匹配解构

println!("x: {}", x);

println!("y: {}", y);

}
```
**如果元组没有内容，则称它为单元元组（unit tuple），也称空元组** 。 **单元元组的类型和值都是()** ，常用于表示没有有意义的返回值。后面介绍函数时， **如果函数体最后没有返回表达式（或以;结尾），默认返回()** 。

示例：

![[Image 27.png]]
# 四、控制流

控制流用于控制程序的执行顺序：根据条件的真假决定是否执行某段代码，或根据条件反复执行一段代码。

## 1、条件分支

使用 **if 条件判断** ，根据条件执行不同分支。

（1）if-else

示例：

```rust
fn main() {

let age: u8 = 10;

if age < 18 {

println!("You are young!");

} else {

println!("You are old!");

}

}
```
注意事项：

Rust的if表达式不需要括号()，这和C/C++不同

if表达式的条件必须是bool表达式，不可以像C/C++使用整数等替代

（2）if - else if - else

当条件较多时，可以使用if - else if - else链式分支。

示例：
```rust
fn main() {

let score: u32 = 70;

if score >= 90 {

println!("Got A");

} else if score >= 80 {

println!("Got B");

} else if score >= 70 {

println!("Got C");

} else {

println!("Got D");

}

}
```
## 2、循环

Rust有三种循环结构： **loop、while和for** 。

### （1）loop

loop是无限循环，循环体会反复执行，直到遇到break退出；continue则用于跳过本次循环剩余部分，进入下一次循环。

示例（注意下面这个循环不会结束）：

```rust
fn main() {

let a = 10;

loop {

println!("{}", a);

}

}
```
### （2）while

while是条件循环：当条件为真时执行循环体。while与loop的区别在于，while在每次循环前会检查布尔表达式。

示例：

```rust
fn main() {

let mut n = 10;

while n > 0 {

println!("{}", n);

n -= 1;

}

}
```
### （3）for

**for循环常用于迭代范围或集合** 。使用for可以避免手动索引，更简洁也更安全。

示例：

```rust
fn main() {

// 遍历范围，这里的0..5不含5，若写成0..=5则含5

for i in 0..5 {

println!("i = {}", i);

}

// 遍历数组

let arr = [1, 2, 3, 4, 5];

for val in arr {

println!("val = {}", val);

}

// 反向遍历

for i in (0..=5).rev() {

println!("i = {}", i);

}

}
```
注意：

start..end表示start到end-1的范围（左闭右开）

start..=end表示start到end的范围（左闭右闭）
### (4）循环标签

循环可以嵌套，break或continue默认作用于当前循环。

Rust支持 **循环标签（loop label）** 来指定跳出/继续哪一层循环，语法是通过 **'标签名:**标注循环。

示例：

```rust
fn main() {

'out_loop: for i in 0..3 {

for j in 0..3 {

if i == 1 && j == 1 {

break 'out_loop;

}

println!("i = {}, j = {}", i, j);

}

}

}
```
结果：

![[Image 28.png]]

如果没有循环标签，那么当i == 1且j == 1退出的是内层循环，外层循环仍然会继续，从i = 2开始打印。
# 五、函数

## 1、表达式和语句

在介绍函数之前，需要了解表达式（expression）和语句（statement）的概念。Rust具有明显的“表达式语言”特征：函数体通常由若干语句组成，并且可以以一个表达式作为最后的求值结果（常见写法是最后一行不加分号来返回值）。

语句会执行操作但不产生可用的值；表达式会求值并产生一个值。

示例：

```rust
let x = x + 1; // 语句1

let y = y + 1; // 语句2

x + y // 表达式（若作为块的最后一行，可作为块的返回值）
```
### （1）语句

语句完成一个具体操作，但不产生一个可被继续使用的值。例如let绑定的就是语句：

```rust
let a = 8;
```
由于let是语句，因此不能将let语句赋值给其他值，下面的语法是错误的：
```rust
let b = (let a = 8);
```
### （2）表达式

表达式会求值并返回一个值。例如 5 + 6会得到11， 5 + 6就是一个表达式。表达式也可以成为语句的一部分，例如let a = 6，6就是一个表达式。

**函数调用是表达式** （会产生一个值，哪怕是()）。 **宏调用在语法上也通常作为表达式使用** 。使用 **花括号{}包裹的代码如果最后产生一个值，那么整个代码块也是表达式** 。简而言之， **能产生值（哪怕是 ()）的，通常都可以看作表达式** 。

示例（把语句块当作表达式赋值给变量）：

```rust
fn main() {

let y = {

let x = 3;

x + 1

};

println!("The value of y is: {}", y);

}
```
上面赋值给 y 的语句块是
```rust
{

let x = 3;

x + 1

}
```
注意：如果最后的 x + 1 加上; 变成语句，那么该语句块返回 ()。

**if语句块也是表达式** ，因此可以用于赋值。

示例：
```rust
let x = 11;

let res = if x % 2 == 1 { "odd" } else { "even" };
```
**loop循环也是表达式** ，在break后可以跟一个表达式作为loop的返回值：

示例：
```rust
fn main() {

let mut count = 0;

let result = loop {

count += 1;

if count == 5 {

break count * 2;

}

};

println!("result: {}", result);

}
```
## 2、函数

### （1）函数定义和调用

在 Rust 中使用 **fn 关键字** 定义函数。Rust 程序的入口函数是 main：

```rust
fn main() {

println!("Hello, world!);

}

函数用于把可复用逻辑封装起来以便多次调用。

示例：
```
```text
fn add(x: i32, y: i32) -> i32 {

x + y

}
```
上面的函数实现了两个 i32 的加法：fn 后是函数名 add，括号里是参数列表并 **标注类型** ，-> i32 指定返回类型。

有了函数定义，就可以调用函数了：
```rust
fn main() {

println!("1 + 2 = {}", add(1, 2));

}

fn add(x: i32, y: i32) -> i32 {

x + y

}
```
**注意：Rust不要求先声明再定义，函数可以写在调用之后（编译器会在同一模块范围内解析）**
### （2）函数参数

函数可以有参数。参数是一种特殊变量，属于函数签名的一部分。 **函数签名通常指：函数名、参数列表、返回类型** ，例如fn add(x: i32, y: i32) -> i32。

多个参数用逗号分隔。函数定义里参数称为形参（parameters），调用时传入的具体值叫做实参（arguments）。

示例：

```rust
fn get(x: u32, y: u32) { // x和y为形参

println!("Got x: {x}, y: {y}");

}

fn main() {

get(10, 20); // 10和20为实参

}
```
注意：

函数参数必须写类型注解，否则编译器无法确定参数类型与大小，编译会失败；同时函数对外可用也需要清晰的类型信息

Rust的实参传递给形参时不会自动做数值类型转换（例如u32不能自动当成i32）
### （3）函数返回值

函数可以有返回值。在参数列表后使用→指定返回类型。

示例：

```text
fn add_one(x: i32) -> i32 {

x + 1

}
```
注意：

若函数体最后一行是表达式（不以;结尾），该表达式的值会作为返回值

若函数体最后一行是语句（以;结尾），函数会隐式返回()

使用 **return关键字** 可以提前返回值

如果返回类型是()，函数签名可以省略 → ()。
# 六、注释

## 1、Rust注释分类

注释用于解释代码，帮助人类理解程序逻辑。编译器在编译时会忽略注释内容。 **Rust 的注释除了常规的代码注释外，还支持文档注释，可以被 rustdoc 解析并生成 API 文档** 。

Rust注释主要分为： **行注释、块注释、文档注释** 。

## 2、行注释

行注释（line comment）使用 **//** 开头，从 // 开始到行尾的内容都会被编译器忽略，适合简短说明。

示例：

```rust
// 这是一个行注释

let x = 5; // 这是另一个行注释，跟在代码后面
```
## 3、块注释

块注释（block comment）使用/*... */包裹，可以跨多行，也可以写在同一行内，适合临时屏蔽一段代码或写较长说明。

示例：

```text
/*
```
这是一个块注释。

它可以跨越多行

*/

let y = 10; /* 也可以这样写在同一行 */

值得注意的是：和C/C++不同， **Rust的块注释支持嵌套** 。

示例：
```text
/* 外层注释

/* 内层注释 */

*/
```
**这在调试时很有用，可以安全地注释掉“内部本身包含注释”的代码块。**
## 4、文档注释

当查看一个 [crates.io](http://crates.io/) 上的库时，通常会看到它的在线API文档，如下所示。这类文档通常就是通过 **文档注释（documentation comment）** 生成的。 **Rust提供专门的注释形式供rustdoc解析，并生成HTML文档** 。 **执行cargo doc会在底层调用rustdoc来生成文档** 。

![[Image 29.png]]

文档注释常见分为： **项（item）文档注释与模块/crate文档注释** 。

### （1）行文档注释（项文档注释）

使用 **///** ，用于为其下方的项（item，例如函数、结构体、枚举、Trait、常量、静态变量等）添加文档注释。

示例：

```rust
/// `add_one` 将指定值加1

///

/// # Examples

///

/// ```

/// let arg = 5;

/// let answer = add_one(arg);

/// assert_eq!(6, answer);

/// ```

pub fn add_one(x: i32) -> i32 {

x + 1

}
```
注意：

文档注释使用Markdown语法，例如上述的 **# Examples** 标题、 **``` ```** 代码块

示例中的代码块会被rustdoc作为文档示例展示，并且可以作为 **文档测试（doctest）** 运行，后续介绍测试再展开。

被注释的项不一定必须是pub才能写文档注释，只是非pub的项在默认生成的公开API文档里通常不会显示（除非生成私有项文档或使用相关开关）
### （2）块文档注释（项文档注释）

使用 **/**... */** 增加块文档注释，作用等价于///，只是写法不同。 **实际项目中更常用///，因为更直观，可读性更好** 。

### （3）行文档注释（模块 / crate文档注释）

也称内部文档注释，使用 **//!**。 **它注释的对象不是紧随其后的某个item，而是所在的模块或crate本身。** 通常写在文件顶部（为crate写说明），或写在mod的花括号内部（为模块写说明）。

示例：

```rust
//! This crate provides some mathematical utility functions.

mod math {

}
```
### （4）块文档注释（模块 / crate文档注释）

与//!对应的块式内部文档注释是/*!... */，用法相同，但也相对少见。

## 5、查看文档注释

编写好文档注释后，在项目目录执行 **cargo doc** 命令：

```bash
cargo doc
```
这会在项目的 **target/doc** 目录下生成HTML文件。

为了方便起见，可以直接加上 **--open** 参数，生成后自动在浏览器打开：
```bash
cargo doc --open
```
示例：

![[Image 30.png]]

在生成的文档中，//!对应的是模块/crate级别的说明（通常显示在页面顶部）。

可以看到定义的函数，可以点击add进去：

![[Image 31.png]]

这块内容就是使用 /// 编写的项注释。其中的Examples就是用Markdown语法#生成的一级标题。

文档中常见的一些小标题（惯例）包括：

# Examples：示例用法（最常用）

# Panics：哪些情况可能panic!，便于调用者规避

# Errors： 若函数返回Result，列出可能的错误及触发条件

# Safety：若涉及unsafe代码，说明调用者必须满足的前置条件

...

注意：这些标题是社区惯例而非语法要求，可以使用中文标题，但建议遵循团队规范与一致性。
