import pandas
import unittest
import random
from Databases import Transaction_database
import pandas as pd
import datetime


class Database_Tests(unittest.TestCase):
    def _get_date_between(self,year1,month1,day1,year2,month2,day2):
        r_year = random.randint(year1,year2)
        r_month = random.randint(month1,month2)
        r_day = random.randint(day1,day2)
        return self._format_date(r_year,r_month,r_day)

    def _format_date(self,year,month,day) -> str:
        if month > 0 and month < 10:
            month = "0" + str(month)
        return f"{year}-{month}-{day}"


    def test_different_days(self):
        f1 = Fake_data()
        #add relevant data
        for x in range(10):
            f1.addTransactions("category1",self._get_date_between(2000,1,1,2000,1,31),50)
        f1.addTransactions("category2",self._get_date_between(2000,1,1,2000,1,31),1)

        df = f1.getdf()
        db = Transaction_database("rountine_tests",verbose = False, drop_zero_sum = False)
        db.add_database(df)

        db.process_data_by_time(1,2000,1)

        db.getDF()
        dict = db.getDF()
        print(dict)
        print(dict["category1"][0])
        print(dict.keys())
        self.assertEqual(500,dict["category1"][0])

        



class Fake_data:
    def __init__(self):
        self.dict = {"Trans_Date":[], "Label":[], "Net-Amount":[]}

    #include date as string in YYYY-MM-DD 
    def addTransactions(self,category:str,date:str,ammount:int):
        if not category:
            raise ValueError("Category cannot be empty")
        
        #should throw an error if not in the right format
        #check_date = datetime.datetime.strftime(date,'%Y-%m-%d')
        
        #add transaction to the dictionary
        self.dict["Trans_Date"].append(date)
        self.dict["Label"].append(category)
        self.dict["Net-Amount"].append(ammount)


    def getdf(self):
        df = pd.DataFrame.from_dict(self.dict)
        return df


if __name__ == '__main__':
    unittest.main()
