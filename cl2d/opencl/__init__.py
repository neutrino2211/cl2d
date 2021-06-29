import pyopencl as cl
import numpy
from .buffer import Buffer

_ctx = None
_buffer = numpy.array([])
_cl2d_buffer = None
_global_cl_buffer = None

memory_flags = cl.mem_flags

def init_global_buffer(x: int = 720, y: int = 480):
    global _ctx
    global _buffer
    global _cl2d_buffer

    if _ctx is None:
        raise Exception("Context not created")

    _cl2d_buffer = Buffer(x, y, _ctx)

    _buffer = _cl2d_buffer.buf
    _global_cl_buffer = _cl2d_buffer.cl_buffer

def global_np_buffer():
    global _buffer
    return _buffer

def global_buffer():
    global _cl2d_buffer
    return _cl2d_buffer

def init_global_context():
    global _ctx

    _ctx = cl.create_some_context()