###Gui for face recognition system with online and offline features

from tkinter import *
from tkinter import filedialog
import os

window=Tk()
window.iconbitmap(r'.\icons\logo1.ico')
window.title('Face Recognition')
window.geometry('800x400')

#function calling for capturing photo and making folder automatic
def capture():
    #enter user_input for makeing folder using diaglog box
    global  user_input
    user_input = simpledialog.askstring(title="Capture",prompt="Please enter your name \n\n and face towards the camera:\n\n")
    #make a folder
    if type(user_input)==str:       #doesnot give nonetype error  if cancel is pressed in dialog box
        folder_path = "./faces/"+user_input
        os.mkdir(folder_path)
        print(folder_path)
        #passing user_input variable value to another file(face-cap.py) to save in new made folder
        myVars = {'user_input':user_input}
        exec(open('face-cap.py').read(), myVars)    #exec() also run another file(face-cap.py) paralleling and passes the value also

#def train():
#	os.system('python face.py')

#fuction to recognize face with offline
def recognize_offline():
    #dialog box for opening the video file
    my_filetypes = [('mp4  files', '*.mp4'), ('png files', '.png'),('jpg files', '.jpg'), ('all files', '.*')]
    file_path = filedialog.askopenfilename(parent=window,
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=my_filetypes)
#    capture_value='C:/Users/Hukka/Desktop/test videos/videorec.mp4'
    if len(file_path) >0:           #check for empty string and to remove error 
        file_path=file_path.replace('/','\\')
        myVars = {'capture_value':file_path}
        exec(open('webcam_recognizer_unknown.py').read(), myVars) 

#fuction to recognize face with online
def recognize_online():
    #capture_value=0 indicatecamera of device
    capture_value=0
    myVars = {'capture_value':capture_value}
    exec(open('webcam_recognizer_unknown.py').read(), myVars) 
#    os.system('python webcam_recognizer.py')

###display text and image and button
l0=Label(window,text='Welcome to face recognition system:')
l0.config(font=("Courier", 20,"bold"))
l0.pack(pady=10)

middleframe=Frame(window)
middleframe.pack(pady=20)

pic1=PhotoImage(file='.\icons\camera.png')
# but1=Button(middleframe,image=pic1,command=capture)
but1=Label(middleframe,image=pic1)
but1.grid(column=0,row=0,padx=25)
b1=Button(middleframe,text='Capture',command=capture,bg='black',fg='white')
b1.config(font=("Courier", 10,"bold"))
b1.grid(column=0,row=1,padx=20,pady=20)


pic2=PhotoImage(file='.\icons\chip.png')
# but2=Button(middleframe,image=pic2,command=train)
but2=Label(middleframe,image=pic2)
but2.grid(column=1,row=0,padx=25)
#b2=Button(middleframe,text='Offline',command=recognize_offline,bg='black',fg='white')
#b2.config(font=("Courier", 10,"bold"))
#b2.grid(column=1,row=1,padx=20,pady=20)

######################## dropdown-option
OPTIONS = [
"Real time",
"Offline"
] #etc
def online():
    print('online')
    recognize_online()


def offline():
    print('offline') 
    recognize_offline()

def recognize_option():
    if variable.get()=='Real time':
        online()
    else:
        offline()

variable = StringVar(window)
variable.set(OPTIONS[0]) # default value
b33 = OptionMenu(window, variable, *OPTIONS)
#b3.config(font=("Courier", 10,"bold"))
#b33.grid(column=2,row=2)
b33.pack()
####################################

pic3=PhotoImage(file='./icons/recog.png')
# but3=Button(middleframe,image=pic3,command=recognize)
but3=Label(middleframe,image=pic3)
but3.grid(column=2,row=0,padx=25)
b3=Button(middleframe,text='Recognize',command=recognize_option,bg='black',fg='white')
b3.config(font=("Courier", 10,"bold"))
b3.grid(column=2,row=1,padx=20,pady=20)



statusbar = Label(window, text="Thank you for using our system. - Comp2073", relief=SUNKEN, anchor=W)
statusbar.config(font=("Courier", 10,"bold"))
statusbar.pack(side=BOTTOM, fill=X)

window.mainloop()