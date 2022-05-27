import json
import csv

#Create all the files csv files to json files with the same name

#Create a list of strings from year_5710 to 5751
year_list = [
    'year_5710',
    'year_5711',
    'year_5712',
    'year_5713',
    'year_5714',
    'year_5715',
    'year_5716',
    'year_5717',
    'year_5718',
    'year_5719',
    'year_5720',
    'year_5721',
    'year_5722',
    'year_5723',
    'year_5724',
    'year_5725',
    'year_5726',
    'year_5727',
    'year_5728',
    'year_5729',
    'year_5730',
    'year_5731',
    'year_5732',
    'year_5733',
    'year_5734',
    'year_5735',
    'year_5736',
    'year_5737',
    'year_5738',
    'year_5739',
    'year_5740',
    'year_5741',
    'year_5742',
    'year_5743',
    'year_5744',
    'year_5745',
    'year_5746',
    'year_5747',
    'year_5748',
    'year_5749',
    'year_5750',
    'year_5751'
]

#Create json files without using panda

csvfile = open('year_5711.csv','r')
jsonfile = open('json/file.json','w')

reader = csv.DictReader(csvfile, skipinitialspace=True)
jsonfile.write(json.dumps(list(reader), ensure_ascii=False))
