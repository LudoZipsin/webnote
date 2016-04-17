from yapsy.IPlugin import IPlugin


class PluginOne(IPlugin):
    def print_name(self):
        print("this is plugin 1")

    def get_compatible_source(self):
        return ["korben", "korben.info"]

    def processor(self, url):
        return url+" object1.py"
