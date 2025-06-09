
from  Helper.ConfigHelper import Configer

# 在这个里面完全可以定义一个加密方法，用于允许前端用户对图片数据等等的访问和上传
class Crypter():
    def  __init__(self) -> None:  
        self.configer = Configer()
        self.crypt_key = self.configer.get_config_value('Crypt_Key') # 加密的key
        self.crypt_salt = self.configer.get_config_value('Crypt_Salt') # 加密盐
        
    def encrypt(self):
        # 加密方法
        
        pass


    def decrypt(self):
        # 解密方法
        
        pass