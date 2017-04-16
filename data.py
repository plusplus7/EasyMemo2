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

    def AttachProjectToUser(self, projectId, userId):
        if not self.checkProjectExistence(projectId):
            return errors.EntityNotExists

        if not self.checkUserExistence(userId):
            return errors.EntityNotExists
        project = self.getProject(projectId)
        user = self.getUser(userId)
        user["Projects"].append({
            "ProjectId" : project["ProjectId"],
            "ProjectName" : project["DisplayName"]
        })
        self.setUser(userId, user)

    def getProject(self, projectId):
        return json.loads(str(self.r.get(self.projectPath(projectId))))

    def setProject(self, projectId, projectInfo):
        self.r.set(self.projectPath(projectId), json.dumps(projectInfo))

    def SetEntity(self, projectId, entityId, entityInfo):
        self.r.set(self.entityPath(projectId, entityId), json.dumps(entityInfo))

    def setLog(self, projectId, logId, logInfo):
        self.r.set(self.logPath(projectId, logId), json.dumps(logInfo))

    def setUser(self, userId, userInfo):
        self.r.set(self.userPath(userId), json.dumps(userInfo))

    def getUser(self, userId):
        return json.loads(str(self.r.get(self.userPath(userId))))

    def getEntity(self, project, entityId):
        return json.loads(str(self.r.get(self.entityPath(projectId, entityId))))

    def CreateProject(self, projectId, displayName, remark):
        if self.checkProjectExistence(projectId):
            return errors.EntityAlreadyExists

        self.setProject(projectId, {
            "ProjectId"     : projectId,
            "DisplayName"   : displayName,
            "Remark"        : remark,
        })

    def QueryEntity(self, projectId, entityId):
        if not self.checkProjectExistence(projectId):
            return errors.EntityNotExists

        if self.checkEntityExistence(projectId, entityId):
            return errors.EntityAlreadyExists

        return self.getEntity(projectId, entityId)

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

        self.setLog(projectId, logId, {
            "From"      : entityOut,
            "To"        : entityIn,
            "Amount"    : amount,
            "Tag"       : tag,
            "Remark"    : remark,
        })

    def CreateUser(self, userId, displayName, secret):
        if self.checkUserExistence(userId):
            return errors.EntityAlreadyExists

        self.setUser(userId, {
            "UserId"        : userId,
            "DisplayName"   : displayName,
            "Projects"      : [],
            "Secret"        : secret,
        })

    def QueryUser(self, userId):
        if not self.checkUserExistence(userId):
            return errors.EntityNotExists

        return self.getUser(userId)

if __name__ == "__main__":
    a = LocalJsonStorage('/tmp/easymemo2.redis.sock')
    a.CreateProject('adfal', "hahah", 'reare')
    a.CreateEntity('adfal', "eid3", "hahah", 'reare', 11, 11)
    a.CreateEntity('adfal', "eid2", "hahah", 'reare', 11, 11)
    a.CreateLog('adfal', "lid1", "eid3", "eid2", "hahah", 'reare', 11)
