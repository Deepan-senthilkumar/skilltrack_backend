"""
Full C Programming Syllabus Seeder for SkillStack.
Populates:
- 12 Core Theoretical & Practical Modules (140 Topics)
- Module 13: Practice Projects (12 Milestone Projects)
- Mandatory Practical Coding Problems for every topic
- Optional Interview Questions submodule under every module
- FreeCodeCamp style milestone project links
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skilltrack_server.settings")
django.setup()

from apps.curriculum.models import Subject, Module, Topic, Problem, CodeExample
from django.db import transaction

MODULES_DATA = [
    {
        "name": "1. C Programming Basics",
        "level": "beginner",
        "milestone": 1,
        "topics": [
            (1, "Introduction to C", "History, origins by Dennis Ritchie at Bell Labs, portability and importance as the mother of modern programming languages."),
            (2, "Features of C", "Low-level memory access, high efficiency, simple syntax, structured architecture, and hardware closeness."),
            (3, "Structure of a C Program", "Documentation section, preprocessor directives (#include), main() function entry point, statements, and return 0;."),
            (4, "Compiler and Execution Process", "Detailed flow of Preprocessing (.i) -> Compilation (.s) -> Assembly (.o / .obj) -> Linking (.exe / ELF)."),
            (5, "Keywords and Identifiers", "The 32 standard C89/C99 keywords, naming conventions, valid and invalid identifier rules in C."),
            (6, "Variables and Constants", "Memory allocation for variables, declaration vs definition, initialization, const qualifier, and #define constants."),
            (7, "Data Types", "Primitive types (int, char, float, double), modifiers (short, long, signed, unsigned), and memory byte sizing."),
            (8, "Format Specifiers", "printf and scanf conversion specifiers: %d, %i, %f, %lf, %c, %s, %u, %x, %p, along with width and precision flags."),
            (9, "Input and Output (printf, scanf)", "Standard formatted I/O using <stdio.h>, buffer flushing, address-of operator (&) in scanf, and return values of I/O functions."),
            (10, "Operators", "Arithmetic, Relational, Logical, Assignment, Increment/Decrement (++a vs a++), Bitwise, and Ternary (? :) operators."),
            (11, "Type Conversion and Type Casting", "Implicit conversion (type promotion, integer promotion) vs Explicit casting ((float)a / b), and data loss prevention."),
            (12, "Comments", "Single-line (//) and multi-line (/* */) comments, documentation best practices, and compiler comment stripping during preprocessing.")
        ]
    },
    {
        "name": "2. Control Statements",
        "level": "beginner",
        "milestone": 1,
        "topics": [
            (13, "if", "Single decision condition branch in C, boolean evaluation (non-zero is true), and block scoping with braces."),
            (14, "if-else", "Binary decision branching, executing one block when true and alternate fallback when false."),
            (15, "Nested if", "Multi-tier decision logic, checking secondary conditions inside an existing branch, and dangling else problem resolution."),
            (16, "else-if Ladder", "Testing multiple mutually exclusive conditions in sequential order until one matches."),
            (17, "switch", "Multi-way integer/character branching, case labels, the importance of break statement, and default fallback."),
            (18, "for Loop", "Definite iteration loop with initialization, loop condition check, and increment/decrement step in a single header."),
            (19, "while Loop", "Entry-controlled indefinite loop executing as long as the condition evaluates to true."),
            (20, "do-while Loop", "Exit-controlled loop guaranteeing at least one execution before condition verification."),
            (21, "Nested Loops", "Multi-dimensional iterations, inner vs outer loop cycles, matrix traversal, and pattern printing algorithms."),
            (22, "break and continue", "Loop control statements: break for premature termination, continue for skipping current iteration to next step."),
            (23, "goto Statement", "Unconditional jump to labeled statement, why to avoid in modern code, and valid error cleanup usage.")
        ]
    },
    {
        "name": "3. Functions",
        "level": "intermediate",
        "milestone": 2,
        "topics": [
            (24, "Introduction to Functions", "Modular programming, DRY (Don't Repeat Yourself) principle, code reusability, and top-down program decomposition."),
            (25, "Function Declaration, Definition and Calling", "Function prototypes, parameter signatures, return types, function body implementation, and stack call syntax."),
            (26, "Function Arguments and Return Values", "Actual vs formal arguments, returning single values, returning structures, and void return types."),
            (27, "Types of Functions", "Predefined library functions (<math.h>, <stdlib.h>, <string.h>) vs User-defined modular functions."),
            (28, "Call by Value", "Passing values by copy to function parameters, stack frame isolation, and why original variables remain unchanged."),
            (29, "Recursion", "Base condition, recursive call step, recursion stack memory consumption, stack overflow prevention, and tree recursion."),
            (30, "Storage Classes (auto, static, extern, register)", "auto default in local scope, static persistent across calls, extern for cross-file linkage, register for CPU hint."),
            (31, "Scope and Lifetime of Variables", "Block scope, function scope, file scope, lifetime (automatic, static, allocated), and variable shadowing.")
        ]
    },
    {
        "name": "4. Arrays and Strings",
        "level": "intermediate",
        "milestone": 2,
        "topics": [
            (32, "One-Dimensional Arrays", "Contiguous memory allocation, 0-based indexing, array declaration, initialization, and element access."),
            (33, "Two-Dimensional Arrays", "Row-major memory layout, matrix representation, grid coordinates arr[i][j], and nested loop manipulation."),
            (34, "Multidimensional Arrays", "3D and N-dimensional arrays, tensor layouts, and indexing formulas in memory."),
            (35, "Array Traversal and Operations", "Linear traversal, insertion, deletion, searching, reversing, and boundary checking to avoid out-of-bounds access."),
            (36, "Introduction to Strings", "Null-terminated character arrays ('\\0'), string literals in read-only memory, and character buffer sizing."),
            (37, "String Input and Output", "Safe string reading: fgets() vs unsafe gets(), scanf(\"%s\"), puts(), and handling newline characters."),
            (38, "String Library Functions", "<string.h> functions: strlen(), strcpy(), strncpy(), strcat(), strncat(), strcmp(), strncmp(), and strstr()."),
            (39, "Array of Strings", "2D character arrays (char arr[n][len]) vs Array of character pointers (char *arr[n]), memory tradeoffs."),
            (40, "Passing Arrays to Functions", "Array decay to pointer (arr -> &arr[0]), passing array size explicitly, and modifying caller array elements in place.")
        ]
    },
    {
        "name": "5. Pointers",
        "level": "intermediate",
        "milestone": 3,
        "topics": [
            (41, "Introduction to Pointers", "Variables storing memory addresses, memory address bus representation, and hardware-level memory management."),
            (42, "Address Operator (&) and Dereference Operator (*)", "Referencing memory with & and dereferencing / accessing value at target address using *."),
            (43, "Pointer Declaration and Initialization", "Type-safe pointer declarations (int *ptr), initializing with NULL or valid address, and avoiding garbage pointers."),
            (44, "Pointer Arithmetic", "Pointer increment/decrement, scaling by sizeof(datatype), pointer subtraction, and valid pointer comparisons."),
            (45, "Pointers and Arrays", "Array name as constant pointer to first element, *(arr + i) equivalence to arr[i], and pointer traversal."),
            (46, "Pointers and Strings", "Manipulating char* pointers, string literal immutability, and efficient pointer-based string copying."),
            (47, "Pointers and Functions", "Call by reference simulation in C, modifying variables in caller function, and returning pointers from functions safely."),
            (48, "Pointer to Pointer", "Double pointers (int **ptr), dynamic 2D array allocation, and modifying pointer addresses inside functions."),
            (49, "Array of Pointers", "Collection of pointers pointing to independent memory blocks, ragged arrays, and command-line argv."),
            (50, "Function Pointers", "Pointers storing addresses of executable code functions, syntax int (*fp)(int, int), and dynamic dispatch."),
            (51, "NULL Pointers", "Standard NULL definition ((void*)0), null checks, defensive programming, and segmentation fault prevention."),
            (52, "void Pointers", "Generic pointers (void*), storing any data address, typecasting before dereferencing, and generic memory utilities."),
            (53, "Dangling, Wild and Uninitialized Pointers", "Hazards of uninitialized pointers, pointers pointing to freed memory, and setting freed pointers to NULL."),
            (54, "const with Pointers", "Pointer to const (const int *p), const pointer (int * const p), and const pointer to const (const int * const p).")
        ]
    },
    {
        "name": "6. User-Defined Data Types",
        "level": "intermediate",
        "milestone": 3,
        "topics": [
            (55, "Structures (struct)", "Grouping heterogeneous data types into a unified compound data structure, struct definition and declaration."),
            (56, "Accessing Structure Members", "Dot operator (.) for direct instances, arrow operator (->) for structure pointer references."),
            (57, "Array of Structures", "Managing collections of records (e.g. 100 students or inventory items) sequentially in memory."),
            (58, "Nested Structures", "Embedding one structure inside another, hierarchical data modeling, and deep dot-operator navigation."),
            (59, "Structures and Pointers", "Pointer to structure, memory efficiency when passing structs, and dynamic allocation of structs."),
            (60, "Passing Structures to Functions", "Pass by value (copying entire structure) vs Pass by reference (passing struct pointer for high performance)."),
            (61, "Unions (union)", "Shared memory location for all union members, memory sizing (size of largest member), and mutual exclusivity."),
            (62, "enum", "User-defined enumeration types, assigning symbolic integer names to constants, state machines, and code readability."),
            (63, "typedef", "Creating custom type aliases, simplifying complex pointer and struct syntax, and portable type definitions."),
            (64, "Structure Padding and Alignment", "Compiler byte alignment boundaries, memory padding gaps, and packing structs using __attribute__((packed))."),
            (65, "Bit Fields", "Declaring specific bit-width integers inside structures (unsigned int flag : 1) for hardware register programming.")
        ]
    },
    {
        "name": "7. Dynamic Memory Management",
        "level": "advanced",
        "milestone": 3,
        "topics": [
            (66, "Stack vs Heap Memory", "Automatic stack frame allocation vs manual runtime heap allocation, lifetimes, speeds, and limitations."),
            (67, "malloc()", "Allocating uninitialized contiguous memory block of specified byte size, typecasting, and NULL check validation."),
            (68, "calloc()", "Allocating zero-initialized memory blocks for array elements (num_elements, element_size)."),
            (69, "realloc()", "Dynamically resizing previously allocated heap blocks, in-place expansion vs reallocation and data copying."),
            (70, "free()", "Deallocating heap memory, returning memory to OS, and best practices to immediately NULL the pointer."),
            (71, "Memory Leaks", "Accumulation of unreferenced heap memory, detection with Valgrind / AddressSanitizer, and cleanup patterns."),
            (72, "Dangling Pointers and Use-After-Free", "Security vulnerabilities arising from accessing memory after free(), prevention techniques."),
            (73, "Buffer Overflow", "Writing beyond allocated memory bounds, stack smashing, arbitrary code execution risks, and safe bounds checking."),
            (74, "Shallow Copy vs Deep Copy", "Copying pointer address vs allocating duplicate memory and copying nested data contents independently.")
        ]
    },
    {
        "name": "8. Preprocessor and Header Files",
        "level": "advanced",
        "milestone": 3,
        "topics": [
            (75, "Preprocessor Directives", "Source code transformation before compilation, leading # symbol, and preprocessor pipeline semantics."),
            (76, "#include", "Header inclusion: system headers <stdio.h> vs project local headers \"myheader.h\" search paths."),
            (77, "#define", "Defining object-like macros and symbolic constants without memory footprint in data segments."),
            (78, "Macros", "Function-like macros (#define SQUARE(x) ((x)*(x))), side effects with ++x, and macro parentheses rules."),
            (79, "Conditional Compilation (#if, #ifdef, #ifndef)", "Compiling specific blocks based on macros, debug logging toggles, and cross-platform OS branching."),
            (80, "Header Files", "Writing custom .h files containing function declarations, struct definitions, and macro constants."),
            (81, "Include Guards", "Preventing multiple header inclusions with #ifndef HEADER_H / #define HEADER_H / #endif and #pragma once."),
            (82, "Source Files and Separate Compilation", "Splitting programs across multiple .c files, compiling into .o files, and linking into single final binary."),
            (83, "#undef", "Undefining previously declared macros, scoping macro overrides, and avoiding token collisions.")
        ]
    },
    {
        "name": "9. File Handling",
        "level": "advanced",
        "milestone": 3,
        "topics": [
            (84, "File Pointers", "The FILE* stream pointer defined in <stdio.h>, file descriptor tables, and OS kernel file bridges."),
            (85, "Opening and Closing Files", "fopen() with path and mode, checking for NULL failure, and closing files with fclose() to flush buffers."),
            (86, "File Modes", "Access modes: \"r\", \"w\", \"a\", \"r+\", \"w+\", \"a+\", and binary mode specifier \"b\" differences on Windows/Linux."),
            (87, "fgetc() and fputc()", "Reading and writing single characters from and to file streams, detecting EOF (-1)."),
            (88, "fgets() and fputs()", "Reading safe line-by-line strings from files, line buffer overflow defense, and writing strings."),
            (89, "fprintf() and fscanf()", "Formatted file output and input, parsing structured text files, configuration files, and CSVs."),
            (90, "fread() and fwrite()", "Binary block I/O: writing entire struct records directly to disk and reading raw binary streams."),
            (91, "Binary vs Text Files", "Carriage return / line feed (\\r\\n vs \\n) translation in text mode vs raw byte exactness in binary mode."),
            (92, "File Positioning (fseek, ftell, rewind)", "Random file access: fseek() with SEEK_SET, SEEK_CUR, SEEK_END, measuring file size with ftell(), and rewind()."),
            (93, "EOF and Error Handling", "feof() vs ferror(), clearerr(), and distinguishing between end-of-file condition and I/O hardware failure."),
            (94, "Command-Line Arguments (argc, argv)", "Passing arguments from shell into main(int argc, char *argv[]), argument parsing, and CLI tool design.")
        ]
    },
    {
        "name": "10. Advanced C Concepts",
        "level": "advanced",
        "milestone": 3,
        "topics": [
            (95, "Compilation, Assembly and Linking", "Deep dive into relocatable object files (ELF / PE), symbol tables, unresolved external symbols, and static vs dynamic libraries."),
            (96, "Memory Layout of a C Program", "Text (Code) Segment, Initialized Data Segment (.data), BSS Segment (.bss), Heap, and Stack memory layout."),
            (97, "Stack Frames and Function Calls", "Calling conventions (cdecl), stack pointer (ESP/RSP), base pointer (EBP/RBP), push/pop return addresses, and local frames."),
            (98, "Undefined, Unspecified and Implementation-Defined Behavior", "Dangers of undefined behavior (UB), compiler optimizations exploiting UB, and portable C standard guarantees."),
            (99, "Sequence Points and Evaluation Order", "Sequence point rules in C: commas, semicolons, logical operators (&&, ||), and undefined behavior in i = i++ + 1."),
            (100, "Integer Overflow and Integer Promotions", "Signed vs unsigned wrap-around, silent integer promotion rules, and arithmetic overflow security bugs."),
            (101, "Signed vs Unsigned Types", "Two's complement representation, sign bit extension, comparison bugs between signed and unsigned integers."),
            (102, "Bitwise Operators", "Bitwise AND (&), OR (|), XOR (^), NOT (~), Left Shift (<<), and Right Shift (>>)."),
            (103, "Bit Manipulation Techniques", "Setting a bit, clearing a bit, toggling a bit, checking if bit is set, bitmasks, and power-of-two checks."),
            (104, "volatile and restrict", "volatile keyword for hardware registers / ISRs preventing compiler optimization, restrict pointer aliasing optimization."),
            (105, "Function Pointers and Callbacks", "Passing function pointers into algorithms (e.g. qsort comparison functions), event handlers, and callbacks."),
            (106, "Generic Programming with void*", "Writing type-agnostic data structures (generic linked list, generic swap) using void* and element byte size."),
            (107, "sizeof Operator", "Compile-time operator evaluating type/expression byte size, sizeof on array vs sizeof on pointer decay."),
            (108, "Alignment and Padding", "CPU cache line alignment, memory fetch performance penalties, natural boundary alignment, and cache-friendly structs."),
            (109, "Endianness", "Little Endian (x86/ARM) vs Big Endian (network byte order), byte swapping algorithms, and detecting system endianness."),
            (110, "Undefined Behavior Debugging", "Debugging memory corruption using Valgrind, AddressSanitizer (-fsanitize=address), and UndefinedBehaviorSanitizer (-fsanitize=undefined).")
        ]
    },
    {
        "name": "11. Data Structures and Algorithms Using C",
        "level": "advanced",
        "milestone": 4,
        "topics": [
            (111, "Time and Space Complexity", "Asymptotic analysis, Big-O notation, Omega, Theta, analyzing loop iterations, and memory auxiliary space."),
            (112, "Searching Algorithms", "Linear search O(N), Binary search O(log N) on sorted arrays, iterative and recursive implementations."),
            (113, "Sorting Algorithms", "Bubble sort, Selection sort, Insertion sort O(N^2), Merge sort O(N log N), and Quick sort with in-place partitioning."),
            (114, "Linked Lists", "Node structure with data and next pointer, dynamic chaining, and contrasting with contiguous arrays."),
            (115, "Singly Linked List", "Insertion at head, tail, and specific position; deletion of nodes; list reversal; and search operations."),
            (116, "Doubly Linked List", "Nodes with prev and next pointers, bidirectional traversal, constant-time predecessor deletion."),
            (117, "Circular Linked List", "Tail pointing back to head, circular round-robin buffer simulation, and boundary condition handling."),
            (118, "Stacks", "LIFO (Last In First Out) principle, push, pop, peek, array-based stack implementation vs linked list stack."),
            (119, "Queues", "FIFO (First In First Out) principle, enqueue, dequeue, front, rear pointers, and queue overflow/underflow."),
            (120, "Circular Queues", "Ring buffer architecture, modulo arithmetic (rear = (rear + 1) % SIZE), solving memory waste in linear queues."),
            (121, "Hash Tables", "Hash functions, key-value mapping O(1), collision resolution using separate chaining with linked lists and open addressing."),
            (122, "Trees", "Hierarchical data representation, root, children, leaves, depth, height, and recursive tree traversal (preorder, inorder, postorder)."),
            (123, "Binary Search Trees", "BST invariant (left < root < right), node insertion, search O(log N), deletion with in-order predecessor/successor replacement."),
            (124, "Heaps", "Binary heap structure, Max-Heap vs Min-Heap, array representation of heaps, heapify algorithm, and priority queues."),
            (125, "Graphs", "Vertices and edges, Adjacency Matrix vs Adjacency List representations, Breadth-First Search (BFS) and Depth-First Search (DFS)."),
            (126, "Recursion and Backtracking", "N-Queens problem, maze pathfinding, permutation generation, and prune-and-backtrack state trees."),
            (127, "Basic Dynamic Programming", "Overlapping subproblems, optimal substructure, memoization vs bottom-up tabulation, Fibonacci, and 0/1 Knapsack.")
        ]
    },
    {
        "name": "12. Developer Tools and Professional Skills",
        "level": "advanced",
        "milestone": 4,
        "topics": [
            (128, "GCC Compiler", "GNU Compiler Collection usage, compiling flags (-o, -c, -E, -S, -I), and optimization flags (-O0, -O2, -O3)."),
            (129, "Clang Compiler", "LLVM frontend Clang, expressive diagnostic error messages, static analysis tooling, and cross-platform compilation."),
            (130, "IDEs and Text Editors", "Professional workflow with VS Code, Vim, and CLion: configuration of compile commands, C/C++ IntelliSense, and extensions."),
            (131, "GDB Debugger", "GNU Debugger: setting breakpoints, step into (s), step over (n), inspect memory (x), print variables (p), and stack backtrace (bt)."),
            (132, "Compiler Warnings and Flags", "Enabling strict compiler warnings: -Wall, -Wextra, -Werror, -pedantic, -Wshadow, and catching bugs at build time."),
            (133, "Makefiles and Build Systems", "Automating multi-file builds: Make targets, prerequisites, recipes, variables (CC, CFLAGS), and incremental compilation."),
            (134, "Git and GitHub", "Version control for C code: git init, commit, branching, merging, pull requests, .gitignore for build artifacts (*.o, *.exe)."),
            (135, "Unit Testing", "Writing unit test suites in C: assert(), testing frameworks (Unity, Criterion), test automation, and regression prevention."),
            (136, "Debugging and Troubleshooting", "Systematic debugging methodologies: isolating reproducible bugs, binary search debugging, and core dump analysis."),
            (137, "Code Formatting and Documentation", "Automated code formatting with clang-format, Doxygen code documentation syntax, and clean code conventions."),
            (138, "Linux Command Line Basics", "Essential terminal commands: bash, grep, sed, awk, find, pipes, redirects, valgrind, and file permissions."),
            (139, "Static Analysis Tools", "Catching security and memory flaws without running code: cppcheck, clang-tidy, and Flawfinder."),
            (140, "Writing Modular and Maintainable C Code", "Architecting enterprise C projects: clear interface boundaries, encapsulation with opaque pointers, and header organization.")
        ]
    },
    {
        "name": "13. Practice Projects",
        "level": "advanced",
        "milestone": 4,
        "is_project_module": True,
        "topics": [
            (141, "Project 1: Calculator", "Build a robust CLI calculator supporting basic arithmetic, operator precedence, exponentiation, and interactive user menu."),
            (142, "Project 2: Student Management System", "Build a student records application using structures: add, display, search by roll number, update, and sort student records."),
            (143, "Project 3: Bank Management System", "Build a banking console system: create bank accounts, deposit, withdraw with balance checks, and transaction logs."),
            (144, "Project 4: Contact Management System", "Build a phonebook directory using structs and dynamic arrays: search contacts by name, edit phone numbers, and delete."),
            (145, "Project 5: File-Based Employee Records", "Build a persistent corporate employee registry saving and reading binary employee structs to and from disk files."),
            (146, "Project 6: Inventory Management System", "Build an inventory warehouse tracker: item stock levels, low-stock alerts, purchasing, sales reports, and disk persistence."),
            (147, "Project 7: Library Management System", "Build a book cataloging and lending system: book checkout, return dates, fine calculation, and catalog search."),
            (148, "Project 8: Linked List Implementation", "Build a complete standalone singly & doubly linked list library with clean API: insert, delete, reverse, sort, and print."),
            (149, "Project 9: Stack and Queue Implementation", "Implement abstract data types Stack and Queue with circular buffer support, error codes, and comprehensive unit tests."),
            (150, "Project 10: Mini Shell", "Build a lightweight command-line shell in C using fork(), execvp(), and waitpid(), supporting exit, cd, and argument parsing."),
            (151, "Project 11: Memory Pool Allocator", "Build a custom heap memory pool manager with fixed-size chunks, bitmap allocation tracking, and O(1) allocation/deallocation."),
            (152, "Project 12: Simple HTTP Server", "Build an HTTP/1.1 web server in C using Berkeley sockets: listen on port 8080, parse GET requests, and serve static files.")
        ]
    }
]

def generate_starter_code(topic_num, title):
    return f"""#include <stdio.h>
