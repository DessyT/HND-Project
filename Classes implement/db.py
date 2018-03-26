#Generic class to connect to DB
from appJar import gui
import sqlite3
import string
from coinmarketcap import Market

class DB:
    def __init__(self,dbloc):
        self.db = sqlite3.connect(dbloc)
        self.c = self.db.cursor()
            
    def createTable(self,dbloc,main):
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
        counter = 0
        for row in recs:
            fcoin = row[0]
            fprice = row[1]
            fholdings = row[2]
            fvalue= row[3]
            main.addListItem("Holdings",(str(row[0]) + "\n Current Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + self.scrapeCoin(counter,dbloc)))
            counter = counter + 1

        db.close()
        
    def readTable(self,dbloc,main):
        db = sqlite3.connect(dbloc)
        c = db.cursor()
        print(dbloc)

        sql = "select * from coins"
        recs = c.execute(sql)
        #Clear listbox
        main.clearListBox("Holdings")
        #Loop through all items and add to box
        counter = 0
        for row in recs:
            fcoin = row[0]
            fprice = row[1]
            fholdings = row[2]
            fvalue= row[3]
            
            main.addListItem("Holdings",(str(row[0]) + "\n Current Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + self.scrapeCoin(counter,dbloc)))
            counter = counter + 1
            
        db.close()
        
    def insert(self,coin,amount,dbloc,main):
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
        counter = 0
        for row in recs:
            fcoin = row[0]
            fprice = row[1]
            fholdings = row[2]
            fvalue= row[3]
            main.addListItem("Holdings",(str(row[0]) + "\n Current Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + self.scrapeCoin(counter,dbloc)))
            counter = counter + 1
            
        db.close()
        
    def edit(self,coin,amount,dbloc,main):
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
        counter = 0
        for row in recs:
            fcoin = row[0]
            fprice = row[1]
            fholdings = row[2]
            fvalue= row[3]
            main.addListItem("Holdings",(str(row[0]) + " Current Price " + str(row[1]) + "\nHoldings " + str(row[2]) + "\nHoldings value " + self.scrapeCoin(counter,dbloc)))
            counter = counter + 1
        db.close()
        
    def scrapeCoin(self,index,dbloc):
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
        coinDict = {"Bitcoin":0, "Litecoin":0, "Vertcoin":0}
            
        if index == 0:
            coinDict["'Bitcoin'"] = btcout["price_usd"]
            #valArr.append(btcout * float(holdings[0]))
        elif index == 1:
            coinDict["'Litecoin'"] = ltcout["price_usd"]
            #valArr.append(ltcout * float(holdings[1]))
        elif index == 2:
            coinDict["'Vertcoin'"] = vtcout["price_usd"]
            #valArr.append(vtcout * float(holdings[2]))
                              
        return coinDict[coins[index]]
        db.close()
