import flagopt
import functools


__all__ = ('State',)


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

    .. code-block::

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


class State(dict):

    """
    Means of adding, parsing and invoking commands.

    :param str lower:
        Separates commands from arguments.
    :param str upper:
        Splits arguments away from each other.
    """

    __slots__ = ('_lower', '_upper', '_cls')

    flags = {}

    def __init__(self, lower = '.', upper = ' '):

        self._lower = lower

        self._upper = upper

        self._cls = functools.partial(self.__class__, lower, upper)

    def sub(self, name, flags = None):

        """
        Decorator for adding commands.

        :param str name:
            The name of the command.
        :param dict[str,any] flags:
            Used for parsing arguments.
        """

        top = sub(self, name, cls = self._cls)

        def wrapper(invoke):

            self.flags[invoke] = flags

            return top(invoke)

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

    def parse(self, content, apply = None):

        """
        Split ``content`` into ``names`` and ``argument``.

        :param func apply:
            Used on the names for further parsing.
        """

        try:

            (instruct, argument) = content.split(self._upper, 1)

        except ValueError:

            (instruct, argument) = (content, '')

        names = instruct.split(self._lower)

        if apply:

            names = apply(names)

        return (names, argument)

    def analyse(self, content, apply = None):

        """
        | Parse ``content`` and find the respective ``invoke``.
        | ``flags`` found against it will be used to parse the ``argument``.
        """

        (names, argument) = self.parse(content, apply or tuple)

        invoke = self.trail(*names) if names else None

        flags = self.flags.get(invoke)

        if flags:

            argument = flagopt.snip(flags, argument)

        return (names, argument, invoke)

    def context(self, starts, content, **kwargs):

        """
        | Splits content between ``start`` and ``rest``.
        | Parses ``rest`` to get ``names`` and ``argument``.
        | Uses ``names`` to get an ``invoke``.
        | Can raise all respective errors.
        """

        (start, content) = prefix(starts, content)

        (names, argument, invoke) = self.analyse(content, **kwargs)

        return (start, names, argument, invoke)
