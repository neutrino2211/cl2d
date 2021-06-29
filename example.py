from cl2d.window import Window
from cl2d.cl_program import CL_PROG
from cl2d.object import Object as CL2DObject
from cl2d.opencl import init_global_context, init_global_buffer, global_buffer
from PIL import Image

init_global_context()
init_global_buffer(3,3)

buffer = global_buffer()
buffer.alias_type = Image.NEAREST
program = CL_PROG(buffer.ctx, file="example/shaders/red_square.cl")
cl_object = CL2DObject(buffer, cl_prog=program)
cl_object.start()

print(buffer.buf.shape)

game = Window("Game", buffer)

game.start()