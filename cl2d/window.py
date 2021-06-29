import tkinter
from numpy import uint8
from PIL import Image, ImageTk
from .opencl import Buffer
from threading import Event, Thread

class Window:

    _is_drawing = False

    def __init__(self, title: str, buffer: Buffer, target_fps = 30, width = 720, height = 480):
        self.window = tkinter.Tk()
        self.window.title(title)
        self.window.configure(bg="black")
        self.window.geometry(f"{width}x{height}")
        self.buffer = buffer

        self.width = width
        self.height = height

        self.target_fps = target_fps
        self.ticker = Event()

    def _init_canvas(self):
        self.buffer_width, self.buffer_height, _ = self.buffer.buf.shape

        self.canvas = tkinter.Canvas(self.window, width=self.width, height=self.height)
        # self.canvas.configure(bg="black")
        img = self._resize_img()
        self.frame = ImageTk.PhotoImage(image=img)

        self.frame_on_canvas = self.canvas.create_image(0, 0, image=self.frame, anchor=tkinter.NW)
        self.window.bind("<Configure>", self._resize_canvas)
        self.canvas.pack()

    def _resize_canvas(self, event):
        self.width = event.width
        self.height = event.height
        self.canvas.config(width=self.width, height =self.height)
        self._resize_img()

    def _resize_img(self):
        img = Image.fromarray(self.buffer.buf.astype(uint8), "RGBA")
        img = img.resize((self.width, self.height), self.buffer.alias_type)
        return img

    def draw(self):
        # self.buffer.rand_buf()
        self.buffer.get_np_buffer()
        # print(self.buffer.buf)
        img = self._resize_img()
        self.frame = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfig(self.frame_on_canvas, image=self.frame)

    def _draw_loop(self):
        while not self.ticker.wait(1/self.target_fps):
            # self.draw()
            self.canvas.after(int(1000/self.target_fps), self.draw)

    def start(self):
        self._init_canvas()
        self.draw_thread = Thread(target=self._draw_loop)
        self.draw_thread.start()
        # t.join()
        self.window.protocol("WM_DELETE_WINDOW", self.on_destroy)
        self.window.mainloop()

    def on_destroy(self):
        self.window.destroy()