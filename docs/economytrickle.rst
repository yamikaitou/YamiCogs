.. _economytrickle:

==============
EconomyTrickle
==============

This is the cog guide for the economytrickle cog. You will
find detailed docs about usage and commands.

``[p]`` is considered as your prefix.

.. note:: To use this cog, load it by typing this::

        [p]load economytrickle

.. _economytrickle-usage:

-----
Usage
-----

Trickle credits into your Economy

Most of the functionality of this cog happens in the background. The following commands are only to configure various settings for the background tasks.


.. _economytrickle-commands:

--------
Commands
--------

.. _economytrickle-command-economytrickle:

^^^^^^^^^^^^^^
economytrickle
^^^^^^^^^^^^^^

**Syntax**

.. code-block:: none

    [p]economytrickle 

**Description**

Configure various settings 

.. _economytrickle-command-economytrickle-info:

""""
info
""""

**Permissions**

*User* -
Global Bank - Bot Owner
Local Bank - Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]economytrickle info <number>

**Description**

Show the current settings 

.. _economytrickle-command-economytrickle-messages:

""""""""
messages
""""""""

**Permissions**

*User* -
Global Bank - Bot Owner
Local Bank - Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]economytrickle messages <number>

**Description**

Set the number of messages required to gain credits

Set the number to 0 to disable
Max value is 100

.. _economytrickle-command-economytrickle-credits:

"""""""
credits
"""""""

**Permissions**

*User* -
Global Bank - Bot Owner
Local Bank - Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]economytrickle credits <number>

**Description**

Set the number of credits to grant

Set the number to 0 to disable
Max value is 1000
