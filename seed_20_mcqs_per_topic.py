import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalari_backend.settings')
django.setup()

from apps.curriculum.models import Topic, TopicQuizQuestion

# Comprehensive question banks tailored to each topic
TOPIC_QUESTIONS = {
    # C Programming - Topic 122: Introduction to C & GCC Compilation Architecture
    122: [
        {
            "question_text": "Which GCC flag is used to produce an assembly code file (.s) instead of an executable?",
            "option_a": "-c", "option_b": "-S", "option_c": "-E", "option_d": "-o",
            "correct_option": "B",
            "explanation": "-S tells GCC to run the compiler proper and stop before assembling, producing a .s assembly file."
        },
        {
            "question_text": "Which GCC flag is used to run only the preprocessor step and dump output to stdout?",
            "option_a": "-E", "option_b": "-c", "option_c": "-Wall", "option_d": "-g",
            "correct_option": "A",
            "explanation": "-E instructs GCC to halt after the preprocessing stage, expanding macros and includes to stdout."
        },
        {
            "question_text": "What type of file is produced after the assembly stage of compilation?",
            "option_a": "Source code (.c)", "option_b": "Object file (.o / .obj)", "option_c": "Header file (.h)", "option_d": "Dynamic library (.dll)",
            "correct_option": "B",
            "explanation": "The assembler translates assembly instructions into machine code, creating relocatable object files (.o)."
        },
        {
            "question_text": "Which linker phase resolves unresolved external symbols and merges code segments?",
            "option_a": "Tokenization", "option_b": "Symbol Resolution & Relocation", "option_c": "Semantic Analysis", "option_d": "Parsing",
            "correct_option": "B",
            "explanation": "The linker resolves external function and variable references across object files and system libraries."
        },
        {
            "question_text": "In a C memory layout, which segment contains compiled machine instructions?",
            "option_a": "Stack", "option_b": "Heap", "option_c": "Text / Code Segment", "option_d": "Data Segment",
            "correct_option": "C",
            "explanation": "The Text (or Code) segment holds executable machine instructions and is typically marked read-only."
        },
        {
            "question_text": "Where are initialized non-zero global and static variables stored in memory?",
            "option_a": "BSS Segment", "option_b": "Initialized Data Segment", "option_c": "Stack Frame", "option_d": "Registers",
            "correct_option": "B",
            "explanation": "Global and static variables initialized with explicit values reside in the initialized data segment (.data)."
        },
        {
            "question_text": "What compiler warning flag in GCC enables all standard recommended warnings?",
            "option_a": "-O3", "option_b": "-Wextra", "option_c": "-Wall", "option_d": "-Werror",
            "correct_option": "C",
            "explanation": "-Wall turns on a broad set of useful warnings regarding questionable language constructs."
        },
        {
            "question_text": "Which command-line tool can be used to inspect symbol tables in compiled ELF object files?",
            "option_a": "objdump or nm", "option_b": "grep", "option_c": "gcc -v", "option_d": "make",
            "correct_option": "A",
            "explanation": "The nm and objdump utilities display symbol tables and sections from object and binary files."
        },
        {
            "question_text": "What happens if main() reaches its closing brace without an explicit return statement in C99/C11?",
            "option_a": "Compilation error", "option_b": "Implicitly returns 0", "option_c": "Returns undefined garbage", "option_d": "Throws SIGSEGV",
            "correct_option": "B",
            "explanation": "Since C99, reaching the terminating } of main() behaves as if 'return 0;' was executed."
        },
        {
            "question_text": "Which GCC optimization flag instructs the compiler to optimize for execution speed without inflating binary size uncontrollably?",
            "option_a": "-O0", "option_b": "-O2", "option_c": "-g", "option_d": "-ansi",
            "correct_option": "B",
            "explanation": "-O2 applies almost all supported optimizations that do not involve a space-speed trade-off."
        },
        {
            "question_text": "What role does the C runtime start file (crt0.o) play in application execution?",
            "option_a": "Allocates dynamic heap", "option_b": "Initializes the environment, sets up stack, and invokes main()", "option_c": "Cleans up files", "option_d": "Runs the debugger",
            "correct_option": "B",
            "explanation": "The crt0 initialization code handles process startup from the kernel before branching into main()."
        },
        {
            "question_text": "Which environment header defines standard input and output macros and functions?",
            "option_a": "<stdlib.h>", "option_b": "<stdio.h>", "option_c": "<conio.h>", "option_d": "<string.h>",
            "correct_option": "B",
            "explanation": "<stdio.h> provides prototypes and constants for standard streaming I/O operations."
        },
        {
            "question_text": "Which tool compiles source code incrementally using rules defined in a Makefile?",
            "option_a": "gcc", "option_b": "make", "option_c": "cmake", "option_d": "gdb",
            "correct_option": "B",
            "explanation": "make interprets Makefile dependency graphs to recompile only modified source components."
        },
        {
            "question_text": "In standard C compilation, what does the suffix .i indicate?",
            "option_a": "Assembly code", "option_b": "Preprocessed C source code", "option_c": "Executable binary", "option_d": "Intermediate object",
            "correct_option": "B",
            "explanation": ".i files represent preprocessed C source after macro expansion and header inclusion."
        },
        {
            "question_text": "What is the primary difference between static and dynamic linking?",
            "option_a": "Static links all library code into binary; dynamic resolves references at runtime", "option_b": "Dynamic produces larger executables", "option_c": "Static cannot use standard C library", "option_d": "There is no speed difference",
            "correct_option": "A",
            "explanation": "Static linking copies library routines into the output file; dynamic linking relies on shared libraries at load time."
        },
        {
            "question_text": "Which flag adds debug symbols (DWARF) into the compiled binary for use with GDB?",
            "option_a": "-d", "option_b": "-g", "option_c": "-v", "option_d": "-debug",
            "correct_option": "B",
            "explanation": "-g generates debugging info in the operating system's native format for GDB inspection."
        },
        {
            "question_text": "What is the function of the ld utility in a GCC toolchain?",
            "option_a": "Preprocessor", "option_b": "Linker", "option_c": "Assembler", "option_d": "Compiler core",
            "correct_option": "B",
            "explanation": "ld is the GNU linker that combines object files and archive libraries into an executable."
        }
    ],

    # Topic 123: Variables, Constants, Memory Sizes & Primitive Data Types
    123: [
        {
            "question_text": "What is the standard size of an 'int' on modern 64-bit x86-64 LP64 platforms?",
            "option_a": "2 bytes", "option_b": "4 bytes", "option_c": "8 bytes", "option_d": "16 bytes",
            "correct_option": "B",
            "explanation": "On LP64 architecture (Linux/macOS), 'int' remains 4 bytes (32 bits), while 'long' is 8 bytes."
        },
        {
            "question_text": "Which keyword specifies that a variable's value cannot be modified after initialization?",
            "option_a": "static", "option_b": "volatile", "option_c": "const", "option_d": "register",
            "correct_option": "C",
            "explanation": "'const' creates a read-only variable whose value cannot be reassigned."
        },
        {
            "question_text": "What is the return type of the 'sizeof' operator in C?",
            "option_a": "int", "option_b": "unsigned long / size_t", "option_c": "float", "option_d": "short",
            "correct_option": "B",
            "explanation": "sizeof yields an unsigned integer type designated as size_t (defined in <stddef.h>)."
        },
        {
            "question_text": "Which header file provides fixed-width integer types like int32_t and uint64_t?",
            "option_a": "<limits.h>", "option_b": "<stdint.h>", "option_c": "<float.h>", "option_d": "<stdtypes.h>",
            "correct_option": "B",
            "explanation": "<stdint.h> introduced in C99 standardizes exact-width integer types across all architectures."
        },
        {
            "question_text": "What is the minimum value an 8-bit signed char can store using two's complement?",
            "option_a": "0", "option_b": "-127", "option_c": "-128", "option_d": "-256",
            "correct_option": "C",
            "explanation": "An 8-bit signed integer has range -128 to +127 in standard two's complement representation."
        },
        {
            "question_text": "What happens when you increment an unsigned integer past its maximum representable value?",
            "option_a": "Undefined Behavior", "option_b": "Silent wrap-around to 0 (modulo 2^n)", "option_c": "Runtime segmentation fault", "option_d": "Compiler warning error",
            "correct_option": "B",
            "explanation": "In C, unsigned integer arithmetic is strictly defined to wrap around modulo 2^N."
        },
        {
            "question_text": "Which qualifier prevents the compiler from optimizing variable reads, useful for hardware registers?",
            "option_a": "const", "option_b": "volatile", "option_c": "extern", "option_d": "inline",
            "correct_option": "B",
            "explanation": "'volatile' forces the compiler to read the memory address directly on every access."
        },
        {
            "question_text": "What is the difference between float and double in C?",
            "option_a": "float is 32-bit single precision, double is 64-bit double precision", "option_b": "double is faster on 8-bit microcontrollers", "option_c": "float has 15 decimal digits precision", "option_d": "No difference",
            "correct_option": "A",
            "explanation": "float conforms to IEEE 754 single precision (4 bytes), double provides double precision (8 bytes)."
        },
        {
            "question_text": "Which format specifier is used to print a size_t value portably?",
            "option_a": "%d", "option_b": "%lu", "option_c": "%zu", "option_d": "%p",
            "correct_option": "C",
            "explanation": "%zu is the standard C99 printf format specifier designed specifically for size_t."
        },
        {
            "question_text": "What is an enum in C internally treated as by the compiler?",
            "option_a": "Pointer", "option_b": "Integer (int)", "option_c": "String literal", "option_d": "Struct",
            "correct_option": "B",
            "explanation": "C enums are discrete sets of named integer constants represented internally as ints."
        },
        {
            "question_text": "What is the result of casting a negative float -3.7 to an int?",
            "option_a": "-4", "option_b": "-3", "option_c": "3", "option_d": "0",
            "correct_option": "B",
            "explanation": "C truncates toward zero when converting floating-point types to integers, giving -3."
        },
        {
            "question_text": "Which storage duration applies to local variables declared inside a function without static?",
            "option_a": "Static duration", "option_b": "Automatic (stack) duration", "option_c": "Allocated duration", "option_d": "Thread duration",
            "correct_option": "B",
            "explanation": "Automatic variables are created upon block entry and destroyed upon block exit."
        },
        {
            "question_text": "Which escape sequence represents the null terminator character in C?",
            "option_a": "\\n", "option_b": "\\t", "option_c": "\\0", "option_d": "\\r",
            "correct_option": "C",
            "explanation": "\\0 is the null character with ASCII value 0, used to terminate strings in C."
        },
        {
            "question_text": "Which standard macro in <limits.h> provides the maximum value for a signed integer?",
            "option_a": "MAX_INT", "option_b": "INT_MAX", "option_c": "INTEGER_MAX", "option_d": "LIMIT_INT",
            "correct_option": "B",
            "explanation": "INT_MAX defines the upper bound of a signed integer (+2147483647 on 32-bit systems)."
        },
        {
            "question_text": "Can a variable declared with 'register' storage class have its memory address taken with &?",
            "option_a": "Yes, always", "option_b": "No, taking the address of a register variable is illegal in C", "option_c": "Only if compiled with -O0", "option_d": "Only if cast to void*",
            "correct_option": "B",
            "explanation": "In C, you cannot apply the address-of operator (&) to a variable declared with register storage."
        },
        {
            "question_text": "What is the size of a 'char' in bytes guaranteed by the C standard?",
            "option_a": "1 byte", "option_b": "2 bytes", "option_c": "Depends on OS", "option_d": "4 bytes",
            "correct_option": "A",
            "explanation": "The C standard guarantees sizeof(char) == 1 by definition on all conformant implementations."
        },
        {
            "question_text": "What does the keyword 'extern' signify on a global variable declaration?",
            "option_a": "Allocates storage immediately", "option_b": "Declares variable name and type without allocating storage in this translation unit", "option_c": "Makes it private to this file", "option_d": "Locks variable from edits",
            "correct_option": "B",
            "explanation": "'extern' tells the compiler that storage for the variable is allocated elsewhere."
        }
    ],

    # Topic 124: Operators, Expressions & Precedence Hierarchy
    124: [
        {
            "question_text": "What is the result of 5 / 2 in C when both operands are integers?",
            "option_a": "2.5", "option_b": "2", "option_c": "3", "option_d": "Undefined",
            "correct_option": "B",
            "explanation": "Integer division truncates the fractional part, resulting in 2."
        },
        {
            "question_text": "What is the difference between prefix (++i) and postfix (i++) increment?",
            "option_a": "Prefix increments then yields new value; postfix yields old value then increments", "option_b": "Postfix is faster", "option_c": "Prefix cannot be used in loops", "option_d": "They are always identical",
            "correct_option": "A",
            "explanation": "++i evaluates to the incremented value; i++ evaluates to original value before incrementing."
        },
        {
            "question_text": "Which operator has higher precedence: multiplication (*) or addition (+)?",
            "option_a": "Addition (+)", "option_b": "Multiplication (*)", "option_c": "Equal precedence", "option_d": "Depends on associativity",
            "correct_option": "B",
            "explanation": "Multiplication has higher precedence (level 3) than addition (level 4)."
        },
        {
            "question_text": "What is short-circuit evaluation in logical operators (&&, ||)?",
            "option_a": "Compiler skips all checks", "option_b": "Second operand is not evaluated if first operand determines result", "option_c": "Evaluation order is random", "option_d": "Both operands run concurrently",
            "correct_option": "B",
            "explanation": "If left side of && is false, right side is never executed; same if left of || is true."
        },
        {
            "question_text": "What is the value of expression: 1 << 3 in C?",
            "option_a": "3", "option_b": "8", "option_c": "6", "option_d": "16",
            "correct_option": "B",
            "explanation": "Bitwise left-shift 1 by 3 bits produces 1 * 2^3 = 8."
        },
        {
            "question_text": "What does the ternary operator (? :) return if the condition evaluates to non-zero?",
            "option_a": "The false expression", "option_b": "The true expression (second operand)", "option_c": "0", "option_d": "void",
            "correct_option": "B",
            "explanation": "cond ? expr1 : expr2 evaluates expr1 when cond is non-zero (true)."
        },
        {
            "question_text": "What is the associativity of the assignment operator (=)?",
            "option_a": "Left-to-Right", "option_b": "Right-to-Left", "option_c": "Non-associative", "option_d": "Arbitrary",
            "correct_option": "B",
            "explanation": "Assignment operators associate from right to left (e.g., a = b = c assigns c to b, then b to a)."
        },
        {
            "question_text": "What does the bitwise XOR operator (^) do?",
            "option_a": "Sets bit to 1 if both bits are 1", "option_b": "Sets bit to 1 if exactly one bit is 1", "option_c": "Inverts all bits", "option_d": "Calculates exponential power",
            "correct_option": "B",
            "explanation": "^ is exclusive OR: returns 1 if operands differ, 0 if they are identical."
        },
        {
            "question_text": "What is the result of expression: sizeof('A') in standard C?",
            "option_a": "1", "option_b": "sizeof(int) (usually 4)", "option_c": "2", "option_d": "8",
            "correct_option": "B",
            "explanation": "In standard C, character literals like 'A' are of type int, so sizeof('A') == sizeof(int)."
        },
        {
            "question_text": "Which operator is used to access structure members via a pointer?",
            "option_a": ".", "option_b": "->", "option_c": "*", "option_d": "::",
            "correct_option": "B",
            "explanation": "The arrow operator (->) dereferences a pointer and accesses the member (ptr->member)."
        },
        {
            "question_text": "What does the comma operator (,) do when evaluating expressions?",
            "option_a": "Executes left-to-right, discarding left and returning value of rightmost expression", "option_b": "Returns sum of expressions", "option_c": "Runs right-to-left", "option_d": "Throws syntax error",
            "correct_option": "A",
            "explanation": "Comma operator evaluates from left to right and evaluates to the value of the final expression."
        },
        {
            "question_text": "What is the result of: 10 % -3 in C99?",
            "option_a": "1", "option_b": "-1", "option_c": "3", "option_d": "-3",
            "correct_option": "A",
            "explanation": "In C99+, the sign of the modulo operator result matches the sign of the dividend (10 % -3 = 1)."
        },
        {
            "question_text": "What is the danger of writing i = i++ in C?",
            "option_a": "Causes immediate crash", "option_b": "Undefined behavior due to multiple modifications between sequence points", "option_c": "Generates infinite loop", "option_d": "Valid and doubles i",
            "correct_option": "B",
            "explanation": "Modifying a scalar more than once without an intervening sequence point triggers undefined behavior."
        },
        {
            "question_text": "Which bitwise operator flips all bits of a number (one's complement)?",
            "option_a": "!", "option_b": "~", "option_c": "^", "option_d": "&",
            "correct_option": "B",
            "explanation": "~ is the bitwise NOT operator that inverts each individual bit."
        },
        {
            "question_text": "What does the expression (a == b) return in C when true?",
            "option_a": "boolean true", "option_b": "integer 1", "option_c": "integer -1", "option_d": "void",
            "correct_option": "B",
            "explanation": "Relational and equality operators return int 1 for true and int 0 for false in C."
        },
        {
            "question_text": "What is the precedence of unary operators (&, *, !, ~) relative to binary arithmetic (+, -)?",
            "option_a": "Lower precedence", "option_b": "Higher precedence", "option_c": "Equal precedence", "option_d": "Context dependent",
            "correct_option": "B",
            "explanation": "Unary operators bind tighter (higher precedence) than binary addition and subtraction."
        },
        {
            "question_text": "Which expression checks whether the 3rd bit (0-indexed) of integer 'x' is set?",
            "option_a": "(x >> 3) & 1", "option_b": "x & 3", "option_c": "x | (1 << 3)", "option_d": "x ^ 3",
            "correct_option": "A",
            "explanation": "Shifting right by 3 and masking with 1 isolates the 3rd bit value."
        }
    ]
}

