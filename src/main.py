import tkinter as tk
import numpy as np
import random as rn
from time import sleep

class person():
    def __init__(self,window,position,velocity,status):
        self.color = ["blue","green","red"]
        self.shape = window.create_circle(position[0],position[1],color=self.color[status])
        self.status = status
        self.position = np.array(position)
        self.velocity = np.array(velocity)

    def move_person(self,canvas):
        #print(self.shape)
        canvas.move(self.shape,self.velocity[0],self.velocity[1])


class Root(tk.Tk):

    def __init__(self):
        super(Root,self).__init__()
        self.title("Test")
        
        self.width = 1200
        self.height = 800

        self.geometry(str(self.width)+"x"+str(self.height))
        
        self.frame_canvas = tk.Frame(self)
        self.frame_canvas.pack(fill=tk.BOTH,side=tk.LEFT,expand= True)
        

        self.frame_widgets = tk.Frame(self,bg="blue")
        self.frame_widgets.pack(fill=tk.BOTH,expand= True)

        self.create_widgets()
    
    def create_widgets(self):
        
        self.canvas = tk.Canvas(self.frame_canvas,bg= "white",width=1000,height=800)
        self.canvas.pack(fill=tk.BOTH,expand=True)

        tk.Label(self.frame_widgets, text="Starting").grid(row=0,sticky="w")
        self.start = tk.Entry(self.frame_widgets)
        self.start.grid(row=0,column=1)
        self.start.insert(0,"100")

        tk.Label(self.frame_widgets, text="Probability").grid(row=1,sticky="w")
        self.prob = tk.Entry(self.frame_widgets)
        self.prob.grid(row=1,column=1)
        self.prob.insert(0,"10")
       
        tk.Label(self.frame_widgets, text="Time").grid(row=2,sticky="w")
        self.time = tk.Entry(self.frame_widgets)
        self.time.grid(row=2,column=1)
        self.time.insert(0,"10")

        startButton = tk.Button(self.frame_widgets,text="Start",command=self.begin_simulation,width=21)
        startButton.grid(row=3,column=0,columnspan=3,sticky="w")
        
    def create_circle(self,x,y,r=8,color="blue"):
        return self.canvas.create_oval(x-r,y-r,x+r,y+r,fill=color)

    def loop(self):
        # TO DO -- check collision
        for i in self.persons:
            i.position[0]+=i.velocity[0]
            if(i.position[0]>=self.canvas.winfo_width() or i.position[0]<=0):
                i.velocity[0]=-i.velocity[0]

            i.position[1]+=i.velocity[1]
            if(i.position[1]>=self.canvas.winfo_height() or i.position[1]<=0):
                i.velocity[1]=-i.velocity[1]

            i.move_person(self.canvas)

    def begin_simulation(self):

        self.noPeople = int(self.start.get())
        self.prob_val = int(self.prob.get())
        self.recovery = int(self.time.get())
        self.persons = []

        for i in range(0,self.noPeople):
            
            x = rn.randint(0,self.width-8)
            y = rn.randint(0,self.height-8)

            vx = rn.randint(-10,10)
            vy = rn.randint(-10,10)
            
            s = 0
            
            if(rn.randint(0,100)<self.prob_val):
                s = 2
            
            temp = person(self,[x,y],[vx,vy],s)
            self.persons.append(temp)

        while True:
            self.canvas.update()
            self.after(40,self.loop())

def main():
    window = Root()
    window.after(20)
    window.mainloop()

if __name__=="__main__":
    main()