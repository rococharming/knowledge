# 一、std::net模块

## 1、概述

`std::net` 是Rust标准库中负责原生网络编程的模块。它提供了 **基于操作系统套接字（socket）的TCP/UDP网络原语，以及IP地址、套接字地址、地址解析等基础类型** 。简单来说， `std::net` 解决的是如何在不依赖第三方网络框架的前提下，直接使用Rust标准库完成网络通信。

`std::net` **本身主要提供同步、阻塞式网络接口** 。也就是说，一个线程在执行 `accept` 、 `read` 、 `recv` 等操作时，如果数据暂时没有送达，通常会阻塞等待。

## 2、整体结构

`std::net` 是围绕“网络地址”和“网络通信“组织起来的类型系统。整体可以分为三层：

地址层：用于表示IP地址和套接字地址，例如 `IpAddr` 、 `Ipv4Addr` 、 `Ipv6Addr` 、 `SocketAddr` 。

连接层：用于表示TCP/UDP套接字，例如 `TcpStream` 、 `TcpListener` 、 `UdpSocket` 。

辅助层：用于通用地址解析和网络行为控制，如 `ToSocketAddrs` 、 `Shutdown` 等

## 3、核心类型概览

`std::net` 中最重要的类型如下：

地址相关类型

`IpAddr` ：统一表示IPv4或IPv6地址

`Ipv4Addr` ：IPv4地址

`Ipv6Addr` ：IPv6地址

`SocketAddr` ：统一表示“IP + 端口”

`SocketAddrV4` 、 `SocketAddrV6` ：分别表示IPv4/IPv6的套接字地址

通信相关类型

`TcpListener` ：TCP服务器监听套接字

`TcpStream` ：TCP连接流

`UdpSocket` ：UDP套接字

辅助类型与Trait

`ToSocketAddrs` ：把多种地址表示解析为一个或多个 `SocketAddr`

`Shutdown` ：用于关闭TCP连接的读端、写端或全部

# 二、网络地址类型

## 1、结构化地址类型

网络通信首先要解决的问题不是怎么发送数据，而是 **数据发送到哪里** 。因此，地址类型是学习网络编程的第一步。

在Rust中，地址并不是简单的字符串，虽然 `"127.0.0.1:8080"` 这种写法很常见，但它只是方便使用时的一种输入形式。更准确来说，真正用于网络通信的是 **结构化的地址类型** ，例如 `IpAddr` 和 `SocketAddr` 。这样设计的好处在于：编译器可以帮助我们区分地址的不同层次，减少字符串拼接和解析错误。

## 2、IP地址和套接字地址

### （1）概念

IP地址只表示主机位置，例如 `127.0.0.1`

套接字地址表示“IP + 端口”，例如 `127.0.0.1:8080`

网络程序真正绑定、连接的通常是套接字地址，而不是单独的IP地址

### （2）IpAddr、Ipv4Addr、Ipv6Addr

`IpAddr` 表示IP地址，它又分为IPv4地址和IPv6地址。

`IpAddr` 是一个枚举类型，用来统一表示IPv4或IPv6，定义如下：

```text
eum IpAddr {

V4(Ipv4Addr),

V6(Ipv6Addr),

}

`Ipv4Addr` 和 `Ipv6Addr` 表示具体的版本。定义如下：
```
```rust
struct Ipv4Addr {

octets: \[u8; 4\];

}

struct Ipv6Addr {

octets: \[u8; 16\];

}
```
### （3）SocketAddr、SocketAddrV4、SocketAddrV6

`SocketAddr` 表示套接字地址，它又分为IPv4地址和IPv6地址。

`SocketAddr` 是枚举类型，可以是V4或V6，，定义如下：

```rust
enum SocketAddr {

V4(SocketAddrV4)

V6(SocketAddrV6)

}

`SocketAddrV4` 和 `SocketAddrV6` 表示具体的版本，定义如下：
```
```rust
struct SocketAddrV4 {

ip: Ipv4Addr,

port: u16,

}

struct SocketAddrV6 {

ip: Ipv6Addr,

port: u16,

flowinfo: u32,

scope\_id: u32,

}
```
示例：
```rust
use std::net::{IpAddr, Ipv4Addr, SocketAddr};

fn main() {

// Ipv4地址

let ip = IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1));

// SocketAddrV4

let addr = SocketAddr::new(ip, 8080);

println!("ip: {}", ip);

println!("addr: {}", addr);

}
```
结果：

![[Image 79.png]]

这段代码手动构造了一个 IPv4 地址 `127.0.0.1` ，再组合成套接字地址 `127.0.0.1:8080` 。
## 3、ToSocketAddrs：统一地址解析机制

`ToSocketAddrs` 是 `std::net` 中一个非常重要的Trait。它的作用是为连接和绑定提供通用地址输入接口。