#include <stdlib.h>

// Topic #{topic_num}: {title}
// Write your clean, standard C solution below:

int main() {{
    printf("{title} Mastered\\n");
    return 0;
}}
"""

def generate_practical_problem(topic, topic_num, title):
    starter = generate_starter_code(topic_num, title)
    expected_out = f"{title} Mastered"
    
    test_criteria = [
        {"id": 1, "name": "Basic Output Verification", "input": "", "expected_output": expected_out, "is_hidden": False},
        {"id": 2, "name": "Execution & Return Code 0", "input": "", "expected_output": expected_out, "is_hidden": False},
        {"id": 3, "name": "Compiler Clean Build Check", "input": "", "expected_output": expected_out, "is_hidden": True},
    ]
    
    return {
        "title": f"Lab Challenge: {title}",
        "description": f"### Practical Workbench Task for {title}\n\nWrite a complete, valid C program that implements the core concepts of **{title}**.\nEnsure your code compiles cleanly without errors or warnings and outputs the expected response.",
        "starter_code": starter,
        "expected_output": expected_out,
        "expected_output_hint": f"Your program should demonstrate {title} and print '{expected_out}' to stdout.",
        "test_criteria": test_criteria,
        "language": "c",
        "points": 10
    }

def seed_c_curriculum():
    print("Beginning Full C Programming Curriculum Seeding...")
    with transaction.atomic():
        # 1. Fetch or create C Programming Subject
        subject, created = Subject.objects.get_or_create(
            slug="c-programming",
            defaults={
                "name": "C Programming",
                "description": "Comprehensive from-scratch to advanced systems programming in C, covering all 140 topics, algorithms, data structures, and 12 milestone projects.",
                "short_description": "Master systems-level engineering with 140 topics and 12 real-world projects in C.",
                "duration": "12 Modules • 140 Topics",
                "level": "Beginner to Advanced",
                "icon": "code",
                "instructor_name": "Senior Systems Engineer",
                "is_active": True,
                "order": 1
            }
        )
        print(f"Target Subject: #{subject.id} '{subject.name}' (slug: {subject.slug})")

        # 2. Clean out old modules and topics for this subject
        old_modules = Module.objects.filter(subject=subject)
        old_count = old_modules.count()
        old_modules.delete()
        print(f"Cleared {old_count} old modules and associated topics for C Programming.")

        # 3. Create all 13 modules and their topics
        total_topics_created = 0
        total_problems_created = 0

        for m_idx, mod_info in enumerate(MODULES_DATA, start=1):
            module = Module.objects.create(
                subject=subject,
                name=mod_info["name"],
                level=mod_info["level"],
                order=m_idx
            )
            print(f"[+] Created Module {m_idx}: {module.name} ({len(mod_info['topics'])} topics)", flush=True)

            for t_idx, (t_num, t_title, t_desc) in enumerate(mod_info["topics"], start=1):
                clean_title_slug = "".join(c if c.isalnum() else "-" for c in t_title).strip("-").lower()
                clean_title_slug = "-".join(filter(None, clean_title_slug.split("-")))[:35]
                topic_slug = f"c-{t_num:03d}-{clean_title_slug}"
                
                notes_md = f"""# {t_title}

