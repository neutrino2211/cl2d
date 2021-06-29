import pyopencl as cl
import numpy
from PIL import Image

memory_flags = cl.mem_flags

class Buffer:

    _draw_events = []

    def __init__(self, width, height, ctx = None, queue = None, alias_type = Image.BILINEAR):
        self.queue = queue
        self.ctx = ctx
        self.width = width
        self.height = height
        self.alias_type = alias_type

        if self.ctx == None:
            self.ctx = cl.create_some_context()

        if self.queue == None:
            self.queue = cl.CommandQueue(self.ctx)

        self.buf = numpy.zeros((height, width, 4)).astype(numpy.uint8)
        self.cl_buffer = cl.Buffer(self.ctx, memory_flags.READ_WRITE | memory_flags.COPY_HOST_PTR, hostbuf=self.buf)
        

    def get_np_buffer(self):
        # cl._enqueue_read_buffer(queue: pyopencl._cl.CommandQueue, mem: pyopencl._cl.MemoryObjectHolder, hostbuf: object)
        cl.enqueue_copy(self.queue, self.buf, self.cl_buffer)
        # print(self.buf[0][0])
        return self.buf