.. _talk:

====
Talk
====

| This is the cog guide for the talk cog.
| You will find detailed docs about usage and commands.

``[p]`` is considered as your prefix.

.. note:: To use this cog, load it by typing this::

        [p]load talk


.. _talk-usage:

-----
Usage
-----

Talk as the bot


.. _talk-commands:

--------
Commands
--------

.. _talk-command-talk:

^^^^
talk
^^^^

| **Permissions**
|
| *User* -
| Bot Mod or Manage Messages

**Syntax**

.. code-block:: none

    [p]talk <message>

**Description**

Send a message as the bot

**Arguments**

<message> - The message content to send as the bot

.. _talk-command-talkm:

^^^^
talkm
^^^^

| **Permissions**
|
| *User* -
| Bot Mod or Manage Messages

**Syntax**

.. code-block:: none

    [p]talkm <message>

**Description**

Send a message as the bot, with mentions enabled

**Arguments**

<message> - The message content to send as the bot

.. _talk-command-talkd:

^^^^
talkd
^^^^

| **Permissions**
|
| *User* -
| Bot Mod or Manage Messages

**Syntax**

.. code-block:: none

    [p]talkd <message>

**Description**

Send a message as the bot, but delete the command message

**Arguments**

<message> - The message content to send as the bot

.. _talk-command-talkmd:

^^^^
talkmd
^^^^

| **Permissions**
|
| *User* -
| Bot Mod or Manage Messages

**Syntax**

.. code-block:: none

    [p]talkmd <message>

**Description**

Send a message as the bot, with mentions enabled and delete the command message

**Arguments**

<message> - The message content to send as the bot

.. _talk-command-talkset:

^^^^^^^
talkset
^^^^^^^

| **Permissions**
|
| *User* -
| Bot Admin or Manage Guild

**Description**

Configure settings

.. _talk-command-talkset-everyone:

""""
everyone
""""

| **Permissions**
|
| *User* -
| Bot Admin or Manage Guild

**Syntax**

.. code-block:: none

    [p]talkset everyone [value]

**Description**

Set the ability to mass mention using `everyone` or `here`

**Arguments**

[value] - Pass `true` or `false` to set it. Pass nothing to see the current setting
