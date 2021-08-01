
import json
import os

'''
Service class used to represent each individual service 

Author: Aasrith Chennapragada 
'''


class Service():

    def __init__(self, servicename: str, hostname: str, port: int, endpointmap: dict, servicedesc: str = None, state="online"):
        if not servicename:
            raise ZeusMissingValError("Service Needs Name")
        if not hostname:
            raise ZeusMissingValError("Service Needs Host")
        if not port:
            raise ZeusMissingValError("Service Needs Port")
        self.sname = servicename
        self.sdesc = servicedesc
        self.state = state
        self.hname = hostname
        self.p = port
        self.endpoints_map = endpointmap
        #self.UpdateEndpoints(self.endpoints_map)
        desc = self.sdesc if self.sdesc else ""
        self.__service_obj = {'name': self.sname, 'desc': desc,
                              'hostname': self.hname, 'port': self.p, 'state': state, 'endpointmap': self.endpoints_map}

    '''
    Function that returns dict object that represents service 
    '''

    def getService(self) -> dict:
        serviceObj = self.__service_obj
        return serviceObj

    def UpdateEndpoints(self, endpoint_map):
        for em, funcs in endpoint_map.items():
            if not hasattr(self, em):
                self.em = funcs

    def __str__(self):
        print("service name: {} service description: {} host: {} port: {}".format(
            self.sname, self.sdesc, self.hname, self.p))
        return "service name: {} service description: {} host: {} port: {}".format(self.sname, self.sdesc, self.hname, self.p)


'''
Service Registry Store can only be instantiated once 

'''


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


'''
Service Registry Store class 

Author: Aasrith Chennapragada
'''


class RegistryStore(metaclass=Singleton):

    def __init__(self, registry_file_name):
        self._fp = registry_file_name
        try:
            registry = self.__GetRegistry()
            if registry:
                self._registry = registry
            else:
                self._registry = dict()
        except Exception as e:
            print(str(e))
    '''

    Functionality: Function that returns registry.Service object from registry store if exists 
    Parameters: service_name (string)
    Addional Info:
        search done by name 
        if does not exist raises ZeusServiceNotFound error  

    '''

    def GetService(self, service_name: str) -> Service:
        if service_name not in self._registry.keys():
            raise ZeusServiceNotFound("{} not found".format(service_name))
        service_obj = self._registry[service_name]
        return service_obj

    '''

    Functionality: Function that adds a service to registry store
    Parameters: registry.Service object 
    Additional Info:
        returns an int 1 if added successfully else 0 
        any other errors ZeusRegistryError is raised 
    '''

    def AddService(self, service_obj: Service) -> int:
        output = 0
        self._registry[service_obj.sname] = service_obj
        if service_obj.sname not in self._registry.keys():
            raise ZeusRegistryError("{} not added".format(service_obj.sname))
        else:
            output = 1
        return output

    '''
    Functionality: Function that deletes a service from registry store 
    Parameters: registry.Service object 
    Additional Info:
        returns an int 1 if deleted successfully else 0
    '''

    def DeleteService(self, service_obj: Service) -> int:
        output = 0
        service_name = service_obj.sname
        del self._registry[service_name]
        if service_name in self._registry.keys():
            raise ZeusRegistryError("{} not deleted".format(service_name))
        else:
            output = 1
        return output

    '''
    Functionality: Function that updates a service in registry store 
    Parameters: registry.Service object 
    Additional Info:
        returns an int 1 if deleted successfully else 0
    '''

    def UpdateService(self, service_obj: Service) -> int:
        output = 0
        service_name = service_obj.sname
        if service_name not in self._registry:
            raise ZeusServiceNotFound("{}".format(service_name))
        self._registry[service_name] = service_obj
        if self._registry == service_obj:
            output = 1
        return output

    '''
    Functionality: Saves registry store into json file self._fp, provided in class constructor 
    Parameters: None
    Additional Info:
        returns an int 1 if deleted successfully else 0
    '''

    def StoreRegistry(self) -> int:
        output = 0
        path = os.path.join(os.path.curdir, self._fp)
        with open(self._fp, 'w') as registry_file:
            try:
                registry_dump = dict()
                print(self._registry)
                for key, value in self._registry.items():
                    print(key)
                    print(value)
                    registry_dump[key] = value.__dict__
                json.dump(registry_dump, registry_file)
                output = 1
            except Exception as e:
                raise ZeusRegistryStorageFailure(str(e))
            registry_file.close()
        return output

    '''
    Functionality: Function that loads registry store from json file, provided in class constructor 
    Parameters: None
    Additional Info:
        returns dictionary 
    '''

    def __GetRegistry(self) -> dict:
        path = os.path.join(os.path.curdir, self._fp)
        if os.path.isfile(path):
            with open(self._fp, 'r+') as registry_file:
                registry = json.load(registry_file)
                if registry is not None:
                    return registry
                else:
                    json.dump({}, registry_file)
                    return dict()
                registry_file.close()
        else:
            registry_dict = dict()
            with open(path, 'w') as registry_file:
                json.dump(registry_dict, registry_file)
                registry_file.close()
            with open(path, 'r+') as registry_file:
                registry = json.load(registry_file)
                # if not registry:
                #     raise ZeusRegistryError("Error loading registry")
                return registry

    '''
    Functionality: Returns registry dict 
    Parameters: None 
    Additional Info:
        None
    '''

    def ReturnRegistry(self):
        if self._registry is None:
            raise ZeusRegistryNotFound("Registry not found")
        else:
            r = self._registry
            return r

    '''
    Functionality: Returns total number of services  
    Parameters: None
    Additional Info:
        returns int length, if registry is not found ZeusRegistryNotFoundError is raised 
    '''

    def GetCount(self) -> int:
        if self._registry is None:
            raise ZeusRegistryNotFound("Registry not found")
        length = len(self._registry)
        if length:
            return length
        else:
            print("Empty Registry")
            return 0

    '''
    Functionality: Function that returns all services as generator  
    Parameters: None
    Additional Info:
        None
    '''

    def GetAllServices(self) -> Service:
        if self._registry is None:
            raise ZeusRegistryNotFound("Registry not found")
        for service in self._registry.values():
            if service:
                yield service
            else:
                raise ZeusRegistryError("Failed to get service")


class ZeusMissingValError(Exception):
    pass


class ZeusServiceNotFound(Exception):
    pass


class ZeusRegistryError(Exception):
    pass


class ZeusRegistryNotFound(Exception):
    pass


class ZeusRegistryStorageFailure(Exception):
    pass
