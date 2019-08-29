import io

import paramiko


class PrivateKeyReader(object):
    available_pkey_classes = (
        paramiko.rsakey.RSAKey,
        paramiko.dsskey.DSSKey,
        paramiko.ecdsakey.ECDSAKey,
        paramiko.ed25519key.Ed25519Key
    )

    def __init__(self, *args, **kwargs):
        self.__key = None

    def __read_private_key_from_file(self, filename, password):
        for pkey_class in self.available_pkey_classes:
            try:
                self.__key = pkey_class.from_private_key_file(filename, password)
            except paramiko.SSHException as e:
                print("{}".format(e))
            except paramiko.PasswordRequiredException:
                raise paramiko.PasswordRequiredException('Password is requred')

    def __read_private_key(self, pkey_str, password):
        for pkey_class in self.available_pkey_classes:
            try:
                file_obj = io.StringIO(pkey_str)
                self.__key = pkey_class.from_private_key(file_obj, password)
            except paramiko.SSHException as e:
                print("{}".format(e))
            except paramiko.PasswordRequiredException:
                raise paramiko.PasswordRequiredException('Password is requred')
            finally:
                file_obj.close()

    def read(self, filename=None, pkey_str=None, password=None):
        if filename is not None:
            self.__read_private_key_from_file(filename, password)
        if pkey_str is not None:
            self.__read_private_key(pkey_str, password)

        if self.__key is None:
            raise paramiko.SSHException("Incorrect input credentials")

        return self.__key


if __name__ == "__main__":

    VM3_KEY_PASSPHRASE = "P@ssw0rd"
    VM3_KEY_FILE = '/home/shabykivai/.ssh/vm3/id_ecdsa'

    key_reader = PrivateKeyReader()

    key = key_reader.read(filename=VM3_KEY_FILE, password=VM3_KEY_PASSPHRASE)