可以把它理解为 Rust 为网络 API 设计的一层“地址适配器”。如果没有它，那么 `TcpStream::connect` 、 `TcpListener::bind` 、 `UdpSocket::bind` 这类方法都只能接受某一种固定地址类型，使用起来会非常僵硬。而有了 `ToSocketAddrs` ，开发者可以直接传字符串、元组、 `SocketAddr` 等多种形式。例如 `"localhost:8080"` 、 `"127.0.0.1:8080"` 、 `("127.0.0.1", 8080)` 这类值，都可以在API中直接使用，是因为这些类型实现了 `ToSocketAddrs` 特征，该特征的作用就是把不同形式的地址输入统一转换成一个或多个 `SocketAddr` 。之所以可以转换成多个 `SocketAddr` ，因为像 `localhost` 这类主机名不一定只解析出一个地址，可能得到多个候选地址。

# 三、TCP编程基础

## 1、概述

TCP是一种面向连接、可靠传输、有序字节流协议。很多常见应用场景——HTTP、数据库连接、聊天服务、远程调用等都建立在TCP之上。

在Rust中，TCP编程的核心类型有两个：

`TcpListener` ：服务器监听某个地址，等待客户端的连接

`TcpStream` ：表示一条已经建立的TCP连接，可用于读写数据

从设计上看，这种区分非常清晰： **监听器负责“接入连接”，连接流负责“传输数据”** 。

## 2、TcpListener

### （1）创建方式（绑定）

`TcpListener` 表示一个服务器监听套接字，它绑定某个本地地址后，就可以等待远程客户端发起连接。 `bind` **成功后，返回的监听器（** `TcpListener` **）已经处于可接收连接的状态** 。

通过 `TcpListener::bind(addr)` 绑定地址，绑定的意思是告诉操作系统： **当前进程希望占用这个本地地址和端口，用于接收TCP连接** 。

如果绑定时端口设为0，表示由操作系统自动分配一个可用端口，之后可以通过 `local_addr()` 查询实际分配的端口。

示例：

```rust
use std::net::TcpListener;

fn main() -> std::io::Result<()> {

let listener = TcpListener::bind("127.0.0.1:0")?;

println!("listening on: {}", listener.local\_addr()?);

Ok(())

}
```
结果：

![[Image 80.png]]

注意事项：

绑定失败通常意味着 **地址不可用、端口被占用或权限不足**

同一个地址端口一般不能被多个进程重复绑定

如果希望对外提供服务，不能只绑定 `127.0.0.1` ，因为这只允许本机访问。通常需要绑定 `0.0.0.0:端口` 。
### （2）接收连接

服务端绑定地址之后，需要等待客户端的连接。 `TcpListener` 提供了两种常见方式：

手动调用 `accept()`

通过 `incoming()` 迭代器循环接收连接

accept()

`accept()` 返回一个二元组：

`TcpStream` ：与客户端建立好的连接

`SocketAddr` ：远程客户端地址

incoming()

`incoming()` 返回一个迭代器，它会持续不断的接受连接，适合编写简单服务器主循环。

示例代码：

```rust
use std::net::TcpListener;

fn main() -> std::io::Result<()> {

let listener = TcpListener::bind("127.0.0.1:8080")?;

for stream\_result in listener.incoming() {

let stream = stream\_result?;

println!("new client: {}", stream.peer\_addr()?);

break; // 示例只接收一个连接

}

Ok(())

}
```
注意：

`incoming()` **返回的是一个迭代器，迭代出来的每一项是** `Result<TcpStream, io::Error>` 。这说明接收连接本身也是可能失败的操作，因此必须进行错误处理。

`incoming()` 不是一次性返回所有连接，而是每来一个连接，就产生一次迭代项。它通常是阻塞的，如果没有新连接，线程会阻塞等待。

可以先通过 `curl` 命令作为客户端测试，执行：
```bash
curl http://127.0.0.1:8080
```
虽然 `curl` 发起的是HTTP请求，但服务端仅仅监听TCP连接，没有实现HTTP响应，因此 `curl` 执行会报错，但这里不重要，因为只需要观察服务器连接时的打印即可。

![[Image 81.png]]
## 3、TcpStream

### （1）创建方式

`TcpStream` 表示一条已经建立好的TCP连接。它可以由客户端通过 `connect` 创建，也可以由服务端通过 `accept` 获得。

建立连接后，可以通过对其进行读取和写入来传输数据。当该值被丢弃时，连接会关闭。

客户端通过 `TcpStream::connect(addr)` 发起连接。前面已经介绍过，服务端通过 `TcpListener::accept()` 或 `TcpListner::incoming()` 迭代产出 `TcpStream` 。

### （2）数据传输

`TcpStream` 实现了 `std::io::Read` 和 `std::io::Write` 所需的读写能力，因此通常配合 `read()` 、 `write_all()` 、 `flush()` 等I/O方法使用。

