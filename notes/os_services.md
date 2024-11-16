## Blocking vs Non-Blocking System Call

### Blocking IO
A blocking system call is one that must wait until the action can be completed.

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