import sys
from flask import Flask, request
from flask.views import MethodView
import requests

sys.path.insert(0, '../zeus_discovery')

if __name__ == '__main__':
    import registry
    import discovery
else:
    import registry
    import discovery


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ZeusGateway(metaclass=Singleton):
    def __init__(self, app: Flask, services: list, ):
        self.app = app
        self.services = services
        self.zeus_routes = []

    def __init_app(self):
        try:
            for service in self.services:
                self.zeus_routes.append(
                    ZeusRoute(service.sname, self.app, service))
        except Exception as e:
            print(str(e))

    def __bind_registry(self,)


class ZeusRoute():

    def __init__(self, routename: str, app: Flask, service: registry.Service, url=''):
        self.name = routename
        self.url = '/{}'.format(service.sname)
        self.service = service
        self.app = app

        self.__add_view()

    def __add_view(self):
        endpoint_map = self.service.endpoints_map
        try:
            for endpoint, map_ in endpoint_map.items():
                print(endpoint)
                url = '/{}/{}'.format(self.service.sname, endpoint)
                print(map_)
                self.app.add_url_rule(url, view_func=ZeusRouteView.as_view(
                    '{}_{}_View'.format(self.service.sname, endpoint), endpoint, self.service, map_))
        except Exception as e:
            print(str(e))


class ZeusRouteView(MethodView):

    def __init__(self, name: str,  service: registry.Service, methods=['GET']):
        self.methods = methods
        self.name = name
        self.service = service

    def get(self):

        try:
            if not self.__CheckMethod('GET'):
                return {"Zeus Error": "Invalid Request"}
            if request.get_json():
                data = request.get_json()
            else:
                data = {}
            if self.service.p != 80:
                url = '{}:{}/{}'.format(self.service.hname,
                                        self.service.p, self.name)
            else:
                url = '{}/{}'.format(self.service.hname, self.name)
            output = requests.get(url, json=data)
            return {"Zeus Output": output.json()}
        except Exception as e:
            return {"Zeus Error": str(e)}, 500

    def post(self):

        try:
            if not self.__CheckMethod('POST'):
                return {"Zeus Error": "Invalid Request"}
            if not request.get_json():
                return {"Zeus Error": "cannot post without data"}, 400
            data = request.get_json()
            if self.service.p != 80:
                url = '{}:{}/{}'.format(self.service.hname,
                                        self.service.p, self.name)
            else:
                url = '{}/{}'.format(self.service.hname, self.name)
            output = requests.post(url, json=data)
            return {'Zeus Output': output.json()}
        except Exception as e:
            return {"Zeus Error": str(e)}, 500

    def put(self):
        try:
            if not self.__CheckMethod('PUT'):
                return {"Zeus Error": "Invalid Request"}
            if not request.get_json():
                return {"Zeus Error": "cannot update without data"}, 400
            data = request.get_json()
            if self.service.p != 80:
                url = '{}:{}/{}'.format(self.service.hname,
                                        self.service.p, self.name)
            else:
                url = '{}/{}'.format(self.service.hname, self.name)
            output = requests.put(url, json=data)
            return {'Zeus Output': output.json()}
        except Exception as e:
            return {"Zeus Error": str(e)}, 500

    def delete(self):
        try:
            if not self.__CheckMethod('DELETE'):
                return {"Zeus Error": "Invalid Request"}
            if not request.get_json():
                return {"Zeus Error": "cannot process delete without data"}, 400
            data = request.get_json()
            if self.service.p != 80:
                url = '{}:{}/{}'.format(self.service.hname,
                                        self.service.p, self.name)
            else:
                url = '{}/{}'.format(self.service.hname, self.name)
            output = requests.delete(url, data=data)
            return {'Zeus Output': output.json()}
        except Exception as e:
            return {"Zeus Error": str(e)}, 500

    def __CheckMethod(self, method):
        if method not in self.methods:
            return False
        else:
            return True
