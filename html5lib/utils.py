from __future__ import absolute_import, division, unicode_literals

from types import ModuleType


class MethodDispatcher(dict):
    """Dict with 2 special properties:

    On initiation, keys that are lists, sets or tuples are converted to
    multiple keys so accessing any one of the items in the original
    list-like object returns the matching value

    md = MethodDispatcher({("foo", "bar"):"baz"})
    md["foo"] == "baz"

    A default value which can be set through the default attribute.
    """

    def __init__(self, items=()):
        # Using _dictEntries instead of directly assigning to self is about
        # twice as fast. Please do careful performance testing before changing
        # anything here.
        _dictEntries = []
        for name, value in items:
            if type(name) in (list, tuple, frozenset, set):
                for item in name:
                    _dictEntries.append((item, value))
            else:
                _dictEntries.append((name, value))
        dict.__init__(self, _dictEntries)
        self.default = None

    def __getitem__(self, key):
        return dict.get(self, key, self.default)


def isSurrogatePair(data):
    """Check whether a string is a surrogate pair or not"""
    return (len(data) == 2 and
            ord(data[0]) >= 0xD800 and ord(data[0]) <= 0xDBFF and
            ord(data[1]) >= 0xDC00 and ord(data[1]) <= 0xDFFF)


def surrogatePairToCodepoint(data):
    """Convert a surrogate pair to a codepoint"""
    char_val = (0x10000 + (ord(data[0]) - 0xD800) * 0x400 +
                (ord(data[1]) - 0xDC00))
    return char_val


def moduleFactoryFactory(factory):
    """Module Factory Factory (no, this isn't Java, I know)
    Here to stop this being duplicated all over the place."""
    moduleCache = {}

    def moduleFactory(baseModule, *args, **kwargs):
        if isinstance(ModuleType.__name__, type("")):
            name = "_%s_factory" % baseModule.__name__
        else:
            name = b"_%s_factory" % baseModule.__name__

        if name in moduleCache:
            return moduleCache[name]
        else:
            mod = ModuleType(name)
            objs = factory(baseModule, *args, **kwargs)
            mod.__dict__.update(objs)
            moduleCache[name] = mod
            return mod

    return moduleFactory