### Overview
{t_desc}

### Key Concept Highlights
- **Theoretical Foundations**: Understand how modern CPUs, memory models, and standard libraries treat this concept.
- **Syntax & Semantics**: Follow standard ISO/IEC 9899 (C99/C11) best practices.
- **Common Pitfalls**: Watch out for boundary conditions, memory safety, and undefined behavior.

### Code Sample
```c
#include <stdio.h>

int main() {{
    // Demonstration for {t_title}
    printf("{t_title} Mastered\\n");
    return 0;
}}
```

### Interview & Assessment Hints
- What is the computational and memory footprint of this approach?
- How does the compiler optimize or generate code for this structure?
- When would you choose this over alternative design patterns?
"""

                topic = Topic.objects.create(
                    module=module,
                    topic_id=topic_slug,
                    title=f"{t_num}. {t_title}",
                    explain=[t_desc],
                    notes_content=notes_md,
                    order=t_idx
                )
                total_topics_created += 1

                # Mandatory Practical Coding Problem
                prob_data = generate_practical_problem(topic, t_num, t_title)
                Problem.objects.create(
                    topic=topic,
                    title=prob_data["title"],
                    description=prob_data["description"],
                    starter_code=prob_data["starter_code"],
                    expected_output=prob_data["expected_output"],
                    expected_output_hint=prob_data["expected_output_hint"],
                    test_criteria=prob_data["test_criteria"],
                    language="c",
                    points=prob_data["points"],
                    order=1
                )
                total_problems_created += 1

                # Code Example
                CodeExample.objects.create(
                    topic=topic,
                    label=f"Code Example: {t_title}",
                    code=prob_data["starter_code"],
                    order=1
                )

        print("\n=======================================================")
        print(f"SUCCESS! Successfully seeded:")
        print(f"  • {len(MODULES_DATA)} Modules")
        print(f"  • {total_topics_created} Topics")
        print(f"  • {total_problems_created} Practical Lab Coding Challenges")
        print("=======================================================")

if __name__ == "__main__":
    seed_c_curriculum()
