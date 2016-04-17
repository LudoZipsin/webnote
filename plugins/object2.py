from yapsy.IPlugin import IPlugin


class PluginTwo(IPlugin):
    def print_name(self):
        print("this is plugin 2")

    def get_compatible_source(self):
        return ["stack", "stack.info"]

    def processor(self, url):
        return url+" object2.py"
