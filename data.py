#! -*- coding: utf8 -*-
import uuid

class DataFactory:
    def __init__(self, store_type, url):
        if store_type == "local":
            return LocalStorage(url)

class LocalStorage:
    def __init__(self, url):
        self.url = url
        self.data = {}

    def checkProjectExists(self, project):
        return project in self.data.keys()

    def checkEntityExists(self, project, entityId):
        return self.checkProjectExists(project) and entityId in self.data[project]["entity"]

    def checkCheckPointExists(self, project, checkPointId):
        print self.checkProjectExists(project)
        print checkPointId in self.data[project]["checkpoint"]
        return self.checkProjectExists(project) and checkPointId in self.data[project]["checkpoint"]

    def newProject(self):
        return {
            "entity" : {},
            "checkpoint" : {}
        }

    def newEntity(self, entityId, displayName, currency, amount, remark):
        return {
            "entityId"    : entityId,
            "displayName"   : displayName,
            "currency"      : currency,
            "amount"        : amount,
            "remark"        : remark,
        }

    def newCheckPointFromBase(self, project):
        return {
            "entity" : project["entity"],
            "logs" : {},
            "balance" : project["entity"],
        }

    def newCheckPointFromCheckPoint(self, previousCheckPoint):
        return {
            "entity" : previousCheckPoint["balance"],
            "logs" : [],
            "balance" : previousCheckPoint["balance"],
        }

    def createProject(self, project):
        if self.checkProjectExists(project):
            return False

        self.data[project] = self.newProject()
        return True

    def addEntity(self, project, entityId, displayName, currency, amount, entityRemark):
        if self.checkEntityExists(project, entityId):
            return False

        self.data[project]["entity"][entityId] = self.newEntity(entityId, displayName, currency, amount, entityRemark)
        return True

    def addCheckPoint(self, project, checkPointId, previousCheckPoint = None):
        if self.checkCheckPointExists(project, checkPointId):
            return False

        if previousCheckPoint == None:
            self.data[project]["checkpoint"][checkPointId] = self.newCheckPointFromBase(self.data[project])
        else:
            self.data[project]["checkpoint"][checkPointId] = self.newCheckPointFromCheckPoint(previousCheckPoint)
        return True

    def addLog(self, project, checkPointId, _from, to, count, tag, remark):
        print project, checkPointId
        if self.checkCheckPointExists(project, checkPointId) == False:
            return False
        
        logId = str(uuid.uuid4())
        self.data[project]["checkpoint"][checkPointId]["logs"][logId] = {
            "from" : _from,
            "to" : to,
            "count" : count,
            "tag" : tag,
            "remark" : remark
        }
        return True
