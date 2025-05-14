import os


class DummyDB:

    def __init__(self, filename: str = ""):
        self.filename = filename

    def set(self, db_id: int, value: str):
        with open(self.filename, "a") as f:
            f.write(f"{db_id},{value}\n")

    def get(self, db_id: int) -> str | None:
        for record in self.read_reverse():
            curr_id, curr_value = record.split(',')
            if int(curr_id) == db_id:
                return curr_value
        return None


    def read_reverse(self, buf_size = 8192):
        with open(self.filename, "rb") as f:
            segment: bytes | None = None
            offset = 0
            f.seek(0, os.SEEK_END)
            file_size = remaining_size = f.tell()

            while remaining_size > 0:
                offset = min(file_size, buf_size + offset)
                f.seek(file_size - offset)
                buffer = f.read(min(remaining_size, buf_size))
                if remaining_size == file_size and buffer[-1] == ord('\n'):
                    buffer = buffer[:-1]
                remaining_size -= buf_size
                lines = buffer.split('\n'.encode())
                if segment is not None:
                    lines[-1] += segment
                segment = lines[0]
                lines = lines[1:]
                for line in reversed(lines):
                    yield line.decode()
            if segment is not None:
                yield segment.decode()

