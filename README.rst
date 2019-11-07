Installing
==========

.. code-block:: bash

  pip3 install throttle

Usage
=====

.. code-block:: python

  import lineopt

  # dict w/ extra methods
  state = lineopt.State()

  @state.sub('echo')
  def state_0(argument):

    return argument

  @state_0.sub('loud')
  def state_0_0(argument):

    return argument.upper()

  flags = {'-c': 'content', '-s': 'meddle'}

  @state_0.sub('fancy', flags)
  def state_0_1(arguments):

    content = arguments['-c']

    meddle = arguments.get('-s', ' ')

    return meddle.join(content)

  starts = ('!', '.')

  def parse(value, starts = starts):

    try:

      (start, names, argument, function) = state.context(starts, value)

    except (KeyError, ValueError) as error:

      raise

      result = repr(error)

    else:

      result = function(argument)

    print(result)

  say = 'vocalizing is fun' # argument

  parse(f'!echo {say}') # vocalizing is fun
  parse(f'.echo.loud {say}') # VOCALIZING IS FUN
  parse(f'!echo.fancy -c {say}') # v o c a l i z i n g   i s   f u n
  parse(f'.echo.fancy {say} -s ~') # v~o~c~a~l~i~z~i~n~g~ ~i~s~ ~f~u~n
  parse(f'-echo.loud {say}') # ValueError: 'invalid start'
  parse(f'.fancy {say}') # KeyError: 'fancy' (only sub of echo)

Links
-----

- `Documentation <https://lineopt.readthedocs.io>`_
