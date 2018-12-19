class Variable():

    """
    Class used for storing information about a variable.
    Should not be manually created.

    Parameters
    ==========
    name -> :str:
        The name of the variable.
    function -> :function:
        The function used to call the variable.
    """

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def __repr__(self):
        return f"Variable(name: {self.name}, function: {self.function})"

    def to_dynamic(self, params = None):
        return DynamicVariable(self.name, self.function, params)

class DynamicVariable(Variable):

    """
    Class used for easier chat command variable handling.
    Very similar to class:Variable: except with an extra parameter.
    Should not be manually created.

    New Parameter
    =============
    params -> :list<str | datetime>: | :None:
        List of params for the variable in the chat command.
    """

    def __init__(self, name, function, params = None):
        super().__init__(name, function)
        self.params = params

    def __repr__(self):
        return f"DynamicVariable(name: {self.name}, function: {self.function}, params: {self.params})"