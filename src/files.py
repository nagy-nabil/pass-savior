'''
data form 
{
    'app':{
        'field':'data'
    }
}
'''
from operator import truediv
from cryptography.fernet import Fernet
import json
from os.path import exists

class Files():
    __name="data.json";
    __userName="user.key"
    __keyFile="thekey.key"
    __KEY=None


    @classmethod
    def load(cls):
        if(Files.__KEY):
            try:
                with open(Files.__name, 'rb') as datafile:
                    encrypted=datafile.read()
                decrypted=Files.__decrypt_data(encrypted)
                return decrypted
            except:
                print("no data to load")
                return {}
        else:
            Files.__load_key()
            return Files.load()

    @classmethod
    def store(cls,contents):
        encrypted= Files.__encrypt_data(contents)
        # print(encrypted)
        if(encrypted):
            with open(Files.__name, "wb") as datafile:
                datafile.write(encrypted)
    
    @staticmethod
    def __encrypt_data(contents):
        if (Files.__KEY):
            try:
                json_byte=json.dumps(contents).encode("utf-8")
            except:
                print("error with converting data to json")
                return None
            else:
                encrypted=Fernet(Files.__KEY).encrypt(json_byte)
                # print(encrypted)
                return encrypted
        else:
            print("no key loading one")
            Files.__load_key()
            return Files.__encrypt_data(contents)

    @staticmethod
    def __decrypt_data(contents):
        if(Files.__KEY):
            try:
                decrypted=Fernet(Files.__KEY).decrypt(contents)
                decrypted=json.loads(decrypted)
                return decrypted
            except:
                print("keyerror?")
        else:
            Files.__load_key()
            return Files.__decrypt_data(contents)

    @classmethod
    def __generate_key(cls):
        Files.__KEY=Fernet.generate_key()
        try:
            with open(Files.__keyFile,'wb') as keyfile:
                keyfile.write(Files.__KEY)
        except:
            print("couldn't create key")


    @classmethod
    def __load_key(cls):
        try:
            with open(Files.__keyFile,"rb") as keyfile:
                Files.__KEY=keyfile.read()
        except:
            print("no KEY so we generate new one")
            Files.__generate_key()

    @classmethod
    def store_user(cls,name,password):
        user={
            'name':name,
            'password':password
        }
        encrypted= Files.__encrypt_data(user)
        # print(encrypted)
        if(encrypted):
            with open(Files.__userName, "wb") as datafile:
                datafile.write(encrypted)

    @classmethod
    def __load_user(cls):
        if(Files.__KEY):
            try:
                with open(Files.__userName, 'rb') as datafile:
                    encrypted=datafile.read()
                    decrypted=Files.__decrypt_data(encrypted)
                    return decrypted
            except:
                print("no data to load")
                return {}
        else:
            Files.__load_key()
            return Files.__load_user()
    @classmethod
    def isUserRight(cls,name,password):
        try:
            rightUser=Files.__load_user()
            if(name==rightUser["name"] and password==rightUser["password"]):
                return True;
        except:
            return False
        return False
    @classmethod
    def userExists(cls):
        if exists(Files.__userName):
            return True;
        else:
            return False

if __name__ == "__main__":
    data={
        "facebook": {
            "email": "facbook",
            "password":"fgdfdg",
            "gfd":"ytrye"
        },
        "twitter": {
            "email": "twitter"
        },
        "gmail2": {
            "email2": "gmail",
            "hdg":"htr"
        }
        }
    print(Files.load())
    Files.isUserRight("hdf","hgf")
    # Files.store(data)