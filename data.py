#! -*- coding: utf8 -*-

import errors
import copy
import json
import uuid
import redis

class DataFactory:
    def create(self, store_type, url):
        if store_type == "local":
            return LocalJsonStorage(url)

# For debuging and testing locallly

class LocalStorage:
    def __init__(self, url=None):
        self.url = url
        self.data = {}
        if url != None:
            self.loadSubscriptions(url)
        else:
            self.url = "./"

    # Internal methods

    def loadSubscriptions(self, url):
        for subscription in os.listdir(url):
            if not subscription.endswith(".dat"):
                continue
            try:
                data = json.load(open(subscription))
                self.data[subscription] = data
            except:
                continue

    def saveSubscription(self, subscription):
        fp = open(self.url + "/" + subscription + ".dat", "w")
        json.dump(self.data[subscription], fp)
        return True

    def checkSubscriptionExists(self, subscription):
        return subscription in self.data.keys()

    def checkProjectExists(self, subscription, project):
        return self.checkSubscriptionExists(subscription) and project in self.data[subscription].keys()

    def checkEntityExists(self, subscription, project, entityId):
        return self.checkProjectExists(subscription, project) and entityId in self.data[subscription][project]["entity"]

    def checkCheckPointExists(self, subscription, project, checkPointId):
        return self.checkProjectExists(subscription, project) and checkPointId in self.data[subscription][project]["checkpoint"]

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
            "entity" : copy.deepcopy(project["entity"]),
            "logs" : {},
            "balance" : copy.deepcopy(project["entity"]),
        }

    def newCheckPointFromCheckPoint(self, previousCheckPoint):
        return {
            "entity" : copy.deepcopy(previousCheckPoint["balance"]),
            "logs" : [],
            "balance" : copy.deepcopy(previousCheckPoint["balance"]),
        }

    # Internal methods end

    def createSubscription(self, subscription):
        if self.checkSubscriptionExists(subscription):
            return False

        self.data[subscription] = {}
        self.saveSubscription(subscription)
        return True

    def createProject(self, subscription, project):
        if self.checkProjectExists(subscription, project):
            return False

        self.data[subscription][project] = self.newProject()
        return True

    def addEntity(self, subscription, project, entityId, displayName, currency, amount, entityRemark):
        if self.checkEntityExists(subscription, project, entityId):
            return False

        self.data[subscription][project]["entity"][entityId] = self.newEntity(entityId, displayName, currency, amount, entityRemark)
        return True

    def addCheckPoint(self, subscription, project, checkPointId, previousCheckPoint = None):
        if self.checkCheckPointExists(subscription, project, checkPointId):
            return False

        if previousCheckPoint == None:
            self.data[subscription][project]["checkpoint"][checkPointId] = self.newCheckPointFromBase(self.data[subscription][project])
        else:
            self.data[subscription][project]["checkpoint"][checkPointId] = self.newCheckPointFromCheckPoint(previousCheckPoint)
        return True

    def addLog(self, subscription, project, checkPointId, _from, to, count, tag, remark):
        if not self.checkCheckPointExists(subscription, project, checkPointId):
            return False
        logId = str(uuid.uuid4())
        self.data[subscription][project]["checkpoint"][checkPointId]["balance"][_from]["amount"] -= count;
        self.data[subscription][project]["checkpoint"][checkPointId]["balance"][to]["amount"] += count;
        self.data[subscription][project]["checkpoint"][checkPointId]["logs"][logId] = {
            "from" : _from,
            "to" : to,
            "count" : count,
            "tag" : tag,
            "remark" : remark
        }

        return True

class LocalJsonStorage:
    def __init__(self, url=None):
        self.url = url
        self.r = redis.Redis(unix_socket_path = self.url)

    def projectPath(self, projectId):
        return '/projects/%s.json' % projectId

    def entityPath(self, projectId, entityId):
        return '/projects/%s/entities/%s.json' % (projectId, entityId)

    def logPath(self, projectId, logId):
        return '/projects/%s/logs/%s.json' % (projectId, logId)

    def checkProjectExistence(self, projectId):
        if self.r.exists(self.projectPath(projectId)):
            return True
        return False

    def checkEntityExistence(self, projectId, entityId):
        if self.r.exists(self.entityPath(projectId, entityId)):
            return True
        return False

    def checkLogExistence(self, projectId, logId):
        if self.r.exists(self.logPath(projectId, logId)):
            return True
        return False

    def SetProject(self, projectId, projectInfo):
        self.r.set(self.projectPath(projectId), projectInfo)

    def SetEntity(self, projectId, entityId, entityInfo):
        self.r.set(self.entityPath(projectId, entityId), entityInfo)

    def SetLog(self, projectId, logId, logInfo):
        self.r.set(self.logPath(projectId, logId), logInfo)

    def CreateProject(self, projectId, displayName, remark):
        if self.checkProjectExistence(projectId):
            return errors.EntityAlreadyExists

        self.SetProject(projectId, {
            "ProjectId"     : projectId,
            "DisplayName"   : displayName,
            "Remark"        : remark,
        })

    def CreateEntity(self, projectId, entityId, displayName, currency, balance, remark):
        if not self.checkProjectExistence(projectId):
            return errors.EntityNotExists

        if self.checkEntityExistence(projectId, entityId):
            return errors.EntityAlreadyExists

        self.SetEntity(projectId, entityId, {
            "EntityId"      : entityId,
            "DisplayName"   : displayName,
            "Currency"      : currency,
            "Balance"       : balance,
            "Remark"        : remark,
        })

    def CreateLog(self, projectId, logId, entityOut, entityIn, amount, tag, remark):
        if not self.checkProjectExistence(projectId):
            return errors.EntityNotExists

        if not self.checkEntityExistence(projectId, entityOut):
            return errors.EntityNotExists

        if not self.checkEntityExistence(projectId, entityIn):
            return errors.EntityNotExists

        self.SetLog(projectId, logId, {
            "From"      : entityOut,
            "To"        : entityIn,
            "Amount"    : amount,
            "Tag"       : tag,
            "Remark"    : remark,
        })

if __name__ == "__main__":
    a = LocalJsonStorage('/tmp/easymemo2.redis.sock')
    a.CreateProject('adfal', "hahah", 'reare')
    a.CreateEntity('adfal', "eid3", "hahah", 'reare', 11, 11)
    a.CreateEntity('adfal', "eid2", "hahah", 'reare', 11, 11)
    a.CreateLog('adfal', "lid1", "eid3", "eid2", "hahah", 'reare', 11)
