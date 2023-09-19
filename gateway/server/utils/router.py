"""
This file contains the functions that will be used to dynamically create routes and match the path of the request to
the microservices path of the scope

Functions:
    make_route(params: dict = None) -> function
    match_path(path: str) -> tuple[str, dict] or tuple[None, None]
"""
import re
from typing import Callable, Dict, Type, TYPE_CHECKING
from urllib.parse import urlparse

import cachetools
from fastapi import Response

if TYPE_CHECKING:
    from server.core.database.models import Scope


# Define the type hint for 'params'
T = Dict[str, Type]

# Initialize the cache
cache = cachetools.LRUCache(maxsize=100)

# Define a regular expression pattern to match text inside a {}
pattern = r'\{([^}]+)\}'


# Define a function to replace matches with the last string after the dot
def replace_last_string(match):
    match_content = match.group(1)  # Extract the content inside {}
    parts = match_content.split('.')  # Split by dot
    if len(parts) > 1:
        return parts[-1]  # Return the last part after the dot
    else:
        return match_content  # If there's no dot, return the original content


# We will use this function to dynamically create a function that will be used as a route
@cachetools.cached(cache, key=lambda func_name, *args: f"cached_f_{func_name}")
def make_route(func_name: str, scope: "Scope", params: T = None) -> Callable[..., Response]:
    """
    This function will dynamically create a function that will be used as a route
    :param scope: Scope
    :param func_name: str
    :param params: dict
    :return: function
    """
    # If params is None, initialize it as an empty dictionary
    if params is None:
        params = {}

    # Create an empty dictionary 'd' to store the function
    d = {}
    import_strings = []
    # Define the required parameters for the function
    string_params = ['request: Request', 'response: Response']

    # Add the parameters from the 'params' dictionary
    for key, value in params.items():
        string_params.append(f"{key}: {value.__name__}")

    if scope.body_params:
        for key, value in scope.body_params.items():
            # Get a module which is inside a {}
            matches = re.findall(pattern, value)
            value = re.sub(pattern, replace_last_string, value)
            string_params.append(f"{key}: {value}")
            for match in matches:
                module_path, class_name = match.rsplit('.', 1)
                import_strings.append(f"from {module_path} import {class_name}\n")

    if scope.query_params:
        for key, value in scope.query_params.items():
            string_params.append(f"{key}: {value}")

    if scope.form_params:
        for key, value in scope.form_params.items():
            string_params.append(f"{key}: Annotated[{value}, Form()]")

    # Define the function using 'exec()'
    function_definition = f"from typing import Annotated, Union, Optional\nfrom fastapi import Body, Form, Request, Response\n{''.join(import_strings)}async def {func_name}({','.join(string_params)}): pass"

    # Execute the function definition and store it in dictionary 'd'
    exec(function_definition, d)

    # Return the dynamically created function 'f'
    return d[func_name]


# We will use this function to match the path of the request to the microservices path of the scope
def match_path(path: str, scopes: list["Scope"] = None) -> tuple["Scope", dict] or tuple[None, None]:
    """
    This function will match the path of the request to the microservices path of the scope
    :param scopes: List[Scope]
    :param path: str
    :return: Tuple[str, dict] or Tuple[None, None]
    """

    d = {}
    for scope_path in scopes:
        if not scope_path.is_active:
            continue

        parsed_scope = urlparse(scope_path.path)
        parsed_path = urlparse(path)
        split_scope = parsed_scope.path.split('/')
        split_path = parsed_path.path.split('/')

        if len(split_scope) != len(split_path):
            continue

        for i, part in enumerate(split_scope):
            if part.startswith('{') and part.endswith('}'):
                _key, _type = part[1:-1].split(':')
                try:
                    python_type = eval(_type)
                    d[_key] = python_type
                except NameError:
                    break
                continue

            if part != split_path[i]:
                return None, None

        return scope_path, d

    return None, None


# We will use this function to get the parameters from the path
@cachetools.cached(cache, key=lambda scope_path: scope_path)
def get_params_from_path(scope_path: str) -> dict:
    """
    This function will get the parameters from the path
    :param scope_path: str
    :return: dict
    """
    parsed_scope = urlparse(scope_path)
    split_scope = parsed_scope.path.split('/')

    d = {}

    for i, part in enumerate(split_scope):
        if part.startswith('{') and part.endswith('}'):
            _key, _type = part[1:-1].split(':')
            try:
                python_type = eval(_type)
                d[_key] = python_type
            except NameError:
                break
            continue

    return d


def delete_cache(scope: "Scope") -> None:
    """
    This function will delete the cache
    :return: None
    """
    func_name = scope.name.replace(' ', '_').lower()
    if f"cached_f_{func_name}" in cache:
        del cache[f"cached_f_{func_name}"]
    if scope.path in cache:
        del cache[scope.path]
    if "openapi_cache" in cache:
        del cache["openapi_cache"]

    cache["need_reload"] = True
