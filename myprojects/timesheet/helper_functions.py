from datetime import datetime, timedelta
from django.db import connection

def dategenerator(wedate):
    initial_date = []
    # if type(wedate) is str:
    date = datetime.strptime(wedate, '%Y-%m-%d')
    # else:
        # date = wedate

    for i in range(7):
        date_dict = {}
        modified_date = date + timedelta(days=i-7+1)
        newdate = datetime.strftime(modified_date, '%Y-%m-%d')
        date_dict['workdate']=newdate
        date_dict['workcode']=1
        initial_date.append(date_dict)
    return initial_date

def numbers_to_strings(argument):
    switcher = {
        0: "zero",
        1: "one",
        2: "two",
    }
    return switcher.get(argument, "nothing")

def queryCounter(*args):
    q = len(connection.queries)

    def queryCount():
        return q
        # for x in args:
            # return x
    return queryCount
