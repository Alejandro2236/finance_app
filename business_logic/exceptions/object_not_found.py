class ObjectNotFound(Exception):
    def __init__(self, message="Object not found in database"):
        self.message = message
        super().__init__(self.message)
