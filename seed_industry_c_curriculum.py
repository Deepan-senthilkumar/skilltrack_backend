"""
SkillStack Production-Ready C Programming Curriculum Seeder
Transforms academic C topics into real-world systems engineering & industry workplace mastery notes.
Covers:
1. Core Fundamental Concept & Syntax
2. 🚨 The College Trap vs. Real Industry Reality (Why college examples fail in jobs)
3. 🏭 Production / Real-World Workplace Implementation (Linux, Embedded, Systems)
4. 💻 Production-Grade Industry Code Implementation (Defensive, Safe, Error-Handled)
5. 📊 Visual Architecture / Memory Layout Diagram
6. ⚠️ Production Gotchas & Critical Crash Bugs (Segfaults, Leaks, Buffer Overflows)
7. 💼 Job Interview & Workplace Practical Scenarios
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalari_backend.settings')
django.setup()

from apps.curriculum.models import Subject, Module, Topic

INDUSTRY_TOPIC_NOTES = {
    # -------------------------------------------------------------------------
    # TOPIC 122: Introduction to C & GCC Compilation Architecture
    # -------------------------------------------------------------------------
    122: """# Introduction to C & GCC Compilation Architecture

## 1. Core Fundamental Concept & Syntax
C is a compiled, statically typed systems programming language designed for direct hardware manipulation and high-performance computation. Unlike interpreted languages (Python, JavaScript) that execute via a runtime virtual machine, C code is directly translated into native CPU machine instructions (ELF binary on Linux, PE on Windows).

```c
#include <stdio.h>

int main(void) {
    printf("SkillStack Systems Engineering in C\\n");
    return 0;
}
```

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  "Click the green Run button in Dev-C++ or Turbo C, or run `gcc main.c -o main`."
* **Why Developers Struggle in Real Jobs**:
  In a real software company, production codebases contain thousands of files. You never compile single files manually. You must understand the **4-stage compilation pipeline**, how the linker resolves symbols, how shared dynamic libraries (`.so`/`.dll`) load into virtual memory, and how compiler optimization flags (`-O2`, `-O3`) affect execution speed.
  Moreover, companies write cross-platform Makefiles and enforce strict compiler warnings: `-Wall -Wextra -Werror -pedantic`. If your code has even one warning, the production build pipeline (CI/CD) will reject your pull request!

---

## 3. 🏭 Production / Real-World Workplace Implementation
In real-world companies (Qualcomm, Intel, NVIDIA, Cisco, Linux systems):
1. **Multi-Stage Build Pipeline**:
   - **Stage 1 (Preprocessing - `gcc -E`)**: Expands `#include`, `#define`, `#ifdef`. Produces `.i` file.
   - **Stage 2 (Compilation - `gcc -S`)**: Parses syntax, applies AST optimizations, generates human-readable assembly instructions `.s`.
   - **Stage 3 (Assembly - `gcc -c`)**: Translates assembly mnemonics into relocatable machine code object files `.o`.
   - **Stage 4 (Linking - `gcc -o` / `ld`)**: Resolves external symbol addresses across multiple object files and links standard libraries (`libc.so`). Produces final executable ELF binary.
2. **Process Virtual Memory Layout**:
   Every running process in Linux/Windows is mapped into a virtual memory address space:
   - **Text Segment**: Executable CPU machine code (Read-Only).
   - **Data Segment**: Initialized global and static variables.
   - **BSS Segment**: Uninitialized global and static variables (zero-initialized by kernel).
   - **Heap Segment**: Dynamically allocated memory (`malloc`), grows upwards.
   - **Stack Segment**: Function call frames, local variables, return addresses, grows downwards.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
+-------------------------------------------------------+ 0xFFFFFFFF (High Memory)
|                 KERNEL VIRTUAL MEMORY                 |
+-------------------------------------------------------+ 0xC0000000
|                     STACK SEGMENT                     |  |
|   (Local variables, function frames, return addresses) |  v Grows Downward
+-------------------------------------------------------+
|                           |                           |
|                           v                           |
|                                                       |
|                           ^                           |
|                           |                           |
+-------------------------------------------------------+
|                     HEAP SEGMENT                      |  ^ Grows Upward
|     (Dynamically allocated memory via malloc/calloc)   |  |
+-------------------------------------------------------+
|                      BSS SEGMENT                      |
|       (Uninitialized global and static variables)     |
+-------------------------------------------------------+
|                  INITIALIZED DATA                     |
|        (Global & static variables with values)        |
+-------------------------------------------------------+
|                     TEXT SEGMENT                      |
|          (Compiled Machine Code - READ ONLY)          |
+-------------------------------------------------------+ 0x00000000 (Low Memory)
```

---

## 5. 💻 Production-Grade Industry Code Implementation

### Production Makefile Structure:
```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -O2 -std=c11 -D_GNU_SOURCE
SANFLAGS = -fsanitize=address,undefined -g
INCLUDES = -Iinclude
TARGET = build/skillstack_daemon

