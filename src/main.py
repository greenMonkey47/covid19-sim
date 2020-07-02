import tkinter as tk
import numpy as np
import random as rn

class person():
    def __init__(self,position,velocity,status):
        self.status = status
        self.pos = np.array(position)
        self.velocity = np.array(velocity)


class Root(tk.Tk):

    def __init__(self):
        super(Root,self).__init__()
        self.title("Test")
        self.geometry("1200x800")
        
        self.frame_canvas = tk.Frame(self)
        self.frame_canvas.pack(fill=tk.BOTH,side=tk.LEFT,expand= True)
        

        self.frame_widgets = tk.Frame(self,bg="blue")
        self.frame_widgets.pack(fill=tk.BOTH,expand= True)

        self.create_widgets()
    
    def create_widgets(self):
        
        self.canvas = tk.Canvas(self.frame_canvas,bg= "white",width=1000,height=800)
        self.canvas.pack(fill=tk.BOTH,expand=True)

        tk.Label(self.frame_widgets, text="Starting").grid(row=0,sticky="w")
        tk.Entry(self.frame_widgets).grid(row=0,column=1)
       
        tk.Label(self.frame_widgets, text="Probability").grid(row=1,sticky="w")
        tk.Entry(self.frame_widgets).grid(row=1,column=1)
       
        tk.Label(self.frame_widgets, text="Time").grid(row=2,sticky="w")
        tk.Entry(self.frame_widgets).grid(row=2,column=1)
       
        startButton = tk.Button(self.frame_widgets,text="Start",command=self.begin_simulation,width=21)
        startButton.grid(row=3,column=0,columnspan=3,sticky="w")
    
    def create_circle(self,x,y,r=10,color="blue"):
        self.canvas.create_oval(x-r,y-r,x+r,y+r,fill=color)

    def begin_simulation(self):
        self.create_circle(10,20)
        self.create_circle(100,20)
        self.create_circle(10,200)
        pass



def main():
    window = Root()
    window.mainloop()

if __name__=="__main__":
    main()