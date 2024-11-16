## Blocking vs Non-Blocking System Call

### Blocking IO
A blocking system call is one that must wait until the action can be completed.

involves transitioning task (eg thread) to waiting state (thread.sleep -> to yield control to other threads to run) to wait for IO to return. meanwhile thread cannot run other tasks.

(
similarly in the coroutine world, if coroutine needs to be awaited (coroutine.sleep -> to yield to other coroutines to run) ie suspended to wait for io operation to return then it's blocking.

BUT for coroutines since it's using cooperative scheduling not preempted, it's up to developer to write the program st it will yield control back to the main event loop IF the operation performed is blocking
-- eg in python when making a blocking network call, developer may use yield / coroutine.sleep to tell the python interpreter to return control back to the main event loop and resume this coroutine whenever python interpreter is able to.
)


For instance, read() is blocking:

If no input is ready, the calling process will be suspended
yield() the remaining quanta, and schedule other processes first
It will only resume execution after some input is ready. Depending on the scheduler implementation it may either:
Be scheduled again and retry (e.g: round robin)
The process re-executes read() and may yield() again if there’s no input.
Repeat until successful.
Not scheduled, use some wait flag/status to tell the scheduler to not schedule this again unless some input is received
wait flag/status cleared by interrupt handler (more info in the next topic)
On the other hand, a non blocking system call can return almost immediately without waiting for the I/O to complete.

### Non-blocking IO
For instance, select() is non-blocking.

since io operation returns almost immediately, need to use polling to check on the progress of the operation eg how many bytes have been read if we're reading the whole file. 

The select() system call can be used to check if there is new data or not, e.g: at stdin file descriptor.
Then a blocking system call like read() may be used afterwards knowing that they will complete immediately.


## System Call via API Examples

#### Example: printf()

We always conveniently call printf() whenever we want to display our output to the console in C. printf itself is a POSIX system call API.

This function requires kernel service as it involves access to hardware: output display.
The function printf is actually making several other function calls to prepare the resources or requirements for this system call and finally make the actual system call that invokes the kernel’s help to display the output to the display.


The full implementation of printf in Mach OS can be found here. It calls other functions like putc and eventually write function that makes the system call to stdout file descriptor.


## System Call

**Implementation**

System calls are interfaces through which user applications interact with the operating system’s kernel to perform tasks that require higher privileges, such as I/O operations, process management, and file manipulations.

System calls are implemented as part of the operating system kernel. When a user program invokes a system call, it executes a software interrupt or a special instruction that switches the processor from user mode to kernel mode. This transition is necessary because system calls often require accessing resources that are protected and can only be safely manipulated by the kernel.

**System Call Number:**

Each system call is associated with a unique identifier known as a system call number. This number is used to index into a system call table maintained by the kernel, which maps numbers to the corresponding system call handlers. When a system call is invoked, the kernel uses this number to find the appropriate function to execute.


