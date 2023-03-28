from Utils.Status import Status


class Stage:
    def __init__(self, name: str):
        self.name = name
        self.completion_date = None
        self.status = Status.TO_DO
