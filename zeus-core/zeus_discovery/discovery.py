import requests
import registry
from flask import Flask, request
from functools import wraps
from flask.views import MethodView
import os
import json


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ServiceChecker():

    def __init__(self, app: Flask, registry_path: str):
        self._registry_path = registry_path
        self.app = app
        try:
            self.rstore = registry.RegistryStore(registry_path)
            if not self.rstore:
                raise registry.ZeusRegistryError(
                    "Failed to Initialise Registry ")
        except Exception as e:
            print(str(e))
            raise ZeusServiceCheckerFailure(str(e))

    @staticmethod
    async def CheckService(service: registry.Service) -> int:
        output = 0
        service_data = service.getService()
        service_name = service_data["name"]
        hostname = service_data["hostname"]
        port = service_data["port"]
        print("Zeus service manager is testing {}".format(service_name))
        http_get = await requests.get("{}:{}".format(hostname, port), timeout=5)
        if http_get.status_code != 200:
            raise ZeusServiceNoResponse(
                "{} gave no response".format(service_name))
        else:
            print("Output from {}".format(service_name))
            print(http_get.content)
            output = 1
        return output

    async def UpdateServiceStates(self):
        if len(self.rstore) <= 0:
            return
        for service in self.rstore:
            try:
                output = await ServiceChecker.CheckService(service)
                if output == 1:
                    service.state = 'online'
                    self.rstore.UpdateService(service)
                elif output == 0:
                    service.state = 'offline'
                    self.rstore.UpdateService(service)
            except Exception as e:
                raise ZeusServiceStateUpdaterError(str(e))

    async def UpdateServiceThread(self):
        for service in self.rstore.GetAllServices():
            pass


class ServiceManager(metaclass=Singleton):

    def __init__(self, app: Flask, file_name: str, route: str, init=True):
        self.app = app
        self._f = file_name
        self._route = route
        if init:
            try:
                self.__init_registry_store()
                self.__add_view()
            except Exception as e:
                print(str(e))

    def __add_view(self):
        try:
            print(self.rstore.__dict__)
            if self.rstore:
                self.app.add_url_rule(self._route, view_func=ServiceManagerView.as_view(
                    'servicemanager', self.rstore))
            else:
                raise ZeusServiceManagerFailure(
                    "Registry Store Not Initialised")
        except Exception as e:
            print(str(e))

    def __init_registry_store(self):
        if not self._f:
            raise ZeusServiceManagerFailure("Invalid File Name")
        try:
            self.rstore = registry.RegistryStore(self._f)
        except Exception as e:
            self.rstore = None
            print(str(e))


class ServiceManagerView(MethodView):
    def __init__(self, rstore: registry.RegistryStore):
        self.rstore = rstore

    def get(self):
        json_data = request.get_json()
        print(json_data)
        if len(json_data) != 1:
            return {"message": "invalid request"}, 400
        if 'servicename' not in json_data.keys():
            return {"message": "invalid request"}, 400
        try:
            service_name = json_data['servicename']
            service = self.rstore.GetService(service_name)
            if not service:
                return {"message": "service not found"}
            service_data = service.getService()
            if service_data is None:
                return {"message": "service data not found"}
            return {"message": "service found", "data": service_data}, 200

        except Exception as e:
            return {"message": "error", "data": str(e)}, 500

    def post(self):
        try:
            json_data = request.get_json()
            if len(json_data.keys()) != 5:
                return {"message": "invalid request"}, 400

            required_field = ['servicename', 'host',
                              'port', 'desc', 'endpointmap']
            for x in required_field:
                if x not in json_data.keys():
                    print(x)
                    return {"message": "invalid request missing {}".format(x)}, 400

            sname = json_data['servicename']
            h = json_data['host']
            port = json_data['port']
            desc = json_data['desc']
            em = json_data['endpointmap']
            print(type(em))
            service = registry.Service(sname, h, port, em, desc)
            output = self.rstore.AddService(service)
            self.rstore.StoreRegistry()
            if not output:
                return {"message": "service not added"}, 500
            return {"message": "Service Added", "data": service.__dict__}, 201

        except Exception as e:
            return {"message": "error", "data": str(e)}, 500
            self.rstore.StoreRegistry()

    def put(self):
        try:
            json_data = request.get_json()
            if len(json_data) != 5:
                return {"message": "invalid request"}, 400

            required_field = ['servicename', 'host',
                              'port', 'desc', 'endpointmap']
            for x in required_field:
                if x not in json_data.keys():
                    print(x)
                    return {"message": "invalid request"}, 400

            sname = json_data['servicename']
            h = json_data['host']
            port = json_data['port']
            desc = json_data['desc']
            em = json_data['endpointmap']

            service = self.rstore.GetService(sname)
            print(type(service))
            if service is None:
                return {"message": "service not found"}, 404

            service.hname = h
            service.p = port
            service.sdesc = desc
            service.endpoints_map = em

            output = self.rstore.UpdateService(service)
            if not output:
                return {"message": "service not updated"}, 500

            return {"message": "Service Updated", "data": service.__dict__}, 204

        except Exception as e:
            return {"message": "error", "data": str(e)}, 500

    def delete(self):

        json_data = request.get_json()
        if len(json_data) != 1:
            return {"message": "invalid request"}, 400
        if 'servicename' not in json_data.keys():
            return {"message": "invalid request"}, 400
        try:
            service_name = json_data['servicename']
            service = self.rstore.GetService(service_name)
            if not service:
                return {"message": "service not found"}

            service_data = service.getService()
            output = self.rstore.DeleteService(service)

            if not output:
                return {"message": "service has not been deleted"}, 500
            return {"message": "service deleted", "data": service_data}, 202

        except Exception as e:
            return {"message": "error", "data": str(e)}, 500
            self.rstore.StoreRegistry()


class ZeusServiceNoResponse(Exception):
    pass


class ZeusServiceStateUpdaterError(Exception):
    pass


class ZeusServiceManagerError(Exception):
    pass


class ZeusServiceManagerFailure(Exception):
    pass


class ZeusServiceCheckerFailure(Exception):
    pass


if __name__ == '__main__':
    pass
