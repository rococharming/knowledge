# 一、变量

## 1、变量的定义

在Rust中，使用 **let关键字** 定义变量。

示例：

```rust
// 定义一个类型为i32（默认，有符号32位整数）的变量

let a = 10;
```
注意事项：

Rust支持类型推导，但也可以显式指定变量类型（或称 **类型注解** ）

示例：
```rust
// 显式指定变量a的类型为u32（无符号32位整数）

let a: u32 = 1;
```
如果定义了某个变量但实际没有使用，编译器会给出警告。可以在变量前加上 **下划线\_** 告诉编译器忽略警告。

示例：

![[Image 20.png]]

修改：
```rust
let \_a: u32 = 10;
```
使用 **as关键字** 可以进行强制类型转换

示例：
```rust
// 字面值3.14是f64(64位浮点数)

// 使用as关键字转换为i32类型，因此a为i32类型

let a = 3.14 as i32;

println!("a = {}", a);
```
结果：

![[Image 21.png]]

输出a = 3，原先的浮点数字面值由于强制类型转换被截断了。

🔉

变量命名规范

**Rust变量以及函数名均采用蛇形命名法（Snake Case），即字母小写，若包含多个单词用下划线隔开。**

示例：

let hello\_world = "Hello, world"; // 定义一个类型为&str的变量hello\_world

**对于后面会介绍的结构体、枚举、Trait定义，则采用帕斯卡命名法（Pascal Case），即每个单词首字母大写，其余小写，单词之间无下划线隔开。**
## 2、变量与不可变性

### （1）不可变性

**Rust中的变量默认是不可变的（immutable）的** 。这种不可变性是Rust实现可靠性和安全性的关键之一。

示例：

```rust
let a = 10;

a = 20; // 错误
```
编译报错：cannot assign twice to immutable variable，即不可以对一个不可变变量赋值两次。

![[Image 22.png]]

Rust的编译器比较强大，在编译报错的同时会给出可能的修改意见，例如这里给出使用 **mut关键字** 修饰变量a使其可变。
### （2）mut关键字

Rust中使用 **mut关键字对变量进行可变声明** ，这样变量就可以修改了。

示例：

```rust
let mut a = 10; // a可变

a = 20;
```
## 3、变量遮蔽

**变量遮蔽（shadowing）** 不是指对一个变量重新赋值，而是 **声明一个与现有变量同名的新变量** ， **同时会隐藏原来同名的变量（但该变量仍然存在）** 。

示例：

```rust
fn main() {

let x = 5;

println!("x = {}", x); // 5

let x = x + 1; // 变量遮蔽，新的x遮蔽旧的x

println!("x = {}", x); // 6

//注： {}内会生成一个内部作用域

{

let x = x \* 2; // x在作用域里再次被遮蔽

println!("x = {}", x); // 12

}

// 内部作用域结束，外层的x不再被遮蔽，此时x为6

println!("x = {}", x);

}
```
结果：

![[Image 23.png]]

从上述的例子可以看出，变量遮蔽的作用之一是—— **当我们在内部作用域不需要使用外部的某个变量时，可以使用变量遮蔽** 。同时，使用变量遮蔽还可以 **复用变量名而不用为起变量名而烦恼** 。

示例：
```rust
fn main() {

let spaces = " "; // spaces为&str类型

let spaces = spaces.len(); // 变量遮蔽，此时spaces是usize类型

println!("{}", spaces);

}
```
这里统计空格的个数，使用spaces直接遮蔽前面的spaces，这样就不必起繁琐的诸如spaces\_str和spaces\_count来区分不同的变量了。

变量遮蔽还可以 **增加可变性** 。

示例：
```rust
let a = 1;

let mut a = a; // 现在新的变量a是可变的
```
这在函数参数中常常使用。

**变量遮蔽的本质是内存的再次分配，创建了一个新的变量，只不过该变量与原来的变量同名，对原来的变量进行了“遮蔽”** 。
# 二、const常量与static变量

## 1、const常量

Rust使用 **const关键字** 定义编译期常量，其值必须是 **编译时可计算的常量表达式** 。

const更像是一个 **编译期就确定下来的值/符号** ， **而不是运行时分配、可变的变量** ，它不可以被重新赋值。

示例：

```text
const SECONDS\_IN\_HOUR: usize = 3\_600;

const SECONDS\_IN\_DAY: usize = 24 \* SECONDS\_IN\_HOUR;
```
注意事项：

**const常量在定义时必须显式指定类型** （例如上述的usize）

