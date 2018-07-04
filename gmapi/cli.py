import sys

class CLI():
    def __init__(self, args=None):
        if args == None:
            self.args = sys.argv
        else:
            self.args = args

    def getOrDie(self, key):
        value = self.getOrDefault(key, None)
        if value == None:
            print("Error, '" + key + "' does not exist.")
            sys.exit(1)
        else:
            return value
        
    def getOrDefault(self, key, defaultValue):
        index = self.indexOf(key)
        if index > -1:
            if len(self.args) <= index+1:
                return ""
            else:
                return self.args[index+1]
        else:
            return defaultValue

    def containsKey(self, key):
        return self.indexOf(key) > -1

    def indexOf(self, key):
        if key in self.args:
            return self.args.index(key)
        else:
            return -1

