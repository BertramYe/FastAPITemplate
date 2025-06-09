from dotenv import load_dotenv
from os import getenv
from typing import Literal,cast  
from settings import DeBug
from pathlib import Path
from .FileHelper import Filer

Config_Keys_Type = Literal[
    'Port',
    'Host',
    'Log_Path',
    'Static_Path',
    'Allow_Host',
    'Allow_Ports',
    'Templates_Path',
    'Crypt_Key',
    'Crypt_Salt'
]

class Configer():
    def __init__(self) -> None:
        self.filer = Filer()
        self._env_path =  self.filer.get_or_create_path('config/.env.develop' if DeBug else "config/.env.production")
        if not Path(self._env_path).exists():
            raise ValueError(f"the env files not existed in path: {self._env_path}!")
        load_dotenv(self._env_path)

    def _check_or_get_default_config_value(self,config_key:Config_Keys_Type) -> str | None:
        default_value = None
        defualt_values_dict = {
            'Log_Path':'Log/app.log',
            'Static_Path':'static',
            'Port':8000,
            'Host':'0.0.0.0',
            'Allow_Host':['localhost'],
            'Allow_Ports':[8000,80,443],
            'Templates_Path':'templates'
        }
        if config_key in defualt_values_dict.keys():
            default_value =  defualt_values_dict[config_key]
        return default_value

    def _reverse_list_env_values(self,to_reverse_value:str,target_item_types:Literal['str','int']='str'):
        temp_env_value_list = []
        for env_value_item in to_reverse_value.split(','):
            clear_env_value_item = env_value_item.strip(' ')
            if clear_env_value_item.__len__() > 0:
                if(target_item_types=='int'):
                    clear_env_value_item = int(clear_env_value_item)
                temp_env_value_list.append(clear_env_value_item)
        return temp_env_value_list


    def get_config_value(self,config_key:Config_Keys_Type,required:bool=False) -> str | list | int| None:
        env_value = getenv(config_key)
        if not (env_value and env_value.strip(' ').__len__() > 0):
            env_value = self._check_or_get_default_config_value(config_key) # 检查是否有默认值
            if required and env_value is None:
                raise ValueError(f"there were error when get the config info, \
                            error: lack config  of {config_key} in {self._env_path} !")
        
        # 对于某些默认的配置的路径文件，最好在获取之前做一遍检查
        if config_key in ['Log_Path','Static_Path','Templates_Path']:
            env_value = self.filer.get_or_create_path(cast(str,env_value))
        elif config_key == 'Allow_Host' and isinstance(env_value,str):
            env_value = self._reverse_list_env_values(env_value)
        elif config_key == 'Allow_Ports' and isinstance(env_value,str):
            env_value = self._reverse_list_env_values(env_value,'int')
        elif env_value and config_key == 'Port':
            env_value = int(env_value)
        return env_value

        