from config.ConnectorMysql import Connector
from models.controllers.CalendarController import CalendarController


class ToolController:
    def __init__(self):
        self.database = Connector().getDatabase()
        self.cursor = self.database.cursor()

    def saveToolToDatabase(self, tool):

        toolDatabaseObject="INSERT INTO TOOLS(NAME,  \
                           OWNER, PRICE_DAY, PRICE_HALF) \
                            VALUES ('%s','%s','%f','%f')" % \
                           (tool.name,tool.owner,tool.priceDay,tool.priceHalf)
        try:
            self.cursor.execute(toolDatabaseObject)
            self.database.commit()
        except:
            self.database.rollback()
            print("ERROR! while saving a tool to db")


    def deleteToolFromDatabase(self, tool):
        sql="DELETE FROM TOOLS WHERE NAME = '%s'" % (tool.name)
        try:
            self.cursor.execute(sql)
            self.database.commit()
        except:
            self.database.rollback()
            print("ERROR! while deleting tool")

    def findAllTools(self):
        tools=[]
        sql="SELECT * FROM TOOLS"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            from models.ToolModel import Tool
            tool=Tool(row[0],row[1],row[2],row[3])
            tools.append(tool)
        return tools

    def findTool(self, toolName):
        sql = "SELECT * FROM TOOLS WHERE NAME = '%s'" % toolName
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            from models.ToolModel import Tool
            tool = Tool(row[0], row[1], row[2], row[3])
            tool.description=row[4]
        return tool

    def findAllToolsForUser(self, username):
        sql = "SELECT * FROM TOOLS WHERE OWNER = '%s'" % username
        tools=[]
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            from models.ToolModel import Tool
            tool=Tool(row[0],row[1],row[2],row[3])
            tool.description=row[4]
            tools.append(tool)
        return tools

    def findAllToolsHiredByUser(self, username):
        allDates=CalendarController().getAllColumns()
        toolsHired=[]
        for date in allDates:
            sql = "SELECT NAME FROM CALENDAR WHERE `%s` = '%s' OR `%s` = '%s'" % (date,username+ "_HALF",
                                                                                  date,username + "_DAY" )
            self.cursor.execute(sql)
            result=self.cursor.fetchall()
            for row in result:
                toolsHired.append(row[0])
        return list(set(toolsHired))

    def getDescriptionForTool(self, toolName):
        sql="SELECT DESCRIPTION FROM TOOLS WHERE NAME='%s'" % toolName
        self.cursor.execute(sql)
        result=self.cursor.fetchone()
        return str(result[0])

    def setDescriptionForTool(self, toolName,desc):
            sql="""UPDATE TOOLS SET DESCRIPTION='%s' WHERE NAME='%s'""" % (desc,toolName)
            self.cursor.execute(sql)
            self.database.commit()