常量名一般大写，单词之间用下划线隔开

const是 **项（item）** ，但允许出现在模块级、函数内甚至更内层的块中，其可见性/可用范围由其所在作用域和可见性规则决定。

**const不保证在运行时有固定的内存地址，编译器通常会把它的值直接内联到使用处** 。即使对同一个const取引用，不同使用点也不保证指向同一地址（甚至可能根本不分配独立存储）。

变量可以进行遮蔽，但 **const常量同一作用域内不能使用相同名字重复定义** 。
## 2、static变量

static变量是具有 **固定内存地址** 、在程序的整个运行期间都存在的静态存储。通过 **static关键字** 定义，static **默认是不可变的** 。

示例：

```rust
static NUM: i32 = 100; // static变量
```
注意：

和const关键字一样，定义static变量 **必须显式指定类型**

static不会被内联。 **在整个程序中，某个static变量只有一个实例，所有引用都会指向同一地址** 。

和const常量不同的是，static变量可以定义为 **可变的（mut）** ，定义方式如下：
```rust
static mut NUM: i32 = 100;
```
因为static mut允许被修改，可能存在多个线程同时访问并修改而引发数据竞争，从而导致内存不安全问题。因此，对static mut的读取与写入都必须放在 **unsafe块** 中。

🔊

unsafe

**需要注意，unsafe块只是允许绕过编译器的部分检查并通过编译，但不再由编译器保证该块内的内存安全，正确性需要程序员自己保证** 。

示例：
```rust
static mut NUM: i32 = 100;

fn main() {

unsafe {

// 修改

NUM += 1;

// 读取

println!("NUM: {}", NUM);

}

}
```
**上述代码在Edition 2021还可以通过，但在Edition 2024下，编译器更严格禁止从static mut派生出共享引用（即使只是为了打印）** ，因此应该使用 **std::ptr:addr\_of! / addr\_of\_mut!**获取原始指针再进行读写，或更推荐使用 **线程安全的全局状态方案** （如Atomic\*、Mutex/RwLock等）来替代static mut。
# 三、基本数据类型

Rust的基本数据类型分为 **标量类型** 和 **复合类型** 。

**标量类型：** 单独一个值的类型，包括整型、浮点型、字符型和布尔型。

**复合类型：** 将多个值组合成一个整体的类型。Rust有两种原生复合类型——数组和元组。

## 1、标量类型

### （1）整型

#### 1）整型类型

整型是指没有小数的数字。下表给出了Rust内置的整型类型。

<table><colgroup><col> <col> <col></colgroup><tbody><tr><th colspan="1" rowspan="1"><p>长度</p></th><th colspan="1" rowspan="1"><p>有符号</p></th><th colspan="1" rowspan="1"><p>无符号</p></th></tr><tr><td colspan="1" rowspan="1"><p>8-bit</p></td><td colspan="1" rowspan="1"><p><code>i8</code></p></td><td colspan="1" rowspan="1"><p><code>u8</code></p></td></tr><tr><td colspan="1" rowspan="1"><p>16-bit</p></td><td colspan="1" rowspan="1"><p><code>i16</code></p></td><td colspan="1" rowspan="1"><p><code>u16</code></p></td></tr><tr><td colspan="1" rowspan="1"><p>32-bit</p></td><td colspan="1" rowspan="1"><p><code>i32</code></p></td><td colspan="1" rowspan="1"><p><code>u32</code></p></td></tr><tr><td colspan="1" rowspan="1"><p>64-bit</p></td><td colspan="1" rowspan="1"><p><code>i64</code></p></td><td colspan="1" rowspan="1"><p><code>u64</code></p></td></tr><tr><td colspan="1" rowspan="1"><p>128-bit</p></td><td colspan="1" rowspan="1"><p><code>i128</code></p></td><td colspan="1" rowspan="1"><p><code>u128</code></p></td></tr><tr><td colspan="1" rowspan="1"><p>架构相关</p></td><td colspan="1" rowspan="1"><p><code>isize</code></p></td><td colspan="1" rowspan="1"><p><code>usize</code></p></td></tr></tbody></table>

注意：

i表示有符号，u表示无符号。

isize和usize的位数和计算机系统的架构相关，亦即地址空间的大小。对于32位机器就是32位，对于64位机器就是64位。 **Rust要求数组的索引必须是usize** 。

**默认情况下，整型字面量值类型为i32** ，例如let a = 1，此时编译器推断a为i32类型。

