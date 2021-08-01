import sys
import os
import json


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Route():
    def __init__(self):
        pass


class RouteStore(metaclass=Singleton):

    def __init__(self, fp: str):
        self._fp = fp

    def __GetRouteStore(self) -> dict:

        try:
            if os.path.isfile(self._fp):
                with open(self._fp, 'r+') as route_store_file:
                    routes = json.load(route_store_file)
                    if len(routes) > 0:
                        return routes
                    else:
                        return {}
            else:
                with open(self._fp, 'w') as route_store_file:
                    routes = dict()
                    json.dump(routes, route_store_file)
                    route_store_file.close()
                    return routes
        except Exception as e:
            print(str(e))

    def StoreRoutes(self) -> int:

        pass

    def AddRoute(self, route: Route) -> int:
        pass

    def GetRoute(self, routename: str) -> Route:
        pass

    def DeleteRoute(self, routename: str) -> int:
        pass

    def UpdateRoute(self, route: Route) -> int:
        pass
