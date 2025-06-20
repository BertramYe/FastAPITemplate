# router: APIRouter,
# *,
# prefix: str = "",
# tags: List[str | Enum] | None = None,
# dependencies: Sequence[Depends] | None = None,
# responses: Dict[int | str, Dict[str, Any]] | None = None,
# deprecated: bool | None = None,
# include_in_schema: bool = True,
# default_response_class: type[Response] = Default(JSONResponse),
# callbacks: List[BaseRoute] | None = None,
# generate_unique_id_function: (APIRoute) -> str = Default(generate_unique_id)

from .pages.home import HomeRouter

RoutersList:list[list]  = [
    # [
    #     HomeRouter,
    #     "/home", 
    #     ["home"]
    # ]
    [
        HomeRouter,
        "", 
        [""]
    ]
]