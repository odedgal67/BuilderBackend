from singleton_decorator import singleton

@singleton
class ProjectController:

    def __init__(self):
        self.projects = list()
        
    