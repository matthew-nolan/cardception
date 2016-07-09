class Organization(object):

    def __init__(self, name):
        self.name = name
        self.users = []
        self.teams = []
        self.projects = []


    def getDocument(self):
        document = {
        "name": self.name,
        "users": self.users,
        "teams": self.teams,
        "projects": self.projects
        }

        return document
