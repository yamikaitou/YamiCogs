.. _lottery:

=======
Lottery
=======

This cog is currently in Beta status. Not all features have been impletemented and/or documented

This is the cog guide for the lottery cog. You will
find detailed docs about usage and commands.

``[p]`` is considered as your prefix.

.. note:: To use this cog, load it by typing this::

        [p]load lottery

.. _lottery-usage:

-----
Usage
-----

Lottery Games


.. _lottery-commands:

--------
Commands
--------

.. _lottery-command-lottery:

^^^^^^^
lottery
^^^^^^^

**Syntax**

.. code-block:: none

    [p]lottery 

**Description**

Lottery Game

.. _lottery-command-lottery-lucky3:

""""""
lucky3
""""""

**Syntax**

.. code-block:: none

    [p]lottery lucky3 

**Description**

Play a game of Lucky 3

.. _lottery-command-lottery-games:

"""""
games
"""""

**Syntax**

.. code-block:: none

    [p]lottery games 

**Description**

View game explanations

.. _lottery-command-lottoset:

^^^^^^^^
lottoset
^^^^^^^^

**Syntax**

.. code-block:: none

    [p]lottoset 

**Description**

Lottery Settings

.. _lottery-command-lottoset-lucky3:

""""""
lucky3
""""""

**Syntax**

.. code-block:: none

    [p]lottoset lucky3 

**Description**

Configure settings for Lucky 3

.. _lottery-command-lottoset-lucky3-prize:

"""""
prize
"""""

**Syntax**

.. code-block:: none

    [p]lottoset lucky3 prize <prize>

**Description**

Set the Prize amount

.. _lottery-command-lottoset-lucky3-cost:

""""
cost
""""

**Syntax**

.. code-block:: none

    [p]lottoset lucky3 cost <cost>

**Description**

Set the cost per game

.. _lottery-command-lottoset-lucky3-icons:

"""""
icons
"""""

**Syntax**

.. code-block:: none

    [p]lottoset lucky3 icons <icons>

**Description**

Sets the number of Emojis to choose from

* Valid options are 2-9

Approximate Win percentrages are

.. code-block:: none

    | Icons: 2 | 25.0%
    | Icons: 3 | 11.1%
    | Icons: 4 |  6.3%
    | Icons: 5 |  4.0%
    | Icons: 6 |  2.8%
    | Icons: 7 |  2.1%
    | Icons: 8 |  1.6%
    | Icons: 9 |  1.2%

.. _lottery-command-lottoset-lucky3-enable:

""""""
enable
""""""

**Syntax**

.. code-block:: none

    [p]lottoset lucky3 enable <state>

**Description**

Enable or Disable the Lucky3 game.

<state> should be any of these combinations,
`on/off`, `yes/no`, `1/0`, `true/false`

.. _lottery-command-lottoset-info:

""""
info
""""

**Syntax**

.. code-block:: none

    [p]lottoset info 

**Description**

View configured settings
