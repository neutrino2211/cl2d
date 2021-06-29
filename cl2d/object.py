from .opencl import buffer, global_np_buffer
from .cl_program import CL_PROG
from threading import Event, Thread
from time import time
import numpy

class Object:
    def __init__(self, buffer: buffer.Buffer, pos: (int, int) = (0,0), cl_prog: CL_PROG = None):
        self.pos = pos
        self.buffer = buffer
        self.cl_prog = cl_prog.kernel();
        self.thread = Thread(target=self._drawing_thread)

    def _drawing_thread(self):
        self.timer = Event()
        while not self.timer.wait(1/30):
            self.draw(time() - self._last_time)
            self._last_time = time()

    def start(self):
        self._last_time = time()
        self.thread.start()

    def draw(self, elapsed_time: float):
        # print("pre-draw")
        draw_call = self.cl_prog.draw(self.buffer.queue, self.buffer.buf.shape, None, self.buffer.cl_buffer, numpy.float32(elapsed_time), numpy.int32(self.buffer.buf.shape[1]), numpy.int32(self.buffer.buf.shape[0]))
        print(self.buffer.buf)
        # self.buffer._draw_events.append(draw_call)
        # print("Draw")