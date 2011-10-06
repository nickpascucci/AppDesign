"""Mock Socket object for use in unit tests."""

class WasNotCalledError(Exception):
    """Generic exception for testing."""
    pass

class MockSocket(object):
    def __init__(self):
        self.called_methods = {}
        self.data = ""
        self.sent = ""
        
    def wasCalled(self, method):
        """Check if a given method was called.

        Args:
        method - The method to check for. This is the actual method
        object.

        Returns:
        A tuple of the arguments the method was called with.

        Raises:
        WasNotCalledError if the method was not called.
        """
        if method in self.called_methods:
            return self.called_methods[method]
        else:
            raise WasNotCalledError("Method %s was not called." % method)

    def send(self, string, flags=0):
        self.called_methods[self.send] = (string, flags)
        self.sent += string

    def sendall(self, string, flags=0):
        self.called_methods[self.sendall] = (string, flags)
        self.sent += string

    def recv(self, bufsize, flags=0):
        """Record the arguments and then return the preset data."""
        self.called_methods[self.recv] = (bufsize, flags)
        return self.data
