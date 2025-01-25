JVM is a language VM ie java source code is compiled down to java byte code and interpreted on the fly by the JVM into machine code. Java byte code defines its own set of opcodes which get translated more directly into machine code.

**1. Compiler compiles Source code -> Instruction Set / Opcodes**
Each virtual machine typically has its own instruction set based on the requirements of the language(s) the VM must support. These instruction sets are similar to instruction sets of hardware CPUs.
Common types of instructions:
• Local variable load and store operations
• Constant value load operations
• Array load and store operations
• Arithmetic operations (add, sub, mul, div, ...)
• Logical operations (and, or, xor, ...)
• Type conversions
• Conditional and unconditional branches
• Method invocations and returns
• ...
The JVM uses a straightforward stack-oriented bytecode instruction set with ~200 instructions (opcodes).

Interpreted code is >2.5-50x slower than compiled code/machine code because there are extra costs associated with interpretation:
• Dispatch (fetch, decode and invoke) next instruction
• Access virtual registers and arguments
• Perform primitive functions outside the interpreter loop
![jvm_compliation_into_bytecode](https://yqintl.alicdn.com/6919097ed53be9ffdfde8f1645bdb8a1b8e81735.pnga)

**1.1 Types of compilation**
1. Dynamic / Just-in-Time (JIT) compilation
- compile code on the fly when VM is running
2. Static / Ahead-of-Time (AOT) compilation --- Faster
- compiles code before execution

**JIT compilation 1.1.1**
Just-In-Time (JIT) compilation is a mechanism employed by the Java Virtual Machine (JVM) to enhance the runtime performance of Java applications. Here’s an overview of how JIT compilation operates:

- Bytecode Interpretation: When a Java application starts, the JVM initially interprets the bytecode. This bytecode is a platform-independent intermediate representation derived from Java source code. The JVM reads and executes this bytecode line by line, converting it into machine code that the computer’s processor can understand. Machine code, or machine language, is the fundamental language of computers, composed of binary numbers that the CPU interprets as ones and zeros. This translation from human-readable source code to binary machine code is necessary because computer hardware can only process instructions in binary form.
- HotSpot Identification: While interpreting the bytecode, the JVM monitors the execution to identify sections of the code that are executed frequently, known as “hot spots”.
- JIT Compilation: When the JVM detects a hot spot, the JIT compiler is activated. The JIT compiler translates the hot spot from bytecode into native machine code, which can be executed directly by the computer’s processor. This native code is then stored for subsequent use.
- Direct Execution: On encountering the hot spot again, the JVM bypasses the interpretation phase and directly executes the precompiled machine code. This phase, often referred to as “warm-up,” is the period during which the Java application transitions to optimal performance by utilizing the compiled machine code. The JIT compiler’s role is to ensure that this compiled code is highly optimized, significantly boosting the application’s performance.

The JIT compiler is integrated into the JVM. Popular JVM implementations, such as Oracle’s HotSpot and OpenJDK, include JIT compilation capabilities. 

JIT compilation of the JVM causes performance penalties:
![jvm_jit_cold_start](https://yqintl.alicdn.com/8045908fe31096c668f724ae35627492ce6548de.png)
During the startup of a Java application, the JVM (Java Virtual Machine) software program corresponding to the application needs to be loaded into memory, as shown in the red part in the figure above. Then, the JVM loads the corresponding application into memory. This process is represented by the light blue class loading (CL) part in the figure above. During the class loading process, the application begins to be interpreted and executed, as shown in the light green part in the figure above. In the interpretation and execution process, the JVM recycles garbage objects, as shown in the yellow part in the figure above. As the program runs deeper, the JVM uses just-in-time (JIT) compilation technology to compile and optimize code with higher execution frequency, improving the running speed of the application. The JIT process is represented by the white part in the figure above. The code optimized by JIT compilation is represented by the dark green part in the figure above. From this analysis, it is clear that a Java program goes through several stages, including VM initialization, App initialization, and App activation before reaching JIT dynamic compilation optimization. Compared to other compiled languages, Java's cold start problem is more severe.

Apart from the cold start problem, it is evident from the above analysis that during the execution of a Java program, the initial step involves loading a JVM, which occupies a certain amount of memory. Additionally, because the Java program first interprets and executes bytecode before performing JIT compiler optimization, it is easy to load more code than is actually required, resulting in some unnecessary memory usage compared to certain compiled languages.

**1.1.2. AOT compilation**
Ahead-Of-Time (AOT) compilation is a technique that enables Java bytecode to be transformed into native machine code before the application is executed. This differs from the traditional Just-In-Time (JIT) compilation, which converts bytecode to machine code at runtime.

Here is how AOT compilation works in Java:
- Compilation: Using an AOT compiler, such as the jaotc tool introduced in JDK 9, the Java bytecode is compiled into native machine code ahead of the application’s execution. This compilation process occurs separately from the actual running of the application, ensuring that the native code is ready before the application starts.
- Linking: The compiled native machine code is then linked with the JVM. This linking step ensures that the native code integrates seamlessly with the JVM, allowing for proper interaction during execution.
- Execution: When the application is launched, the JVM can immediately execute the pre-compiled native code. This eliminates the need for the JVM to interpret the bytecode or compile it to machine code at runtime, resulting in faster startup times and reduced runtime overhead.

AOT compilation is especially advantageous for applications that require quick startup times or operate in environments where runtime performance is critical. While AOT compilation can significantly enhance performance, it is not intended to completely replace JIT compilation. Instead, it works alongside JIT compilation. The JVM can still employ JIT compilation for code sections that were not pre-compiled using AOT.

GraalVM is a notable JVM that supports AOT compilation. It features a tool called native-image, which can generate standalone native executables from Java applications. These executables package the application, necessary libraries, JDK, and a streamlined JVM, allowing them to run independently without a separate JVM installation.
![graal_vm_aot](https://yqintl.alicdn.com/f5051c036d35b06925e4649a566e417000a953bc.png)


**Multi-threading support**
Each thread behaves as if it owns the entire virtual machine
- ... except when the thread needs to access external resources such as storage, network, display, or perform I/O operations in general.
- ...or when the thread needs to communicate with the other threads.
For multi-threading, each Java thread has its own execution stack to store its individual state; Critical places of the VM (and libraries) must use mutual exclusion to avoid deadlocks and resource conflicts; Access to external resources (e.g., storage, network) must be controlled so that two threads do not interfere with each other; 

Avoiding Atomicity Problems Using Safepoints
• In operating systems, threads can usually be interrupted at arbitrary locations.
    - Interrupts may be generated by hardware at any time.
    - The entire operating system must be designed to take into account mutual exclusion problems!
    - Must use monitors or semaphores to protect code that can be executed only by one thread at the time.
• In VMs, simpler solutions are often used.
    - Threads can only be interrupted in certain locations inside the VM source code.
    - These locations are known as “safepoints”.
    - In the simplest case, thread switching is only allowed in one place inside the VM.

Case study: KVM
The original KVM implementation used a simple, portable round robin
scheduler.
- Threads stored in a circular list; each thread got to execute a fixed number of bytecodes until interrupt was forced.
- Thread priority only affected the number of bytecodes a thread may run before it gets interrupted.
- Fully portable thread implementation; interrupts driven by bytecode counting; thread switching handled inside the interpreter loop


Typed languages e.g. Java translate more directly into byte code.
