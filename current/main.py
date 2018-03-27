from appJar import gui
import sqlite3
import string
from coinmarketcap import Market
dbloc = ""

#Main form
def main():
    main = gui("Crypto Tracker", "600x300")
    #Button functions for all forms
    #Functions are grouped by form
    
    def press(button):
        global dbloc
        
        ### START OF MAIN FORM BUTTON FUNCTIONS ###
        #Add form to be displayed
        if button == "Add a Transaction":
            main.showSubWindow("Add_Form")
            #As we're only hiding the form, clear the textbox once done
            main.clearEntry("no_coin")

        #Display edit form
        elif button == "Edit Holdings":
            main.showSubWindow("Edit_Form")
            #As we're only hiding the form, clear the textbox once done
            main.clearEntry("edit_no_coin")

        #Toggle currency displayed
        elif button == "Toggle Currency":
            print("Toggle")

        #Generate a pie chart
        elif button == "Generate Pie Chart":
            print("Chart")

        #Open a different folio dialog
        elif button == "Open different folio":
            print("Open other")
            #File open dialog
            dbloc = main.openBox("Open Different File",asFile=False,fileTypes=[('database', '*.sqlite')])
            #Read function
            dsp(dbloc,main)

        #Save as dialog
        elif button == "Save":
            print("Save")
            #File save dialog
            newloc = main.saveBox("Save Current",fileExt=".sqlite",fileTypes=[('database','*.sqlite')],asFile=False)
            #Save function
            saveNew(newloc,dbloc,main)
        
        elif button == "Quit":
            #Exit the program
            main.stop()
            
        ### END OF MAIN FORM BUTTON FUNCTIONS ###
            
        ### ADD FUNCTIONS ###
            
        elif button == "Add":
            #Get number of coins
            amount = 0
            amount = main.getEntry("no_coin")
            #Get number of coins
            coin_amount = 0
            coin_amount = main.getEntry("no_coin")
            #Get type of coin
            coin = ""
            coin = main.getOptionBox("Coins")

            #Insert into database
            insert(coin,amount,dbloc,main)
            
            #return to main form
            main.hideSubWindow("Add_Form")

        #If cancel is pressed return to main form
        elif button == "Cancel":
            main.hideSubWindow("Add_Form")
            
        ### END OF ADD FUNCTIONS ###

        ### START OF EDIT FUNCTIONS ###
        elif button == "Edit":
            #Get new no coins
            amount = 0
            amount = main.getEntry("edit_no_coin")
            #Get coin type
            coin = ""
            coin = main.getOptionBox("Edit Coins")
            
            #Edit database values
            edit(coin,amount,dbloc,main)
            
            #Return to main form
            main.hideSubWindow("Edit_Form")

        #If cancel button is pressed return to main form
        elif button == "Edit Cancel":
            main.hideSubWindow("Edit_Form")
            

        ### START OF INITIAL FORM FUNCTIONS ###
            
        #Open file select form
        if button == "Existing":
            #Display file open dialog
            dbloc = main.openBox("init_existing",asFile=False,parent="Init_Form",fileTypes=[('database', '*.sqlite')])
            #Read database
            dsp(dbloc,main)
            
            #Hide first window and show main
            main.hideSubWindow("Init_Form")
            main.show()
            
        #Open file save form
        elif button == "New":
            #Display file create dialog
            dbloc = main.saveBox("Init_New",fileExt=".sqlite",fileTypes=[('database','*.sqlite')],asFile=False,parent="Init_Form")
            #Create database and table
            createTable(dbloc,main)

            #Hide first window and show main
            main.hideSubWindow("Init_Form")
            main.show()
            
        #End execution
        elif button == "Exit":
            main.stop()
            
        ### END OF INITIAL FORM FUNCTIONS ###
            
    ### START INITIAL SUBWINDOW ###
    main.startSubWindow("Init_Form","Crypto Tracker")

    #Form layout
    main.setFont(16)
    main.addLabel("title", "Please select file to be used or create a new one")
    main.addButtons(["Existing","New"],press)
    main.addButton("Exit",press)    

    main.stopSubWindow()
    ### END OF INITIAL SUBWINDOW ###
    
    ### MAIN FORM LAYOUT ###
    main.setFont(12)
    main.addLabel("totalval", "Crypto Holdings Value: £99999")
    main.addButton("Add a Transaction",press,1,0,0,1)
    main.addButton("Edit Holdings",press,2,0,0,1)
    main.addButton("Toggle Currency",press,3,0,0,1)
    main.addButton("Generate Pie Chart",press,4,0,0,1)
    main.addButton("Open different folio",press,5,0,0,1)
    main.addButton("Save",press,5,1,0,1)
    main.addButton("Quit",press,5,3,0,1)
    main.addListBox("Holdings", [""],1,1,2,4)
    ### END OF MAIN FORM LAYOUT ###
    
    ### START ADD SUBWINDOW ###
    main.startSubWindow("Add_Form","Add a new transaction",modal=True)
    
    #Form layout
    main.setFont(12)
    main.addLabel("Header","To add a transaction, select the coin purchased and enter the quantity, then press add")
    up_coin = main.addLabelOptionBox("Coins",["Bitcoin","Litecoin","Vertcoin"],1)
    up_val = main.addNumericEntry("no_coin")
    main.setEntryDefault("no_coin", "Enter amount purchased")
    main.addButton("Add",press)
    main.addButton("Cancel",press)

    main.stopSubWindow()    
    ### END OF ADD SUBWINDOW ###
    
    ### START EDIT SUBWINDOW ###
    main.startSubWindow("Edit_Form","Edit a transaction",modal=True)
    #Form layout
    main.setFont(12)
    main.addLabel("Edit_Head","To edit holdings, select the coin and enter the new amount")
    edit_coin = main.addLabelOptionBox("Edit Coins",["Bitcoin","Litecoin","Vertcoin"],1)
    edit_no_coin = main.addNumericEntry("edit_no_coin")
    main.setEntryDefault("edit_no_coin", "Enter amount purchased")
    main.addButton("Edit",press)
    main.addButton("Edit Cancel",press)

    main.stopSubWindow()    
    ### END OF ADD SUBWINDOW ###
    
    #Execute, showing the initial form first
    main.go(startWindow = "Init_Form")

