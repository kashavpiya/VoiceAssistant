

root = Tk()
root.title ("Voice Assistant")
root.geometry("600x600")
#for icon, hereu send the location of the file
root.iconbitmap("robo.ico")
#root.iconbitmap()

#create label widget
#myLabel1 = Label(root, text = "Hello World!")
#myLabel2 = Label(root, text = "My name is Srijal Shrestha")
#myLabel3 = Label(root, text = " ").grid(row = 1, column = 2)
# shoving it onto the screen
#this will just display everything to 
#the extent of what  u need
#myLabel.pack()


#myLabel1.grid(row = 0, column = 0)
#myLabel2.grid(row = 1, column = 5)
#this is the program running, it can be disrupted
#by the x button or any other exit button u include

#buttons are basically widgets too

#myButton = Button(root, text = "Click Me!", state=DISABLED)
#myButton = Button(root, text = "Click Me!", padx=50, pady=50)

#e = Entry(root)
e = Entry(root, width = 50, borderwidth= 5)
e.pack()

def myClick():
    myLabel = Label(root, text = "Button Clicked")
    myLabel.pack()

def clickInput():
    hello =  "Hello " + e.get()
    myLabel = Label(root, text = e.get())
    myLabel.pack()

myButton = Button(root, text = "Click Me!", command = clickInput, fg="yellow", bg="#000000")
myButton.pack()

#tkiner only supports gif or pnm
#but Pillow helps use other

myImg = ImageTk.PhotoImage(Image.open("valorant-collectible-make-em-dance-spray.png"))
my_label = Label(image = myImg)
my_label.pack()

#drop down boxes
clicked = StringVar()
clicked.set("Usable Functions")
dropList = ["Monday", "Tuesday", "Wednesday"]
drop = OptionMenu(root, clicked, *dropList)
drop.pack()

button_quit = Button(root, text= "Exit Program", command=root.quit)
button_quit.pack()
#creating input fields
root.mainloop()

