from Tkinter import *


def buttonAction():
    print "Time Period:",yrEnt.get()


#dont forget about var Int() thing for  drop down menu!!!!!!!!!
master = Tk()

var=StringVar(master)
var.set("minutes")
#master.configure(background='light gray')
#Instantiations
q1 = Label(master,text="Over what amount of time would you like to generate fake data?")
q2 = Label(master,text="How often would you like to sample the data?")
q3 = Label(master,text="How many nodes do you want to test?")
q4 = Label(master,text="What percent of nodes do you want to be failing?")
q5 = Label(master,text="What range of times do you want nodes to fail?")

#Question 1
q1.grid(row=0,padx=20,pady=20,columnspan=5)

##yrChk = Checkbutton(master)
##wkChk = Checkbutton(master)
##dayChk = Checkbutton(master)
##hrChk = Checkbutton(master)
##minChk = Checkbutton(master)

yrEnt = Entry(master, width=4)
wkEnt = Entry(master,width=4)
dayEnt = Entry(master,width=4)
hrEnt = Entry(master,width=4)
minEnt = Entry(master,width=4)

yr1Label = Label(master,text="years")
wk1Label = Label(master,text="weeks")
day1Label = Label(master,text="days")
hr1Label = Label(master,text="hours")
min1Label = Label(master,text="minutes")

yrEnt.grid(row=1,column=2,sticky=E)
wkEnt.grid(row=2,column=2,sticky=E)
dayEnt.grid(row=3,column=2,sticky=E)
hrEnt.grid(row=4,column=2,sticky=E)
minEnt.grid(row=5,column=2,sticky=E)

##yrChk.grid(row=1,column=1,sticky=E)
##wkChk.grid(row=2,column=1,sticky=E)
##dayChk.grid(row=3,column=1,sticky=E)
##hrChk.grid(row=4,column=1,sticky=E)
##minChk.grid(row=5,column=1,sticky=E)

yr1Label.grid(row=1,column=3,sticky=W)
wk1Label.grid(row=2,column=3,sticky=W)
day1Label.grid(row=3,column=3,sticky=W)
hr1Label.grid(row=4,column=3,sticky=W)
min1Label.grid(row=5,column=3,sticky=W)

#Question 2
q2.grid(row=6,padx=10,pady=10,columnspan=5)

##yrChk2 = Checkbutton(master)
##wkChk2 = Checkbutton(master)
##dayChk2 = Checkbutton(master)
##hrChk2 = Checkbutton(master)
##minChk2 = Checkbutton(master)

yrEnt1 = Entry(master, width=4)
wkEnt1 = Entry(master,width=4)
dayEnt1 = Entry(master,width=4)
hrEnt1 = Entry(master,width=4)
minEnt1 = Entry(master,width=4)

yrEnt1.grid(row=7,column=2,sticky=E)
wkEnt1.grid(row=8,column=2,sticky=E)
dayEnt1.grid(row=9,column=2,sticky=E)
hrEnt1.grid(row=10,column=2,sticky=E)
minEnt1.grid(row=11,column=2,sticky=E)

##yrChk2.grid(row=7,column=1,sticky=E)
##wkChk2.grid(row=8,column=1,sticky=E)
##dayChk2.grid(row=9,column=1,sticky=E)
##hrChk2.grid(row=10,column=1,sticky=E)
##minChk2.grid(row=11,column=1,sticky=E)

yr2Label = Label(master,text="years")
wk2Label = Label(master,text="weeks")
day2Label = Label(master,text="days")
hr2Label = Label(master,text="hours")
min2Label = Label(master,text="minutes")

yr2Label.grid(row=7,column=3,sticky=W)
wk2Label.grid(row=8,column=3,sticky=W)
day2Label.grid(row=9,column=3,sticky=W)
hr2Label.grid(row=10,column=3,sticky=W)
min2Label.grid(row=11,column=3,sticky=W)

#Question 3
q3.grid(row=12,padx=10,pady=10,columnspan=5)

nodeEnt = Entry(master, width=4)
nodeLabel = Label(master,text="nodes")

nodeEnt.grid(row=13, column=2)
nodeLabel.grid(row=13,column=3,sticky=W)

#Question 4
q4.grid(row=14,padx=10,pady=10,columnspan=5)

percentEnt = Entry(master, width=4)
percentLabel = Label(master,text="% of nodes")

percentEnt.grid(row=15, column=2)
percentLabel.grid(row=15,column=3,sticky=W)

#Question 5
q5.grid(row=16,padx=16,pady=10,columnspan=5)

leftEnt = Entry(master,width=4)
rightEnt = Entry(master,width=4)
midLabel = Label(master,text="to")
menu=OptionMenu(master,var,"years","weeks","days","hours","minutes")

leftEnt.grid(row=17,column=1,sticky=E)
rightEnt.grid(row=17,column=3,sticky=W)
midLabel.grid(row=17,column=2)
menu.grid(row=17,column=4,sticky=W)


#Generate button
genBut = Button(master,text="Generate Data",command=buttonAction)
genBut.grid(row=118,padx=20,pady=20,columnspan=5)


#master.geometry("640x480")
master.title("Node Data Generator")
master.mainloop()