除了let a: u32 = 10这种显式类型注解外，还可以在整型字面值后加 **类型后缀** 指定类型。例如let a = 10u32。

整型字面量可通过 **\_分隔符** 提高可读性，例如let a = 1\_000\_000，let a = 10\_u32等。

整型字面值可以用不同的进制数表示，通过 **进制前缀（0b二进制，0o八进制、0x十六进制）** 表示。

示例：

```rust
let a = 1\_000; // 十进制

let b = 0xffff\_ffff; // 十六进制

let c = 0o12; // 八进制

let d = 0b1110\_0011; // 二进制

Rust为 **u8类型** 提供了 **字节字符字面量** ： **以b为前缀、用单引号包裹的单个字符（如b'A'）** 。该字面量表示一个单字节，因此内容必须是ASCII字符（或相应的字节转义），不能直接包含非ASCII的Unicode字符。
```
示例：
```rust
let a = b'A'; // a的类型为u8
```
注： **这里的'A'前面加上b前缀，如果不加，'A'默认是char类型。在Rust中，char类型占4个字节，采用Unicode编码** 。
#### 2）检查算法、回绕算法、饱和算法和溢出算法

整型类型都有固定的取值范围，例如u8的范围为0～255，i8的范围为-128~127。 **在编译期即可确定的常量表达式如果超出范围，Rust编译器会直接报错** 。

**但很多时候，整数本身在定义时是合法的，溢出发生在运行时计算过程中** 。此时 **Rust的默认行为与构建模式有关** ：

**调试构建（debug）** ：对整数溢出进行检查，溢出时触发 **panic** （在Rust中，程序崩溃的术语称为panic）

**发布构建（release）** ：默认采用二进制补码回绕 **（wrapping）** 语义（即按模运算回绕）。例如u8，255 + 1 == 0，255 + 2 == 1，依次类推。

不同构建行为不同，为了让行为更统一、并显式表达希望如何处理溢出，Rust为整数类型提供了四种常用方法（以xxx表示具体运算如add/sub/mul等）。

##### i）检查算法（checked\_xxx）

checked\_xxx会返回一个 **Option<T>** （Option是常用枚举类型，其中的变体Some(v)表示有值，None表示无值）：

如果没有溢出，返回Some(v)

如果溢出，返回None

示例：

```rust
fn main() {

let a: u8 = 254;

// 有溢出返回None

println!("{:?}", a.checked\_add(1)); // Some(255)

println!("{:?}", a.checked\_add(2)); // None

}
```
检查算法适用于“宁可显式失败，也不要错误结果”的安全计算场景。
##### ii）回绕算法（wrapping\_xxx）

wrapping\_xxx会在发生溢出时强制按补码规则回绕。

示例：

```rust
fn main() {

let a: u8 = 254;

// 有溢出返回强制回绕

println!("{:?}", a.wrapping\_add(1)); // 255

println!("{:?}", a.wrapping\_add(2)); // 0

}
```
回绕算法适用于明确需要“像时钟一样循环计数”、或实现哈希/加密等依赖模运算的场景。
##### iii）饱和算法（saturating\_xxx）

saturating\_xxx在发生溢出时，将结果 **钳制（clamp）到类型边界** ，不会回绕。

示例：

```rust
fn main() {

let a: u8 = 254;

// 有溢出保持饱和边界值不变

println!("{:?}", a.saturating\_add(1)); // 255

println!("{:?}", a.saturating\_add(2)); // 255

}
```
饱和算法常用于音视频、图像处理、计数器上限等不希望超过边界的场景。
##### iv）溢出算法（overflowing\_xxx）

overflowing\_xxx会返回一个二元组（result, overflowed），其中result是结果值，而overflowed是布尔类型的值，表示是否发生溢出（溢出为true，否则为false）。

示例：

```rust
fn main() {

let a: u8 = 254;

// 返回一个元组

println!("{:?}", a.overflowing\_add(1)); // (255, false)

println!("{:?}", a.overflowing\_add(2)); // (0, true)

}
```
溢出算法适用于既想得到结果、又想知道是否发生溢出的场景。
### （2）浮点型

浮点数是带小数的数字。Rust提供了 **IEEE 754 单精度浮点数 f32 和IEEE双精度浮点数 f64** ，它们大致对应C/C++中的 **float和double** 。

浮点数字面量的一般化形式如下：

![[Image 24.png]]

浮点数字面量通常由整数部分、小数部分、指数部分以及类型后缀组成。其中小数部分、指数部分、后缀都是可选的，但要让它识别为浮点数字面量，一般需要满足下面任一条件：

