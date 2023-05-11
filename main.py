# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import calendar
from datetime import datetime, timedelta


def readTxtFile():
    filename = 'AAPL_Daily_test.csv'

    with open(filename, 'r') as data:
        monthTracker = 0
        finalStockDataDict = {}
        adjCloseOfDayPrior = 0.0
        lastDayOfMonthObj = None
        lastDayOfMonthAdjClose = 0.0
        firstDayofThePriorMonth = None
        months ={1 : "January", 2: "February", 3: "March", 4: "April", 5:"May", 6: "June",
                 7:"July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

        for line in csv.DictReader(data):
            date_str = line.get('date')
            adjClose = float(line.get('adjClose'))
           # print(adjClose)
            # print("Current working day:", date_str)
            firstDayOfMonthObj = makeDateintoDTO(date_str)

            if lastDayOfMonthObj == None:
                lastDayOfMonthObj = firstDayOfMonthObj
                adjCloseOfDayPrior = adjClose
                firstDayofThePriorMonth = firstDayOfMonthObj
                lastDayOfMonthAdjClose = adjClose



            if firstDayOfMonthObj.month != monthTracker: #when we get to this line, we are on the first day of next month. which means we should have last day saved.
                #print ("first day of the prior month" , firstDayofThePriorMonth)
                finalStockDataDict[lastDayOfMonthObj] = adjCloseOfDayPrior
                finalStockDataDict[firstDayOfMonthObj] = adjClose
                monthTracker = firstDayOfMonthObj.month
                #print ("formula should be: ", firstDayofThePriorMonth, " ", finalStockDataDict[firstDayofThePriorMonth], lastDayOfMonthObj ,
                 #      " - ", lastDayOfMonthAdjClose , " / ", finalStockDataDict[firstDayofThePriorMonth])
                finalAdjustedClose = (finalStockDataDict[firstDayofThePriorMonth] - lastDayOfMonthAdjClose) / finalStockDataDict[firstDayofThePriorMonth]

                print("Return for", months[firstDayofThePriorMonth.month], firstDayofThePriorMonth.year, "is", round(finalAdjustedClose,2), "%")
                firstDayofThePriorMonth = firstDayOfMonthObj
                monthTracker = firstDayOfMonthObj.month
              #  print (firstDayOfMonthObj.month, " adj close is: ", (adjClose - lastDayOfMonthAdjClose)/adjClose)
            else:
                adjCloseOfDayPrior = adjClose
                lastDayOfMonthObj = firstDayOfMonthObj

            lastDayOfMonthAdjClose = adjClose

def isDayFirstDay(currentDTOObject):
    if currentDTOObject.day == 1:
        return True
    else:
        return False


def makeDateintoDTO(dateString):
    date_format = '%Y-%m-%d'
    currentDTObject = datetime.strptime(dateString, date_format)
    return currentDTObject


def GetLastDay(currentDTObject):
    # give it DTO and returns last day
    next_month = currentDTObject.replace(day=28) + timedelta(days=4)
    res = next_month - timedelta(days=next_month.day)
    lastDayOfMonth = res.date()
    return lastDayOfMonth


readTxtFile()