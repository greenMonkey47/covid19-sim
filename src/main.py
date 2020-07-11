import tkinter as tk
import numpy as np
import random as rn
from time import sleep
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation


class person():
    def __init__(self,window,position,radius,velocity,status):
        #TODO  change status to tydef variables
        
        self.color = ['blue','green','red']
        self.shape = window.create_circle(position[0],position[1],r=radius,color=self.color[status])
        self.status = status
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.radius = radius

        if(status==2):
            self.timeInfected = 0
        else:
            self.timeInfected = -1

    def change_color(self,canvas,idx):
        self.status=idx
        canvas.itemconfig(self.shape,fill=self.color[idx])


    def move_person(self,canvas):
        canvas.move(self.shape,self.velocity[0],self.velocity[1])

    def collided(self,other):
        if(np.linalg.norm(self.position-other.position)<2*self.radius):
            return True
        else:
            return False


class Root(tk.Tk):

    def __init__(self):
        super(Root,self).__init__()
        self.title("Test")
        
        self.width = 1200
        self.height = 800

        self.geometry(str(self.width)+"x"+str(self.height))
        
        self.frame_graph = tk.Frame(self,height=150)
        self.frame_graph.pack()

        self.frame_canvas = tk.Frame(self)
        self.frame_canvas.pack(fill=tk.BOTH,side=tk.LEFT,expand= True)
        

        self.frame_widgets = tk.Frame(self,bg="blue")
        self.frame_widgets.pack(fill=tk.BOTH,expand= True)

        self.create_widgets()
        self.run=True
        self.pause = False
        self.time_var = 0

        self.x = np.vstack((np.array([0]),np.array([0])))
        self.y = np.vstack((np.array([0,0,0]),np.array([0,0,0]))) 

    def _destroy(self):
        self.run=False
        self.quit()
    
    def create_widgets(self):
        
        
        '''
        self.canvas_graph = tk.Canvas(self.frame_graph,bg="white",width=1200,height=150)
        self.canvas_graph.pack(fill=tk.BOTH,expand=True)
        '''
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
        self.time.insert(0,"100")

        tk.Label(self.frame_widgets, text="Trasmission").grid(row=3,sticky="w")
        self.trans = tk.Entry(self.frame_widgets)
        self.trans.grid(row=3,column=1)
        self.trans.insert(0,"100")

        self.f = Figure(figsize=(12,2))
        self.a = self.f.add_subplot(111,xlim=(0,500),ylim=(0,100))
        self.graph = FigureCanvasTkAgg(self.f, self.frame_graph)
        self.graph.draw()


        self.status_vector = np.zeros([1,3])

        startButton = tk.Button(self.frame_widgets,text="Start",command=self.begin_simulation,width=9)
        startButton.grid(row=4,column=0,sticky="w")

        pauseButton = tk.Button(self.frame_widgets,text="Pause",command=self.end_simulation,width=9)
        pauseButton.grid(row=4,column=1,sticky="w")

    def end_simulation(self):
        if(self.pause == False):
            self.run = False
            self.pause = True
        else:
            print("checking")
            self.run = True
            self.pause = False
            self.loop_wrapper()



    def create_circle(self,x,y,r=8,color="blue"):
        return self.canvas.create_oval(x-r,y-r,x+r,y+r,fill=color)

    def count_status(self):
        self.status_vector = np.zeros(3)
        for i in self.persons:
            self.status_vector[i.status]+=1



    def make_graph(self):

        self.b_line = self.a.plot(self.x[1:],self.y[1:,0],'b-')
        self.g_line = self.a.plot(self.x[1:],self.y[1:,1],'g-')
        self.r_line = self.a.plot(self.x[1:],self.y[1:,2],'r-')

        self.graph.draw()
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def loop(self):
        self.time_var+=1

        for i in self.persons:
            i.position[0]+=i.velocity[0]
            if(i.position[0]>=self.canvas.winfo_width() or i.position[0]<=0):
                i.velocity[0]=-i.velocity[0]

            i.position[1]+=i.velocity[1]
            if(i.position[1]>=self.canvas.winfo_height() or i.position[1]<=0):
                i.velocity[1]=-i.velocity[1]

            
            for j in self.persons:
                if(i==j):
                    pass
                else:
                    if(i.collided(j) and i.status==2 and rn.randint(0,100)<self.trans_rate):
                        j.change_color(self.canvas,2)
            
            if(i.status==2):

                if(i.timeInfected==-1):
                    i.timeInfected=0
                elif(i.timeInfected<self.recovery_time):
                    i.timeInfected+=1
                else:
                    i.status=1
                    i.change_color(self.canvas,1)
            
            i.move_person(self.canvas)
        
        self.count_status()
        
        self.x = np.vstack((self.x,self.time_var))
        self.y = np.vstack((self.y,self.status_vector))
        self.make_graph()


    def loop_wrapper(self):
        
        while self.run:
            self.canvas.update()
            self.after(10,self.loop())

    def begin_simulation(self):
        
        self.run = True
        self.canvas.delete("all")
        self.noPeople = int(self.start.get())
        self.prob_val = int(self.prob.get())
        self.recovery_time = int(self.time.get())
        self.trans_rate = int(self.trans.get())
        self.radius =8
        self.persons = []
        

        for i in range(0,self.noPeople):
            
            x = rn.randint(0,self.width-8)
            y = rn.randint(0,self.height-8)

            vx = rn.randint(-10,10)
            vy = rn.randint(-10,10)
            
            s = 0
            
            if(rn.randint(0,100)<self.prob_val):
                s = 2
            
            temp = person(self,[x,y],self.radius,[vx,vy],s)
            self.persons.append(temp)
        
        
        self.loop_wrapper()
        

def main():
    window = Root()
    window.after(20)
    window.protocol("WM_DELETE_WINDOW", window._destroy)
    window.mainloop()
    window.destroy()

if __name__=="__main__":
    main()