#Save to a new file
def saveNew(newloc,old,main):

    #Clear listbox
    main.clearListBox("Holdings")

    #Create old and new database objects and cursors
    old = sqlite3.connect(old)
    db = sqlite3.connect(newloc)
    oc = old.cursor()
    nc = db.cursor()

    #Calculate value before saving
    calcVal(dbloc)

    #Get data from old database
    sql = "select * from coins"
    recs = oc.execute(sql)    

    #Create table in new database
    nc.execute("CREATE TABLE if not exists coins (coin varchar(10) not null, price float not null, holdings float not null, holdings_value float not null)")
    counter = 0
    for row in recs:

        #Insert each record into new table
        nc.execute("insert into coins (coin,price,holdings,holdings_value) values('" + row[0] + "','" + str(row[1]) + "','" + str(row[2]) + "','" + str(row[3]) + "');")
        counter = counter + 1

    #Update listbox
    dsp(dbloc,main)
    
    #Commit changes and close databases
    db.commit()
    db.close()
    old.close()

#Create new database and a table within
def createTable(dbloc,main):

    #Connect to database and create cursor for SQL commands
    db = sqlite3.connect(dbloc)
    c = db.cursor()

    #Create table and insert 3 records
    c.execute("CREATE TABLE if not exists coins (coin varchar(10) not null, price float not null, holdings float not null, holdings_value float not null)")
    c.execute("insert into coins (coin,price,holdings,holdings_value) values('Bitcoin','0','0','0');")
    c.execute("insert into coins (coin,price,holdings,holdings_value) values('Litecoin','0','0','0');")
    c.execute("insert into coins (coin,price,holdings,holdings_value) values('Vertcoin','0','0','0');")

    #Commit changes to DB
    db.commit()
    
    #Update listbox
    dsp(dbloc,main)

