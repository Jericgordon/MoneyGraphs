import pandas
import datetime

  #'Trans_Date' 'Label' 'Net-Amount'


class Fake_data:
    def __init__(self):
        self.dict = {"Trans_Date":[], "Label":[], "Net-Amount":[]}

    #include date as string in YYYY-MM-DD 
    def addTransactions(self,category:str,date:str,ammount:int):
        if not category:
            raise ValueError("Category cannot be empty")
        
        
        check_date = datetime.datetime.strftime(date,'%Y-%m-%d')


    
        

        self.dict["Trans_Date"].append(date)
        self.dict["Label"].append(date)
        self.dict["Net-Amount"].append(date)


    def getdf(self):
        return self.df

