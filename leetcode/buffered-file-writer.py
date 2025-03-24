class File:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write(self, bytes: bytearray):
        with open(self.file_path, mode="ab") as f:
            f.write(bytes)


class BufferedFile(File):
    def __init__(self, f: File, buffer_size: int):
        self.f = f
        self.buffer_size = buffer_size
        self.buffer = bytearray()

    def write(self, bytes: bytearray):
        print("write", bytes)
        # write from byte array to buffer until full then flush this first
        remaining_buffer_cap = self.buffer_size - len(self.buffer)
        self.buffer += bytes[:remaining_buffer_cap]
        self.flush()

        # then fill up buffer with remaining bytes from byte array so we don't overflow
        self.buffer += bytes[remaining_buffer_cap + 1 :]

    def flush(self):
        print("flushing to disk")
        self.f.write(self.buffer)
        self.buffer.clear()
