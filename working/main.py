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
        elif button == "Edit Holdings":
            main.showSubWindow("Edit_Form")
            #As we're only hiding the form, clear the textbox once done
            main.clearEntry("edit_no_coin")
        elif button == "Toggle Currency":
            print("Toggle")
        elif button == "Generate Pie Chart":
            print("Chart")
        elif button == "Open different folio":
            print("Open other")
            dbloc = main.openBox("Open Different File",asFile=False,fileTypes=[('database', '*.sqlite')])
            readTable(dbloc,main)
        elif button == "Save":
            print("Save")
            main.saveBox("Save Current",fileExt=".sqlite",fileTypes=[('database','*.sqlite')],asFile=True)
        elif button == "Quit":
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
            #Output for testing
            edit(coin,amount,dbloc,main)
            #Return to main form
            main.hideSubWindow("Edit_Form")
        elif button == "Edit Cancel":
            main.hideSubWindow("Edit_Form")
            

        ### START OF INITIAL FORM FUNCTIONS ###
            
        #Open file select form
        if button == "Existing":
            #Display file open form
            dbloc = main.openBox("init_existing",asFile=False,parent="Init_Form",fileTypes=[('database', '*.sqlite')])
            readTable(dbloc,main)
            main.hideSubWindow("Init_Form")
            main.show()
        #Open file save form
        elif button == "New":
            dbloc = main.saveBox("Init_New",fileExt=".sqlite",fileTypes=[('database','*.sqlite')],asFile=False,parent="Init_Form")
            createTable(dbloc,main)
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
    main.addListBox("Holdings", ["BTC: £500", "LTC: £200", "VTC: £100"],1,1,2,4)
    ### END OF MAIN FORM LAYOUT ###
    
    ### START ADD SUBWINDOW ###
    main.startSubWindow("Add_Form","Add a new transaction",modal=True)
    global up_coin, up_val
    
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
    global edit_coin,edit_no_coin
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
    
def createTable(dbloc,main):
    db = sqlite3.connect(dbloc)
    c = db.cursor()
    print(dbloc)

    c.execute("CREATE TABLE if not exists coins (coin varchar(10) not null, price float not null, holdings float not null, holdings_value float not null)")
    #c.execute("CREATE TABLE if not exists coins (coin varchar(10) not null, price float, holdings float, holdings_value float)")
    c.execute("insert into coins (coin,price,holdings,holdings_value) values('Bitcoin','0','0','0');")
    c.execute("insert into coins (coin,price,holdings,holdings_value) values('Litecoin','0','0','0');")
    c.execute("insert into coins (coin,price,holdings,holdings_value) values('Vertcoin','0','0','0');")

    db.commit()
    
    sql = "select * from coins"
    recs = c.execute(sql)
    #Clear listbox
    main.clearListBox("Holdings")
    #Loop through all items and add to box
    for row in recs:
        fcoin = row[0]
        fprice = row[1]
        fholdings = row[2]
        fvalue= row[3]
        #print(row[0] + "\nCurrent Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + str(row[3]))
        main.addListItem("Holdings",(str(row[0]) + "\n Current Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + str(row[3])))
    
#Must import gui object
def readTable(dbloc,main):
    db = sqlite3.connect(dbloc)
    c = db.cursor()
    print(dbloc)

    sql = "select * from coins"
    recs = c.execute(sql)
    #Clear listbox
    main.clearListBox("Holdings")
    #Loop through all items and add to box
    i = 0
    for row in recs:
        fcoin = row[0]
        fprice = row[1]
        fholdings = row[2]
        fvalue= row[3]
        
        #main.addListItem("Holdings",(str(row[0]) + "\n Current Price scrapeCoin(i,dbloc)) +\nHoldings " + str(row[2]) + "\nHoldings value ")) #+ str(calcVal(i,dbloc)
        i = i+ 1

        #print(row[0] + "\nCurrent Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + str(row[3]))
        main.addListItem("Holdings",(str(row[0]) + "\n Current Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + str(row[3])))
    
def insert(coin,amount,dbloc,main):
    #Insert into table
    db = sqlite3.connect(dbloc)
    c = db.cursor()
    sql = ("update coins set holdings = (holdings + " +  str(amount) + ") where coin = '" + coin + "';")
    c.execute(sql)
    db.commit()

    sql = "select * from coins"
    recs = c.execute(sql)
    #Clear listbox
    main.clearListBox("Holdings")
    #Loop through all items and add to box
    for row in recs:
        fcoin = row[0]
        fprice = row[1]
        fholdings = row[2]
        fvalue= row[3]
        #print(row[0] + "\nCurrent Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + str(row[3]))
        main.addListItem("Holdings",(str(row[0]) + "\n :Current Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + str(row[3])))

def edit(coin,amount,dbloc,main):
    #Edit table
    db = sqlite3.connect(dbloc)
    c = db.cursor()
    sql = ("update coins set holdings = (" + str(amount) + ") where coin = '" + coin + "';")
    c.execute(sql)
    db.commit()

    #Just for testing
    sql = "select * from coins"
    recs = c.execute(sql)
    main.clearListBox("Holdings")
    for row in recs:
        fcoin = row[0]
        fprice = row[1]
        fholdings = row[2]
        fvalue= row[3]
        main.addListItem("Holdings",(str(row[0]) + " Current Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + str(row[3])))

"""def scrapeCoin(index,dbloc):
    coinmarketcap = Market()
    bitcoin = coinmarketcap.ticker("bitcoin")
    litecoin = coinmarketcap.ticker("litecoin")
    vertcoin = coinmarketcap.ticker("vertcoin")
    btcout = bitcoin[0]   
    ltcout = litecoin[0]
    vtcout = vertcoin[0]
    
    db = sqlite3.connect(dbloc)
    c = db.cursor()

    coins = ["'Bitcoin'","'Litecoin'","'Vertcoin'"]
        
    outArr = []
    coinDict = {"Bitcoin":0, "Litecoin":0, "Vertcoin":0}
        
    if index == 0:
        coinDict["'Bitcoin'"] = btcout["price_usd"]
        #valArr.append(coinArr[0] * float(holdings[0]))
    elif index == 1:
        coinDict["'Litecoin'"] = ltcout["price_usd"]
        #valArr.append(coinArr[1] * float(holdings[1]))
    elif index == 2:
        coinDict["'Vertcoin'"] = vtcout["price_usd"]
        #valArr.append(coinArr[2] * float(holdings[2]))
                          
    return coinDict[coins[index]]"""

main()
