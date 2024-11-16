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

The select() system call can be used to check if there is new data or not, e.g: at stdin file descriptor.
Then a blocking system call like read() may be used afterwards knowing that they will complete immediately.