### （3）生命周期结束即关闭连接

当 `TcpStream` 被 `drop` 时，连接会关闭。这也是 Rust 资源管理模型在网络编程中的体现：资源的释放与值的生命周期绑定。

示例：

```rust
use std::io::{Read, Write};

use std::net::TcpStream;

fn main() -> std::io::Result<()> {

let mut stream = TcpStream::connect("www.rust-lang.org:80")?;

println!("Connected to the server");

let mut buffer = \[0u8; 1024\];

stream.write\_all(

b"GET / HTTP/1.1\\r\\n\\

Host: www.rust-lang.org\\r\\n\\

Connection: close\\r\\n\\

\\r\\n"

)?;

loop {

let n = stream.read(&mut buffer)?;

if n == 0 {

break;

}

println!("{}", String::from\_utf8\_lossy(&buffer\[..n\]));

}

Ok(())

}
```
注意事项：

TCP是字节流，不是消息包协议。一次 `read` 读到的数据，不一定对应一次 `write` 写出的完整业务消息

`read` 返回0，往往表示对端已关闭连接
## 4、基于std::io的TCP读写

网络读写本质上也是I/O，因此 `TcpStream` 的使用和文件读写在抽象层面是想通的，这也是Rust在统一I/O设计的重要体现。 `Read` 和 `Write` 是最核心的 I/O trait

读取

常用方法有 `read(&mut buf)` ，返回值是 `io::Result<usize>` ，其中 `usize` 表示实际读取的字节数。

写入

常用方法有：

`write(&buf)` ：尝试写入部分数据

`write_all(&buf)` ：持续写，直到全部写完或者失败

更推荐使用 `write_all()` 是因为底层I/O写操作不保证一次写完全部数据。

示例：

```rust
use std::io::{Read, Write};

use std::net::{TcpListener, TcpStream};

use std::thread;

fn handle\_client(mut stream: TcpStream) -> std::io::Result<()> {

let mut buf = \[0; 1024\];

let n = stream.read(&mut buf)?;

println!("Received: {}", String::from\_utf8\_lossy(&buf\[..n\]));

stream.write\_all(b"pong")?;

Ok(())

}

fn main() -> std::io::Result<()> {

let listener = TcpListener::bind("127.0.0.1:8080")?;

thread::spawn(|| {

if let Ok(mut client) = TcpStream::connect("127.0.0.1:8080") {

client.write\_all(b"ping").unwrap();

let mut buf = \[0; 1024\];

let n = client.read(&mut buf).unwrap();

println!("client got {}", String::from\_utf8\_lossy(&buf\[..n\]));

}

});

let (stream, \_) = listener.accept()?;

handle\_client(stream)?;
```
上述代码演示了一个最小TCP往返流程：

（1）服务器监听本地端口

（2）客户端连接服务器端并发送 `ping`

（3）服务端读取到数据后回复 `pong`

（4）客户端再读取服务端响应

这里需要特别注意：服务端函数 `handle_client` 接受的是 `TcpStream` 的所有权。这样设计很自然，因为连接的处理逻辑通常需要独占该流对象。
## 5、关闭连接与连接属性

网络连接并不是只要建立成功就会一直使用的资源。实际开发中，经常需要获取本地/远端地址、设置是否非阻塞、关闭读写端、设置超时等。因此， `TcpStream` 除了基本连接和读写，还提供了一系列连接控制方法。

### （1）地址查询

`local_addr()` ：本机地址

`peer_addr()` ：远端地址

### （2）关闭连接

使用 `shutdown(Shutdown::Read | Write | Both)` 可以关闭连接的一部分或全部。注意，不同平台在多次调用时行为可能不同，例如Linux与macOS的行为并不完全一致。

当然，值被 `drop` 也会关闭连接，一般情况下，无序释放底层套接字句柄。

示例代码：

```rust
use std::net::{Shutdown, TcpStream};

fn main() -> std::io::Result<()> {

let stream = TcpStream::connect("example.com:80")?;

println!("local = {}", stream.local\_addr()?);

println!("peer = {}", stream.peer\_addr()?);

stream.shutdown(Shutdown::Write)?;

Ok(())

}
```
说明：

`Shutdown::Write` 的含义是关闭写端，即本端不再发送数据，但仍可继续接收对端数据。这个操作常用于 **半关闭连接** 的状态。

注意， `shutdown` 不等于销毁对象，它是对底层连接行为的控制。真正销毁对象需要 `drop` 。
# 四、UDP编程基础

## 1、概述

UDP和TCP的最大区别在于：它是 **无连接、面向数据报** 的协议。也就是说， **UDP不建立像TCP那样的持久连接，也不保证可靠、有序到达** 。