#Add new holdings to those previously held in db
def insert(coin,amount,dbloc,main):

    #Connect to database
    db = sqlite3.connect(dbloc)
    c = db.cursor()

    #SQL to update table
    sql = ("update coins set holdings = (holdings + " +  str(amount) + ") where coin = '" + coin + "';")
    c.execute(sql)
    db.commit()

    #Update listbox
    dsp(dbloc,main)

#Edit holding amounts of a coin in the db
def edit(coin,amount,dbloc,main):

    #Connect to DB
    db = sqlite3.connect(dbloc)
    c = db.cursor()

    #SQL to edit holdings values
    sql = ("update coins set holdings = (" + str(amount) + ") where coin = '" + coin + "';")
    c.execute(sql)
    db.commit()

    #Update listbox
    dsp(dbloc,main)

#Scrapes coin values from CoinMarketCap API
def scrapeCoin(index,dbloc):

    #Create market API instance
    coinmarketcap = Market()
    #Scrape relevant data
    bitcoin = coinmarketcap.ticker("bitcoin")
    litecoin = coinmarketcap.ticker("litecoin")
    vertcoin = coinmarketcap.ticker("vertcoin")
    #Load into variables
    btcout = bitcoin[0]   
    ltcout = litecoin[0]
    vtcout = vertcoin[0]

    #Connect to database
    db = sqlite3.connect(dbloc)
    c = db.cursor()

    #Create coin array and dictionary
    coins = ["'Bitcoin'","'Litecoin'","'Vertcoin'"]
    coinDict = {"Bitcoin":0, "Litecoin":0, "Vertcoin":0}

    #Load values into dictionary
    if index == 0:
        coinDict["'Bitcoin'"] = btcout["price_usd"]
    elif index == 1:
        coinDict["'Litecoin'"] = ltcout["price_usd"]
    elif index == 2:
        coinDict["'Vertcoin'"] = vtcout["price_usd"]
                          
    return coinDict[coins[index]]

#Calculates value of holdings
def calcVal(dbloc):

    valArr = []

    #Connect to database
    db = sqlite3.connect(dbloc)
    c = db.cursor()

    #Select only holdings
    sql = "select holdings from coins"
    vals = c.execute(sql)

    coins = ["'Bitcoin'","'Litecoin'","'Vertcoin'"]
    
    counter = 0
    #Append value of each coin * holding to array
    for row in vals:
        current = float(scrapeCoin(counter,dbloc))
        valArr.append(current * float(row[0]))
        counter = counter + 1

    #Update database to show value of holdings
    for i in range(3):
        sql = ("update coins set holdings_value = (" + str(valArr[i]) + ") where coin = " + coins[i] + ";")
        c.execute(sql)

    #Commit and close database
    db.commit()
    db.close()

#Function to update listbox 
def dsp(dbloc,main):

    #Clear listbox
    main.clearListBox("Holdings")
    
    #Connect to database
    db = sqlite3.connect(dbloc)
    c = db.cursor()

    #Always calculate value here to show most relevant price
    calcVal(dbloc)

    #Select all to display from database
    sql = "select * from coins"
    recs = c.execute(sql)
    
    counter = 0

    #Loop through records and add each to listbox
    for row in recs:

        #Format output to 2 dp
        currentPrice = "%0.2f" % float(scrapeCoin(counter,dbloc))
        holdings = "%0.2f" % row[2]
        value = "%0.2f" % row[3]        

        #Add each item to listbox
        main.addListItem("Holdings",(str(row[0]) + " price:$" + currentPrice + " Holdings:" + holdings + " Holdings value:$" + value))
        counter = counter + 1

#Go
main()

