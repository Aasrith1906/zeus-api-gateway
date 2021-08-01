
import json 
import os 

'''
Service class used to denote each individual service 
'''


class Service():
    
    def __init__(self, servicename:str, hostname:str, port:int, servicedesc:str=None):
        if not servicename:
            raise ZeusMissingValError("Service Needs Name")
        if not hostname:
            raise ZeusMissingValError("Service Needs Host")
        if not port:
            raise ZeusMissingValError("Service Needs Port")
        self.sname = servicename
        self.sdesc = servicedesc 

        self.hname = hostname
        self.p = port 
        desc = self.sdesc if self.sdesc else ""
        self.__service_obj = {'name':self.sname,'desc':desc,'hostname':self.hname,'port':self.p}

    def getService(self)->dict:
        serviceObj = self.__service_obj
        return serviceObj

    def __str__(self):
        print("service name: {} service description: {} host: {} port: {}".format(self.sname, self.sdesc, self.hname, self.p))
        return "service name: {} service description: {} host: {} port: {}".format(self.sname, self.sdesc, self.hname, self.p)


'''
Service Registry Store
'''

class RegistryStore(): 
    
    def __init__(self, registry_file_path):
        self._fp = registry_file_path
        try:
            registry = self.__GetRegistry()
            self._registry = registry
        except Exception as e:
            print(str(e))

    def GetService(self, service_name:str)->Service:
        if service_name not in self._registry.keys():
            raise ZeusServiceNotFound("{} not found".format(service_name))
        service_obj = self._registry[service_name]
        return service_obj

    def AddService(self, service_obj:Service)->int:
        output = 0
        self._registry[service_obj.sname] = service_obj
        if service_obj.sname not in self._registry.keys():
            raise ZeusRegistryError("{} not added".format(service_obj.sname))
        else:
            output = 1
        return output

    def DeleteService(self, service_obj:Service)->int:
        output = 0
        service_name = service_obj.sname
        del self._registry[service_name]
        if service_name in self._registry.keys():
            raise ZeusRegistryError("{} not deleted".format(service_name))
        else:
            output = 1
        return output 

    def UpdateService(self, service_obj:Service)->int:
        output = 0
        service_name = service_obj.sname
        if service_name not in self._registry:
            raise ZeusServiceNotFound("{}".format(service_name))
        self._registry[service_name] = service_obj
        if self._registry == service_obj:
            output = 1
        return output

    def StoreRegistry(self, registry_dict:dict)->int:
        output = 0
        with open(self._fp,'w') as registry_file:
            try:
                json.dump(registry_dict, registry_file)
                output = 1
            except Exception as e:
                raise ZeusRegistryStorageFailure(str(e))
            registry_file.close()
            return output

    def __GetRegistry(self)->dict:       
        if os.path.exists(self._fp):
            with open(self._fp, 'a') as registry:
                registry = json.load(registry)
                if registry:
                    return registry
                else:
                    raise ZeusRegistryNotFound("Registry not found")
        else:
            registry_dict = dict()
            with open(self._fp, 'w') as registry:
                json.dump(registry_dict, registry)
                registry.close()
                return registry_dict
            
    def ReturnRegistry(self):
        if not self._registry:
            raise ZeusRegistryNotFound("Registry not found")
        else:
            r = self._registry
            return r

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
