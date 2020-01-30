import functools
import types
import weakref


__all__ = ('prefix', 'State', 'empty')


def sub(state, name, cls = None):

    def wrapper(invoke):

        value = (cls or state.__class__)()

        state[name] = (invoke, value)

        return value

    return wrapper


def asset(state, *names):

    for name in names:

        pair = state[name]

        state = pair[1]

    return pair


def trail(state, *names):

    (value, state) = asset(state, *names)

    return value


def prefix(values, content):

    """
    Discover start and separate from content.

    :param list[str] values:
        Will scan through up to the one ``content`` starts with.
    :param str content:
        The value to scan, will separate from the start if found.

    :raises:
        :class:`ValueError` if no start matches.

    .. code-block:: py

        >>> prefix(('-', '.', '!'), './echo')
        >>> ('.', '/echo')

    """

    for value in values:

        if content.startswith(value):

            break

    else:

        raise ValueError('invalid start')

    size = len(value)

    content = content[size:]

    return (value, content)


def parse(content, lower = '.', upper = ' '):

    try:

        (instruct, argument) = content.split(upper, 1)

    except ValueError:

        (instruct, argument) = (content, '')

    names = instruct.split(lower)

    return (names, argument)


_functions = weakref.WeakValueDictionary()


empty = type('empty', (), {'__slots__': (), '__bool__': False.__bool__})()


class Invoke(types.SimpleNamespace):

    def __init__(self, function, **kwargs):

        super().__init__(**kwargs)

        _functions[self] = function

        functools.update_wrapper(self, function)

    @property
    def __call__(self):

        return _functions[self]

    def __getattr__(self, key):

        return empty

    def __hash__(self):

        return hash(self.__Call__)


class State(dict):

    """
    Means of adding, parsing and invoking commands.

    :param str lower:
        Separates commands from arguments.
    :param str upper:
        Splits arguments away from each other.
    """

    __slots__ = ('_lower', '_upper', '_cls', '_spaces')

    def __init__(self, lower = '.', upper = ' '):

        self._lower = lower

        self._upper = upper

        self._cls = functools.partial(self.__class__, lower, upper)

    def sub(self, name, **space):

        """
        Decorator for adding commands.

        :param str name:
            The name of the command.
        """

        def wrapper(function):

            invoke = Invoke(function, **space)

            return sub(self, name, cls = self._cls)(invoke)

        return wrapper

    def asset(self, *names):

        """
        Get ``(name, invoke)`` pair from ``names``.

        :raises:
            :class:`KeyError` with the name not found.
        """

        return asset(self, *names)

    def trail(self, *names):

        """
        Uses :meth:`asset` to get invoke.
        """

        return trail(self, *names)

    def parse(self, content):

        """
        Get ``(names, argument)`` from ``content`` .
        """

        return parse(content, self._lower, self._upper)

    def analyse(self, content, starts = ('',), apply = None):

        """
        Split the content into its components and derive the invoke.

        :param tuple[str] starts:
            Will be checked against the beginning of the content.
        :param func apply:
            Used on names for any further parsing.
        """

        (start, content) = prefix(starts, content)

        (names, argument) = self.parse(content)

        names = (apply or tuple)(names)

        invoke = self.trail(*names)

        return (start, names, argument, invoke)
