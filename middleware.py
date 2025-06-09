from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction,RequestResponseEndpoint
from starlette.types import ASGIApp
from starlette.responses import JSONResponse
from Helper.LoggerHelper import Logger
from Helper.ConfigHelper import Configer
from typing import cast
#  当然以下为了访问安全，完全可以添加一个加密方法，对称加密即可, 详细可以在 CryptHelper.py 中去定义和调用

class MiddleWare(BaseHTTPMiddleware):
    def __init__(self,app:ASGIApp,dispatch:DispatchFunction | None = None) -> None:
        # super().__init__(app,
        #                     allow_origins=["*"],  # 您可以指定允许的域名列表
                              # 是否允许跨域请求携带凭据（如 cookies、HTTP认证信息或客户端证书）。如果设置为 True，浏览器将会在跨域请求中携带凭据。如果设置为 False，则不会允许在跨域请求中携带凭据。
        #                     allow_credentials=True,  
        #                     # allow_methods=["*"],  # 允许所有方法
        #                     allow_methods=["GET",'POST'],  # 允许所有方法
        #                     allow_headers=["*"],  # 允许所有请求头
        #                  )
        super().__init__(app,dispatch)
        self.logger = Logger()
        self.configer = Configer()
        self.white_list = cast(list[str],self.configer.get_config_value('Allow_Host')) 
        self.allow_ports_list = cast(list[int],self.configer.get_config_value('Allow_Ports')) 

    async def dispatch(self, request, call_next:RequestResponseEndpoint):
        try:
            valid_request_port = 80 if request.url.port is None else int(request.url.port)
            if valid_request_port not in self.allow_ports_list:  # 接口不被允许
                self.logger.error(f'request from port  ({request.url.port}) not allowed, the allowed host please checking the settings.py of the config "Allow_Ports" ! ')
                return JSONResponse(
                    content= 'request not allowed, error type 1 !',
                    status_code= 504
                )
            # '*' 代表允许所有的接口请求
            if '*' not in self.white_list and request.url.hostname not in self.white_list:
                self.logger.error(f'request from host ({request.url.hostname}) not allowed, the allowed host please checking the settings.py of the config "Allow_Host" ! ')
                return JSONResponse(
                    content= 'request not allowed, error type 2',   # host 不被允许
                    status_code= 504
                )
            response = await call_next(request)
            return response
        except Exception as er:
            self.logger.error(f'error in the MiddleWare, error: {er}') 
            return JSONResponse(
                    content= f'there were some errors in the server !!!',
                    status_code= 505
            )

