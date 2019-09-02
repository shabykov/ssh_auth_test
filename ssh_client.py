import paramiko


class SSHClient(object):
    def __init__(self):
        self.__client = paramiko.SSHClient()
        self.__client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())

    def connect(self, hostname, username, password=None, pkey=None):
        self.__client.connect(hostname=hostname, username=username, password=password, pkey=pkey)

    def close(self):
        self.__client.close()

    def exec_command(self, cmd):
        return self.__client.exec_command(cmd)
