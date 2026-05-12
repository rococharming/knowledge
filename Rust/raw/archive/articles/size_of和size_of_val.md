
Rust 标准库中的 `std::mem::size_of` 和 `std::mem::size_of_val` 都用于查看数据在内存中占用的字节数。

它们的核心区别是：

- `size_of::<T>()`：查看某个类型 `T` 占多少字节；
- `size_of_val(&value)`：查看某个具体值占多少字节。

简单来说，`size_of`面向类型，`size_of_val`面向具体值。

对于**普通固定大小类型**，例如`i32`，`char`、`bool`等，两者得到的结果通常一样。

对于**动态大小类型**，也就是`DST`，例如 `str`、`[T]`、`dyn Trait`，`size_of_val` 更有意义，因为它可以根据引用携带的元数据计算实际大小。

`size_of` 和 `size_of_val` 都是 `const fn`，因此可以在常量上下文中使用。

还需要注意：这两个函数计算的是**值本身的大小**，不递归统计它内部指向的堆内存大小。例如 `String` 本身通常只包含指针、长度和容量，`size_of::<String>()` 统计的是这个结构本身的大小，不包括字符串内容在堆上的占用。

# 二、size_of

`size_of::<T>()` 用于获取类型 `T` 在内存中占用的字节数。

示例：

```rust
fn main() {
    println!("{}", size_of::<i32>());  // i32 占 4 个字节
    println!("{}", size_of::<char>()); // char 占 4 个字节
    println!("{}", size_of::<bool>()); // bool 占 1 个字节
}
```

`size_of::<T>()` 要求 `T` 在编译期有确定大小，也就是 `T: Sized`。因此可以写：

```rust
fn main() {  
	println!("{}", size_of::<i32>());       // 4
	println!("{}", size_of::<[i32; 3]>());  // 12
}
```

但不能直接写：

```rust
fn main() {  
	println!("{}", size_of::<str>()); // 错误：str 是动态大小类型  
}
```

# 三、size_of_val

`size_of_val::<T: ?Sized>(val: &T)` 返回的是 `val` 所借用的那个值，也就是 `*val`，在内存中占用的字节数，而不是引用 `&T` 本身的大小。

示例：

```rust
fn main() {  
	let x: i32 = 5;  
	println!("{}", size_of_val(&x)); // 4  
}
```

这里的 `size_of_val(&x)` 计算的是 `x` 这个 `i32` 值本身的大小，而不是 `&x` 这个引用的大小。

对于普通`Sized`类型，`size_of_val(&x)`的结果和`size_of::<T>()`一样。

但对于动态大小类型，例如 `str`、`[T]`、`dyn Trait`，`size_of_val` 会利用引用中的元数据计算实际大小。

示例：

```rust
fn main() {
    let s: &str = "hello";

    println!("{}", size_of_val(s));  // 5  字符串内容的字节数
    println!("{}", size_of_val(&s)); // // 64 位平台通常是 16，&str 胖指针大小
}
```

这里要区分：

- `size_of_val(s)`：计算 `s` 指向的 `str` 内容本身的字节数；
- `size_of_val(&s)`：计算变量 `s` 本身的大小，也就是 `&str` 这个胖指针的大小。

`&str` 是胖指针，包含两部分：

- 数据指针
- 长度信息

在 64 位平台上，一个指针通常是 8 字节，长度信息也是 8 字节，因此 `&str` 通常是 16 字节。