在Rust中，UDP编程由 `UdpSocket` 负责。 `UdpSocket` 绑定到某个地址之后，可以向任意地址发送数据，也可以从任意地址接收数据。虽然UDP本身是 **无连接协议** ，但API仍然提供了 `connect` ，用于 **设置一个默认远端地址** 。

## 2、UdpSocket

### （1）创建方式

使用 `UdpSocket::bind(addr)` 绑定本地地址。

### （2）收发方式

未 `connect` 时

使用 `send_to` / `recv_from`

`connect` 时

使用 `send` / `recv`

### （3）connect

UDP提供 `connect` 方法的含义不是像TCP那样建立连接，而是设置默认目标地址，并限制接收来源，使得后续使用 `send` / `recv` 更加方便。协议本质仍然是 UDP。

## 3、代码示例

**非connect版本**

```rust
use std::net::UdpSocket;

use std::thread;

fn main() -> std::io::Result<()> {

let server = UdpSocket::bind("127.0.0.1:9001")?;

println!("Server starts on {}", server.local\_addr()?);

thread::spawn(|| {

let client = UdpSocket::bind("127.0.0.1:0").unwrap();

client.send\_to(b"hello", "127.0.0.1:9001").unwrap();

});

let mut buf = \[0u8; 512\];

let (n, src) = server.recv\_from(&mut buf)?;

println!("{} bytes received from {}", n, src);

println!("{}", String::from\_utf8\_lossy(&buf\[..n\]));

Ok(())

}

`connect` 版本
```
```rust
use std::net::UdpSocket;

use std::thread;

fn main() -> std::io::Result<()> {

let server = UdpSocket::bind("127.0.0.1:9001")?;

println!("Server starts on {}", server.local\_addr()?);

thread::spawn(|| {

let client = UdpSocket::bind("127.0.0.1:0").unwrap();

client.connect("127.0.0.1:9001").unwrap();

client.send(b"hello").unwrap(); // 可以直接用send而不是send\_to

});

let mut buf = \[0u8; 512\];

let (n, src) = server.recv\_from(&mut buf)?;

println!("{} bytes received from {}", n, src);

println!("{}", String::from\_utf8\_lossy(&buf\[..n\]));

Ok(())

}
```
# 五、克隆套接字和共享底层资源

## 1、概述

在系统编程或网络编程中，可能会遇到这样的需求： **希望多个Rust对象共同操作同一个底层套接字** 。例如， **一个线程负责接收数据，另一个线程负责发送数据** ， **二者都需要访问同一个套接字** 。

为此，Rust标准库为若干网络类型提供了 `try_clone()` 方法，用来创建一个新的句柄，使其与原对象共同引用同一个底层网络资源。

注意， `try_clone()` 的语义并不是复制出一个新的独立的socket，而是创建一个新的Rust句柄，用来共享同一个底层socket或连接。

## 2、示例代码

这里实现一个简单的TCP回显程序：

服务端程序：接收客户端发来的数据，再原样回发

客户端程序：使用 `TcpStream::try_clone()` ，一个线程发送数据，另一个线程接收数据

### （1）服务端程序

```rust
use std::net::{TcpListener, TcpStream};

use std::io::{Read, Write};

use std::thread;

fn handle\_client(mut stream: TcpStream) -> std::io::Result<()> {

let peer = stream.peer\_addr()?;

println!("客户端 {} 连接成功", peer);

let mut buf = \[0u8; 512\];

loop {

let n = stream.read(&mut buf)?;

if n == 0 {

println!("客户端 {} 断开连接", peer);

break;

}

let text = String::from\_utf8\_lossy(&buf\[..n\]);

println!("收到客户端 {} 消息：{}", peer, text);

// 回显给客户端

stream.write\_all(&buf\[..n\])?;

}

Ok(())

}

fn main() -> std::io::Result<()> {

let listener = TcpListener::bind("127.0.0.1:9000")?;

println!("服务器 {} 已开启监听", listener.local\_addr()?);

for stream in listener.incoming() {
```
### （2）客户端程序

```rust
use std::net::TcpStream;

use std::io::{Read, Write, BufRead};

use std::thread;

fn main() -> std::io::Result<()> {

let stream = TcpStream::connect("127.0.0.1:9000")?;

let stream\_clone = stream.try\_clone()?;

let receiver = thread::spawn(move || {

let mut reader = stream\_clone;

let mut buf = \[0u8; 512\];

loop {

let n = reader.read(&mut buf)?;

if n == 0 {

break;

}

let text = String::from\_utf8\_lossy(&buf\[..n\]);

println!("收到服务端的echo：{}", text);

}

Ok::<\_, std::io::Error>(())

});

let sender = thread::spawn(move || {

let mut writer = stream;

let stdin = std::io::stdin();

println!("请输入要发送的内容，输入quit退出");

for line in stdin.lock().lines() {

let line = line?;
```
