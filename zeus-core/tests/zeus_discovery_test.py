from flask import Flask, request
from flask.views import MethodView
import unittest
import sys
sys.path.insert(0, '../zeus_discovery')

if __name__ == '__main__':
    import discovery
else:
    from zeus_discovery import discovery


# class Dummy(MethodView):
#     def __init__(self, filePath):
#         self.fp = filePath
#     def get(self):
#         return "test"
#     def post(self):
#         return self.fp


# class FlaskWrapper():
#     def __init__(self, app:Flask):
#         self.app = app
#         self.add_method()
#     def add_method(self):
#         self.app.add_url_rule('/',  view_func=Dummy.as_view('testview', 'testpath'))


# if __name__ == '__main__':
#     app = Flask(__name__)
#     flask_wrapper = FlaskWrapper(app)
#     app.run(debug=True)


if __name__ == '__main__':
    try:
        app = Flask(__name__)
        service_manager = discovery.ServiceManager(
            app, "test_registry_store.json", '/svcmanager')
        app.run(debug=True)
    except Exception as e:
        print(str(e))
