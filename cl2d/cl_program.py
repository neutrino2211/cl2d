import pyopencl as cl

class CL_PROG:
    def __init__(self, ctx, file = None, code = None):
        self.code = code
        self.ctx = ctx
        
        if file:
            f = open(file)
            self.code = f.read()
            f.close()

        self._kernel = cl.Program(self.ctx, self.code)

    def kernel(self):
        return self._kernel.build()