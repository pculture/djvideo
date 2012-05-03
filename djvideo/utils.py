from django.template import Variable

def get_variable_or_string(name):
    """
    If the name given is a raw string, just return that string.  Otherwise,
    return a ``Variable`` object which we'll load later.
    """
    if name[0] in '"\'':
        return name[1:-1]
    else:
        return Variable(name)
