.. _kill:

====
Kill
====

| This is the cog guide for the kill cog.
| You will find detailed docs about usage and commands.

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

**Arguments**

<user> - You can either mention the member, provide its ID, its exact name with the tag or not, or its nickname enclosed in quotes if there are spaces.

.. _kill-command-killset:

^^^^^^^
killset
^^^^^^^

| **Permissions**
|
| *User* -
| Bot Admin or Manage Guild

**Description**

Configure the kill messages

.. _kill-command-killset-list:

""""
list
""""

| **Permissions**
|
| *User* -
| Bot Admin or Manage Guild
|
| *Bot* -
| Embed Links

**Syntax**

.. code-block:: none

    [p]killset list

**Description**

List all the kill messages

.. _kill-command-killset-bot:

"""
bot
"""

| **Permissions**
|
| *User* -
| Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset bot <msg>

**Description**

Sets the message for killing the bot

**Arguments**

<msg> - The message you want to set as the Bot Kill message

**Context Parameters**

You can enhance your message by leaving spaces for the bot to substitute.

+-----------+----------------------------------------------------+
| Argument  | Substitute                                         |
+===========+====================================================+
| {killer}  | The user who called the command, as a Mention      |
+-----------+----------------------------------------------------+
| {killer2} | The user who called the command, as italic text    |
+-----------+----------------------------------------------------+
| {victim}  | The user is passed to the command, as a Mention    |
+-----------+----------------------------------------------------+
| {victim2} | The user is passed to the command, as italic text  |
+-----------+----------------------------------------------------+

.. _kill-command-killset-self:

""""
self
""""

| **Permissions**
|
| *User* -
| Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset self <msg>

**Description**

Sets the message for killing yourself

**Arguments**

<msg> - The message you want to set as the Self Kill message

**Context Parameters**

You can enhance your message by leaving spaces for the bot to substitute.

+-----------+----------------------------------------------------+
| Argument  | Substitute                                         |
+===========+====================================================+
| {killer}  | The user who called the command, as a Mention      |
+-----------+----------------------------------------------------+
| {killer2} | The user who called the command, as italic text    |
+-----------+----------------------------------------------------+
| {victim}  | The user is passed to the command, as a Mention    |
+-----------+----------------------------------------------------+
| {victim2} | The user is passed to the command, as italic text  |
+-----------+----------------------------------------------------+

.. _kill-command-killset-add:

"""
add
"""

| **Permissions**
|
| *User* -
| Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset add <msg>

**Description**

Add a new kill message.

**Arguments**

<msg> - The message you want to add to the Kill Messages

**Context Parameters**

You can enhance your message by leaving spaces for the bot to substitute.

+-----------+----------------------------------------------------+
| Argument  | Substitute                                         |
+===========+====================================================+
| {killer}  | The user who called the command, as a Mention      |
+-----------+----------------------------------------------------+
| {killer2} | The user who called the command, as italic text    |
+-----------+----------------------------------------------------+
| {victim}  | The user is passed to the command, as a Mention    |
+-----------+----------------------------------------------------+
| {victim2} | The user is passed to the command, as italic text  |
+-----------+----------------------------------------------------+

.. _kill-command-killset-delete:

""""""
delete
""""""

| **Permissions**
|
| *User* -
| Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]killset delete <num>

**Description**

Removes a kill message. Use `[p]killset list` to for the numbers
