from Utils.Status import Status

class Mission:

    def __init__(self, name:str, link:str, green_building:bool):
        self.name = name
        self.link = link
        self.green_building = green_building
        self.status = Status.TO_DO
        self.proof = None
        self.completion_date = None
        self.completing_user = None
    