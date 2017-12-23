from datetime import datetime, date, time,timedelta
import datetime as dt
from config.ConnectorMysql import Connector


class CalendarController:
    PERIOD=4

    def __init__(self):
        self.database = Connector().getDatabase()
        self.cursor = self.database.cursor()

    def saveToolCalendar(self, tool):
        sql = "INSERT INTO CALENDAR(NAME) VALUES ('%s')" % \
              (tool)
        try:
            self.cursor.execute(sql)
            self.database.commit()

        except:
            self.database.rollback()

    def addDayToTableCalendar(self, day):
        if(day == self.lastDate()):
            print("DATE ALREADY EXIST")
            return
        elif(day < self.lastDate()):
            print("U CAN NOT GO BACK IN TIME")
            return
        sql="ALTER TABLE CALENDAR ADD COLUMN \
          `%s` CHAR(20) NOT NULL DEFAULT 'FREE'" % (day)
        try:
            print(sql)
            self.cursor.execute(sql)
            self.database.commit()
        except:
            self.database.rollback()

    def getAllColumns(self):
        sql = "DESCRIBE CALENDAR"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        tab = []
        for row in result:
            tab.append(row[0])
        tab.remove("NAME")
        return tab

    def lastDate(self):
        tab=self.getAllColumns()
        last=tab[len(tab)-1]
        lastDate=datetime.strptime(last,"%Y-%m-%d").date()
        return lastDate

    def updateCalendar(self):
        tmp=dt.date.today()
        last=self.lastDate()
        dif=(last-tmp).days
        daysToAdd=self.PERIOD-dif-1
        for i in range(0,daysToAdd):
            self.addDayToTableCalendar(last+timedelta(i+1))

    def getCalendarForTool(self, toolName):
        sql="SELECT * FROM CALENDAR WHERE NAME = '%s'" % toolName
        self.cursor.execute(sql)
        result=self.cursor.fetchone()
        types=list(result)
        types.remove(toolName)
        dates=self.getAllColumns()
        mapList={} # DATE : TYPE
        counter=0
        for i in dates:
            mapList[dates[counter]]=(types[counter])
            counter += 1
        return mapList

    #TODO: FINISH IT KIDO
    def bookToolForDate(self, toolName, dateToBook):
        toolCalendar=self.getCalendarForTool(toolName)
        if(toolCalendar[dateToBook] == 'FREE'):
            print("BOOKED")
        else: print("ERR")


