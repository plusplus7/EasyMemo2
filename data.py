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

    def userPath(self, userId):
        return '/users/%s' % (userId, )

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

    def checkUserExistence(self, userId):
        if self.r.exists(self.userPath(userId)):
            return True
        return False

    def SetProject(self, projectId, projectInfo):
        self.r.set(self.projectPath(projectId), projectInfo)

    def SetEntity(self, projectId, entityId, entityInfo):
        self.r.set(self.entityPath(projectId, entityId), entityInfo)

    def SetLog(self, projectId, logId, logInfo):
        self.r.set(self.logPath(projectId, logId), logInfo)

    def SetUser(self, userId, userInfo):
        self.r.set(self.userPath(userId), userInfo)

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

    def CreateUser(self, userId, displayName, secret):

        self.SetUser(userId, {
            "UserId"        : userId,
            "DisplayName"   : displayName,
            "Secret"        : secret,
        })

if __name__ == "__main__":
    a = LocalJsonStorage('/tmp/easymemo2.redis.sock')
    a.CreateProject('adfal', "hahah", 'reare')
    a.CreateEntity('adfal', "eid3", "hahah", 'reare', 11, 11)
    a.CreateEntity('adfal', "eid2", "hahah", 'reare', 11, 11)
    a.CreateLog('adfal', "lid1", "eid3", "eid2", "hahah", 'reare', 11)
