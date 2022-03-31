import tkinter, random, sys, os, json

window = tkinter.Tk()
window.title("FPS Trainer")
window.geometry("500x350")
window.config(bg="black")

with open("file-remember/highscore.json", "r") as file:
    highscore = file.read()
    highscore = json.loads(highscore)
#variables
list = ["Press W", "Press A", "Press D", "Press S", "Press Space", "Single Click", "Double Click", "Triple Click"]
time    = 20
points  = 0
labels  = []
#tkinter variables
timeTK   = tkinter.StringVar()
pointsTK = tkinter.StringVar()

#defines
def start():
    global time
    time = int(entryTime.get()) + 1
    entryTime.destroy()
    labelAsk.destroy()
    buttonStart.destroy()
    updateTime()
    counter()
    createRandomlabel()

def counter():
    global time, x
    if time > 1:
        time -= 1
        window.after(1000, counter)
        updateTime()
    else:
        time -= 1
        updateTime()
        randomLabel.destroy()
        window.unbind(var1)
        scorebord()
        popup()

def createRandomlabel():
    global randBind, randomLabel, var1
    randBind = random.choice(list)
    var1 = bindVar(randBind)
    randomLabel = tkinter.Label(
        window,
        text=randBind,
        width=10,
        height=2
    )
    randomLabel.pack()
    randomLabel.place(x=(random.randint(0,421)), y=random.randint(36, 307))
    if "Press" in randBind:
        window.bind(var1, hit)
    else:
        randomLabel.bind(var1, hit)

def bindVar(var):
    if var == "Press W":
        return "w"
    elif var == "Press A":
        return "a"
    elif var == "Press D":
        return "d"
    elif var == "Press S":
        return "s"
    elif var == "Press Space":
        return "<space>"
    elif var == "Single Click":
        return "<Button-1>"
    elif var == "Double Click":
        return "<Double-Button-1>"
    elif var == "Triple Click":
        return "<Triple-Button-1>"

def hit(event):
    global points
    if "Press" in randBind:
        points += 1
    else:
        points += 2
    updatePoints()
    randomLabel.destroy()
    if "Press" in randBind:
        window.unbind(var1)    
    createRandomlabel()

def updateTime():
    global timeTK
    timeTK = "time: " + str(time)
    labelTime.config(text=timeTK)

def updatePoints():
    global pointsTK
    pointsTK = "points: " + str(points)
    labelPoints.config(text=pointsTK)

def stop():
    popUp.destroy()
    window.destroy()

def scorebord():
    global entry_, scoreB, button, labels
    scoreB = tkinter.Toplevel(window)
    rank = checkScore()
    if rank != False:
        entry_ = tkinter.Entry(scoreB,
            width=25
        )
        button = tkinter.Button(scoreB,
            width=25,
            text= "save",
            command= lambda: updateHighscore(rank)
        )
    for z in range(10):
        tekst = (highscore[str(z+1)]["name"] +"\n"+ str(highscore[str(z+1)]["score"]))
        labels.append(tkinter.Label(
            scoreB,
            text = tekst,
            width= 30
        ))
        labels[z].pack()
    if rank != False:
        entry_.pack()
        button.pack()

        
def checkScore():
    for x in range(1, 11):
        if points > highscore[str(x)]["score"]:
            return x
    return False

def updateHighscore(rank):
    global highscore
    z = 10 - rank
    s = 10
    for x in range(z):
        d = s - 1
        highscore[str(s)] = {'name': highscore[str(d)]["name"], 'score': highscore[str(d)]["score"]}
        s -= 1
    highscore[str(rank)] = {'name': entry_.get(), 'score': points}
    with open("file-remember/highscore.json", "w") as file:
        save = json.dumps(highscore, indent= 2)
        file.writelines(save)
    for z in range(1, 11):
        tekst = (highscore[str(z)]["name"] +"\n"+ str(highscore[str(z)]["score"]))
        labels[z-1].config(text = tekst)
    button.destroy()
    entry_.destroy()


def popup():
    global popUp
    popUp = tkinter.Tk()
    popUp.geometry("200x200")

    retry = tkinter.Button(
        popUp,
        text = "Retry",
        width= 3,
        height= 1,
        command=restart
    )
    
    quit = tkinter.Button(
        popUp,
        text = "Quit",
        width = 3,
        height= 1,
        command=stop
    )
    
    pointVar = str(points) + " Point(s)"
    label1 = tkinter.Label(
    popUp,
    text = pointVar
    )

    label1.pack()
    retry.pack()
    quit.pack()

    label1.place(anchor="c", x = "100", y = "75")
    retry.place(anchor= "s", x= 50, y=150)
    quit.place(anchor= "s", x= 150, y=150)

    popUp.mainloop()

def restart():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

#tkinter labels, widgets, pop ups etc...
labelTime = tkinter.Label(
    window,
    padx = 125
)

labelPoints = tkinter.Label(
    window,
    padx=125
)

labelAsk = tkinter.Label(
    window,
    text="Time in seconds: ",
    width=16,
    borderwidth=0,
    padx=2
)

entryTime = tkinter.Entry(
    window,
    width=19,
    borderwidth=0
)

buttonStart = tkinter.Button(
    window,
    text="Start",
    command=start
)

labelTime.pack()
labelPoints.pack()
labelAsk.pack()
entryTime.pack()
buttonStart.pack()

labelTime.place(anchor="n", x=125)
labelPoints.place(anchor="n", x=375)
labelAsk.place(anchor="s", y=140, x=250)
entryTime.place(anchor="n", y=140, x=250)
buttonStart.place(anchor="c", x=250, y=175)

entryTime.focus()

#run first
updateTime()
updatePoints()

window.mainloop()