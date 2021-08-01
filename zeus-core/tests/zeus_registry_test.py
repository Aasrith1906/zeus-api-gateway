import unittest
import sys
sys.path.insert(0, '../zeus_discovery')

if __name__ == '__main__':
    import registry
else:
    from zeus_discovery import registry


class RegistryTests(unittest.TestCase):

    def setUp(self):
        self.rstore = registry.RegistryStore("test_registry_store.json")

    def test_add_service(self):
        service1 = registry.Service(
            "test_service_1", "0.0.0.0", 5000, "test service")
        self.rstore.AddService(service1)
        self.assertEqual(self.rstore.GetCount(), 1)

    def test_delete_service(self):
        service1 = registry.Service(
            "test_service_1", "0.0.0.0", 5000, "test service")
        self.rstore.DeleteService(service1)
        self.assertEqual(self.rstore.GetCount(), 0)

    def test_get_service(self):
        service1 = registry.Service(
            "test_service_1", "0.0.0.0", 5000, "test service")
        self.rstore.AddService(service1)
        service = self.rstore.GetService(service1.sname)
        print(service.__dict__)
        self.assertEqual(service, service1)

    def test_update_service(self):
        service2 = registry.Service(
            "test_service_1", "0.0.0.0", 5001, "test service 2")
        self.rstore.AddService(service2)
        service2.port = 5000
        self.rstore.UpdateService(service2)
        service = self.rstore.GetService(service2.sname)
        self.assertEqual(service.port, 5000)
        self.rstore.StoreRegistry()

    def test_service_not_found(self):
        random_search_name = 'adasfafsfawfasfwf'
        with self.assertRaises(registry.ZeusServiceNotFound):
            self.rstore.GetService(random_search_name)


if __name__ == '__main__':
    unittest.main()
