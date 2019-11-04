"""
Dungeon Masters Tools
Has two main abilties: Encounters and Player Information
The encounters enables a DM to put in details of monsters and characters and it works out what type of encounter it is
The Player information takes note of the players name, their character name and their max health.
"""

from tkinter import *#include everything from the tkinter module
charName_arr=[]
playerName_arr=[]
charInfo=[]     
class App(Tk):#constructor for the frames
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #setup menu so we can access the exit option from a File menu
        MainMenu(self)
        #setup frame for each of the 'pages'
        container = Frame(self,bg="Red",width = 500, height = 500)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}#creates a list of frames

        for f in (StartPage, encounters, players):#for each frame f in the list of pages
            frame = f(container, self)
            self.frames[f]=frame#will make an entry of the frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)#show the frame for the start page as this initialises it. looks to the show frame method below

    def show_frame(self, context):# passes in the name of the frame which is the context name here
        frame = self.frames[context]#uses the frame name that is passed into it, so to begin it passes StartPage
        frame.tkraise()#shows the frame


class StartPage(Frame):#the main starting page to access the other functionality.
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        f = Frame(self, width = 500, height = 500)#creates the frame on the page
        f.pack(side=LEFT, expand = 1)
        label = Label(f, text="Dungeon Masters Tools",font=("Verdana",16))#adds the label for the title of the program.the f determines it is placed in the frame
        label.grid(row=2,column=2)#determines where inside the frame the label is placed

        page_two = Button(f, text="Character Info", command=lambda:controller.show_frame(players))#creates the button to the Character Info page
        page_two.grid(row=4,column=2)
        page_one = Button(f, text="Encounters", command=lambda:controller.show_frame(encounters))#creates the button to go to the encounters page
        page_one.grid(row=4,column=5)

class encounters(Frame):#the encounters page
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        def partyXPThreshold(level_ans2,char_ans2):#works out the party XP threshold to determine the encounter level
            party=[]
            level=level_ans2
            characters=char_ans2
            partyFile=open("charXPthreshold.txt","r")#opens the file in read mode to look at the values from the D&D Players Handbook
            for arec in partyFile:
                values = arec.split()
                party.append([int(values[0]),int(values[1]),int(values[2]),int(values[3]),int(values[4])])#stores the items in a 2D array
                #0 = level, 1=easy, 2=medium, 3=hard, 4=deadly
            lengthParty=len(party)
            for i in range(0,lengthParty):
                if party[i][0]==level:#performs the calculations for each of the levels as obtained from the D&D Players Handbook
                    easy=party[i][1]*characters
                    medium=party[i][2]*characters
                    hard=party[i][3]*characters
                    deadly=party[i][4]*characters

            easyLabel = Label(f, text="Easy: "+str(easy))#displays the levels and each of the value thresholds
            easyLabel.grid(row=6,column=2, columnspan=3, sticky=E)
            mediumLabel = Label(f, text="Medium: "+str(medium))
            mediumLabel.grid(row=7,column=2, columnspan=3,sticky=E)
            hardLabel = Label(f, text="Hard: "+str(hard))
            hardLabel.grid(row=8,column=2, columnspan=3,sticky=E)
            deadlyLabel = Label(f, text="Deadly: "+str(deadly))
            deadlyLabel.grid(row=9,column=2, columnspan=3,sticky=E)
            return easy, medium, hard, deadly
        
            partyFile.close()

        def readValues():#reads in the values from the boxes for the character number and the level number
            char_ans2=int(char_ans.get())#gets the answer from the entry box
            level_ans2=int(level_ans.get())   
            level=partyXPThreshold(level_ans2,char_ans2)
            return level
            
        def monsterReading():
            mons_ans2=int(mons_ans.get())#gets the answer from the entry box
            monXP_ans2=int(monXP_ans.get())
            
            total = mons_ans2 * monXP_ans2#works out the monster encounter value by taking the number of monsters and the XP and multiplying
            easyLabel = Label(f, text="Monster XP: "+str(total))#displays the encounter response
            easyLabel.grid(row=6,column=7, columnspan=3, sticky=E)
            return total

        def encounterType():#works out the encounter by comparing the total monster value and the party XP threshold
            level = readValues()
            monsTotal=monsterReading()
            titleLabel = Label(f, text="Encounter type",font=("Verdana",14))
            titleLabel.grid(row=13,column=2, columnspan=3, sticky=E)
            encLabel = Label(f, text="                           ",font=("Verdana",14))
            encLabel.grid(row=14,column=2, columnspan=3, sticky=E)
            if monsTotal>=level[3]:#compares the answer and displays the appropriate response.
                encLabel = Label(f, text="DEADLY",bg="red",fg="White",font=("Verdana",14))
                encLabel.grid(row=14,column=2, columnspan=3, sticky=E)
            elif monsTotal>=level[2]:
                encLabel = Label(f, text="Hard",font=("Verdana",14))
                encLabel.grid(row=14,column=2, columnspan=3, sticky=E)
            elif monsTotal>=level[1]:
                encLabel = Label(f, text="Medium",font=("Verdana",14))
                encLabel.grid(row=14,column=2, columnspan=3, sticky=E)
            else:
                encLabel = Label(f, text="Easy",font=("Verdana",14))
                encLabel.grid(row=14,column=2, columnspan=3, sticky=E)
            
                

        f=Frame(self, width=500, height=500)#sets the frame up on the encounters page
        f.pack(side=LEFT, expand=1)
        
        welcome = Label(f, text="Encounter Check", bg="red",fg="white",font=("Verdana",14))#displays the title
        welcome.grid(row=1,column=2,columnspan=10)
        
        characters = Label(f, text="Number of Characters",font=("Verdana",8))#asks for the number of characters
        characters.grid(row=2,columnspan=4, sticky=E)
        char_ans=Entry(f)
        char_ans.grid(row=2,column=4)

        level = Label(f, text="Level",font=("Verdana",8))#asks for the level of the characters
        level.grid(row=4,columnspan=4, sticky=E)
        level_ans=Entry(f)
        level_ans.grid(row=4,column=4)

        monsters = Label(f, text="Number of Monsters",font=("Verdana",8))#asks for the number of monsters
        monsters.grid(row=2,column=7, columnspan=4, sticky=E)
        mons_ans=Entry(f)
        mons_ans.grid(row=2,column=12)

        monXP= Label(f, text="Monster XP",font=("Verdana",8))#asks for the monster XP value
        monXP.grid(row=4,column=7, columnspan=4, sticky=E)
        monXP_ans=Entry(f)
        monXP_ans.grid(row=4,column=12)

        Button(f,text="Calculate Character",command=readValues).grid(row=10, column=3)#provides the button to calculate the character values
        Button(f,text="Calculate Monsters",command=monsterReading).grid(row=10, column=7)#provides the button to calculate the monster values
        note = Label(f, text="(All boxes must be complete) for the type of encounter to be calculated",font=("Verdana, 10"))
        note.grid(row=11,column=4, columnspan=4)
        Button(f,text="Type of Encounter",command=encounterType).grid(row=12, column = 5)#provides the button to calculate the final encounter type

        start_page = Button(f, text="Back to start page", command=lambda:controller.show_frame(StartPage))#provides the button back to the main page
        start_page.grid(row=20,column=2)
        page_two = Button(f, text="Characters", command=lambda:controller.show_frame(players))#provides the button to the characters or players page
        page_two.grid(row=20,column=5)

