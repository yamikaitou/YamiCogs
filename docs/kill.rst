.. _kill:

====
Kill
====

This is the cog guide for the kill cog. You will
find detailed docs about usage and commands.

``[p]`` is considered as your prefix.

.. note:: To use this cog, load it by typing this::

        [p]load kill

.. _kill-usage:

-----
Usage
-----

Kill people in interesting ways


.. _kill-commands:

--------
Commands
--------

.. _kill-command-kill:

^^^^
kill
^^^^

**Syntax**

.. code-block:: none

    [p]kill <user>

**Description**

Kill a user in a random way

.. _kill-command-killset:

^^^^^^^
killset
^^^^^^^

**User Permissions**

Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset 

**Description**

Configure the kill messages

.. _kill-command-killset-list:

""""
list
""""

**User Permissions**

Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset list 

**Description**

List all the kill messages

.. _kill-command-killset-bot:

"""
bot
"""

**User Permissions**

Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset bot <msg>

**Description**

Sets the message for killing the bot
{killer} and {victim} will be replaced with a users mention
{killer2} and {victim2} will be replaced with a users name in italics

.. _kill-command-killset-add:

"""
add
"""

**User Permissions**

Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset add <msg>

**Description**

Add a new kill message.
{killer} and {victim} will be replaced with a users mention
{killer2} and {victim2} will be replaced with a users name in italics

.. _kill-command-killset-self:

""""
self
""""

**User Permissions**

Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset self <msg>

**Description**

Sets the message for killing yourself
{killer} and {victim} will be replaced with a users mention
{killer2} and {victim2} will be replaced with a users name in italics

.. _kill-command-killset-delete:

""""""
delete
""""""

**User Permissions**

Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset delete <num>

**Description**

Removes a kill message. Use `[p]killset list` to for the numbers