带小数点（如2.、3.14）

带指数（如1e-3、12E+99）

使用浮点后缀（如5f32）

特别注意，5. 是有效的浮点数字面量。

**如果没有显式指定类型，编译器默认将浮点数字面量推断为f64类型** 。

示例：

```rust
let x = 2.0; // f64类型

let y: f32 = 3.14; // f32类型
```
**f32和f64具有IEEE要求的一些特殊值的关联常量** ，如INFINITY（无穷大）、NEG\_INFINITY（负无穷大）、NAN（非数值）、MIN（最小有限值：最负）、MAX（最大有限值）等。

**建议使用f32::INFINITY / f64::NAN这类原生类型的关联常量，而不是std::f32::INFINITY这类旧入口** 。

**std::f32::consts和std::f64::consts模块** 提供了一些常用的数学常量，如PI。

示例：
```rust
let v = std::f32::consts::PI;
```
**注意：Rust同时存在两套入口：**

原生类型f32 / f64自带的关联常量与方法（新代码推荐）

标准库早期提供的std::f32 / std::f64模块（其中直接定义的常量更偏向兼容用途，新代码建议改用f32::XXX或f64::XXX形式）
### （3）布尔类型

Rust的布尔类型bool只有两个取值： **true和false** 。比较运算符 ==, <, >等会直接生成bool结果，例如1 < 2的结果就是true。

示例：

```rust
let x = 1 < 2; // x为bool类型

let y: bool = false;
```
许多语言在需要布尔值的上下文中对其他类型比较宽松，例如C/C++会把整数、字符、浮点数、指针等隐式转换为布尔值。但 **Rust不允许这样做，if、while等控制结构的条件必须是bool类型** 。

因此，像C/C++里可以写if(x)的代码，在Rust中必须写长if x!= 0（不能直接写if x，除非x本身就是bool）。

**Rust允许使用as运算符将bool值转换为整数** （true → 1，false → 0），但不允许把整数用as转换为bool（例如1 as bool是非法的）。

**虽然从信息量上来说，bool只需要1bit，但在Rust中，bool的大小是1字节，这样它可以像其他标量类型一样进行寻址、创建引用和指针** 。（并且 bool 的有效内存表示通常是 0x00 表示 false、0x01 表示 true。）
### （4）字符类型

**Rust中char类型占4个字节，表示一个Unicode标量值** 。因此，无论是英文字母、汉字，甚至很多表情符号，都可以用char类型表示。char类型字面值使用 **单引号' '** 括起来。

示例：

```rust
fn main() {

let c = 'z';

let z: char = '中';

let smile = '😊';

}
```
需要注意： **Rust对单个字符使用char，但是对字符串与文本序列使用UTF-8字节序列存储** 。例如String / &str的内部表示的是UTF-8编码的字节数组，而不是char数组。因此， **按索引访问字符串的第n个字符并不是O(1)且Rust默认不允许用下标直接索引字符串** 。
### （5）size\_of和size\_of\_val

**size\_of和size\_of\_val都是const fn（常量函数），这意味着它们可在编译期求值** 。其中 size\_of::<T>() 对给定类型 T 的结果通常是编译期已知的，而 size\_of\_val 在遇到 DST（动态大小类型）时会依赖运行时的元数据计算实际大小。

**std::mem::size\_of::<T>()返回类型T的所占内存大小（字节数）** ，T的类型必须是实现了Sized特征的类型，关于特征后续会详细介绍。

示例：

```rust
fn main() {

println!("{}", size\_of::<i32>()); // 4

println!("{}", size\_of::<char>()); // 4

println!("{}", size\_of::<bool>()); // 1

}
```
**std::mem::size\_of\_val::<T:?Sized>(val: &T)** 返回的是val所借用的那个值（即\*val）在内存中占用的字节数，而不是引用&T本身的大小。

若T: Sized，结果等同于size\_of::<T>()

若T是DST（如str、\[T\]、trait object），则&T是胖指针，携带长度或vtable等元数据。size\_of\_val会利用这些元数据在运行时计算\*val的实际大小。

若想获得引用/指针本身的大小，应使用size\_of::<&T>()，或者对引用再取一次引用：size\_of\_val(&val)

示例：
```rust
let x: i32 = 5;

println!("{}", size\_of\_val(&x)); // 获取x所占内存的大小 4

let s: &str = "hello";

// s本身引用，且&str是胖指针，实际得到的大小就是str字符串内容的UTF-8字节数

println!("{}", size\_of\_val(s)); // 5

// 获取&str这个胖指针的字节数 64位平台，胖指针就是16字节

println!("{}", size\_of\_val(&s)); // 16
```
## 2、复合类型

