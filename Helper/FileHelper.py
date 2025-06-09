from os import path,makedirs
from typing import Literal
from pathlib import Path


File_Types = Literal[
    'Static'
    'Root'
]


class Filer():
    def __init__(self) -> None:
        self.project_root_path = self.get_project_root_path()
    def get_project_root_path(self) -> Path:
        # 假设你有一个相对路径
        relative_path = Path('.')
        # 获取该路径的绝对路径
        absolute_path = relative_path.resolve()
        return absolute_path
    def get_or_create_path(self,file_path:str,created_file_if_not_existed:bool=False) -> str:
        # 由于这里面是绝对路径拼接的，所以当前我只需判断是否 含有 '.'， 如果含有 '.' 就不是一个 folder
        abs_path = path.join(self.project_root_path,file_path) 
        is_folder = abs_path.count(".") == 0
        directory_path = path.dirname(abs_path) if not is_folder else abs_path
        try:
            if not (path.exists(directory_path)):
                makedirs(abs_path,exist_ok=True)
            if not is_folder:
                if created_file_if_not_existed and (not path.exists(abs_path)):
                    makedirs(abs_path)
        except FileExistsError:
            print(f"The file '{abs_path}' already exists !")
            return abs_path
        except Exception as error:
            print(f'error when check the path: {abs_path} ,error: {error}')
        return abs_path