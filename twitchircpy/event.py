class Event():

    """
    This class is used for storing information about events.
    Used interally to bundle events efficiently.
    Should not be manually created in most cases.
    
    Parameters
    ==========
    id -> :int:
        The internal ID of the event.
    name -> :str:
        The name of the event.
        Used for easy event firing.
    args -> :int:
        Amount of arguments the event takes.
        Used to ensure the user is using the event correctly.
    """

    def __init__(self, id, name, args):
        self.id = id
        self.name = name
        self.args = args

    def __repr__(self):
        return f"Event(id: {self.id}, name: {self.name}, args: {self.args})"