import tkinter as tk
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading, cv2,  time
import numpy as np

class TkVideoPlayer(tk.LabelFrame):
    def __init__(self, root, text, source, fps_label, res_label):
        super().__init__(root, text=text)
        self.height=int(1080/2)
        self.width=int(1920/2)
        
        self.prev_time = 0
        self.new_time = 0

        self.use_fps_counter = True
        self.use_internal_thread = True
        self.run = True
        self.record = False

        self.frame = 0
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.fps_label = fps_label
        self.res_label = res_label

        if self.use_internal_thread:
            self.thread = threading.Thread(target=self.Update)
            self.thread.start()

    def Convert_frame(self, frame):
        height = frame.shape[0]
        width = frame.shape[1]

        #WTF
        data = f'P6 {width} {height} 255 '.encode() + frame[..., ::-1].tobytes()

        PI = tk.PhotoImage(width=width, height=height, data=data, format="PPM")

        return PI
    
    def Update_screen(self, frame):
        photo = self.Convert_frame(frame)
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo

    def Process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        self.scan.append(np.argmax(gray, axis=0))
        self.intsensity.append(np.max(gray, axis=0))
        self.frame += 1

    def Update(self):
        while self.run:
            _, frame = self.video.read()
            
            if self.record:
                self.Process_frame(frame)


            else: # This code is super slow
                self.Update_screen()

            if self.use_fps_counter:
                self.Calculate_FPS(frame)
                self.res_label.set(f"{frame.shape[1]}x{frame.shape[0]}")



    def Calculate_FPS(self):
        self.new_time = time.time() 
        time_diff = self.new_time-self.prev_time
        fps = 1/time_diff
        self.prev_time = self.new_time 
        fps = int(fps) 
        fps = str(fps) 
        self.fps_label.set(f"{fps}")

    def Quit(self):
        self.run = False
        self.video.release()


class TkWebCam(tk.LabelFrame):
    def __init__(self, root, text, fps_label, res_label):
        super().__init__(root, text=text)
        self.resolutions = [
            "4032x3040",
            "3840x2144",
            "1920x1088",
            "1280x704",
            "1024x768",
            "640x480"
        ]
        self.height=int(1080/2)
        self.width=int(1920/2)
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.prev_time = 0
        self.new_time = 0
        self.fps_font = cv2.FONT_HERSHEY_SIMPLEX 
        self.use_fps_counter = True
        self.use_internal_thread = True
        self.run = True
        self.record = False
        self.frame = 0
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.picture_count = 0
        self.fps_label = fps_label
        self.res_label = res_label
        self.scan = []
        self.intsensity = []

        if self.use_internal_thread:
            self.thread = threading.Thread(target=self.FrameUpdate)
            self.thread.start()

    def Convert_frame(self, frame):
        height = frame.shape[0]
        width = frame.shape[1]

        #WTF
        data = f'P6 {width} {height} 255 '.encode() + frame[..., ::-1].tobytes()

        PI = tk.PhotoImage(width=width, height=height, data=data, format="PPM")

        return PI
    

    def FrameUpdate(self):
        while self.run:
            _, frame = self.video.read()
            
            if self.record:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
                self.scan.append(np.argmax(gray, axis=0))
                self.intsensity.append(np.max(gray, axis=0))
                self.frame += 1

            else: # This code is super slow
                photo = self.Convert_frame(frame)
                self.canvas.create_image(0, 0, image=photo, anchor=NW)
                self.canvas.image = photo

            if self.use_fps_counter:
                self.Calculate_FPS(frame)
                self.res_label.set(f"{frame.shape[1]}x{frame.shape[0]}")



    def Calculate_FPS(self, frame):
        self.new_time = time.time() 
        time_diff = self.new_time-self.prev_time
        fps = 1/time_diff

        self.prev_time = self.new_time 
        fps = int(fps) 
        fps = str(fps) 
        self.fps_label.set(f"{fps}")
        #cv2.putText(frame, fps, (7, 70), self.fps_font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    def Set_exposure(self, exposure):
        self.video.set(cv2.CAP_PROP_EXPOSURE, int(exposure)) 

    def Set_focus(self, focus):
        self.video.set(28, int(focus))


    def Toggle_record(self):
        self.frame = 0
        self.record = not self.record
        np.save("Heightmap/scan.npy", self.scan)
        np.save("Heightmap/intensity.npy", self.intsensity)
        self.scan = []
        self.intsensity = []
        print(self.record)

    def Take_picture(self):
        _, frame = self.video.read()
        np.save(f"Heightmap/picture_{self.picture_count}.npy", frame)
        self.picture_count += 1

    def Change_resolution(self, event):
        res = cb2.get().split("x")
        self.width = int(res[0])
        self.height = int(res[1])
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        print(self.width, self.height)
        


    def Quit(self):
        self.run = False
        self.video.release()