### （1）数组

数组中的每一个元素类型必须相同。数组一旦定义，长度必须固定，不能增减（长度是类型的一部分）。

定义数组使用 **\[\]** ，将数组的值写到\[\]中并用,隔开。

数组的类型为 **\[元素类型;元素个数\]** ，例如\[u32;5\]是包含5个u32类型值的数组。

示例：

```rust
let arr1 = \[1, 2, 3, 4, 5\]; // \[i32; 5\]

let arr2: \[f64; 3\] = \[1.0, 2.0, 3.0\]; // \[f64; 3\]

let arr3 = \[10; 3\]; // 快捷写法，定义一个长度为3，值都为10的数组

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

let arr = \[1, 2, 3, 4, 5\];

let first = arr\[0\];

let second = arr\[1\];

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

let arr = \[1, 2, 3, 4, 5\];

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

'out\_loop: for i in 0..3 {

for j in 0..3 {

if i == 1 && j == 1 {

break 'out\_loop;

}

println!("i = {}, j = {}", i, j);

}

}

}
```
结果：

![[Image 28.png]]

如果没有循环标签，那么当i == 1且j == 1退出的是内层循环，外层循环仍然会修，从i = 2开始打印。
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

**函数调用是表达式** （会产生一个值，哪怕是()）。 **宏调用在语法上也通常作为表达式使用** 。使用 **花括号{}包裹的代码如果最后产生一个值，那么整个代码块也是表达式** 。简而言之。 **能产生值（哪怕是 ()）的，通常都可以看作表达式** 。

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

break count \* 2;

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

函数用于把可服用逻辑封装起来以便多次调用。

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
fn add\_one(x: i32) -> i32 {

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

块注释（block comment）使用/\*... \*/包裹，可以跨多行，也可以写在同一行内，适合临时屏蔽一段代码或写较长说明。

示例：

```text
/\*
```
这是一个块注释。

它可以跨越多行

\*/

let y = 10; /\* 也可以这样写在同一行 \*/

值得注意的是：和C/C++不同， **Rust的块注释支持嵌套** 。

示例：
```text
/\* 外层注释

/\* 内层注释 \*/

\*/
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
/// \`add\_one\` 将指定值加1

///

/// # Examples

///

/// \`\`\`

/// let arg = 5;

/// let answer = add\_one(arg);

/// assert\_eq!(6, answer);

/// \`\`\`

pub fn add\_one(x: i32) -> i32 {

x + 1

}
```
注意：

文档注释使用Markdown语法，例如上述的 **\# Examples** 标题、 **\`\`\` \`\`\`** 代码块

示例中的代码块会被rustdoc作为文档示例展示，并且可以作为 **文档测试（doctest）** 运行，后续介绍测试再展开。

被注释的项不一定必须是pub才能写文档注释，只是非pub的项在默认生成的公开API文档里通常不会显示（除非生成私有项文档或使用相关开关）
### （2）块文档注释（项文档注释）

使用 **/\*\*... \*/** 增加块文档注释，作用等价于///，只是写法不同。 **实际项目中更常用///，因为更直观，可读性更好** 。

### （3）行文档注释（模块 / crate文档注释）

也称内部文档注释，使用 **//!**。 **它注释的对象不是紧随其后的某个item，而是所在的模块或crate本身。** 通常写在文件顶部（为crate写说明），或写在mod的花括号内部（为模块写说明）。

示例：

```rust
//! This crate provides some mathematical utility functions.

mod math {

}
```
### （4）块文档注释（模块 / crate文档注释）

与//!对应的块式内部文档注释是/\*!... \*/，用法相同，但也相对少见。

## 5、查看文档注释

编写好文档注释后，在项目目录执行 **cargo doc** 命令：

```bash
cargo doc
```
这会在项目的 **target/doc** 目录下生成HTML文件。

为了方便起见，可以直接加上 **\--open** 参数，生成后自动在浏览器打开：
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

\# Examples：示例用法（最常用）

\# Panics：哪些情况可能panic!，便于调用者规避

\# Errors： 若函数返回Result，列出可能的错误及触发条件

\# Safety：若涉及unsafe代码，说明调用者必须满足的前置条件

...

注意：这些标题是社区惯例而非语法要求，可以使用中文标题，但建议遵循团队规范与一致性。
