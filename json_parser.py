
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Creates dictionary containing users
"""
def createUsers(data, userIds):
    users = open('user.dat', 'a')
    # add seller
    if data['Seller']['UserID'] not in userIds:
        ID = data['Seller']['UserID']
        rating = data['Seller']['Rating']
        location = data['Location'] if data['Location'] is not None else 'NULL'
        location = location.replace('\"','\"\"')
        country = data['Country'] if data['Country'] is not None else 'NULL'
        country = country.replace('\"','\"\"')
        userIds.append(ID)
        users.write(ID+"|"+rating+'|"'+location+'"|"'+country+'"\n')
    
    # add buyer
    if data['Bids']!=None:
        for b in data['Bids']:
            if b['Bid']['Bidder']['UserID'] not in userIds:
                ID = b['Bid']['Bidder']['UserID']
                rating = b['Bid']['Bidder']['Rating']
                location = b['Bid']['Bidder']['Location'] if 'Location' in b['Bid']['Bidder'] else 'NULL'
                location = location.replace('\"','\"\"')
                country = b['Bid']['Bidder']['Country'] if 'Country' in b['Bid']['Bidder'] else 'NULL'
                country = country.replace('\"','\"\"')
                userIds.append(ID)
                users.write(ID+"|"+rating+'|"'+location+'"|"'+country+'"\n')
    users.close()

"""
Creates dictionary containing item categories
"""
def createCategories(itemID, categories):
    category = open ('category.dat', 'a')
    for c in categories:
        category.write(itemID+"|"+c+"\n")
    category.close()

"""
Creates Item dat file
"""
def createItems(item):
    items = open ('item.dat', 'a')
    itemID = item['ItemID']
    name = item['Name'] if item['Name'] is not None else 'NULL'
    name = name.replace('\"','\"\"')
    description = item['Description'] if item['Description'] is not None else 'NULL'
    description = description.replace('\"','\"\"')
    seller = item['Seller']['UserID']
    started = transformDttm(item['Started']) if item['Started'] is not None else 'NULL'
    ends = transformDttm(item['Ends']) if item['Ends'] is not None else 'NULL'
    currently = transformDollar(item['Currently']) if item['Currently'] is not None else 'NULL'
    buy_price = transformDollar(item['Buy_Price']) if 'Buy_Price' in item else 'NULL'
    first_bid = transformDollar(item['First_Bid']) if item['First_Bid'] is not None else 'NULL'
    numBids = item['Number_of_Bids'] if item['Number_of_Bids'] is not None else 'NULL'
    items.write(itemID+'|"'+name+'"|"'+description+'"|'+seller+"|"+started+"|"+ends+"|"+currently+"|"+buy_price+"|"+first_bid+"|"+numBids+"\n")
    items.close()
    
"""
Creates Bid dat file
"""
def createBids(item):
    bids = open ('bid.dat', 'a')
    itemID = item['ItemID']
    if item['Bids'] is not None:
        for b in item['Bids']:
            time = transformDttm(b['Bid']['Time'])
            amount = transformDollar(b['Bid']['Amount'])
            userID = b['Bid']['Bidder']['UserID']
            bids.write(itemID+"|"+userID+"|"+time+"|"+amount+"\n")
    bids.close()

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file, userIds):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
       
        # first=json_file.find("-")
        # second=json_file.find(".")
        # num = json_file[first+1:second] # get the string between two delimiters
        # categoryName = 'category'+num+'.dat'
        # userName = 'user'+num+'.dat'
        # bidName = 'bid'+num+'.dat'
        # itemName = 'item'+num+'.dat'

    #    remove duplicate tuples
        itemIds = []
        
        for item in items:
            if item['ItemID'] in itemIds:
                items.remove(item)
                continue
            else:
                itemIds.append(item['ItemID'])

        
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            createCategories(item['ItemID'], item['Category'])
            createUsers(item, userIds)
            createItems(item)
            createBids(item)
            pass

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    userIds = []
    for f in argv[1:]:
        if isJson(f):
            parseJson(f, userIds)
            print ("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
