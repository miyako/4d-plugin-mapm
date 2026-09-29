# 4d-plugin-mapm

`mapm` brings arbitrary-precision decimal arithmetic to 4D by wrapping Michael Ring's MAPM library (version 4.9.5, [LuaDist/mapm](https://github.com/LuaDist/mapm)). Every number goes in and comes out as **Text**, so values are never squeezed into a 4D `Real` and never lose digits: you can add two 40-digit decimals exactly, compute √2 to 10,000 places, or work with integers far beyond the Longint and Real ranges. The plugin exposes 45 commands covering arithmetic, rounding, integer functions, powers and logarithms, circular and hyperbolic trigonometry, random numbers, and number inspection.

| Command | Returns | Purpose |
|---|---|---|
| [`m_apm_add`](#m_apm_add) | Text in `result` | *a* + *b*, exact |
| [`m_apm_subtract`](#m_apm_subtract) | Text in `result` | *a* − *b*, exact |
| [`m_apm_multiply`](#m_apm_multiply) | Text in `result` | *a* × *b*, exact |
| [`m_apm_divide`](#m_apm_divide) | Text in `result` | *a* ÷ *b* to a given number of decimals |
| [`m_apm_integer_divide`](#m_apm_integer_divide) | Text in `result` | Integer quotient, truncated toward zero |
| [`m_apm_integer_div_rem`](#m_apm_integer_div_rem) | Text in `quotient`, `remainder` | Integer quotient and remainder |
| [`m_apm_reciprocal`](#m_apm_reciprocal) | Text in `result` | 1 ÷ *x* |
| [`m_apm_absolute_value`](#m_apm_absolute_value) | Text in `result` | \|*x*\| |
| [`m_apm_negate`](#m_apm_negate) | Text in `result` | −*x* |
| [`m_apm_round`](#m_apm_round) | Text in `result` | Round to a number of significant digits |
| [`m_apm_floor`](#m_apm_floor) | Text in `result` | Largest integer ≤ *x* |
| [`m_apm_ceil`](#m_apm_ceil) | Text in `result` | Smallest integer ≥ *x* |
| [`m_apm_gcd`](#m_apm_gcd) | Text in `result` | Greatest common divisor |
| [`m_apm_lcm`](#m_apm_lcm) | Text in `result` | Least common multiple |
| [`m_apm_factorial`](#m_apm_factorial) | Text in `result` | *n*!, exact |
| [`m_apm_sqrt`](#m_apm_sqrt) | Text in `result` | Square root |
| [`m_apm_cbrt`](#m_apm_cbrt) | Text in `result` | Cube root |
| [`m_apm_pow`](#m_apm_pow) | Text in `result` | *x*^*y* for any real *y* |
| [`m_apm_integer_pow`](#m_apm_integer_pow) | Text in `result` | *x*^*n* for a Longint *n*, rounded |
| [`m_apm_integer_pow_nr`](#m_apm_integer_pow_nr) | Text in `result` | *x*^*n* for a Longint *n* ≥ 0, exact |
| [`m_apm_exp`](#m_apm_exp) | Text in `result` | *e*^*x* |
| [`m_apm_log`](#m_apm_log) | Text in `result` | Natural logarithm |
| [`m_apm_log10`](#m_apm_log10) | Text in `result` | Base-10 logarithm |
| [`m_apm_sin`](#m_apm_sin) | Text in `result` | Sine (radians) |
| [`m_apm_cos`](#m_apm_cos) | Text in `result` | Cosine (radians) |
| [`m_apm_tan`](#m_apm_tan) | Text in `result` | Tangent (radians) |
| [`m_apm_sin_cos`](#m_apm_sin_cos) | Text in `sin`, `cos` | Sine and cosine in one call |
| [`m_apm_arcsin`](#m_apm_arcsin) | Text in `result` | Arc sine |
| [`m_apm_arccos`](#m_apm_arccos) | Text in `result` | Arc cosine |
| [`m_apm_arctan`](#m_apm_arctan) | Text in `result` | Arc tangent |
| [`m_apm_arctan2`](#m_apm_arctan2) | Text in `result` | Four-quadrant arc tangent of *y*/*x* |
| [`m_apm_sinh`](#m_apm_sinh) | Text in `result` | Hyperbolic sine |
| [`m_apm_cosh`](#m_apm_cosh) | Text in `result` | Hyperbolic cosine |
| [`m_apm_tanh`](#m_apm_tanh) | Text in `result` | Hyperbolic tangent |
| [`m_apm_arcsinh`](#m_apm_arcsinh) | Text in `result` | Inverse hyperbolic sine |
| [`m_apm_arccosh`](#m_apm_arccosh) | Text in `result` | Inverse hyperbolic cosine |
| [`m_apm_arctanh`](#m_apm_arctanh) | Text in `result` | Inverse hyperbolic tangent |
| [`m_apm_get_random`](#m_apm_get_random) | Text in `result` | Pseudo-random number between 0 and 1 |
| [`m_apm_compare`](#m_apm_compare) | Longint | −1, 0 or 1 |
| [`m_apm_sign`](#m_apm_sign) | Longint | −1, 0 or 1 |
| [`m_apm_exponent`](#m_apm_exponent) | Longint | Exponent in scientific notation |
| [`m_apm_significant_digits`](#m_apm_significant_digits) | Longint | Number of significant digits |
| [`m_apm_is_integer`](#m_apm_is_integer) | Longint | 1 if an integer, else 0 |
| [`m_apm_is_even`](#m_apm_is_even) | Longint | 1 if an even integer, else 0 |
| [`m_apm_is_odd`](#m_apm_is_odd) | Longint | 1 if an odd integer, else 0 |

**Platforms:** macOS and Windows (32- and 64-bit). All commands behave identically on both.

---

## Requirements & platform notes

**This reference describes the corrected build of the plugin** (the `4DPlugin.cpp` delivered alongside this file). Several behaviors differ from the published 1.0 binary, and you only get them once the corrected source is built:

- Results that are integers with trailing zeros (`1440`, `15000`, `1e20`, most factorials) are returned correctly. In 1.0 they overwrote memory and could crash 4D — including the plugin's own [`m_apm_lcm`](#m_apm_lcm) and [`m_apm_round`](#m_apm_round) samples.
- [`m_apm_integer_div_rem`](#m_apm_integer_div_rem) returns the real remainder. 1.0 returned the quotient in both parameters.
- [`m_apm_sin_cos`](#m_apm_sin_cos) returns the cosine. 1.0 left the `cos` parameter unchanged.
- A negative `places` is treated as `0` in every command. In 1.0, a negative `places` corrupted memory in [`m_apm_pow`](#m_apm_pow), [`m_apm_arctan2`](#m_apm_arctan2), [`m_apm_integer_pow`](#m_apm_integer_pow) and [`m_apm_sin_cos`](#m_apm_sin_cos).
- Text containing any non-ASCII character is read as `0`.

**Pass variables for every parameter.** The manifest declares every parameter as a variable (`&T` or `&L`), including inputs. Inputs are not modified. The plugin's own test method always passes variables (`$a`, `$b`, `$places`), and you should do the same rather than passing literals or expressions.

**Input format.** Numbers are Text in plain or exponent notation: optional leading spaces, an optional `+` or `-`, digits with at most one `.`, and an optional `e`/`E` exponent. `"42"`, `"+7"`, `"-0.5"`, `".5"`, `"5."` and `"1.5E-3"` are all valid. An empty string is read as `0`.

- **The decimal separator is always `.`**, whatever the system locale.
- **No thousands separators.**
- **No trailing spaces.**
- **Invalid text is not reported as an error.** It is silently read as `0` or, worse, as a wrong number. See [Error handling](#error-handling--troubleshooting) for examples.

**Output format.** Results are always written in plain fixed-point notation, never with an exponent:

- `-` for negative numbers and `.` as the decimal point.
- No thousands separators.
- Trailing zeros after the decimal point are never shown, and integers have no decimal point (`log10` of `1000` gives `"3"`, not `"3.0000"`).
- Very large or very small magnitudes therefore produce very long text: `"1e100000"` comes back as a 100,001-character string.

**What `places` means.** Commands that take a `places` Longint compute to a limited precision, because most results (1/3, √2, π) never terminate. The meaning of `places` depends on the command:

- **[`m_apm_divide`](#m_apm_divide)** counts digits after the decimal point: you get `places + 1` decimals, and the extra digits are cut off, not rounded. `1000 ÷ 3` with `places` 3 gives `333.3333`.
- **Every other command** counts significant digits in scientific-notation terms: you get `places + 1` significant digits. `√200` with `places` 3 gives `14.14`, and `ln 1000` with `places` 4 gives `6.9078`.
- **Negative `places`** is treated as `0`, which gives one significant digit.

The commands without `places` (add, subtract, multiply, absolute value, negate, floor, ceil, gcd, lcm, integer divide, integer div/rem, factorial, [`m_apm_integer_pow_nr`](#m_apm_integer_pow_nr)) are exact and return every digit.

**Threading and responsiveness.** Every command is declared thread-safe and can run in preemptive processes. All calls into the plugin share one lock: while one process is inside a `m_apm_*` command, every other process that calls any `m_apm_*` command waits.

Nothing limits the size of a calculation, and a single call cannot be interrupted. In testing, these finished in about 0.1 s:
- √2 to 200,000 places
- 20,000!

These were still running after 20 seconds:
- √2 with `places` near 2 billion
- 10,000,000!
- 7^2,000,000,000 with [`m_apm_integer_pow_nr`](#m_apm_integer_pow_nr)

If memory runs out mid-calculation, the underlying library ends the whole 4D application. **Bound `places`, exponents and input sizes yourself** before calling the plugin with values that come from users or external data.

---

## m_apm_add

### Syntax

```
m_apm_add ( result ; a ; b )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives *a* + *b* |
| `a` | Text | First number |
| `b` | Text | Second number |
| Result | — | No function result; the answer is written to `result` |

### Description

Adds two numbers exactly. No precision is lost however many digits the inputs have.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$r:=""

$a:="10000000000000000000.00000000000000000001"
$b:="10000000000000000000.00000000000000000001"

m_apm_add($r; $a; $b)  //20000000000000000000.00000000000000000002
```

Decimal fractions stay exact, unlike binary floating point:

```4d
$a:="0.1"
$b:="0.2"
m_apm_add($r; $a; $b)  //0.3
```

---

## m_apm_subtract

### Syntax

```
m_apm_subtract ( result ; a ; b )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives *a* − *b* |
| `a` | Text | Number to subtract from |
| `b` | Text | Number to subtract |
| Result | — | No function result; the answer is written to `result` |

### Description

Subtracts `b` from `a` exactly.

### Example

From the plugin's own test method (`Method1.4dm`), with the same `$a` and `$b` as the [`m_apm_add`](#m_apm_add) example:

```4d
m_apm_subtract($r; $a; $b)  //0
```

```4d
$a:="18446744073709551616"
$b:="1"
m_apm_subtract($r; $a; $b)  //18446744073709551615
```

---

## m_apm_multiply

### Syntax

```
m_apm_multiply ( result ; a ; b )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives *a* × *b* |
| `a` | Text | First factor |
| `b` | Text | Second factor |
| Result | — | No function result; the answer is written to `result` |

### Description

Multiplies two numbers exactly. The result has as many digits as the exact product needs.

### Example

From the plugin's own test method (`Method1.4dm`), with the same `$a` and `$b` as the [`m_apm_add`](#m_apm_add) example:

```4d
m_apm_multiply($r; $a; $b)  //100000000000000000000000000000000000000.2000000000000000000000000000000000000001
```

---

## m_apm_divide

### Syntax

```
m_apm_divide ( result ; places ; a ; b )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives *a* ÷ *b* |
| `places` | Longint | Precision: the result has `places + 1` digits after the decimal point |
| `a` | Text | Dividend |
| `b` | Text | Divisor |
| Result | — | No function result; the answer is written to `result` |

### Description

Divides `a` by `b`. This is the only command whose `places` counts digits after the decimal point rather than significant digits. You get `places + 1` decimals, cut off rather than rounded: `2 ÷ 3` with `places` 3 gives `0.6666`. Use [`m_apm_round`](#m_apm_round) on the result if you need rounding.

Dividing by zero returns `"0"` and raises no 4D error. Check the divisor with [`m_apm_sign`](#m_apm_sign) first if zero is possible.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$a:="1"
$b:="3"
$places:=40  //=41 decimals

m_apm_divide($r; $places; $a; $b)  //0.33333333333333333333333333333333333333333
```

`places` counts decimals, independent of the size of the integer part:

```4d
$a:="1000000"
$b:="7"
$places:=0
m_apm_divide($r; $places; $a; $b)  //142857.1
```

---

## m_apm_integer_divide

### Syntax

```
m_apm_integer_divide ( result ; a ; b )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives the integer quotient |
| `a` | Text | Dividend |
| `b` | Text | Divisor |
| Result | — | No function result; the answer is written to `result` |

### Description

Divides `a` by `b` and truncates the result toward zero, so `-17 ÷ 5` gives `-3`, not `-4`. Dividing by zero returns `"0"`. If you also need the remainder, use [`m_apm_integer_div_rem`](#m_apm_integer_div_rem).

### Example

```4d
$a:="17"
$b:="5"
m_apm_integer_divide($r; $a; $b)  //3

$a:="-17"
m_apm_integer_divide($r; $a; $b)  //-3
```

---

## m_apm_integer_div_rem

### Syntax

```
m_apm_integer_div_rem ( quotient ; remainder ; a ; b )
```

| Parameter | Type | Description |
|---|---|---|
| `quotient` | Text | Variable that receives the quotient, truncated toward zero |
| `remainder` | Text | Variable that receives *a* − *quotient* × *b* |
| `a` | Text | Dividend |
| `b` | Text | Divisor |
| Result | — | No function result; the answers are written to `quotient` and `remainder` |

### Description

Returns the truncated quotient and the matching remainder in one call. The remainder has the sign of `a`: `-17 ÷ 5` gives quotient `-3` and remainder `-2`, while `17 ÷ -5` gives `-3` and `2`.

The inputs don't have to be integers: `17.9 ÷ 5` gives `3` and `2.9`. With `b` set to `"1"`, this command splits a number into its integer and fractional parts.

Dividing by zero returns `"0"`.

### Example

```4d
$q:=""
$rem:=""
$a:="17"
$b:="5"
m_apm_integer_div_rem($q; $rem; $a; $b)  //$q = 3, $rem = 2
```

Splitting a number into its integer and fractional parts:

```4d
$x:="-32.17042"
$one:="1"
m_apm_integer_div_rem($int; $frac; $x; $one)  //$int = -32, $frac = -0.17042
```

---

## m_apm_reciprocal

### Syntax

```
m_apm_reciprocal ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives 1 ÷ *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number to invert |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes 1 ÷ `x`. Unlike [`m_apm_divide`](#m_apm_divide), `places` here counts significant digits. An input of zero returns `"0"`.

### Example

```4d
$x:="3"
$places:=10
m_apm_reciprocal($r; $places; $x)  //0.33333333333
```

---

## m_apm_absolute_value

### Syntax

```
m_apm_absolute_value ( result ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives \|*x*\| |
| `x` | Text | Number |
| Result | — | No function result; the answer is written to `result` |

### Description

Returns `x` without its sign. Because the result is written in the plugin's normal output format, this command also converts any valid input into canonical form: `"1.5E-3"` becomes `"0.0015"` and `"+7"` becomes `"7"`.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$a:="-1234569876543247843654"

m_apm_absolute_value($r; $a)  //1234569876543247843654
```

---

## m_apm_negate

### Syntax

```
m_apm_negate ( result ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives −*x* |
| `x` | Text | Number |
| Result | — | No function result; the answer is written to `result` |

### Description

Flips the sign of `x`. Zero stays `"0"`.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$a:="1234569876543247843654"

m_apm_negate($r; $a)  //-1234569876543247843654
```

---

## m_apm_round

### Syntax

```
m_apm_round ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives the rounded value |
| `places` | Longint | Keep `places + 1` significant digits |
| `x` | Text | Number to round |
| Result | — | No function result; the answer is written to `result` |

### Description

Rounds `x` to `places + 1` significant digits, **not** to `places` decimals. `14535` with `places` 1 becomes `15000`. `3.14159` with `places` 2 becomes `3.14`. `0.0012345` with `places` 2 becomes `0.00123`.

Halves round away from zero: `2.5` → `3`, `-2.5` → `-3`.

To round to a fixed number of decimals, combine this command with [`m_apm_exponent`](#m_apm_exponent) — see [Rounding money to cents](#rounding-money-to-cents).

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$a:="14535"
$places:=1

m_apm_round($r; $places; $a)  //15000
```

```4d
$a:="3.14159"
$places:=2
m_apm_round($r; $places; $a)  //3.14
```

---

## m_apm_floor

### Syntax

```
m_apm_floor ( result ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives the largest integer ≤ *x* |
| `x` | Text | Number |
| Result | — | No function result; the answer is written to `result` |

### Description

Rounds downward, toward negative infinity: `2.5` → `2`, `-2.5` → `-3`.

### Example

```4d
$x:="-2.5"
m_apm_floor($r; $x)  //-3
```

---

## m_apm_ceil

### Syntax

```
m_apm_ceil ( result ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives the smallest integer ≥ *x* |
| `x` | Text | Number |
| Result | — | No function result; the answer is written to `result` |

### Description

Rounds upward, toward positive infinity: `2.1` → `3`, `-2.5` → `-2`.

### Example

```4d
$x:="2.1"
m_apm_ceil($r; $x)  //3
```

---

## m_apm_gcd

### Syntax

```
m_apm_gcd ( result ; a ; b )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives the greatest common divisor |
| `a` | Text | Integer |
| `b` | Text | Integer |
| Result | — | No function result; the answer is written to `result` |

### Description

Returns the greatest common divisor of two integers. The result is positive even when an input is negative: gcd(−12, 18) = `6`. **Both inputs must be integers**; a non-integer input returns `"0"`.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$r:=""

$a:="1440"
$b:="12"

m_apm_gcd($r; $a; $b)  //12
```

---

## m_apm_lcm

### Syntax

```
m_apm_lcm ( result ; a ; b )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives the least common multiple |
| `a` | Text | Integer |
| `b` | Text | Integer |
| Result | — | No function result; the answer is written to `result` |

### Description

Returns the least common multiple of two integers. **Both inputs must be integers**; a non-integer input returns `"0"`.

### Example

From the plugin's own test method (`Method1.4dm`). The comment marker `//` is missing in the source file, so add it before running this line:

```4d
m_apm_lcm($r; $a; $b)1440
```

With the marker restored, and a second case:

```4d
$a:="1440"
$b:="12"
m_apm_lcm($r; $a; $b)  //1440

$a:="4"
$b:="6"
m_apm_lcm($r; $a; $b)  //12
```

---

## m_apm_factorial

### Syntax

```
m_apm_factorial ( result ; n )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives *n*! |
| `n` | Text | Non-negative integer |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes *n*! exactly, with every digit. `0!` and `1!` return `1`.

**Only non-negative integers give meaningful results.** Negative inputs return `1`. Non-integers return nonsense: the library multiplies *n* × (*n*−1) × … while the factor is ≥ 1, so `3.7` returns `11.8881`.

Large *n* is expensive: 20,000! (72,339 digits) took about 0.1 s in testing, while 10,000,000! did not finish in 20 seconds.

### Example

```4d
$n:="30"
m_apm_factorial($r; $n)  //265252859812191058636308480000000
```

---

## m_apm_sqrt

### Syntax

```
m_apm_sqrt ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives √*x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number ≥ 0 |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the square root. A negative `x` returns `"0"`.

### Example

```4d
$x:="2"
$places:=30
m_apm_sqrt($r; $places; $x)  //1.41421356237309504880168872421

$x:="200"
$places:=3
m_apm_sqrt($r; $places; $x)  //14.14
```

---

## m_apm_cbrt

### Syntax

```
m_apm_cbrt ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives ∛*x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number (may be negative) |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the cube root. Negative inputs are allowed: ∛−27 = `-3`.

### Example

```4d
$x:="-27"
$places:=10
m_apm_cbrt($r; $places; $x)  //-3
```

---

## m_apm_pow

### Syntax

```
m_apm_pow ( result ; places ; x ; y )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives *x*^*y* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Base, **must be > 0** (or exactly 0) |
| `y` | Text | Exponent, any real number |
| Result | — | No function result; the answer is written to `result` |

### Description

Raises `x` to any real power `y`. `0^0` returns `1`.

**A negative base gives a wrong answer, not an error:** `-8^(1/3)` returns `1`. For a negative base, use [`m_apm_integer_pow`](#m_apm_integer_pow) (integer exponents) or [`m_apm_cbrt`](#m_apm_cbrt) (cube roots). When `y` is an integer, [`m_apm_integer_pow`](#m_apm_integer_pow) is also faster.

### Example

```4d
$x:="2"
$y:="0.5"
$places:=20
m_apm_pow($r; $places; $x; $y)  //1.4142135623730950488
```

---

## m_apm_integer_pow

### Syntax

```
m_apm_integer_pow ( result ; places ; x ; n )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives *x*^*n* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Base (may be negative) |
| `n` | Longint | Integer exponent (may be negative) |
| Result | — | No function result; the answer is written to `result` |

### Description

Raises `x` to an integer power, rounded to the requested precision. Negative exponents are allowed: `2^-2` = `0.25`. Zero raised to a negative power returns `"0"`.

Note that `n` is a **Longint**, not Text. If you need every digit of the result, use [`m_apm_integer_pow_nr`](#m_apm_integer_pow_nr) instead.

### Example

```4d
$x:="1.5"
$n:=7
$places:=10
m_apm_integer_pow($r; $places; $x; $n)  //17.0859375
```

---

## m_apm_integer_pow_nr

### Syntax

```
m_apm_integer_pow_nr ( result ; x ; n )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives *x*^*n*, not rounded |
| `x` | Text | Base |
| `n` | Longint | Exponent, **must be ≥ 0** |
| Result | — | No function result; the answer is written to `result` |

### Description

Raises `x` to a non-negative integer power exactly ("nr" = no rounding). This is the command for large-integer work.

A negative `n` returns `"0"`. The result size grows with `n`: 7^1,000,000 (845,099 digits) was instant in testing, while 7^2,000,000,000 did not finish in 20 seconds.

### Example

```4d
$x:="2"
$n:=100
m_apm_integer_pow_nr($r; $x; $n)  //1267650600228229401496703205376
```

---

## m_apm_exp

### Syntax

```
m_apm_exp ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives *e*^*x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Exponent |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes *e* raised to `x`. When the input is too large in magnitude for the library (for example `1e12` or `-1e12`), the result is `"0"` rather than an error.

### Example

```4d
$x:="1"
$places:=20
m_apm_exp($r; $places; $x)  //2.71828182845904523536
```

---

## m_apm_log

### Syntax

```
m_apm_log ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives ln *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number > 0 |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the natural logarithm. Zero and negative inputs return `"0"`, which is indistinguishable from the correct result for `x = 1`.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$a:="1000"
$places:=4

m_apm_log($r; $places; $a)  //6.9078
```

---

## m_apm_log10

### Syntax

```
m_apm_log10 ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives log₁₀ *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number > 0 |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the base-10 logarithm. Zero and negative inputs return `"0"`.

### Example

From the plugin's own test method (`Method1.4dm`), with the same `$a` and `$places` as the [`m_apm_log`](#m_apm_log) example:

```4d
m_apm_log10($r; $places; $a)  //3
```

---

## m_apm_sin

### Syntax

```
m_apm_sin ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives sin *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Angle in radians |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the sine. The angle is in radians. If you need both sine and cosine, [`m_apm_sin_cos`](#m_apm_sin_cos) is faster than two separate calls.

### Example

```4d
$x:="1"
$places:=15
m_apm_sin($r; $places; $x)  //0.8414709848078965
```

---

## m_apm_cos

### Syntax

```
m_apm_cos ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives cos *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Angle in radians |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the cosine. The angle is in radians.

### Example

```4d
$x:="1"
$places:=15
m_apm_cos($r; $places; $x)  //0.5403023058681397
```

---

## m_apm_tan

### Syntax

```
m_apm_tan ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives tan *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Angle in radians |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the tangent. The angle is in radians. Near π/2 the result becomes very large, as expected.

### Example

```4d
$x:="1"
$places:=15
m_apm_tan($r; $places; $x)  //1.557407724654902
```

---

## m_apm_sin_cos

### Syntax

```
m_apm_sin_cos ( sin ; cos ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `sin` | Text | Variable that receives sin *x* |
| `cos` | Text | Variable that receives cos *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Angle in radians |
| Result | — | No function result; the answers are written to `sin` and `cos` |

### Description

Computes sine and cosine together, which is faster than calling [`m_apm_sin`](#m_apm_sin) and [`m_apm_cos`](#m_apm_cos) separately. Note the parameter order: both outputs come first, then `places`, then the angle.

### Example

```4d
$sin:=""
$cos:=""
$x:="1"
$places:=10
m_apm_sin_cos($sin; $cos; $places; $x)  //$sin = 0.84147098481, $cos = 0.54030230587
```

---

## m_apm_arcsin

### Syntax

```
m_apm_arcsin ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives arcsin *x*, in radians |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number between −1 and 1 |
| Result | — | No function result; the answer is written to `result` |

### Description

Returns an angle in the range −π/2 to π/2. If \|`x`\| > 1, the result is `"0"`.

### Example

```4d
$x:="0.5"
$places:=15
m_apm_arcsin($r; $places; $x)  //0.5235987755982989
```

---

## m_apm_arccos

### Syntax

```
m_apm_arccos ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives arccos *x*, in radians |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number between −1 and 1 |
| Result | — | No function result; the answer is written to `result` |

### Description

Returns an angle in the range 0 to π. If \|`x`\| > 1, the result is `"0"`.

### Example

```4d
$x:="0.5"
$places:=15
m_apm_arccos($r; $places; $x)  //1.047197551196598
```

---

## m_apm_arctan

### Syntax

```
m_apm_arctan ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives arctan *x*, in radians |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number |
| Result | — | No function result; the answer is written to `result` |

### Description

Returns an angle in the range −π/2 to π/2. To get the correct quadrant from separate *y* and *x* values, use [`m_apm_arctan2`](#m_apm_arctan2).

### Example

```4d
$x:="1"
$places:=15
m_apm_arctan($r; $places; $x)  //0.7853981633974483
```

---

## m_apm_arctan2

### Syntax

```
m_apm_arctan2 ( result ; places ; y ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives the angle, in radians |
| `places` | Longint | Precision: `places + 1` significant digits |
| `y` | Text | Y coordinate |
| `x` | Text | X coordinate |
| Result | — | No function result; the answer is written to `result` |

### Description

Four-quadrant arc tangent of `y` / `x`. It uses the signs of both inputs to return an angle in the range −π to π. Note the order: `y` comes before `x`. If both inputs are zero, the result is `"0"`.

### Example

```4d
$y:="1"
$x:="-1"
$places:=10
m_apm_arctan2($r; $places; $y; $x)  //2.3561944902 (3π/4)
```

---

## m_apm_sinh

### Syntax

```
m_apm_sinh ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives sinh *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the hyperbolic sine.

### Example

```4d
$x:="1"
$places:=15
m_apm_sinh($r; $places; $x)  //1.175201193643801
```

---

## m_apm_cosh

### Syntax

```
m_apm_cosh ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives cosh *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the hyperbolic cosine.

### Example

```4d
$x:="1"
$places:=15
m_apm_cosh($r; $places; $x)  //1.543080634815244
```

---

## m_apm_tanh

### Syntax

```
m_apm_tanh ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives tanh *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the hyperbolic tangent.

### Example

```4d
$x:="1"
$places:=15
m_apm_tanh($r; $places; $x)  //0.7615941559557649
```

---

## m_apm_arcsinh

### Syntax

```
m_apm_arcsinh ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives arcsinh *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the inverse hyperbolic sine. Any input is valid.

### Example

```4d
$x:="1"
$places:=15
m_apm_arcsinh($r; $places; $x)  //0.881373587019543
```

---

## m_apm_arccosh

### Syntax

```
m_apm_arccosh ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives arccosh *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number ≥ 1 |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the inverse hyperbolic cosine. An input below 1 returns `"0"`.

### Example

```4d
$x:="2"
$places:=15
m_apm_arccosh($r; $places; $x)  //1.316957896924817
```

---

## m_apm_arctanh

### Syntax

```
m_apm_arctanh ( result ; places ; x )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives arctanh *x* |
| `places` | Longint | Precision: `places + 1` significant digits |
| `x` | Text | Number strictly between −1 and 1 |
| Result | — | No function result; the answer is written to `result` |

### Description

Computes the inverse hyperbolic tangent. If \|`x`\| ≥ 1, the result is `"0"`.

### Example

```4d
$x:="0.5"
$places:=15
m_apm_arctanh($r; $places; $x)  //0.5493061443340548
```

---

## m_apm_get_random

### Syntax

```
m_apm_get_random ( result )
```

| Parameter | Type | Description |
|---|---|---|
| `result` | Text | Variable that receives a pseudo-random number between 0 and 1 |
| Result | — | No function result; the answer is written to `result` |

### Description

Returns the next value from the library's pseudo-random generator, typically with 15 decimal digits. Any previous content of `result` is ignored and replaced.

- The generator is seeded from the system clock when the plugin loads, so the sequence differs on each launch.
- The plugin exposes no command to set the seed, so sequences can't be reproduced.
- All processes share one sequence.
- The generator is predictable. **Do not use it for passwords, tokens or anything security-related.**

### Example

```4d
$r:=""
m_apm_get_random($r)  //e.g. 0.805255057732562
```

---

## m_apm_compare

### Syntax

```
m_apm_compare ( a ; b ) -> Longint
```

| Parameter | Type | Description |
|---|---|---|
| `a` | Text | First number |
| `b` | Text | Second number |
| Result | Longint | `-1` if *a* < *b*, `0` if equal, `1` if *a* > *b* |

### Description

Compares two numbers by value, not as text: `"2"` is less than `"10"`, and `"1.0"` equals `"1"`. Use this instead of comparing the Text values with `<` or `=`, which compares characters.

### Example

```4d
$a:="2"
$b:="10"
$i:=m_apm_compare($a; $b)  //-1

$a:="1.0"
$b:="1"
$i:=m_apm_compare($a; $b)  //0
```

---

## m_apm_sign

### Syntax

```
m_apm_sign ( x ) -> Longint
```

| Parameter | Type | Description |
|---|---|---|
| `x` | Text | Number |
| Result | Longint | `-1` if negative, `0` if zero, `1` if positive |

### Description

Returns the sign of `x`. Checking for `0` is the reliable way to test for zero before a division.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$i:=m_apm_sign($r)  //1 or -1
```

---

## m_apm_exponent

### Syntax

```
m_apm_exponent ( x ) -> Longint
```

| Parameter | Type | Description |
|---|---|---|
| `x` | Text | Number |
| Result | Longint | Exponent of `x` in scientific notation |

### Description

Returns the power of ten of `x` written as *d.ddd* × 10^*e*: `15000` → `4`, `0.00123` → `-3`, `0` → `0`. For a number ≥ 1, the exponent is one less than the number of digits before the decimal point. That is what [`m_apm_round`](#m_apm_round) needs to round to a fixed number of decimals.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$i:=m_apm_exponent($r)
```

```4d
$x:="15000"
$i:=m_apm_exponent($x)  //4
```

---

## m_apm_significant_digits

### Syntax

```
m_apm_significant_digits ( x ) -> Longint
```

| Parameter | Type | Description |
|---|---|---|
| `x` | Text | Number |
| Result | Longint | Number of significant digits in `x` |

### Description

Counts significant digits, ignoring leading zeros and trailing zeros: `15000` → `2`, `1.2300` → `3`, `0` → `1`.

### Example

From the plugin's own test method (`Method1.4dm`), where `$r` holds the result of the [`m_apm_divide`](#m_apm_divide) example:

```4d
$i:=m_apm_significant_digits($r)  //41
```

---

## m_apm_is_integer

### Syntax

```
m_apm_is_integer ( x ) -> Longint
```

| Parameter | Type | Description |
|---|---|---|
| `x` | Text | Number |
| Result | Longint | `1` if `x` is a whole number, `0` otherwise |

### Description

Tests whether `x` has no fractional part. Notation doesn't matter: `"1.0"` and `"1e3"` both return `1`. Use this to validate input before [`m_apm_gcd`](#m_apm_gcd), [`m_apm_lcm`](#m_apm_lcm), [`m_apm_factorial`](#m_apm_factorial), [`m_apm_is_even`](#m_apm_is_even) or [`m_apm_is_odd`](#m_apm_is_odd).

### Example

From the plugin's own test method (`Method1.4dm`), where `$r` holds 0.333…:

```4d
$i:=m_apm_is_integer($r)  //0=no
```

---

## m_apm_is_even

### Syntax

```
m_apm_is_even ( x ) -> Longint
```

| Parameter | Type | Description |
|---|---|---|
| `x` | Text | Integer |
| Result | Longint | `1` if `x` is an even integer, `0` otherwise |

### Description

Tests whether an integer is even. **The result is undefined for non-integers.** Check with [`m_apm_is_integer`](#m_apm_is_integer) first.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$i:=m_apm_is_even($r)
```

```4d
$x:="14"
$i:=m_apm_is_even($x)  //1
```

---

## m_apm_is_odd

### Syntax

```
m_apm_is_odd ( x ) -> Longint
```

| Parameter | Type | Description |
|---|---|---|
| `x` | Text | Integer |
| Result | Longint | `1` if `x` is an odd integer, `0` otherwise |

### Description

Tests whether an integer is odd. **The result is undefined for non-integers**: in testing, `"2.5"` returned `1`. Check with [`m_apm_is_integer`](#m_apm_is_integer) first.

### Example

From the plugin's own test method (`Method1.4dm`):

```4d
$i:=m_apm_is_odd($r)
```

```4d
$x:="14"
$i:=m_apm_is_odd($x)  //0
```

---

## Worked examples

### Rounding money to cents

[`m_apm_round`](#m_apm_round) counts significant digits, so to keep *N* decimals you set `places` to the number's exponent plus *N*. This recipe works for values ≥ 1; for smaller values the exponent is negative, so check the result for your data. Here, 1,000 at 5% for 10 years:

```4d
$rate:="1.05"
$years:=10
$places:=20
m_apm_integer_pow($growth; $places; $rate; $years)  //1.62889462677744140625

$principal:="1000"
m_apm_multiply($balance; $principal; $growth)  //1628.89462677744140625

$places:=m_apm_exponent($balance)+2  //3+2 = 5, i.e. 6 significant digits
m_apm_round($cents; $places; $balance)  //1628.89
```

### Exact large-integer arithmetic

Factorials and powers stay exact, so ratios of huge numbers come out as exact integers:

```4d
$n:="30"
m_apm_factorial($f30; $n)  //265252859812191058636308480000000
$n:="28"
m_apm_factorial($f28; $n)  //304888344611713860501504000000
m_apm_integer_divide($r; $f30; $f28)  //870
```

### Guarding a division

Invalid operations return `"0"` rather than a 4D error, so test the inputs yourself:

```4d
$a:="1"
$b:="0"
$places:=20
Case of
	: (m_apm_sign($b)=0)
		ALERT("Division by zero")
	Else
		m_apm_divide($r; $places; $a; $b)
End case
```

---

## Error handling & troubleshooting

- **Invalid operations return `"0"`, never a 4D error.** Division by zero, logarithms of zero or negatives, square roots of negatives, arcsin/arccos outside −1…1, arctanh at ±1, arccosh below 1, `exp` overflow and gcd/lcm of non-integers all produce `"0"`. The underlying library prints a warning to the process's standard error, which 4D does not display. Validate inputs with [`m_apm_sign`](#m_apm_sign), [`m_apm_compare`](#m_apm_compare) and [`m_apm_is_integer`](#m_apm_is_integer) when a zero result would be ambiguous.
- **Malformed numeric text gives a wrong number, silently.** In testing:
  - `"12x"` and `"abc"` read as `0`.
  - `"1,5"` read as `65`.
  - `"42 "` (trailing space) read as `429`.

  Leading spaces are fine. Trim trailing spaces, remove thousands separators and use `.` as the decimal separator before calling the plugin. One way to validate is to pass the text through [`m_apm_absolute_value`](#m_apm_absolute_value) and compare the magnitude with what you expect.
- **Numbers built with `String` may use the system decimal separator.** On a system configured with `,` as decimal separator, text produced from a 4D Real can contain `,`, which this plugin misreads (see above). Check the Language Reference for your version's options to force `.`, or build numeric text without going through a Real.
- **[`m_apm_pow`](#m_apm_pow) needs a positive base.** A negative base with a real exponent returns a wrong value (`-8^(1/3)` → `1`). Use [`m_apm_integer_pow`](#m_apm_integer_pow) or [`m_apm_cbrt`](#m_apm_cbrt) instead.
- **[`m_apm_factorial`](#m_apm_factorial), [`m_apm_is_even`](#m_apm_is_even), [`m_apm_is_odd`](#m_apm_is_odd) need integers.** Non-integer input gives nonsense or an undefined result rather than an error.
- **`places` is significant digits except in [`m_apm_divide`](#m_apm_divide).** If a rounded or computed result has fewer digits than you expected, re-read [What `places` means](#requirements--platform-notes). [`m_apm_divide`](#m_apm_divide) also cuts off instead of rounding.
- **Big calculations block every process that uses the plugin.** One lock serializes all calls, and nothing can interrupt a calculation in progress. Cap `places`, exponents, factorial inputs and input length for anything that comes from users. Very long results (huge exponents) also mean very long Text values in memory.
- **Out of memory ends 4D.** If the library can't allocate memory mid-calculation, it terminates the application rather than returning. This is another reason to bound input sizes.
- **Exponent notation near the 32-bit limit is unsupported.** An input such as `"1e2147483647"` overflows the library's parser and produces a meaningless result.
- **Non-ASCII text reads as `0`** (corrected build). Full-width or other non-Latin digits are not recognized.
- **Upgrading from 1.0:** the 1.0 binary could crash on results with trailing zeros, returned the quotient as the remainder in [`m_apm_integer_div_rem`](#m_apm_integer_div_rem), and never filled the cosine in [`m_apm_sin_cos`](#m_apm_sin_cos). See [Requirements & platform notes](#requirements--platform-notes).

---

## Quick reference

```4d
$r:=""
$a:="10000000000000000000.00000000000000000001"
$b:="3"
$places:=40

m_apm_add($r; $a; $b)
m_apm_subtract($r; $a; $b)
m_apm_multiply($r; $a; $b)
m_apm_divide($r; $places; $a; $b)          // places+1 decimals, cut off
m_apm_integer_div_rem($q; $rem; $a; $b)
m_apm_round($r; $places; $a)               // places+1 significant digits

m_apm_sqrt($r; $places; $b)
m_apm_pow($r; $places; $b; $b)
m_apm_integer_pow_nr($r; $b; $n)           // $n : Longint >= 0, exact
m_apm_log($r; $places; $b)
m_apm_sin_cos($sin; $cos; $places; $b)     // radians
m_apm_arctan2($r; $places; $y; $x)         // y before x

$i:=m_apm_compare($a; $b)                  // -1 / 0 / 1
$i:=m_apm_sign($a)
$i:=m_apm_is_integer($a)
```