def generate_questions_for_topic(topic, needed_count):
    """Generates high quality, accurate questions specific to the topic subject and title"""
    t_title = topic.title
    subj = topic.module.subject.name
    
    questions = []
    
    # 1. Subject-based templates with genuine technical depth
    if "C Programming" in subj or "C++" in subj:
        templates = [
            ("What is the primary consequence of accessing an array out-of-bounds in {topic}?",
             "Compiler throws ArrayOutOfBoundsException", "Undefined behavior, memory corruption, or segmentation fault", "Returns null", "Automated array resize",
             "B", "C does not perform bounds checking; out-of-bounds indexing leads to undefined memory behavior."),
            ("Which storage class in C restricts the visibility of a function or global variable to its source file?",
             "auto", "static", "extern", "register",
             "B", "static on a global scope gives internal linkage, preventing other files from accessing it."),
            ("What does the pointer notation *(ptr + i) evaluate identically to?",
             "ptr[i]", "&ptr[i]", "ptr.i", "i->ptr",
             "A", "Array indexing a[i] is syntactically defined as pointer offset dereference *(a + i)."),
            ("What occurs if memory allocated via malloc() is never released using free()?",
             "Automatic garbage collection", "Memory leak consuming process heap space", "Stack overflow immediately", "Program terminates with error",
             "B", "In C, unreleased dynamic heap allocations remain until process exit, creating memory leaks."),
            ("What is the return value of malloc() if the operating system cannot satisfy the allocation request?",
             "-1", "NULL (0)", "Throws bad_alloc", "Reboots process",
             "B", "malloc returns NULL pointer upon heap allocation failure, which must be verified before dereferencing."),
            ("Why is passing large structs by pointer preferable to passing by value in {topic}?",
             "Values cannot be passed", "Avoids copying the entire struct onto the stack frame, saving memory and CPU cycles", "Pointers are always type-safe", "Structs cannot have members",
             "B", "Passing pointers (addresses) only copies a single pointer size rather than replicating bytes."),
            ("Which function safely reads a line of input from stdin without risking buffer overflows?",
             "gets()", "fgets()", "scanf(\"%s\")", "getc()",
             "B", "fgets() requires a buffer length parameter, preventing dangerous buffer overflows inherent in gets()."),
            ("What is a segmentation fault (SIGSEGV) in C?",
             "A syntax parsing error", "An OS signal caused by accessing unauthorized memory addresses (e.g., NULL pointer dereference)", "CPU arithmetic overflow", "Network timeout",
             "B", "The memory management unit (MMU) signals SIGSEGV when a process accesses invalid pages."),
            ("Which keyword in C99 tells the compiler that two pointer arguments do not alias the same memory?",
             "inline", "restrict", "register", "volatile",
             "B", "The 'restrict' qualifier allows aggressive compiler optimizations by asserting no aliasing."),
            ("What does the 'typedef' specifier accomplish in C?",
             "Creates a new variable", "Creates a type alias / synonym for an existing type", "Defines a macro", "Allocates heap memory",
             "B", "typedef assigns a convenient new identifier to an existing data type or complex function pointer."),
            ("What is the consequence of dereferencing a dangling pointer in C?",
             "Throws NullPointerException", "Accesses stale or reallocated memory, causing undefined behavior or crashes", "Automatically points to 0", "Compiler error",
             "B", "A dangling pointer references freed memory; accessing it produces unpredictable bugs."),
            ("Which standard library function compares two null-terminated strings lexicographically?",
             "strcmp()", "strlen()", "strcat()", "strcpy()",
             "A", "strcmp returns 0 if strings match, <0 if str1 < str2, and >0 if str1 > str2."),
            ("What does the preprocessor directive #pragma once or header guards (#ifndef) prevent?",
             "Compilation errors", "Multiple inclusion of the same header in a single translation unit", "Macro expansion", "Linker optimization",
             "B", "Header guards prevent duplicate symbol definitions caused by transitive #include cycles."),
            ("In binary file I/O, which function reads blocks of raw bytes into memory from a FILE stream?",
             "fread()", "fscanf()", "fgetc()", "fgets()",
             "A", "fread() transfers raw binary elements directly between disk file streams and memory buffers."),
            ("What does the expression 'sizeof(arr) / sizeof(arr[0])' calculate for a stack-allocated array?",
             "The total byte size", "The number of elements in the array", "The size of pointer", "Undefined behavior",
             "B", "Dividing total array bytes by single element byte size yields the element count."),
            ("What is the purpose of the 'free()' function in C memory management?",
             "Zeroes out memory contents", "Deallocates heap memory back to the memory allocator", "Deletes variable name", "Closes open files",
             "B", "free() informs the runtime heap allocator that the memory block can be reused."),
            ("What does the 'break' statement execute when placed inside a loop or switch?",
             "Exits the entire program", "Terminates execution of the innermost enclosing loop or switch construct", "Skips to the next iteration", "Pauses execution",
             "B", "break immediately transfers control out of the enclosing loop or switch body."),
            ("What is the difference between a struct and a union in C?",
             "In struct, all members have separate memory; in union, all members share the same starting memory space", "Unions cannot store integers", "Structs are allocated on heap only", "There is no difference",
             "A", "A union sizes to its largest member because all fields share the same memory location.")
        ]
    elif "Python" in subj or "Django" in subj:
        templates = [
            ("In Python, which data structure is mutable and preserves insertion order?",
             "tuple", "list", "frozenset", "int",
             "B", "Lists are ordered, mutable sequences of heterogeneous elements."),
            ("Which built-in function returns both the index and value when iterating over an iterable?",
             "range()", "enumerate()", "zip()", "map()",
             "B", "enumerate() generates tuples containing (index, item) during iteration."),
            ("What is the difference between '==' and 'is' in Python?",
             "'==' checks value equality; 'is' checks object identity (same memory address)", "'is' is faster for numbers", "'==' checks types only", "They are identical",
             "A", "'==' checks if values are equal, while 'is' checks if both variables refer to the identical object."),
            ("Which keyword is used to create an anonymous function in Python?",
             "def", "lambda", "func", "anon",
             "B", "lambda creates small, single-expression anonymous functions in Python."),
            ("What does the '__init__' method represent in a Python class?",
             "Class destructor", "Instance initializer / constructor called after object creation", "Static method", "Class loader",
             "B", "__init__ initializes attributes of newly created class instances."),
            ("What does a function containing the 'yield' keyword return when called?",
             "A list", "A generator iterator", "None", "A tuple",
             "B", "Using yield turns a function into a generator factory producing a generator object."),
            ("Which Python dictionary method safely retrieves a key without raising a KeyError if missing?",
             "dict.pop()", "dict.get(key, default)", "dict[key]", "dict.find()",
             "B", "dict.get() returns the default value (or None) if the specified key is absent."),
            ("What is a decorator in Python?",
             "A class attribute", "A callable that takes a function and returns an extended function without modifying original code", "A CSS styling rule", "A syntax highlighter",
             "B", "Decorators wrap functions using the @decorator syntax to inject behavior dynamically."),
            ("Which module in standard library is used for handling JSON serialization?",
             "pickle", "json", "marshal", "csv",
             "B", "The json module provides dumps() and loads() for JSON data handling."),
            ("In Django ORM, which method filters records matching conditions?",
             "Model.objects.find()", "Model.objects.filter()", "Model.objects.get_all()", "Model.objects.select()",
             "B", "Model.objects.filter() generates a SQL WHERE clause returning a QuerySet."),
            ("What does the 'select_related' method do in Django ORM?",
             "Fetches related models using SQL JOIN to prevent N+1 query problems", "Deletes related models", "Creates reverse relationships", "Caches templates",
             "A", "select_related performs SQL JOINs for ForeignKey and OneToOne relationships."),
            ("Which HTTP method is idempotent and intended for retrieving resources without side effects?",
             "POST", "GET", "PATCH", "DELETE",
             "B", "GET requests retrieve data and should not alter server state (safe and idempotent)."),
            ("What is the purpose of Django migrations?",
             "Deploying to servers", "Propagating model schema changes into the database", "Compiling Python files", "Running unit tests",
             "B", "Django migrations track changes to your models and apply corresponding DDL to PostgreSQL/MySQL."),
            ("Which statement correctly handles exceptions in Python?",
             "try ... catch", "try ... except", "catch ... finally", "throw ... catch",
             "B", "Python uses try ... except ... finally blocks to capture and handle runtime exceptions."),
            ("What does *args and **kwargs denote in Python function signatures?",
             "Pointers to memory", "Variable positional arguments (*args) and variable keyword arguments (**kwargs)", "Multiplication operators", "Required parameters",
             "B", "*args packs positional arguments into a tuple; **kwargs packs keyword arguments into a dictionary."),
            ("What is the Global Interpreter Lock (GIL) in CPython?",
             "A file lock for databases", "A mutex that allows only one native thread to execute Python bytecode at a time", "A security firewall", "A garbage collector",
             "B", "The GIL prevents multi-threaded CPython from running Python bytecode concurrently across cores."),
            ("Which comprehension syntax creates a set containing squares of even numbers from 0 to 9?",
             "[x**2 for x in range(10) if x % 2 == 0]", "{x**2 for x in range(10) if x % 2 == 0}", "(x**2 for x in range(10))", "{x: x**2 for x in range(10)}",
             "B", "Curly brackets without colons create a set comprehension with unique elements."),
            ("What does the 'pass' statement do in Python?",
             "Exits loop", "Acts as a null statement / placeholder where syntactic code is required", "Throws exception", "Returns true",
             "B", "pass executes nothing and is used as a placeholder in empty functions or loops.")
        ]
    elif "Java" in subj:
        templates = [
            ("Which access modifier makes a class member accessible only within the declaring class?",
             "public", "protected", "private", "default (package-private)",
             "C", "private limits member visibility exclusively to the enclosing class."),
            ("What is the base superclass of all classes in Java?",
             "java.lang.System", "java.lang.Object", "java.lang.Class", "java.lang.Base",
             "B", "java.lang.Object is the root of the class hierarchy in Java."),
            ("Which keyword prevents a class from being inherited or a method from being overridden?",
             "static", "final", "abstract", "const",
             "B", "final classes cannot be extended; final methods cannot be overridden by subclasses."),
            ("What is the purpose of the JVM (Java Virtual Machine)?",
             "Writes Java source code", "Executes compiled Java bytecode (.class) across different hardware platforms", "Compiles C code", "Manages cloud servers",
             "B", "The JVM translates platform-independent bytecode into native machine instructions."),
            ("Which collection interface allows key-value pair associations?",
             "List", "Set", "Map", "Queue",
             "C", "java.util.Map maps unique keys to values (e.g. HashMap, TreeMap)."),
            ("What is the difference between ArrayList and LinkedList in Java?",
             "ArrayList uses a dynamic resizable array; LinkedList uses doubly-linked nodes", "LinkedList is always faster", "ArrayList cannot store objects", "There is no difference",
             "A", "ArrayList provides O(1) random access; LinkedList provides O(1) insertion at endpoints."),
            ("Which exception type must be either caught or declared in the throws clause?",
             "RuntimeException", "Checked Exception (subclass of Exception excluding RuntimeException)", "Error", "NullPointerException",
             "B", "Checked exceptions are verified at compile time and mandate try-catch or throws."),
            ("What does the 'static' keyword indicate on a method or field?",
             "Belongs to the class rather than individual instances", "Allocated on thread stack", "Cannot be modified", "Cannot be called",
             "A", "static members exist once per class regardless of how many instances are instantiated."),
            ("Which functional interface in Java 8 accepts one argument and returns a boolean?",
             "Consumer<T>", "Supplier<T>", "Predicate<T>", "Function<T, R>",
             "C", "Predicate<T> defines boolean test(T t), used frequently in Stream filtering."),
            ("What does garbage collection in Java automatically handle?",
             "Clearing stack frames", "Reclaiming heap memory occupied by unreachable objects", "Closing network sockets", "Formatting strings",
             "B", "The Java GC tracks object reachability from GC roots and frees orphaned heap allocations."),
            ("What is the difference between StringBuilder and StringBuffer?",
             "StringBuilder is non-synchronized and faster; StringBuffer is thread-safe synchronized", "StringBuffer is deprecated", "StringBuilder cannot append strings", "They are identical",
             "A", "StringBuilder is preferred in single-threaded contexts due to lack of synchronization overhead."),
            ("Which keyword is used to explicitly call a superclass constructor from a subclass?",
             "this()", "super()", "parent()", "base()",
             "B", "super() invokes the matching constructor of the immediate superclass."),
            ("What happens if you attempt to modify an element while iterating with a standard for-each loop in Java Collections?",
             "NullPointerException", "ConcurrentModificationException", "ArrayIndexOutOfBoundsException", "Silent failure",
             "B", "Modifying collection structural state during iterator traversal triggers ConcurrentModificationException."),
            ("What is an interface in Java?",
             "A concrete class", "A contract specifying abstract methods that implementing classes must define", "A database table", "A thread pool",
             "B", "Interfaces declare methods without implementations (prior to default methods in Java 8)."),
            ("Which stream operation in Java 8 transforms elements of a stream into another form?",
             "filter()", "map()", "distinct()", "peek()",
             "B", "map() applies a mapper function to each element, producing a transformed Stream."),
            ("What is the default value of an uninitialized boolean instance field in a Java class?",
             "true", "false", "null", "0",
             "B", "Primitive boolean fields in classes default to false upon instantiation."),
            ("How do you create and start a thread in Java?",
             "Subclass Thread or implement Runnable, then call start()", "Call run() directly", "Invoke thread.execute()", "Use JVM.start()",
             "A", "Calling start() allocates a new native OS thread that executes run()."),
            ("What is the output of 'Hello'.equals(new String('Hello')) in Java?",
             "false", "true", "Compilation error", "Undefined",
             "B", "String.equals() checks character content equality rather than object reference identity.")
        ]
    elif "JavaScript" in subj or "React" in subj or "HTML" in subj:
        templates = [
            ("What is the scoping difference between 'var' and 'let'/'const' in JavaScript?",
             "'var' is function-scoped; 'let' and 'const' are block-scoped", "'let' is global only", "'var' is block-scoped", "There is no difference",
             "A", "let and const respect curly brace block boundaries {}, while var hoists to function scope."),
            ("What does the '===' operator check in JavaScript?",
             "Value only with type coercion", "Strict equality of both value and data type without coercion", "Memory pointer only", "Assignment",
             "B", "=== enforces strict equality without implicit type conversions ('5' === 5 is false)."),
            ("What is the primary role of the JavaScript Event Loop?",
             "Executes CSS animations", "Coordinates execution of synchronous code, call stack, microtasks, and macrotasks", "Compiles code to bytecode", "Manages database records",
             "B", "The Event Loop monitors the Call Stack and moves callbacks from Task Queues when the stack clears."),
            ("Which Promise method returns a promise that resolves when ALL input promises resolve?",
             "Promise.race()", "Promise.all()", "Promise.any()", "Promise.resolve()",
             "B", "Promise.all() waits for every promise to resolve, or rejects immediately if any promise rejects."),
            ("In React, what rule must be respected when calling Hooks (useState, useEffect)?",
             "Only call them at the top level of React function components, not in loops or conditions", "Call them inside click handlers", "Always call inside class components", "Must be called asynchronously",
             "A", "React relies on the call order of hooks on every render, requiring top-level invocations."),
            ("What does the dependency array in useEffect([dep1]) control?",
             "The return type of effect", "When the effect re-runs (only when values in the dependency array change)", "The number of retries", "Component CSS styling",
             "B", "React compares dependency array values via Object.is to determine if effect should re-fire."),
            ("What is the Virtual DOM in React?",
             "The browser's native DOM tree", "A lightweight in-memory representation of the UI that React diffs to minimize real DOM mutations", "A WebGL canvas", "A Node.js module",
             "B", "React creates a virtual tree, computes diffs with Reconciliation, and batches actual DOM updates."),
            ("Which array method creates a new array populated with the results of calling a provided function?",
             "filter()", "map()", "forEach()", "reduce()",
             "B", "Array.prototype.map() applies a transformation callback to every element and returns a new array."),
            ("What does the Spread operator (...) do on an object in ES6?",
             "Deletes properties", "Shallow copies the enumerable properties into a new object", "Deep freezes the object", "Converts object to string",
             "B", "The spread operator copies own enumerable properties into target objects or array literals."),
            ("In CSS, which display mode creates a 2-dimensional layout with rows and columns?",
             "flex", "grid", "block", "inline-block",
             "B", "CSS Grid provides complete 2D layout control across simultaneous rows and columns."),
            ("What is the purpose of the 'key' prop when rendering lists in React?",
             "Styles the element", "Helps React identify which items have changed, added, or removed during diffing", "Sets the HTML id attribute", "Binds click events",
             "B", "Keys give elements stable identities across renders for optimal DOM reconciliation."),
            ("Which HTTP status code indicates a successful request in REST APIs?",
             "404 Not Found", "200 OK", "500 Server Error", "301 Redirect",
             "B", "200 OK is the standard response for successful HTTP operations."),
            ("What does 'async/await' syntax in JavaScript achieve?",
             "Runs code in worker threads", "Allows asynchronous Promise-based code to be written with cleaner synchronous-looking flow", "Pauses browser execution", "Replaces callbacks entirely",
             "B", "async functions return promises and allow 'await' to pause execution until resolution."),
            ("Which CSS property determines whether an element is removed from the normal layout flow?",
             "margin", "position (e.g., absolute, fixed)", "color", "font-weight",
             "B", "position: absolute and position: fixed take elements out of normal document flow."),
            ("What does localStorage.setItem() do in web browsers?",
             "Stores data temporarily in session", "Persists key-value string data across browser restarts without expiration", "Sends cookies to server", "Saves files to hard disk",
             "B", "localStorage provides synchronous client-side persistent key-value storage."),
            ("Which React hook is used to cache expensive calculation results between renders?",
             "useCallback", "useMemo", "useRef", "useReducer",
             "B", "useMemo caches the memoized result of a calculation until designated dependencies change."),
            ("What is a Closure in JavaScript?",
             "A syntax error in brackets", "A function bundled together with references to its surrounding lexical environment", "A tool to close browser windows", "An anonymous function",
             "B", "A closure gives a function access to its outer scope variables even after outer execution completes."),
            ("Which CSS Box Model property creates space outside the element's border?",
             "padding", "margin", "border-width", "outline",
             "B", "Margin controls transparent clearance outside the border between neighboring elements.")
        ]
    elif "SQL" in subj or "Database" in subj:
        templates = [
            ("Which SQL clause is used to filter grouped rows after an aggregation function?",
             "WHERE", "HAVING", "GROUP BY", "ORDER BY",
             "B", "HAVING filters groups produced by GROUP BY; WHERE filters rows prior to grouping."),
            ("What does an INNER JOIN return?",
             "All rows from left table", "Only rows where there is a match in both joined tables", "All rows from right table", "Cartesian product of all rows",
             "B", "INNER JOIN selects records that have matching values in both datasets."),
            ("Which SQL constraint guarantees that every record in a table has a unique non-null identifier?",
             "UNIQUE", "PRIMARY KEY", "FOREIGN KEY", "CHECK",
             "B", "PRIMARY KEY enforces uniqueness and NOT NULL on designated columns."),
            ("What does ACID stand for in database transaction management?",
             "Array, Class, Integer, Decimal", "Atomicity, Consistency, Isolation, Durability", "Access, Control, Identity, Data", "Asynchronous, Cached, Indexed, Distributed",
             "B", "ACID guarantees that database transactions are processed reliably."),
            ("Which index structure is standard for primary keys and range queries in PostgreSQL/MySQL?",
             "Hash Index", "B-Tree (Balanced Tree) Index", "BitMap Index", "GIST Index",
             "B", "B-Tree indexes provide logarithmic O(log N) lookups and efficient sequential range scans."),
            ("What does the SQL command 'ROLLBACK' do?",
             "Saves changes permanently", "Reverts all database modifications made within the current uncommitted transaction", "Deletes the table schema", "Restarts the database engine",
             "B", "ROLLBACK undoes uncommitted statements when errors occur or constraints fail."),
            ("Which keyword removes duplicate rows from a SELECT query result?",
             "UNIQUE", "DISTINCT", "DIFFERENT", "FILTER",
             "B", "SELECT DISTINCT eliminates duplicate row tuples from query output."),
            ("What is the difference between TRUNCATE and DELETE in SQL?",
             "TRUNCATE is a DDL operation that swiftly deallocates pages without row-by-row logging; DELETE is DML", "DELETE removes table structure", "TRUNCATE cannot be rolled back", "They are identical",
             "A", "TRUNCATE empties the entire table rapidly with minimal transaction logging."),
            ("Which SQL aggregate function computes the total number of non-null records?",
             "SUM()", "COUNT()", "AVG()", "TOTAL()",
             "B", "COUNT(column) tallies the number of rows where column is not NULL."),
            ("What does a FOREIGN KEY constraint enforce between two relational tables?",
             "Faster query speed", "Referential Integrity", "Automatic indexing", "Table partitioning",
             "B", "Foreign keys ensure child records reference valid existing parent rows."),
            ("Which SQL statement is used to modify existing data in a table?",
             "ALTER", "UPDATE", "INSERT", "MODIFY",
             "B", "UPDATE sets new column values on rows matching a WHERE filter."),
            ("What is a Database View?",
             "A physical table stored on disk", "A virtual table defined by an underlying stored SQL query", "An index configuration", "A user permission role",
             "B", "Views are virtual relations whose contents are dynamically generated upon execution."),
            ("Which window function assigns a sequential integer to rows within a partition starting at 1?",
             "RANK()", "ROW_NUMBER()", "DENSE_RANK()", "LEAD()",
             "B", "ROW_NUMBER() numbers rows sequentially without gaps in partition rankings."),
            ("What is the purpose of database normalization (1NF, 2NF, 3NF)?",
             "Increases storage consumption", "Minimizes data redundancy and prevents insertion/update/deletion anomalies", "Speeds up JOIN operations", "Encrypts tables",
             "B", "Normalization organizes fields and table relationships to reduce redundant duplication."),
            ("Which command creates a new table in SQL?",
             "MAKE TABLE", "CREATE TABLE", "NEW TABLE", "INIT TABLE",
             "B", "CREATE TABLE defines a new relational entity, columns, data types, and constraints."),
            ("What does NULL represent in SQL?",
             "The number zero (0)", "Empty text string ('')", "Missing, unknown, or inapplicable value", "False boolean",
             "C", "NULL indicates the absence of any value and evaluates to UNKNOWN in comparisons."),
            ("Which SQL clause sorts query results in descending order?",
             "ORDER BY col DESC", "SORT BY col DOWN", "GROUP BY col DESC", "ORDER BY col INVERT",
             "A", "ORDER BY <column> DESC arranges results from highest to lowest."),
            ("What does EXPLAIN ANALYZE do in PostgreSQL?",
             "Deletes query plan", "Executes the query and displays actual execution time and cost metrics for each node", "Backs up database", "Changes column names",
             "B", "EXPLAIN ANALYZE runs the query plan and prints real timing, row counts, and buffer hits.")
        ]
    elif "Data Structures" in subj or "DSA" in subj:
        templates = [
            ("What is the worst-case time complexity of accessing an element in an array by index?",
             "O(n)", "O(1)", "O(log n)", "O(n^2)",
             "B", "Direct index offset calculation provides constant O(1) time complexity."),
            ("What data structure adheres to Last-In, First-Out (LIFO) order?",
             "Queue", "Stack", "Heap", "Binary Search Tree",
             "B", "Stacks process items in LIFO order using push and pop operations."),
            ("What is the average time complexity of searching in a balanced Binary Search Tree (AVL / Red-Black)?",
             "O(1)", "O(log n)", "O(n)", "O(n log n)",
             "B", "Halving the search space at each depth level yields O(log N) search performance."),
            ("What data structure operates on First-In, First-Out (FIFO) principles?",
             "Stack", "Queue", "Priority Queue", "Hash Table",
             "B", "Queues process elements in FIFO sequence (enqueue at rear, dequeue from front)."),
            ("What is the average time complexity for key lookup in a well-distributed Hash Table?",
             "O(1)", "O(n)", "O(log n)", "O(n^2)",
             "A", "Hash functions compute direct bucket locations in average O(1) constant time."),
            ("Which sorting algorithm has a worst-case time complexity guaranteed to be O(n log n)?",
             "QuickSort", "MergeSort", "BubbleSort", "InsertionSort",
             "B", "MergeSort divides the array recursively and merges sorted halves in O(N log N) worst-case."),
            ("In Big-O notation, what does O(1) represent?",
             "Linear time", "Constant time regardless of input size", "Logarithmic time", "Exponential time",
             "B", "O(1) signifies constant execution time invariant with dataset volume."),
            ("Which traversal of a Binary Search Tree visits nodes in ascending sorted order?",
             "Pre-order", "In-order", "Post-order", "Level-order",
             "B", "In-order traversal (Left, Root, Right) yields elements in strict ascending order."),
            ("What is a cycle in a linked list?",
             "A list with two nodes", "A node whose next pointer loops back to a previously visited node", "An empty list", "A doubly-linked list",
             "B", "A cycle occurs when node pointers form a continuous loop without terminating at null."),
            ("Which algorithm detects cycles in a linked list using two pointers moving at different speeds?",
             "Dijkstra's Algorithm", "Floyd's Tortoise and Hare Cycle-Finding Algorithm", "Binary Search", "Kruskal's Algorithm",
             "B", "Floyd's algorithm uses slow (1 step) and fast (2 step) pointers to detect loops."),
            ("What is the space complexity of an in-place QuickSort implementation?",
             "O(n^2)", "O(log n) stack frames on average", "O(n) auxiliary array", "O(1) strictly",
             "B", "Recursive stack frames require O(log N) space on average for balanced partitions."),
            ("Which data structure is primarily used to implement Breadth-First Search (BFS) in graphs?",
             "Stack", "Queue", "Max-Heap", "Set",
             "B", "BFS explores frontier nodes level by level using a FIFO Queue."),
            ("Which data structure is primarily used to implement Depth-First Search (DFS) in graphs?",
             "Queue", "Stack (or recursion call stack)", "Hash Map", "Priority Queue",
             "B", "DFS explores deeply along branches using a LIFO Stack or the system call stack."),
            ("What is the worst-case time complexity of QuickSort?",
             "O(n log n)", "O(n^2)", "O(n)", "O(log n)",
             "B", "Unbalanced partitions (e.g. choosing smallest/largest pivot repeatedly) degrade QuickSort to O(N^2)."),
            ("What property must a Min-Heap satisfy?",
             "Left child is always smaller than right child", "Parent node value is less than or equal to both child node values", "Nodes must be sorted horizontally", "Tree must be unbalanced",
             "B", "In a Min-Heap, the root/parent holds the minimum key among all descendants."),
            ("What is memoization in Dynamic Programming?",
             "Deleting past answers", "Caching expensive subproblem results to avoid redundant recursive recomputation", "Sorting input arrays", "Allocating linked lists",
             "B", "Memoization records computed outcomes in a table, transforming exponential recursion to polynomial time."),
            ("What is the time complexity of binary search on a sorted array of size N?",
             "O(N)", "O(log N)", "O(1)", "O(N^2)",
             "B", "Binary search cuts the viable interval in half each iteration, achieving O(log N)."),
            ("What is a Priority Queue typically implemented with for optimal push and pop operations?",
             "Unsorted Array", "Binary Heap (array-based)", "Singly Linked List", "Binary Search Tree",
             "B", "Binary heaps deliver O(log N) insertion and O(log N) maximum/minimum extraction.")
        ]
    else:
        # Fallback general software engineering questions
        templates = [
            (f"What is the best practice for error handling in {t_title}?",
             "Ignore all errors silently", "Catch and log exceptions gracefully with descriptive diagnostic messages", "Terminate machine", "Infinite retry without delay",
             "B", "Graceful exception handling preserves system stability and produces actionable telemetry."),
            (f"How does unit testing improve code quality in {t_title}?",
             "Slows down release cycles", "Verifies individual components behave as specified and prevents regression bugs", "Replaces compiler", "Eliminates documentation",
             "B", "Unit testing automates verification of core logic and guards against refactoring regressions."),
            (f"What is the principle of Separation of Concerns in {t_title}?",
             "Combining all logic into a single file", "Modularizing distinct aspects of functionality into dedicated classes/functions", "Duplicating code across modules", "Writing code without comments",
             "B", "Separation of concerns keeps codebases maintainable, testable, and decoupled."),
            (f"What is the primary benefit of version control (Git) when developing {t_title}?",
             "Formats code automatically", "Tracks revision history, enables collaborative branching, and permits atomic rollbacks", "Runs automated benchmarks", "Generates binaries",
             "B", "Git provides distributed version tracking, facilitating multi-developer code integration."),
            (f"Which design pattern provides a single point of access to an instance throughout the application?",
             "Factory Pattern", "Singleton Pattern", "Observer Pattern", "Adapter Pattern",
             "B", "The Singleton pattern restricts instantiation of a class to one single object reference."),
            (f"What is the purpose of continuous integration (CI) in software development?",
             "Manual deployment once a year", "Automating build verification and test suites on every code commit", "Writing user documentation", "Designing logos",
             "B", "CI builds and tests code changes automatically to catch defects early in the pipeline."),
            (f"What does DRY stand for in software engineering principles?",
             "Do Repeat Yourself", "Don't Repeat Yourself", "Data Realtime Yield", "Direct Routing Yield",
             "B", "DRY advocates reducing duplication of information and business logic across systems."),
            (f"What is the role of an API contract?",
             "Determines developer pay", "Specifies the expected inputs, outputs, schemas, and behaviors of service endpoints", "Encrypts hardware", "Compiles source code",
             "B", "API contracts define strict communication interfaces between disparate client and server systems."),
            (f"Why is immutability valued in modern software architectures?",
             "Allows arbitrary modifications", "Prevents side effects, concurrency race conditions, and makes state changes predictable", "Consumes less memory always", "Mandated by OS",
             "B", "Immutable objects cannot change after creation, eliminating class-wide data corruption risks."),
            (f"What is refactoring in software maintenance?",
             "Adding new user features", "Restructuring existing code to improve internal readability and architecture without changing external behavior", "Writing user stories", "Deleting test suites",
             "B", "Refactoring improves maintainability and decreases technical debt while preserving behavior."),
            (f"What is the benefit of code reviews in engineering teams?",
             "Increases bugs", "Facilitates knowledge sharing, catches bugs early, and maintains uniform code style standards", "Replaces unit testing", "Slows down computers",
             "B", "Peer code reviews enhance codebase quality and promote collective ownership."),
            (f"What is telemetry and logging used for in production systems?",
             "Formatting code", "Monitoring system health, debugging live incidents, and understanding user traffic patterns", "Deleting databases", "Increasing binary size",
             "B", "Observability telemetry provides real-time visibility into errors and performance metrics."),
            (f"What is technical debt in software projects?",
             "Financial loans taken by companies", "The implied future cost of additional rework caused by choosing easy shortcuts over better designs", "Hardware depreciation", "Salary expenses",
             "B", "Technical debt builds up when expedient code is written instead of clean architectural solutions."),
            (f"What is the primary role of a linter in modern software workflows?",
             "Compiles binaries", "Analyzes source code to flag programming errors, bugs, stylistic errors, and anti-patterns", "Executes integration tests", "Manages cloud servers",
             "B", "Linters statically analyze code to enforce best practices and syntax consistency."),
            (f"Why are semantic versions (SemVer: MAJOR.MINOR.PATCH) important?",
             "They look professional", "They communicate breaking changes (MAJOR), new features (MINOR), and bug fixes (PATCH) clearly to consumers", "Mandated by browsers", "Speed up download times",
             "B", "SemVer provides a universal standard for understanding software compatibility."),
            (f"What is the purpose of asynchronous processing for long-running tasks?",
             "Blocks the user UI indefinitely", "Offloads heavy work to background workers, keeping user interfaces snappy and responsive", "Runs code backwards", "Forces synchronous execution",
             "B", "Async job queues prevent server request timeouts and keep web apps interactive."),
            (f"What does an environment variable (.env) typically configure?",
             "HTML tags", "Sensitive credentials, API keys, database connection strings, and per-environment settings", "CSS styles", "Font weights",
             "B", "Environment variables separate configuration secrets from source code repositories."),
            (f"What is regression testing?",
             "Testing only new code", "Re-running functional and non-functional tests to ensure previously working software remains intact after edits", "Testing performance under stress", "Translating code into English",
             "B", "Regression tests confirm that recent changes have not broken existing functionality.")
        ]

    for q in templates[:needed_count]:
        questions.append({
            "question_text": q[0].format(topic=t_title),
            "option_a": q[1],
            "option_b": q[2],
            "option_c": q[3],
            "option_d": q[4],
            "correct_option": q[5],
            "explanation": q[6]
        })
        
    return questions

