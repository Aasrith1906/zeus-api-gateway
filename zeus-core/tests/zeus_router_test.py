from flask import Flask, url_for
import sys
import unittest

sys.path.insert(0, '../zeus_discovery')
sys.path.insert(0, '../zeus_routing')
if __name__ == '__main__':
    import registry
    import routing
else:
    from zeus_discovery import registry
    from zeus_routing import routing

app = Flask(__name__)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/api-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return str(links)


if __name__ == '__main__':

    endpointmap = {"userauth": ['GET', 'POST', 'DELETE', 'PUT']}
    endpointmap_pcache = {"frpath": ['GET', 'POST', 'DELETE', 'PUT'], 'rfpath': [
        'GET', 'POST', 'DELETE', 'PUT']}
    service1 = registry.Service(
        'auth', 'https://auth.pilltheapp.com', 80, endpointmap, "auth service")
    service2 = registry.Service(
        'pcache', 'https://pcache.pilltheapp.com', 80, endpointmap_pcache, "pcache service")
    svc_route = routing.ZeusRoute(service1.sname, app, service1)
    pcache_route = routing.ZeusRoute(service2.sname, app, service2)
    app.run(debug=True)