class players(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def showCharBoxes():#this will show the boxes to enter the character information for character name, player name and the max health
            numChar=int(numCharBox_ans.get())
            for i in range(0,numChar):
                #labels
                charName = Label(f, text="Character Name",font=("Verdana",8))
                charName.grid(row=i+5,columnspan=4, sticky=E)
                #entry
                charName_ans = Entry(f)
                charName_ans.grid(row=i+5,column=4)
          
                #labels
                playerName = Label(f, text="Player Name",font=("Verdana",8))
                playerName.grid(row=i+5,column=4,columnspan=4, sticky=E)
                #entry
                playerName_ans = Entry(f)
                playerName_ans.grid(row=i+5,column=9)
                              #labels
                health = Label(f, text="Max Health",font=("Verdana",8))
                health.grid(row=i+5,column=9,columnspan=4, sticky=E)
                #entry
                health_ans = Entry(f)
                health_ans.grid(row=i+5,column=15)
                charInfo.append([charName_ans,playerName_ans,health_ans])
    

        def saveCharacterInfo():#this will save the information entered for the characters into a file
            fName=fileName.get()
            t=""
            n=open(fName+".txt","w")
            for i in charInfo:
                t="Character: "+i[0].get()+", is played by "+i[1].get()+". Their max health is:"+i[2].get()
                n.write(t+"\n")
            fname= Label(f, text="Complete!",font=("Verdana",14))
            fname.grid(row=18,column=1, columnspan=20)
            n.close()
         
        f = Frame(self, width = 500, height = 500)#setup of the frame for the characters page
        f.pack(side=LEFT, expand = 1)

        characters= Label(f, text="Characters",font=("Verdana",14))#displays the heading
        characters.grid(row=1, column=3)

        numCharBox= Label(f, text="Number of Characters",font=("Verdana",8))#asks for the number of characters
        numCharBox.grid(row=2,column=3, columnspan=8, sticky=E)
        numCharBox_ans=Entry(f)
        numCharBox_ans.grid(row=2,column=12)
        button=Button(f,text="Enter Character Details",command=showCharBoxes).grid(row=3, column=1,columnspan=10)#button to allow the user to enter the correct number of character details
        button=Button(f,text="Save Details",bg="light blue",command=saveCharacterInfo).grid(row=3, column=14,columnspan=4)#ensures the information is saved into a file

        fname= Label(f, text="Enter file name below to save these details to...(any existing file name will be overwritten)",font=("Verdana",10))
        fname.grid(row=15,column=1, columnspan=20)
        fname= Label(f, text="Once you have entered the file name press Save Details above",font=("Verdana",10))#allows the user to enter a file name
        fname.grid(row=16,column=1, columnspan=20)
        fileName = Entry(f)
        fileName.grid(row=17,column=1)

    
        start_page = Button(f, text="Back to start page", command=lambda:controller.show_frame(StartPage))#button to go back to the main page
        start_page.grid(row=20,column=2)
        page_one = Button(f, text="Encounters", command=lambda:controller.show_frame(encounters))#button to go to the encounters page
        page_one.grid(row=20,column=5)

class MainMenu:
    def __init__(self, master):#the main menu to allow the user to quit by going to File and Exit
        menubar= Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)

app = App()#creates an instance of itself
app.mainloop()
