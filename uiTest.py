from tkinter import*
from tokenize import String
from PIL import ImageTk, Image

root = Tk()
root.title ("Voice Assistant")
root.geometry("400x600")
root.iconbitmap("robo.ico")

clicked = StringVar()
clicked.set("Functions:")
dropList = ["Monday","Tuesday", "Wednesday", "Functions:"]
drop = OptionMenu(root, clicked, *dropList)
drop. grid(row = 0, column = 0)

myImg = ImageTk.PhotoImage(Image.open("robot.jpg"))
my_label = Label(image = myImg)
my_label.grid(row=1, column = 1)

def myClick():
    myLabel = Label(root, text = "Button Clicked")
    myLabel.grid(row)

myButton = Button(root, text = "Listen!", width = 25, command = myClick, fg="yellow", bg="#000000")
myButton.grid(row = 2, column = 1)

button_quit = Button(root, text= "Exit", command=root.quit)
button_quit.grid(row = 2, column = 2)

myLabel2 = Label(root, text = "Logs:", borderwidth=5)
myLabel2.grid(row = 3, column = 0)


root.mainloop()