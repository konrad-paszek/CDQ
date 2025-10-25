import os


class Environment:
    @staticmethod
    def node():
        return os.getenv("CDQ__CORE__NODE")
