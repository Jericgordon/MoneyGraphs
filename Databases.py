import pandas as pd
import datetime
import math #for floor calculations in level()
import statistics #for level()
from datetime import datetime as dt
from datetime import date
from dateutil.relativedelta import relativedelta
import os

import copy 


class Transaction_database:
	def __init__(self,package_name:str,**kwargs):
		self._original_data = None #Seperates out the original data without processing
		self.df = None #Edited data, somtimes with dropped or renamed objects
		self.drop_zero_sum = True # Drop all categories with a zero sum from the graph
		self.remove_categories_list = []#Drop the categories specified in the 'remove_categories list'
		self.remove_categories_bool = False
		self.rename_categories_dict = {}
		self.rename_categories_bool = False
		self.level_categories_list = []
		self.level_categories_list_bool = False
		self.drop_zero_sum = kwargs["drop_zero_zum"] #default should be true
		self.verbose = kwargs["verbose"]
		self.package_name = package_name
		
	 # specifies the timeframe for the graph in months (multiplied by 12 for 12 months in a year)
	
	def level_categories(self,catories_to_level:list):
		self.level_categories_list = catories_to_level
		self.level_categories_list_bool = True

	def rename_categories(self,rename_dictionary:dict):
		self.rename_categories_dict = self._reformat_dict(rename_dictionary)
		self.rename_categories_bool = True

	def remove_categories(self,to_remove_list):
		self.remove_categories_list = to_remove_list
		self.remove_categories_bool = True

	def add_database(self,dataframe) -> None:
		if self._original_data is None:
			self._original_data = dataframe
		else:
			self._original_data = pd.concat([self._original_data,dataframe])
		self._saveData()

	#Internal save function that provides a backup of original data.
	def _saveData(self) -> None:
		self._original_data.to_csv(f"./Graphing_Data/{self.package_name}_Latest_Graph.csv",index=False)
	
	#for manual saves
	def saveData(self,path,fileName) -> None:
		if fileName == "Latest_Graph": #prevent user from overwriting default saves
			raise NameError("That name is reserved for this class")
		
		if self.df is None: #if no data is processesed, save the data
			raise InterruptedError("No data to save, please process")
		self.df.to_csv(f"{path}{self.package_name}_{fileName}.csv")

	#internal function to aid in renaming categories
	def _add_arrays(self,array1:list,array2:list) -> list:
		if (len(array1) != len(array2)):
			raise Exception("Cannot add array lists of differnt lengths")
		
		for index in range(len(array1) -1):
			array1[index] = array1[index] + array2[index]

		return array1
			

	def _rename_categories(self,dict_to_modify) -> dict:
		print("------Renaming categories------")
		if not (self.rename_categories_bool):
			return dict_to_modify
		
		dict_copy_for_iteration = copy.deepcopy(dict_to_modify)
		#merge categories together based on renaming protocol
		for key in dict_copy_for_iteration.keys():
			if key in self.rename_categories_dict.keys(): 
				new_key = self.rename_categories_dict[key]
				if new_key in dict_to_modify.keys():
					dict_to_modify[new_key] = self._add_arrays(dict_to_modify[new_key],dict_to_modify[key])
					dict_to_modify.pop(key)

				if new_key not in dict_to_modify.keys():
					dict_to_modify[new_key] = dict_to_modify[key]
					dict_to_modify.pop(key)
				print(f"renamed {key} to {new_key}")

		print("------Renaming categories completed------")
		return dict_to_modify

	def _reformat_dict(self,dictionary:dict):
		return_dict = {}
		for key,value in dictionary.items():
			for item in value:
				return_dict[item] = key
		return return_dict
	
	def _remove_categories(self,dict_to_modify) -> dict:
		if not self.remove_categories_bool:
			return dict_to_modify

		for category in self.remove_categories_list:
				try:
					dict_to_modify.pop(category)
					print(f"Removed {category}")
				except KeyError:
					print(f"Could not find {category} to remove")
		
		return dict_to_modify
	
	def _drop_zero_sum(self,dict_to_modify) -> dict:
		if not self.drop_zero_sum:
			return dict_to_modify
		
		print("------Dropping Zero sum categories------")
		dict_to_modify_copy = copy.deepcopy(dict_to_modify)
		for key,values in dict_to_modify_copy.items(): #Function Goes through and drops all labels with 0 sum from the graph
			if key != 'Trans_Date' and sum(values) == 0:
				dict_to_modify.pop(key)
				print("Dropped {key} Due to 0 sum".format(key=key))
		print("------Finished Dropping Zero sum categories------")
		return dict_to_modify
	
	def _level_transactions(self,dict_to_modify) -> dict:
		if not self.level_categories_list_bool: #return early if no leveling
			return dict_to_modify
		
		print("------Leveling categories------")
		print(f'level is {self.level_categories_list_bool}')
		dict_to_modify_copy = copy.deepcopy(dict_to_modify)
		for key,values in dict_to_modify_copy.items(): #Function Goes through and drops all labels with 0 sum from the graph
			if self.level_categories_list_bool == True:
				if key in self.level_categories_list:
					monthly_data_for_category = values
					years = math.floor(len(monthly_data_for_category)/12)
					new_list = []
					for times in range(years): # deal with whole year averages
						start_splice = (times * 12) + 0
						end_splice = (times * 12) + 12
						new_average = statistics.mean(monthly_data_for_category[start_splice:end_splice])
						for x in range(12):
							new_list.append(new_average)
					remainder = len(monthly_data_for_category) % 12
					for times in range(remainder):
						new_average = statistics.mean(monthly_data_for_category[(-1 * times):])
						new_list.append(new_average)
					dict_to_modify[key] = new_list
					print('Leveled {key}'.format(key=key))
		print("------Finished Leveling categories------")
		return dict_to_modify


	def process_data_by_time(self) -> None:
		self.df = self._original_data.copy(deep=True) #make a deep copy of the df to modify
		self.df['Trans_Date'] = pd.to_datetime(self.df['Trans_Date'],format="%Y-%m-%d").dt.date #ensure datetime Functionality		

		#Creates the Export Dictionary, and populates it with blank lists, with the labels from the concatinated df
		costs_by_week = {'Trans_Date':[]}
		labels = self.df['Label'].unique()
		for label in labels:
			costs_by_week[label] = []
		
		time_delta = relativedelta(months=+1)
		years = 5 * 12 #Specifies the timeframe for the graph

		print("----- Processing Data-------")

		#Cycles through everything in the df by date range. It records the raw transactions in a csv
		for period in range(years):
			start = datetime.date(2018,7,1) + (time_delta * period)
			end = start + time_delta
			#start = pd.Timestamp(start)
			#end = pd.Timestamp(end)
			print(start,end)
			period_costs = self.df[(self.df['Trans_Date'] > start) & (self.df['Trans_Date'] < end)]

			if self.verbose:
				period_costs.to_csv(f'./Verbose_data/{self.package_name}_data_from_{start}_to_{end}.csv')	

			#With the smaller df for those dates, we append the sum of every category to the export dict for that date range. We also add the start date to the date column for final export
			costs_by_week['Trans_Date'].append(start)
			for label in labels: 
				tempdf = period_costs[(period_costs['Label'] == label)]
				costs_by_week[label].append(tempdf['Net-Amount'].sum())

		self.df = pd.DataFrame.from_dict(costs_by_week) #save df for future transacitons

		costs_by_week = self._rename_categories(costs_by_week) #renames relevant transactions
		costs_by_week = self._remove_categories(costs_by_week) #removes relevant labels
		costs_by_week = self._level_transactions(costs_by_week) #levels categories
		costs_by_week = self._drop_zero_sum(costs_by_week)
		self.df = pd.DataFrame.from_dict(costs_by_week)

	def save_with_Totals(self,path:str) -> None:
		#self.hide()
		row_sum = [] #This block sums up all the columns for labeling purposes
		df_copy = self.df.copy(deep=True)
		try:
			df_copy.set_index('Trans_Date', inplace=True)
		except KeyError:
			print("Tried to set index, but was not able to.")
			print("This may error may be ignored")


		for row in df_copy.index:
			row_sum.append(round(df_copy.loc[row].sum()))

		#Add totals to graph, drop them afterwords
		df_copy['Totals'] = df_copy.sum(axis=1).astype(int)
		
		self.saveData(path,"Data_with_totals")

	def package_data(self,**kwargs) -> None:
		if "package_name" in kwargs.keys() and kwargs["package_name"]: #check if usr entered valid string
			self.package_name = kwargs["package_name"]

		#ensure a file exists to move files to
		if not os.path.exists(f"./{self.package_name}"):
			os.makedirs(f"./{self.package_name}")

		#get a list of verbose files to move
		list_of_verbose_files_to_move = []
		for file in os.listdir("./Verbose_data"):
			if self.package_name in file:
				list_of_verbose_files_to_move.append(file)

		#moveFiles
		for file in list_of_verbose_files_to_move:
			os.rename(f"./Verbose_data/{file}",f"./{self.package_name}/{file}")
		
		#add data file with totals
		self.save_with_Totals(f"./{self.package_name}/{file}")

		

		






	def getDF(self) -> object:
		self.df.set_index('Trans_Date', inplace=True)
		return self.df
	

