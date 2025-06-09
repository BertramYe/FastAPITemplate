from Helper.ConfigHelper import Configer,cast
from fastapi.templating import Jinja2Templates


# 指定模板文件夹路径
configer = Configer()
templates = Jinja2Templates(directory=cast(str,configer.get_config_value('Templates_Path')))