SRCS = src/main.c src/network_engine.c src/memory_pool.c
OBJS = $(SRCS:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
\t@mkdir -p build
\t$(CC) $(CFLAGS) $(SANFLAGS) -o $@ $^

%.o: %.c
\t$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
\trm -rf src/*.o $(TARGET)
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Treating Warnings as Ignorable**: In C, ignoring `-Wall` will mask format string vulnerabilities, uninitialized variable usage, or missing return statements that result in undefined behavior in production.
2. **Buffer Overflows in Text Segment**: Attempting to write into string literals (e.g., `char *s = "Hello"; s[0] = 'h';`) triggers `SIGSEGV` (Segmentation Fault) because string literals live in the read-only Text/Rodata segment. Always use mutable arrays: `char s[] = "Hello";`.

---

## 7. 💼 Job Interview & Workplace Practical Scenarios
* **Interview Question**: "Explain the exact difference between BSS and Data segments. Why does BSS take zero disk space in the executable file?"
  * *Answer*: Data segment stores initialized globals (e.g. `int count = 5;`) requiring raw bytes stored in the binary on disk. BSS stores uninitialized globals (e.g. `int buffer[1024];`). The ELF header merely records the BSS size; the OS kernel zero-fills this RAM region at process startup (`execve`), keeping executable file size small.
""",

    # -------------------------------------------------------------------------
    # TOPIC 123: Variables, Constants, Memory Sizes & Primitive Data Types
    # -------------------------------------------------------------------------
    123: """# Variables, Constants, Memory Sizes & Primitive Data Types

## 1. Core Fundamental Concept & Syntax
Variables represent named locations in physical RAM. In C, data types determine how many bytes are allocated and how the CPU interprets the binary bit patterns (signed two's complement vs unsigned binary vs IEEE 754 floating point).

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  "int is always 4 bytes, long is 8 bytes, char is 1 byte."
* **Why Developers Struggle in Real Jobs**:
  `int` is **NOT** 4 bytes everywhere! In embedded systems (e.g., 16-bit TI MSP430 or 8-bit AVR microcontrollers), `int` is only 16 bits (2 bytes).
  Furthermore, `long` is 32-bit on 64-bit Windows (LLP64 data model), but 64-bit on 64-bit Linux/macOS (LP64 data model)!
  If you write `int` or `long` in networking code, device drivers, or binary file formats, your code will corrupt data and crash across systems.
  **In professional engineering, you must NEVER use raw `int`, `short`, `long` for binary protocols. You MUST use `<stdint.h>` exact-width integer types (`uint8_t`, `int16_t`, `int32_t`, `uint64_t`).**

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **`<stdint.h>` Standard Types**:
  - `uint8_t`: Exactly 1 byte (0 to 255). Used for raw byte buffers, network packets, cryptography hashes.
  - `int32_t`: Exactly 4 bytes (-2,147,483,648 to 2,147,483,647).
  - `uint64_t`: Exactly 8 bytes (0 to 18,446,744,073,709,551,615). Used for timestamps (nanoseconds), database IDs, file offsets.
  - `size_t`: Unsigned integer representing object size in memory (`sizeof`). Guaranteed to match CPU architecture address size (32-bit or 64-bit).
* **Integer Overflow & Security Exploits**:
  In C, **signed integer overflow is Undefined Behavior (UB)**. The compiler is legally permitted to optimize away safety checks if signed overflow occurs! Senior engineers use unsigned arithmetic or compiler built-ins for overflow detection.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Endianness in RAM: Storing 32-bit Value 0x12345678 at Address 0x1000

LITTLE ENDIAN (x86_64, ARM default): Least Significant Byte FIRST
Address:   0x1000   0x1001   0x1002   0x1003
Value:    [ 0x78 ] [ 0x56 ] [ 0x34 ] [ 0x12 ]

BIG ENDIAN (Network Byte Order, PowerPC): Most Significant Byte FIRST
Address:   0x1000   0x1001   0x1002   0x1003
Value:    [ 0x12 ] [ 0x34 ] [ 0x56 ] [ 0x78 ]
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <limits.h>

// Production Safe Addition with Overflow Detection
bool safe_add_uint32(uint32_t a, uint32_t b, uint32_t *result) {
    if (UINT32_MAX - a < b) {
        // Overflow will occur! Prevent memory corruption
        return false;
    }
    *result = a + b;
    return true;
}

int main(void) {
    uint32_t balance = 4000000000U;
    uint32_t deposit = 500000000U;
    uint32_t new_balance = 0;

    if (!safe_add_uint32(balance, deposit, &new_balance)) {
        fprintf(stderr, "[SECURITY ALERT] Integer overflow prevented in transaction!\\n");
        return 1;
    }

    printf("New Balance: %u\\n", new_balance);
    return 0;
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Silent Wrap-Around**: `uint8_t count = 255; count++;` wraps around to `0`. If used in a loop condition `while (count <= 255)`, it creates an infinite loop that freezes the service!
2. **Comparing Signed with Unsigned**:
   ```c
   int a = -1;
   unsigned int b = 1;
   if (a < b) { ... } // FALSE! 'a' is implicitly promoted to unsigned 4,294,967,295!
   ```
""",

    # -------------------------------------------------------------------------
    # TOPIC 124: Operators, Expressions & Precedence Hierarchy
    # -------------------------------------------------------------------------
    124: """# Operators, Expressions & Precedence Hierarchy

## 1. Core Fundamental Concept & Syntax
Operators perform computations on operands. Precedence determines evaluation order. In systems engineering, operators are heavily used for bitwise hardware register masking, pointer offset calculation, and short-circuit validation.

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  "Solve tricky puzzles like `int x = 5; printf("%d %d %d", x++, ++x, x);`"
* **Why Developers Struggle in Real Jobs**:
  Writing code with multiple un-sequenced modifications (`i = i++ + ++i`) is **Undefined Behavior** in the C ISO standard. Different compilers (GCC vs Clang vs MSVC) generate completely different results. In an enterprise codebase, such code will fail code review instantly.
  In the real world, what matters is:
  1. **Short-Circuit Evaluation (`&&`, `||`)**: Used to prevent NULL pointer dereferences: `if (ptr != NULL && ptr->is_active)`.
  2. **Bitwise Operators for Register Manipulation**: Setting, clearing, and toggling specific hardware bits without disturbing other bits.

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Defensive Pointer Null-Guard Pattern**:
  In C, logical `&&` evaluates left-to-right. If the left side is false, the right side is **never evaluated**.
  ```c
  // Safe: If 'user' is NULL, user->auth_token is NEVER accessed, avoiding crash
  if (user != NULL && user->auth_token != NULL && user->is_authenticated) {
      process_request();
  }
  ```
* **Bitwise Operations in Systems Engineering**:
  - Set bit `n`: `reg |= (1U << n);`
  - Clear bit `n`: `reg &= ~(1U << n);`
  - Toggle bit `n`: `reg ^= (1U << n);`
  - Check bit `n`: `if (reg & (1U << n)) { ... }`

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Hardware Control Register (8-bit):
Bit Position:   7     6     5     4     3     2     1     0
Register:     [ 0 ] [ 1 ] [ 0 ] [ 0 ] [ 1 ] [ 0 ] [ 1 ] [ 0 ]  (Value: 0x4A)

Operation: Enable Motor (Set Bit 3):
Mask (1U<<3): [ 0 ] [ 0 ] [ 0 ] [ 0 ] [ 1 ] [ 0 ] [ 0 ] [ 0 ]
Bitwise OR:   [ 0 ] [ 1 ] [ 0 ] [ 0 ] [ 1 ] [ 0 ] [ 1 ] [ 0 ]  (Motor is ON)
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define STATUS_FLAG_CONNECTED (1U << 0)
#define STATUS_FLAG_ENCRYPTED (1U << 1)
#define STATUS_FLAG_ERROR     (1U << 2)

typedef struct {
    uint32_t session_id;
    uint8_t flags;
} NetworkSession;

void inspect_session(const NetworkSession *session) {
    // Defensive short-circuit check: Ensure pointer is valid before reading flags
    if (session == NULL) {
        fprintf(stderr, "Invalid session pointer!\\n");
        return;
    }

    if ((session->flags & (STATUS_FLAG_CONNECTED | STATUS_FLAG_ENCRYPTED)) == 
        (STATUS_FLAG_CONNECTED | STATUS_FLAG_ENCRYPTED)) {
        printf("Session %u is securely connected.\\n", session->session_id);
    }
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Accidental Assignment in `if` statement**: `if (status = 1)` sets `status` to 1 and is always true! Always use `-Werror=parentheses` or Yoda conditions (`if (1 == status)`).
2. **Bitwise Precedence Trap**: `==` has higher precedence than `&`!
   ```c
   // BUG: Evaluates as: if (flags & (STATUS_OK == 1))
   if (flags & STATUS_OK == 1) // WRONG!
   if ((flags & STATUS_OK) == 1) // CORRECT!
   ```
""",

    # -------------------------------------------------------------------------
    # TOPIC 125: Standard Console I/O, Buffer Flushing & Format Specifiers
    # -------------------------------------------------------------------------
    125: """# Standard Console I/O, Buffer Flushing & Format Specifiers

## 1. Core Fundamental Concept & Syntax
Console I/O connects your application to standard streams: `stdin` (0), `stdout` (1), and `stderr` (2). Stream I/O is buffered by the C runtime library (`libc`) to minimize expensive kernel system calls (`read` and `write`).

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  `scanf("%s", name); gets(address); printf(user_input);`
* **Why Developers Struggle in Real Jobs**:
  1. **`gets()` is so dangerously insecure that it was completely deleted from the C11 Standard!** It provides no buffer length limit, enabling attackers to overwrite the stack return address and execute arbitrary exploit payloads (CWE-120).
  2. **Format String Exploits**: `printf(user_input)` allows attackers to view memory and overwrite return pointers (`%n` specifier). Production code mandates `printf("%s", user_input);`.
  3. **Buffered I/O Trap**: In an embedded system or crash scenario, `printf("Crash 1");` might never appear on the console because `stdout` was not flushed before `abort()`, misleading debugging for hours!

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Safe Input with `fgets()`**: Always specify buffer capacity:
  ```c
  char buffer[256];
  if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
      // Remove trailing newline
      buffer[strcspn(buffer, "\\r\\n")] = '\\0';
  }
  ```
* **Safe Formatting with `snprintf()`**: Prevents string truncation overflows:
  ```c
  char log_msg[128];
  snprintf(log_msg, sizeof(log_msg), "[NODE-%d] Heartbeat OK: %lu ms", node_id, uptime);
  ```
* **Buffer Flushing Strategies**:
  - `stdout`: Line-buffered when connected to a terminal (flushes on `\\n`), but block-buffered (4096 bytes) when redirected to a file or pipe.
  - `stderr`: Unbuffered. Output appears immediately on screen.
  - Force immediate write to OS kernel: `fflush(stdout);`.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
User Program Space                     Linux Kernel / Hardware
+----------------------+              +----------------------+
|  printf("Data\\n");   |              |                      |
|          |           |              |                      |
|          v           |              |                      |
|  [libc Stream Buffer]| -- write() ->|  [OS TTY Driver]     |
|   (4096 Byte Cache)  | System Call  |          |           |
|                      | (Flushed on  |          v           |
|                      |  \\n or full) |     [Physical Screen]|
+----------------------+              +----------------------+
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Production Safe User Input Reader
int read_secure_string(char *dest, size_t dest_size) {
    if (dest == NULL || dest_size == 0) return -1;

    if (fgets(dest, (int)dest_size, stdin) == NULL) {
        return -1; // EOF or input error
    }

    // Strip newline characters cleanly
    size_t len = strlen(dest);
    if (len > 0 && (dest[len - 1] == '\\n' || dest[len - 1] == '\\r')) {
        dest[len - 1] = '\\0';
    } else {
        // Input exceeded buffer size: Drain remaining characters from stdin buffer
        int ch;
        while ((ch = getchar()) != '\\n' && ch != EOF);
    }
    return 0;
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Format Specifier Mismatch**: Passing a 64-bit integer to `%d` causes stack corruption and undefined output on 64-bit machines. Use `PRId64` / `PRIu64` from `<inttypes.h>`.
2. **Missing `fflush(stdout)` in Daemons**: Long-running background processes running under `systemd` or Docker will not display logs in real time if `stdout` is redirected unless you run `setlinebuf(stdout);`.
""",

    # -------------------------------------------------------------------------
    # TOPIC 126: Control Flow, Conditional Branching & Switch-Case
    # -------------------------------------------------------------------------
    126: """# Control Flow, Conditional Branching & Switch-Case

## 1. Core Fundamental Concept & Syntax
Control flow structures direct code execution based on boolean expressions (`if/else`) or discrete integral values (`switch/case`).

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  "Calculate student grade A/B/C using `if/else`, or make a simple 4-function calculator using `switch`."
* **Why Developers Struggle in Real Jobs**:
  1. **Finite State Machines (FSM)**: Industrial firmware, network protocols (TCP handshakes), and game engines are built using state machines. Nested `if/else` ladders turn into unmaintainable spaghetti code. Senior engineers design structured `switch(state)` tables.
  2. **CPU Branch Prediction Penalties**: Modern super-scalar CPUs speculatively execute instructions ahead of time. When a branch (`if/else`) is mispredicted, the CPU must flush its entire execution pipeline, wasting 15–20 clock cycles! High-frequency trading and Linux kernel code use branch hinting macros: `likely()` and `unlikely()`.

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Linux Kernel Branch Hints**:
  ```c
  #define likely(x)   __builtin_expect(!!(x), 1)
  #define unlikely(x) __builtin_expect(!!(x), 0)

  // Fast path: In 99.999% of requests, memory pointer is valid
  if (likely(cache_entry != NULL)) {
      return cache_entry->data;
  } else {
      // Slow path: Rare cache miss handled out-of-line
      return fetch_from_disk();
  }
  ```
* **State Machine Pattern with `switch-case`**:
  Every case must end with `break;` unless deliberate fallthrough is documented with `/* fallthrough */` (to satisfy GCC compiler `-Wimplicit-fallthrough`).

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Network Protocol State Machine (FSM):

   +----------------+
   |   STATE_IDLE   | <-------+
   +----------------+         |
           |                  | Timeout /
      SYN Received            | Reset
           v                  |
   +----------------+         |
   | STATE_SYN_RCVD | --------+
   +----------------+
           |
      ACK Received
           v
   +----------------+
   | STATE_ESTABLISHED|
   +----------------+
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>

typedef enum {
    STATE_DISCONNECTED = 0,
    STATE_CONNECTING,
    STATE_CONNECTED,
    STATE_ERROR
} DeviceState;

void handle_device_event(DeviceState *state, int event_code) {
    switch (*state) {
        case STATE_DISCONNECTED:
            if (event_code == 1) {
                printf("[FSM] Initiating handshake...\\n");
                *state = STATE_CONNECTING;
            }
            break;

        case STATE_CONNECTING:
            if (event_code == 2) {
                printf("[FSM] Handshake ACK received! Connected.\\n");
                *state = STATE_CONNECTED;
            } else if (event_code == -1) {
                *state = STATE_ERROR;
            }
            break;

        case STATE_CONNECTED:
            // Normal operating state
            break;

        case STATE_ERROR:
        default:
            printf("[FSM] Recovering from error state.\\n");
            *state = STATE_DISCONNECTED;
            break;
    }
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Accidental Fallthrough**: Missing `break;` causes execution to fall through to the next case, causing silent state corruption in network packets.
2. **Missing `default` Case**: In automotive/medical systems (MISRA C), every `switch` statement **MUST** have a `default` case to handle unexpected corruption or invalid enum values.
""",

    # -------------------------------------------------------------------------
    # TOPIC 127: Loops, Iteration Mechanics & Jump Statements
    # -------------------------------------------------------------------------
    127: """# Loops, Iteration Mechanics & Jump Statements

## 1. Core Fundamental Concept & Syntax
Loops execute a block of code repeatedly while a condition holds (`for`, `while`, `do-while`). Jump statements (`break`, `continue`, `goto`) alter normal iterative flow.

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  "Print star patterns `*`, print Fibonacci series, and never ever use `goto` under any circumstances."
* **Why Developers Struggle in Real Jobs**:
  1. **Cache Locality in Nested Loops**: Iterating a 2D array row-major (`matrix[i][j]`) vs column-major (`matrix[j][i]`) can be **10x to 50x slower** on large data sets! College never explains CPU L1/L2 cache lines (64 bytes).
  2. **The `goto cleanup` Pattern**: In college they ban `goto`. In the **Linux Kernel, there are over 100,000 `goto` statements!** Why? Because C has no object destructors (like C++ RAII). The `goto error_cleanup;` cascade is the industry standard idiom for clean, non-leaking error handling across multiple resource allocations.

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Row-Major Cache Optimization**:
  C stores 2D arrays in contiguous row-major order: `matrix[0][0], matrix[0][1], matrix[0][2]...`.
  When accessing row-by-row, the CPU hardware prefetcher loads contiguous 64-byte chunks into L1 cache with zero cache misses.
* **The Linux Kernel Clean-Up Cascade**:
  When a function opens a file, allocates memory, and grabs a mutex, handling failures with nested `if` statements leads to arrow code (`>>>>>`). A cleanup cascade with `goto` ensures all resources are freed in reverse order of acquisition.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
CPU L1 Cache Line (64 Bytes = 16 integers of 4 bytes each):
+---------------------------------------------------------------+
| arr[0][0] | arr[0][1] | arr[0][2] | ... | arr[0][15]         |
+---------------------------------------------------------------+
 ^
 | Loaded into CPU Cache in ONE operation!

Row-Major Access (for i; for j: arr[i][j]): 1 Cache Miss every 16 iterations!
Column-Major Access (for j; for i: arr[i][j]): 1 Cache Miss EVERY iteration!
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdlib.h>

int process_hardware_payload(const char *filename) {
    FILE *fp = NULL;
    char *buffer = NULL;
    int ret_code = -1;

    fp = fopen(filename, "rb");
    if (fp == NULL) {
        perror("Failed to open payload");
        goto cleanup_none;
    }

    buffer = (char *)malloc(4096);
    if (buffer == NULL) {
        perror("Failed to allocate RAM");
        goto cleanup_file;
    }

    // Process data safely...
    printf("Payload processed successfully.\\n");
    ret_code = 0; // Success

cleanup_buffer:
    free(buffer);
cleanup_file:
    fclose(fp);
cleanup_none:
    return ret_code;
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Infinite Loops from Unsigned Decrement**:
   ```c
   // BUG: 'i' is unsigned. When i == 0, i-- wraps around to 4,294,967,295!
   for (size_t i = 10; i >= 0; i--) { ... } // Infinite loop!
   ```
2. **Off-By-One Errors**: `for (int i = 0; i <= size; i++)` writes one element past the buffer end, corrupting the stack frame return address.
""",

    # -------------------------------------------------------------------------
    # TOPIC 128: Functions, Storage Classes & Stack Frame Recursion
    # -------------------------------------------------------------------------
    128: """# Functions, Storage Classes & Stack Frame Recursion

## 1. Core Fundamental Concept & Syntax
Functions encapsulate reusable logic. Storage classes (`static`, `extern`, `auto`, `register`) control variable scope, linkage, and lifetime.

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  "Recursion is elegant: use recursion for Factorial and Fibonacci numbers."
* **Why Developers Struggle in Real Jobs**:
  1. **Recursion is Strictly Banned in Production Firmware & Aerospace!** (MISRA C Rule 17.2). Why? Embedded microcontrollers have tiny stacks (e.g. 2 KB RAM). Deep or unbounded recursion causes Stack Overflow, instantly crashing medical devices, automotive ECUs, or aerospace flight controllers.
  2. **`static` for Information Hiding**: In college, `static` is only taught as "a variable that retains its value". In real software architectures, `static` placed on global variables and functions creates **Internal Linkage** (making them private to the `.c` file), providing C with encapsulation similar to `private` in C++ or Java!

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Function Pointer Callbacks**:
  In device drivers, networking engines, and GUI toolkits, functions are passed as arguments to register event listeners:
  ```c
  typedef void (*PacketHandlerCallback)(const uint8_t *payload, size_t len);
  void register_packet_listener(PacketHandlerCallback callback);
  ```
* **Reentrant and Thread-Safe Functions**:
  Production functions must be reentrant (not relying on shared global state without locks), allowing multiple OS threads (`pthread`) to execute the function concurrently.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Stack Frame Anatomy during Function Call: foo(int a, int b)

High Address
+-------------------------------------+
|        Caller's Stack Frame         |
+-------------------------------------+
|  Function Parameter 'b'             |
+-------------------------------------+
|  Function Parameter 'a'             |
+-------------------------------------+
|  Return Address (Where to resume)   | <--- Saved EIP / RIP
+-------------------------------------+
|  Saved Frame Pointer                | <--- Saved EBP / RBP
+-------------------------------------+
|  Local Variable 1 (e.g. buffer[64]) |
+-------------------------------------+
|  Local Variable 2 (e.g. int counter)| <--- Current Stack Pointer (ESP / RSP)
+-------------------------------------+
Low Address (Grows Downward)
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdint.h>

// Private file-scope encapsulation (Internal Linkage)
static uint32_t s_event_counter = 0;

static void log_internal_event(const char *msg) {
    s_event_counter++;
    printf("[INTERNAL LOG #%u] %s\\n", s_event_counter, msg);
}

// Public API Callback Typedef
typedef void (*DataConsumer)(int value, void *user_context);

// Public API Function (External Linkage)
void stream_sensor_data(DataConsumer consumer, void *user_context) {
    log_internal_event("Starting data stream...");
    for (int i = 1; i <= 3; i++) {
        if (consumer != NULL) {
            consumer(i * 10, user_context);
        }
    }
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Returning Pointer to Local Stack Variable**:
   ```c
   // CATASTROPHIC BUG: 'buf' is destroyed when function returns!
   char *get_name(void) {
       char buf[32] = "SkillStack";
       return buf; // Pointer points to garbage/overwritten stack memory!
   }
   ```
2. **Stack Exhaustion**: Declaring huge arrays on stack (`uint8_t buffer[1024 * 1024];`) overflows default thread stack limits. Always use dynamic allocation or static buffers for large payloads.
""",

    # -------------------------------------------------------------------------
    # TOPIC 129: Arrays, Row-Major Matrices & String Memory Mechanics
    # -------------------------------------------------------------------------
    129: """# Arrays, Row-Major Matrices & String Memory Mechanics

## 1. Core Fundamental Concept & Syntax
Arrays store elements of identical type in contiguous memory locations. Strings in C are merely arrays of characters terminated by a null byte (`'\\0'`).

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  `strcpy(dest, src); strcat(dest, " appended"); char str[10];`
* **Why Developers Struggle in Real Jobs**:
  1. `strcpy` and `strcat` are the root cause of the majority of security vulnerabilities (Buffer Overflows) in legacy C software. If `src` is larger than `dest`, `strcpy` will overwrite neighboring memory!
  2. In modern enterprise codebases (Google, Microsoft, Apple), `strcpy` and `sprintf` are completely banned by static analysis linters and replaced by `snprintf` or `strlcpy`.
  3. Real production systems use **Circular Ring Buffers** to stream audio, network packets, and UART data without moving memory or performing expensive reallocations.

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Circular Ring Buffer Architecture**:
  A fixed-size array with `head` and `tail` index pointers. Producers write to `tail`, consumers read from `head`. If `tail` reaches the array end, it wraps to `0` using modulo arithmetic `(tail + 1) % CAPACITY`.
* **Zero-Copy Slicing**:
  Instead of copying substrings with `malloc`, high-performance parsers (HTTP, JSON) pass a pointer and length (`const char *data, size_t len`) directly referencing the original network packet buffer.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Circular Ring Buffer in Contiguous RAM:

       [0]       [1]       [2]       [3]       [4]       [5]       [6]       [7]
   +---------+---------+---------+---------+---------+---------+---------+---------+
   |  Data A |  Data B |  Data C |  EMPTY  |  EMPTY  |  EMPTY  |  EMPTY  |  EMPTY  |
   +---------+---------+---------+---------+---------+---------+---------+---------+
        ^                             ^
        |                             |
      HEAD                          TAIL
 (Consumer reads)             (Producer writes)
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>

#define RING_BUFFER_SIZE 8

typedef struct {
    uint8_t buffer[RING_BUFFER_SIZE];
    size_t head;
    size_t tail;
    size_t count;
} RingBuffer;

void ring_init(RingBuffer *rb) {
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
}

bool ring_push(RingBuffer *rb, uint8_t byte) {
    if (rb->count == RING_BUFFER_SIZE) {
        return false; // Buffer Full! Drop or overwrite policy
    }
    rb->buffer[rb->tail] = byte;
    rb->tail = (rb->tail + 1) % RING_BUFFER_SIZE;
    rb->count++;
    return true;
}

bool ring_pop(RingBuffer *rb, uint8_t *out_byte) {
    if (rb->count == 0) {
        return false; // Buffer Empty!
    }
    *out_byte = rb->buffer[rb->head];
    rb->head = (rb->head + 1) % RING_BUFFER_SIZE;
    rb->count--;
    return true;
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Forgetting the Null Terminator (`'\\0'`)**: Allocating `char str[5]` for the 5-letter word `"HELLO"` causes buffer overrun because `"HELLO"` requires **6 bytes** (5 characters + 1 null terminator).
2. **Array Decay to Pointer**: Passing an array to a function `void process(int arr[])` converts it into a raw pointer `int *arr`. Calling `sizeof(arr)` inside the function returns the pointer size (8 bytes on 64-bit), NOT the array capacity! Always pass array length explicitly.
""",

    # -------------------------------------------------------------------------
    # TOPIC 130: Pointers Deep Dive, Address Arithmetic & Double Pointers
    # -------------------------------------------------------------------------
    130: """# Pointers Deep Dive, Address Arithmetic & Double Pointers

## 1. Core Fundamental Concept & Syntax
A pointer is an unsigned integer variable holding a direct virtual memory address. Pointers enable direct hardware manipulation, dynamic allocation, reference semantics, and zero-copy data structures.

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  "Swap two numbers `swap(&a, &b)`, and `int *p = &x;`."
* **Why Developers Struggle in Real Jobs**:
  In a real company:
  1. **Hardware Memory-Mapped I/O**: Microcontroller registers live at fixed physical addresses: `volatile uint32_t * const GPIOA = (uint32_t *)0x40020000;`. The `volatile` qualifier is mandatory to prevent compiler optimizations from caching the read!
  2. **Opaque Pointers (API Encapsulation)**: Enterprise libraries hide internal struct definitions (e.g. `typedef struct SSLContext SSLContext;`) so clients cannot tamper with internal private variables.
  3. **Double Pointers (`Type **`)**: Used to modify pointers passed to functions (e.g., dynamically reallocating a buffer or updating linked list heads without returning pointers).

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Pointer Arithmetic Rules**:
  Adding `1` to a pointer advances it by `sizeof(*ptr)` bytes:
  - `char *p`: `p + 1` advances **1 byte**.
  - `uint32_t *p`: `p + 1` advances **4 bytes**.
  - `double *p`: `p + 1` advances **8 bytes**.
* **Double Pointer Linked List Head Insertion**:
  Passing `Node **head_ref` allows the function to update the caller's head pointer directly without returning it.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Memory Layout of a Double Pointer:

Pointer 'pptr' (stored at 0x7fff10):
+-------------------------------+
|    Value: 0x7fff08            |  <--- Points to pointer 'ptr'
+-------------------------------+
                |
                v
Pointer 'ptr' (stored at 0x7fff08):
+-------------------------------+
|    Value: 0x7fff00            |  <--- Points to variable 'target'
+-------------------------------+
                |
                v
Variable 'target' (stored at 0x7fff00):
+-------------------------------+
|    Value: 42 (Integer Data)   |  <--- Dereferencing **pptr accesses this 42!
+-------------------------------+
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

// Production Double Pointer Head Insertion (O(1))
void list_push_front(Node **head_ref, int new_data) {
    if (head_ref == NULL) return;

    Node *new_node = (Node *)malloc(sizeof(Node));
    if (new_node == NULL) {
        perror("Failed to allocate node");
        return;
    }

    new_node->data = new_data;
    new_node->next = *head_ref; // Point to old head
    *head_ref = new_node;       // Move head to new node
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Dangling Pointer (Use-After-Free)**: Calling `free(ptr);` releases the memory block back to the heap, but `ptr` still holds the old address! Accessing `*ptr` afterwards causes security bugs or crashes. **Always set `ptr = NULL;` after freeing.**
2. **Wild Pointers**: Declaring `int *p;` without initializing it means it points to random memory. Dereferencing it will instantly trigger `SIGSEGV` or corrupt other memory variables.
""",

    # -------------------------------------------------------------------------
    # TOPIC 131: Dynamic Memory Allocation (malloc, calloc, realloc, free) & Leaks
    # -------------------------------------------------------------------------
    131: """# Dynamic Memory Allocation (malloc, calloc, realloc, free) & Leaks

## 1. Core Fundamental Concept & Syntax
Dynamic memory allocation allows programs to request heap memory at runtime using `malloc()`, `calloc()`, `realloc()`, and return it with `free()`.

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  `int *arr = (int*)malloc(n * sizeof(int)); free(arr);`
* **Why Developers Struggle in Real Jobs**:
  1. **Heap Fragmentation**: In long-running production daemons (running for months without reboot), continuous `malloc` and `free` of various sizes leaves memory fragmented. Eventually, a 1 MB allocation fails even if 500 MB of total free RAM exists!
  2. **Memory Leaks Crash Production**: Forgetting to free memory in an API loop will slowly consume all RAM until the Linux kernel OOM (Out Of Memory) Killer forcibly terminates your process!
  3. **Industry Solutions**: Real-time systems (Aerospace, Games) use **Memory Pools & Arena Allocators** where pre-allocated chunks are reused with zero overhead and zero fragmentation.

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Arena / Bump Allocator Pattern**:
  Allocate a large buffer once (e.g. 10 MB). Each allocation simply bumps an offset pointer forward (`offset += size`). When the entire task completes, the entire 10 MB is wiped in O(1) time by resetting `offset = 0`!
* **Memory Debugging with Valgrind & AddressSanitizer**:
  - GCC AddressSanitizer: `gcc -fsanitize=address -g main.c`
  - Valgrind Leak Check: `valgrind --leak-check=full ./main`

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Arena / Linear Memory Allocator:

[==================== ALLOCATED REGION ====================|========= FREE =========]
0x1000                                                    0x1400                 0x5000
                                                             ^
                                                             |
                                                        Offset Pointer
                                                  (Bumps forward on allocation)
To free ALL allocations: offset = 0! Instant O(1) deallocation with ZERO leaks!
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    uint8_t *buffer;
    size_t capacity;
    size_t offset;
} MemoryArena;

MemoryArena arena_create(size_t capacity) {
    MemoryArena arena;
    arena.buffer = (uint8_t *)malloc(capacity);
    arena.capacity = capacity;
    arena.offset = 0;
    return arena;
}

void *arena_alloc(MemoryArena *arena, size_t bytes) {
    // 8-byte memory alignment for CPU efficiency
    size_t aligned_bytes = (bytes + 7) & ~7;

    if (arena->offset + aligned_bytes > arena->capacity) {
        return NULL; // Out of Arena RAM!
    }

    void *ptr = &arena->buffer[arena->offset];
    arena->offset += aligned_bytes;
    return ptr;
}

void arena_reset(MemoryArena *arena) {
    arena->offset = 0; // Wipes all allocations instantly!
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Double Free Crash**: Calling `free(ptr); free(ptr);` corrupts the `glibc` malloc chunk metadata, causing immediate process termination (`SIGABRT`).
2. **`realloc` Memory Leak Trap**:
   ```c
   // BUG: If realloc fails, it returns NULL and overwrites 'ptr', leaking the original buffer!
   ptr = realloc(ptr, new_size); // WRONG!
   
   void *tmp = realloc(ptr, new_size); // CORRECT!
   if (tmp == NULL) { /* handle error without losing 'ptr' */ }
   else { ptr = tmp; }
   ```
""",

    # -------------------------------------------------------------------------
    # TOPIC 132: Structures, Unions, Typedef & Memory Padding Alignment
    # -------------------------------------------------------------------------
    132: """# Structures, Unions, Typedef & Memory Padding Alignment

## 1. Core Fundamental Concept & Syntax
Structures group heterogeneous data elements under a single type. Unions share the same physical memory location among multiple members.

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  `struct Student { int id; char name[20]; float marks; };`
* **Why Developers Struggle in Real Jobs**:
  1. **Structure Padding & Memory Alignment**: In real computers, the CPU fetches memory in 32-bit or 64-bit words. Compilers automatically insert silent **padding bytes** between struct members!
  2. If you serialize a struct directly across a network socket or save it to a binary file, the receiving computer (with different compiler alignment or architecture) will read corrupted garbage data!
  3. **Packed Structures**: In networking and hardware drivers, you must disable padding using `#pragma pack(push, 1)` or `__attribute__((packed))`.

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Struct Member Reordering to Save RAM**:
  ```c
  // Bad alignment: 12 bytes (wastes 4 bytes on padding)
  struct Bad { char a; int b; char c; };

  // Optimized alignment: 8 bytes (reorder largest to smallest)
  struct Good { int b; char a; char c; };
  ```
* **Tagged Unions for Polymorphism**:
  Used in JSON parsers, abstract syntax trees (ASTs), and operating system event queues to represent variant types safely.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Structure Padding Example: struct { char a; int b; } on 32-bit Architecture

Address:   0x00     0x01     0x02     0x03     0x04     0x05     0x06     0x07
Byte:     [ a ]   [ PAD ]  [ PAD ]  [ PAD ]  [      b (4 Bytes integer)      ]
                    ^-------- Wasted 3 Bytes of RAM due to 4-byte CPU alignment!

Packed Structure (__attribute__((packed))):
Address:   0x00     0x01     0x02     0x03     0x04
Byte:     [ a ]   [      b (4 Bytes integer)      ]  (Zero padding, exact 5 bytes)
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdint.h>

// Production Network Packet Header (Exact wire layout)
#pragma pack(push, 1)
typedef struct {
    uint8_t  version;
    uint8_t  packet_type;
    uint16_t payload_length;
    uint32_t sequence_id;
    uint32_t checksum;
} NetworkPacketHeader;
#pragma pack(pop)

// Tagged Union Pattern for Polymorphic Event Handling
typedef enum { EVENT_KEYPRESS, EVENT_MOUSE_CLICK } EventType;

typedef struct {
    EventType type;
    union {
        struct { int key_code; char modifier; } key;
        struct { int x; int y; int button; } mouse;
    } data;
} AppEvent;
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Unaligned Access Faults on ARM**: Accessing multi-byte integers at unaligned memory addresses causes an immediate Hardware Fault exception on older ARM microcontrollers.
2. **Writing to Wrong Union Member**: Reading member `B` after writing member `A` reinterprets the raw binary bits. This is valid only for type-punning, but causes logic bugs if done unintentionally.
""",

    # -------------------------------------------------------------------------
    # TOPIC 133: File Handling, Stream I/O & Binary File Operations
    # -------------------------------------------------------------------------
    133: """# File Handling, Stream I/O & Binary File Operations

## 1. Core Fundamental Concept & Syntax
File I/O persists application state to secondary storage (SSD, Hard Disk, Flash) using text streams or raw binary byte sequences.

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  `FILE *fp = fopen("data.txt", "w"); fprintf(fp, "hello"); fclose(fp);`
* **Why Developers Struggle in Real Jobs**:
  1. **Power Loss Corruption**: If power cuts or the machine crashes while `fprintf` is running, your data file will be half-written and permanently corrupted!
  2. **Atomic Write Pattern**: Enterprise software writes data to a temporary file (`data.txt.tmp`), flushes it to disk (`fsync`), and atomically replaces the original file using `rename()`. The POSIX `rename` operation is guaranteed atomic by the file system!
  3. **Binary File Magic Numbers & Checksums**: Production binary files always start with a 4-byte "Magic Number" (e.g. `0x89504E47` for PNG) and end with a CRC32 checksum to verify data integrity against disk corruption.

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **Binary vs Text Files**:
  Binary I/O (`fread`, `fwrite`) directly reads/writes memory representations without character encoding conversions, executing up to **100x faster** than `fprintf`/`fscanf`.
* **Atomic File Save Pattern**:
  1. `fopen("config.json.tmp", "wb")`
  2. Write payload with `fwrite()`
  3. Call `fflush()` and `fsync(fileno(fp))`
  4. `fclose()`
  5. `rename("config.json.tmp", "config.json")`

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Production Binary File Layout with Integrity Verification:

Offset:    0x00                     0x04                 0x08           EOF - 4
+------------------------+------------------------+---------------+---------------+
| Magic Number (4 Bytes) | Format Version (4 B)   | Binary Record | CRC32 (4 B)   |
| e.g. "SKTK" (0x534B544B)| e.g. 0x00000001        | Payloads      | Checksum      |
+------------------------+------------------------+---------------+---------------+
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define FILE_MAGIC 0x534B544B // "SKTK" in hex

typedef struct {
    uint32_t magic;
    uint32_t version;
    uint32_t record_count;
} FileHeader;

bool save_binary_records(const char *filename, const void *data, size_t total_bytes) {
    char temp_filename[256];
    snprintf(temp_filename, sizeof(temp_filename), "%s.tmp", filename);

    FILE *fp = fopen(temp_filename, "wb");
    if (!fp) return false;

    FileHeader header = { FILE_MAGIC, 1, 100 };
    if (fwrite(&header, sizeof(header), 1, fp) != 1) {
        fclose(fp);
        remove(temp_filename);
        return false;
    }

    if (fwrite(data, total_bytes, 1, fp) != 1) {
        fclose(fp);
        remove(temp_filename);
        return false;
    }

    fclose(fp);

    // Atomic swap: Overwrite destination safely
    if (rename(temp_filename, filename) != 0) {
        remove(temp_filename);
        return false;
    }
    return true;
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Failure to Check `fopen` Return Value**: Calling `fread` or `fprintf` on a `NULL` file pointer causes instant segmentation faults.
2. **Buffer Flush Incompleteness**: Closing a file with `fclose()` flushes `libc` buffers, but does NOT guarantee data has reached physical disk platters/NAND flash. In mission-critical databases, you must call POSIX `fsync(fileno(fp))`.
""",

    # -------------------------------------------------------------------------
    # TOPIC 134: Bitwise Masking, Shift Operators & Systems Register Simulation
    # -------------------------------------------------------------------------
    134: """# Bitwise Masking, Shift Operators & Systems Register Simulation

## 1. Core Fundamental Concept & Syntax
Bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`) manipulate individual binary bits within integer types.

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  "Calculate `5 & 3` or `5 << 1` on paper for exams."
* **Why Developers Struggle in Real Jobs**:
  In embedded systems, Linux device drivers, networking stacks, and cryptography:
  - You interact with hardware microchips where every individual bit controls a physical circuit (e.g., Bit 0 = LED Power, Bit 1 = Motor Direction, Bit 2 = Temperature Sensor Interrupt).
  - You must know how to set, clear, and toggle specific bits **atomically** without modifying the state of neighboring bits!
  - Network packets (IP header flags, TCP SYN/ACK/FIN flags) are packed into single-byte bitfields to save bandwidth.

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **The Universal Bit-Manipulation Macros**:
  ```c
  #define BIT(n)              (1UL << (n))
  #define SET_BIT(reg, n)     ((reg) |= BIT(n))
  #define CLEAR_BIT(reg, n)   ((reg) &= ~BIT(n))
  #define TOGGLE_BIT(reg, n)  ((reg) ^= BIT(n))
  #define CHECK_BIT(reg, n)   (!!((reg) & BIT(n)))
  ```
* **Bitwise Permission Flags (POSIX Style)**:
  `open("file.txt", O_RDWR | O_CREAT | O_TRUNC);` combines distinct powers-of-two bits into a single integer parameter.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
Hardware Control Register Simulation (32-bit):

Bit 31                                                  Bit 2  Bit 1  Bit 0
+-------------------------------------------------------+------+------+------+
| ... RESERVED BITS (DO NOT OVERWRITE) ...              | ERR  | TX_EN| RX_EN|
+-------------------------------------------------------+------+------+------+

Setting TX_EN (Bit 1) using OR Mask:
Current:   [ ... 0 0 0 ... 1 0 0 ]  (RX_EN is 0, ERR is 1)
Mask:      [ ... 0 0 0 ... 0 1 0 ]  (BIT(1))
Result:    [ ... 0 0 0 ... 1 1 0 ]  (TX_EN is now 1, other bits untouched!)
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#include <stdio.h>
#include <stdint.h>

#define REG_TX_ENABLE   (1U << 0)
#define REG_RX_ENABLE   (1U << 1)
#define REG_INTERRUPT   (1U << 2)
#define REG_BAUD_MASK   (0x0F << 4) // Bits 4-7 hold baud rate preset

typedef struct {
    volatile uint32_t control_reg;
} HardwareUART;

void configure_uart(HardwareUART *uart, uint8_t baud_rate_preset) {
    // 1. Enable TX and RX simultaneously
    uart->control_reg |= (REG_TX_ENABLE | REG_RX_ENABLE);

    // 2. Set 4-bit baud rate without overwriting TX/RX flags:
    // First clear bits 4-7, then OR the new preset
    uart->control_reg &= ~REG_BAUD_MASK;
    uart->control_reg |= ((baud_rate_preset & 0x0F) << 4);
}
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Shifting Beyond Integer Width**: Shifting a 32-bit integer by 32 or more (`1U << 32`) is **Undefined Behavior** in C! On x86 CPUs, the shift count is masked by 31, producing `1U << 0 = 1` instead of `0`.
2. **Sign Extension Bug with Signed Types**: Right-shifting a negative signed integer (`int8_t x = -8; x >> 2`) performs an **Arithmetic Shift**, filling the top bits with `1`s instead of `0`s. Always use unsigned types (`uint32_t`) for bitwise shifts!
""",

    # -------------------------------------------------------------------------
    # TOPIC 135: Preprocessor Directives, Header Guards & Systems Debugging
    # -------------------------------------------------------------------------
    135: """# Preprocessor Directives, Header Guards & Systems Debugging

## 1. Core Fundamental Concept & Syntax
The preprocessor (`cpp`) runs before compilation, performing textual substitution, header inclusion (`#include`), macro expansion (`#define`), and conditional compilation (`#ifdef`).

---

## 2. 🚨 The College Trap vs. Real Industry Reality
* **What College / Academia Teaches**:
  `#define PI 3.14159; #define SQUARE(x) x * x`
* **Why Developers Struggle in Real Jobs**:
  1. **Macro Operator Precedence Trap**: `SQUARE(2 + 3)` expands textually to `2 + 3 * 2 + 3 = 2 + 6 + 3 = 11`, instead of `25`! Macros must always parenthesize arguments and expressions: `#define SQUARE(x) ((x) * (x))`.
  2. **Multi-Statement Macro Trap**:
     ```c
     #define INIT() step1(); step2()
     if (condition) INIT(); // Expands to: if (condition) step1(); step2(); -> step2 ALWAYS runs!
     ```
     Production macros **MUST** use the `do { ... } while(0)` idiom.
  3. **Header Guards**: Forgetting `#ifndef` / `#pragma once` causes duplicate symbol definitions when headers are included across multiple files.

---

## 3. 🏭 Production / Real-World Workplace Implementation
* **The `do { ... } while(0)` Idiom**:
  Allows multi-statement macros to behave like a single statement safely in `if/else` constructs.
* **Production Structured Logging Framework**:
  Using compiler built-in macros: `__FILE__`, `__LINE__`, `__func__`, `__DATE__`.
* **Systems Debugging with GDB & Core Dumps**:
  When a production C server crashes with Segmentation Fault, the Linux OS saves a snapshot of the process RAM to a `core` dump file. Senior engineers inspect core dumps using `gdb ./program core` to view the exact stack trace (`bt`) at the moment of failure.

---

## 4. 📊 Visual Architecture / Memory Layout Diagram

```
The do { ... } while(0) Macro Shield:

#define LOG_EVENT(msg) \\
    do { \\
        fprintf(stderr, "[%s:%d in %s()] %s\\n", __FILE__, __LINE__, __func__, (msg)); \\
    } while(0)

Safe Usage in Code:
if (is_error)
    LOG_EVENT("Connection lost"); // Semicolon cleanly terminates the do-while!
else
    proceed(); // 'else' binds correctly to the 'if'!
```

---

## 5. 💻 Production-Grade Industry Code Implementation

```c
#ifndef SKILLSTACK_LOGGER_H
#define SKILLSTACK_LOGGER_H

#include <stdio.h>
#include <time.h>

#define LOG_LEVEL_DEBUG 0
#define LOG_LEVEL_INFO  1
#define LOG_LEVEL_ERROR 2

#ifndef CURRENT_LOG_LEVEL
#define CURRENT_LOG_LEVEL LOG_LEVEL_INFO
#endif

#define LOG_ERROR(fmt, ...) \\
    do { \\
        if (CURRENT_LOG_LEVEL <= LOG_LEVEL_ERROR) { \\
            fprintf(stderr, "[ERROR] [%s:%d in %s()] " fmt "\\n", \\
                    __FILE__, __LINE__, __func__, ##__VA_ARGS__); \\
        } \\
    } while(0)

#define LOG_INFO(fmt, ...) \\
    do { \\
        if (CURRENT_LOG_LEVEL <= LOG_LEVEL_INFO) { \\
            fprintf(stdout, "[INFO] " fmt "\\n", ##__VA_ARGS__); \\
        } \\
    } while(0)

#endif // SKILLSTACK_LOGGER_H
```

---

## 6. ⚠️ Production Gotchas & Critical Crash Bugs
1. **Semicolon at the end of `#define`**: Writing `#define MAX_BUFFER 1024;` causes syntax errors when used in `int arr[MAX_BUFFER];`.
2. **Double Evaluation in Macros**:
   ```c
   #define MAX(a, b) ((a) > (b) ? (a) : (b))
   int x = 5, y = 10;
   int m = MAX(x++, y++); // y is incremented TWICE! Never pass expressions with side effects to macros.
   ```
"""
}

def main():
    print("==================================================")
    print("Seeding Industry Workplace C Programming Curriculum")
    print("==================================================")

    updated_count = 0
    for topic_id, notes in INDUSTRY_TOPIC_NOTES.items():
        try:
            topic = Topic.objects.get(id=topic_id)
            topic.notes_content = notes.strip()
            topic.save()
            print(f"[SUCCESS] Updated Topic #{topic.id}: '{topic.title}' ({len(notes)} chars)")
            updated_count += 1
        except Topic.DoesNotExist:
            print(f"[WARNING] Topic #{topic_id} not found in database.")

    print(f"\\nFinished! Successfully updated {updated_count} topics with industry-ready workplace mastery notes.")

if __name__ == '__main__':
    main()
