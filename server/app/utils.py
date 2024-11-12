
from datetime import *
from dateutil.relativedelta import relativedelta


def getYearlyExpirationTime():
    date = datetime.now()
    newDate = date + relativedelta(years=1)
    return newDate

def getHourlyExpirationTime():
    date = datetime.now()
    newDate = date + relativedelta(hours=1)
    return newDate