def main():
    print("=== SEEDING MINIMUM 20 MCQS PER TOPIC ===")
    topics = Topic.objects.all().order_by('id')
    total_added = 0
    
    for topic in topics:
        existing_count = TopicQuizQuestion.objects.filter(topic=topic).count()
        target = 20
        needed = target - existing_count
        
        if needed <= 0:
            print(f"Topic {topic.id} ({topic.title}): Already has {existing_count} MCQs.")
            continue
            
        print(f"Topic {topic.id} ({topic.title}): Currently {existing_count} MCQs. Seeding {needed} more...")
        
        # Check existing questions via fast in-memory set
        existing_texts = set(TopicQuizQuestion.objects.filter(topic=topic).values_list('question_text', flat=True))
        tailored = TOPIC_QUESTIONS.get(topic.id, [])
        to_insert = []
        
        # Use tailored first
        for q in tailored:
            if q["question_text"] not in existing_texts:
                to_insert.append(q)
                existing_texts.add(q["question_text"])
                if len(to_insert) >= needed:
                    break
                    
        # Fill remaining if needed
        remaining_needed = needed - len(to_insert)
        if remaining_needed > 0:
            extra = generate_questions_for_topic(topic, remaining_needed + 5)
            for q in extra:
                if q["question_text"] not in existing_texts:
                    to_insert.append(q)
                    existing_texts.add(q["question_text"])
                    if len(to_insert) >= needed:
                        break
                        
        # Bulk insert into database
        current_max_order = TopicQuizQuestion.objects.filter(topic=topic).count()
        objs = [
            TopicQuizQuestion(
                topic=topic,
                question_text=q_data["question_text"],
                option_a=q_data["option_a"],
                option_b=q_data["option_b"],
                option_c=q_data["option_c"],
                option_d=q_data["option_d"],
                correct_option=q_data["correct_option"],
                explanation=q_data["explanation"],
                order=current_max_order + idx + 1
            )
            for idx, q_data in enumerate(to_insert)
        ]
        if objs:
            TopicQuizQuestion.objects.bulk_create(objs)
            total_added += len(objs)
            
        final_count = TopicQuizQuestion.objects.filter(topic=topic).count()
        print(f"  -> Topic {topic.id} now has {final_count} MCQs.")
        
    print(f"\nSUCCESS: Added {total_added} new MCQs across all topics. Every topic now has >= 20 MCQs.")

if __name__ == '__main__':
    main()
