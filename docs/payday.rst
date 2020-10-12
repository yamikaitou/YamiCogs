.. _payday:

======
PayDay
======

This is the cog guide for the payday cog. You will
find detailed docs about usage and commands.

``[p]`` is considered as your prefix.

.. note:: To use this cog, load it by typing this::

        [p]load payday

.. note:: 
    Setting the amount of credits for any option to 0 will disable the command.
    
    By default, all options are set to 0. 
    
    Also, every user will be able to claim every available option on their first attempt.

.. _payday-usage:

-----
Usage
-----

Customizable PayDay system


.. _payday-commands:

--------
Commands
--------

.. _payday-command-freecredits:

^^^^^^^^^^^
freecredits
^^^^^^^^^^^

**Description**

Get some free more currency.

.. _payday-command-freecredits-times:

"""""
times
"""""

**Syntax**

.. code-block:: none

    [p]freecredits times 

**Description**

Display remaining time for all options

.. _payday-command-freecredits-all:

"""
all
"""

**Syntax**

.. code-block:: none

    [p]freecredits all 

**Description**

Claim all available freecredits

.. _payday-command-freecredits-hourly:

""""""
hourly
""""""

**Syntax**

.. code-block:: none

    [p]freecredits hourly 

**Description**

Get some free currency every hour

.. _payday-command-freecredits-daily:

"""""
daily
"""""

**Syntax**

.. code-block:: none

    [p]freecredits daily 

**Description**

Get some free currency every day

.. _payday-command-freecredits-weekly:

""""""
weekly
""""""

**Syntax**

.. code-block:: none

    [p]freecredits weekly 

**Description**

Get some free currency every week (7 days)

.. _payday-command-freecredits-monthly:

"""""""
monthly
"""""""

**Syntax**

.. code-block:: none

    [p]freecredits monthly 

**Description**

Get some free currency every month (30 days)

.. _payday-command-freecredits-quarterly:

"""""""""
quarterly
"""""""""

**Syntax**

.. code-block:: none

    [p]freecredits quarterly 

**Description**

Get some free currency every quarter (122 days)

.. _payday-command-freecredits-yearly:

""""""
yearly
""""""

**Syntax**

.. code-block:: none

    [p]freecredits yearly 

**Description**

Get some free currency every year (365 days)

.. _payday-command-pdconfig:

^^^^^^^^
pdconfig
^^^^^^^^

**User Permissions**

Bot Admin or Administrator

**Description**

Configure the `freecredits` options

.. _payday-command-pdconfig-settings:

""""""""
settings
""""""""

**User Permissions**

Bot Admin or Administrator

**Syntax**

.. code-block:: none

    [p]pdconfig settings 

**Description**

Print the `freecredits` options

.. _payday-command-pdconfig-hourly:

""""""
hourly
""""""

**User Permissions**

Bot Admin or Administrator

**Syntax**

.. code-block:: none

    [p]pdconfig hourly <value>
    [p]pdconfig hour <value>

**Description**

Configure the `hourly` options

**Arguments**

<value> - The amount of credits to grant the user. Setting this to 0 will disable the command

.. _payday-command-pdconfig-daily:

"""""
daily
"""""

**User Permissions**

Bot Admin or Administrator

**Syntax**

.. code-block:: none

    [p]pdconfig daily <value>
    [p]pdconfig day <value>

**Description**

Configure the `daily` options

**Arguments**

<value> - The amount of credits to grant the user. Setting this to 0 will disable the command

.. _payday-command-pdconfig-weekly:

""""""
weekly
""""""

**User Permissions**

Bot Admin or Administrator

**Syntax**

.. code-block:: none

    [p]pdconfig weekly <value>
    [p]pdconfig week <value>

**Description**

Configure the `weekly` options

**Arguments**

<value> - The amount of credits to grant the user. Setting this to 0 will disable the command

.. _payday-command-pdconfig-monthly:

"""""""
monthly
"""""""

**User Permissions**

Bot Admin or Administrator

**Syntax**

.. code-block:: none

    [p]pdconfig monthly <value>
    [p]pdconfig month <value>

**Description**

Configure the `monthly` options

**Arguments**

<value> - The amount of credits to grant the user. Setting this to 0 will disable the command

.. _payday-command-pdconfig-quarterly:

"""""""""
quarterly
"""""""""

**User Permissions**

Bot Admin or Administrator

**Syntax**

.. code-block:: none

    [p]pdconfig quarterly <value>
    [p]pdconfig quarter <value>

**Description**

Configure the `quarterly` options

**Arguments**

<value> - The amount of credits to grant the user. Setting this to 0 will disable the command

.. _payday-command-pdconfig-yearly:

""""""
yearly
""""""

**User Permissions**

Bot Admin or Administrator

**Syntax**

.. code-block:: none

    [p]pdconfig yearly <value>
    [p]pdconfig year <value>

**Description**

Configure the `yearly` options

**Arguments**

<value> - The amount of credits to grant the user. Setting this to 0 will disable the command
