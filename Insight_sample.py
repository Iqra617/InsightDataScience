"""
Insight data engineering challenge: Consumer complaints
Input: Complaints.csv Link to download: http://files.consumerfinance.gov/ccdb/complaints.csv.zip
Output: report.csv
		Each line in the output file should list the following fields in the following order:
			1 - product (name should be written in all lowercase)
			2 - year
			3 - total number of complaints received for that product and year
			4 - total number of companies receiving at least one complaint for that product and year
			5 - highest percentage (rounded to the nearest whole number) of total complaints filed against one company for that product and year. Use standard rounding conventions (i.e., Any percentage between 0.5% and 1%, inclusive, should round to 1% and anything less than 0.5% should round to 0%)
"""

#Import useful libraries
import csv
import math
import os
from collections import defaultdict, OrderedDict
from operator import itemgetter
import time


class Insight:

	#constructor
	def __init__(self):
		# self.start = time.time()  #uncomment this to calculate the timing of execution of whole program.
		self.main()
		# print(time.time() - self.start)

	def read_csv(self, reader):
		for index, row in enumerate(reader):
			yield index, row

	#function to calculate the answers
	def calculation(self, header, d):
		#open reports.csv file to write the answer columns 
		with open('report.csv','w', newline = '') as file:
			csv_writer = csv.writer(file)
			csv_writer.writerow(header)
			res = list()
			for years in d:

				#create default dictionary to store the answers in list format as dict_.
				#create nested default dictionary to calculate the company operations as company_dict.
				dict_ = defaultdict(lambda: [years,0,0,0])
				company_dict = defaultdict(lambda: defaultdict(lambda: 0))

				for line in d[years]:
					product_ = line[0]
					company_ = line[1]

					###3 answer(column: Total Complaints): number of total complaints for that product for that year
					dict_[product_][1] += 1

					###4 answer(column: Total Companies(complaints)): number of companies receiving that complaint at least one time. 
					company_dict[company_][product_] += 1
					if company_dict[company_][product_] > 1:
						dict_[product_][2] += 1

				#5 answer(column: Percentage): To calculate the highest percentage
				for product in dict_:
					var_ = 0
					total_count = dict_[product][1]

					for companies in company_dict:
						total_company = company_dict[companies][product]
						var_ = max(total_company, var_)

					final_percentage = math.ceil((var_/total_count)*100)
					dict_[product][3] = final_percentage

				for product in dict_:
					res.append([product.lower(), dict_[product][0], dict_[product][1], dict_[product][2], dict_[product][3]])

			#sort the csv file based on product(alphabetically) and year(ascending) order
			res = sorted(res, key = itemgetter(0, 1))
			for val in res:
					csv_writer.writerow(val) 	#write asnwer as rows in report.csv


	#function to read csv file
	def main(self):
		d = defaultdict(list) 	
		file = open('complaints.csv', 'r', newline = '', encoding = "utf8") 	#open csv file in reading mode.
		reader = csv.reader(file, delimiter = ',', quotechar = '"') 	#use delimeter and quotechar to read comma seperated file.
		for index, data in self.read_csv(reader):
			if index == 0:
				header = [data[1], data[0], "Total Complaints", "Total Companies(complaints)", "Percentage"]
				continue
			year = data[0].split("/")[-1] 	#return only year from column "Date received"
			d[year].append([data[1], data[7]]) 	#make dictionary of lists with column ["Date received", "Prodcut", "Company"]
		
		self.calculation(header, d)


if __name__ == "__main__":
	I = Insight()

######################################### Few suggestions ###############################################################
'''
--> You can write your exception case. eg. Proper format of data, File io, Calculation exceptions. 
--> You can write your own test cases. eg. You can copy the field again and again and then check the timings of the code. Check if the code is scalable or not. 
--> Make sure to read all the instructions from the README.md

total rows:1 million rows

test cases: increase data,2 million....3 million
'''
