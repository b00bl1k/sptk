import time

import wx
from pubsub import pub
from serial.threaded import Protocol, ReaderThread  # noqa


class SerialReceiver(Protocol):

    def __init__(self):
        self.buffer = bytearray()
        self.transport = None

    def __call__(self):
        return self

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        self.transport = None
        wx.CallAfter(pub.sendMessage, "serial.connection_lost")

    def data_received(self, data):
        wx.CallAfter(pub.sendMessage, "serial.receive", data=data)


class SerialLogView:

    def update_line(self, index, data):
        raise NotImplementedError()

    def insert_line(self, index, tm, data):
        raise NotImplementedError()

    def clear_lines(self):
        raise NotImplementedError()


class SerialLog:

    def __init__(self, view: SerialLogView, delim_count=None, delim_time=None,
                 delim_char=None):
        self.view = view
        self.delim_count = delim_count
        self.delim_time = delim_time
        self.delim_char = delim_char
        self.time = 0
        self.bytes_count = 0
        self.lines_count = 0
        self.line_len = 0
        self.lines_time = []
        self.lines_data = []
        self._is_new_line = False

    def _new_line(self, t):
        self.lines_count += 1
        self.line_len = 0
        self.lines_time.append(t)
        self.lines_data.append(b"")

    def add_bytes(self, data):
        for b in data:
            self.add_byte(bytes([b]))

    def add_byte(self, b):
        t = time.time()
        is_new_line = (
                self._is_new_line
                or not self.lines_count
                or (self.delim_count and self.line_len >= self.delim_count)
                or (self.delim_char and self.delim_char == b)
                or (self.delim_time and t - self.time > self.delim_time)
        )
        self._is_new_line = False
        self.time = t
        if is_new_line:
            self._new_line(t)
        i = self.lines_count - 1
        self.lines_data[i] += b
        self.line_len += 1
        self.bytes_count += 1
        if is_new_line:
            self.view.insert_line(i, self.lines_time[i], self.lines_data[i])
        else:
            self.view.update_line(i, self.lines_data[i])

    def clear(self):
        self.bytes_count = 0
        self.lines_count = 0
        self.time = 0
        self.lines_time.clear()
        self.lines_data.clear()
        self.view.clear_lines()

    def new_line(self):
        self._is_new_line = True
