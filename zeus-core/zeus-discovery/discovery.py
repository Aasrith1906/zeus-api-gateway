import requests
from . import registry
from flask import Flask
from functools import wraps

class ServiceChecker():
    
    def __init__(self, registry:registry.RegistryStore):
        self.rstore = registry


    @staticmethod
    def CheckService(service:registry.Service)->int:
        output = 0
        service_data = service.getService()
        service_name = service_data["name"]
        hostname = service_data["hostname"]
        port = service_data["port"]
        print("Zeus service manager is testing {}".format(service_name))
        http_get = requests.get("{}:{}".format(hostname, port), timeout=5)
        if http_get.status_code!=200:
            raise ZeusServiceNoResponse("{} gave no response".format(service_name))
        else:
            print("Output from {}".format(service_name))
            print(http_get.content)
        return output 

class ServiceManager():
    
    def __init__(self, app:Flask, registry:registry.RegistryStore):
        self.rstore = registry
        self.app = app 

    @staticmethod
    def get_service(app):
        pass
    
    def add_service(self):
        pass 
    
    def delete_service(self):
        pass

    def update_service(self):
        pass


class ZeusServiceNoResponse(Exception):
    pass