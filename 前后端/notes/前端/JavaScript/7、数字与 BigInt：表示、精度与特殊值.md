---
title: 数字与 BigInt：表示、精度与特殊值
date: 2026-08-11
tags: [Web, 前端, JavaScript, 数字]
aliases:
  - JavaScript Number
  - JavaScript数字
  - BigInt
---

# 一、Number 是统一的普通数字类型

JavaScript 用一个 `number` 类型同时表示常见整数和小数，没有单独的 `int` 或 `float` 类型。`50`、`4.5`、`-7` 的 `typeof` 都是 `"number"`。

```js
console.log(typeof 50);  // "number"
console.log(typeof 4.5); // "number"
console.log(typeof -7);  // "number"
```

数字字面量可以使用不同进制；这些只是写法不同，最终仍是 `number` 值。

```js
const decimal = 42;
const binary = 0b101010;
const octal = 0o52;
const hexadecimal = 0x2a;
const scientific = 1.5e3;

console.log(decimal, binary, octal, hexadecimal, scientific);
```

# 二、精度边界

`number` 使用双精度浮点表示，能精确保存的整数范围有限。超过 `Number.MAX_SAFE_INTEGER` 后，连续整数可能变成同一个值。

```js
console.log(Number.MAX_SAFE_INTEGER); // 9007199254740991
console.log(Number.isSafeInteger(9007199254740991)); // true
console.log(Number.isSafeInteger(9007199254740992)); // false
```

小数也可能出现二进制浮点误差：

```js
console.log(0.1 + 0.2); // 0.30000000000000004
```

> [!warning] 金额
> 不要把 `number` 的小数计算直接当作精确货币计算。常见做法是以“分”这类最小货币单位保存整数；需要任意精度小数时再选择合适的十进制库。

# 三、BigInt

`bigint` 用于任意精度整数，字面量以 `n` 结尾。它适合超出安全整数范围的 ID、计数或整数计算，不是 `number` 的日常替代品。

```js
const largeId = 9007199254740993n;

console.log(typeof largeId); // "bigint"
console.log(largeId + 2n);   // 9007199254740995n
```

`number` 和 `bigint` 不能直接混合运算：

```js
const count = 10n;

// count + 1; // TypeError
console.log(count + 1n);
```

只有确认不会丢失精度时，才使用 `Number(bigintValue)` 转回 `number`。

# 四、特殊数值

`NaN` 表示无效的数值结果，`Infinity` 和 `-Infinity` 表示无穷大与无穷小，`-0` 则是与 `0` 在大多数比较中相等的特殊零。

```js
console.log(0 / 0);          // NaN
console.log("hello" / 2);    // NaN
console.log(1 / 0);          // Infinity
console.log(-1 / 0);         // -Infinity
console.log(Object.is(-0, 0)); // false
```

`NaN` 不等于任何值，也不等于自己；检查它应使用 `Number.isNaN()`，详见 [[9、类型转换与数值处理|类型转换与数值处理]]。
