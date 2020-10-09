===
Kill
===

.. note:: These docs are for version **2.0**.
    Make sure you are on the latest version by typing ``[p]cog update``.

This is the docs for the ``kill`` cog. Everything you need is here.

``[p]`` is considered as your prefix.

------------
Installation
------------

To install the cog, first load the downloader cog, included
in core Red.::

    [p]load downloader

Then you will need to install the YamiCogs repository::

    [p]repo add yamicogs https://github.com/yamikaitou/YamiCogs

Finally, you can install the cog::

    [p]cog install yamicogs kill

.. warning:: The cog is not loaded by default. 
    To load it, type this::

        [p]load kill

-----
Usage
-----

Here's the list of all commands of this cog.

.. _command-killset:
    
~~~
killset
~~~

**Description**

Configure the kill messages

**User Permissions**

Bot Admin or Manage Guild


~~~
killset add
~~~

**Syntax**

.. code-block:: none

    [p]killset add <message>

**Description**

Add a new kill message

**Context Parameters**

You can enhance your message by leaving spaces for the bot to substitute.

+-----------+----------------------------------------------------+
| Argument  | Substitute                                         |
+===========+====================================================+
| {killer}  | The user who called the command, as a Mention      |
+-----------+----------------------------------------------------+
| {killer2} | The user who called the command, as normal text    |
+-----------+----------------------------------------------------+
| {victim}  | The user is passed to the command, as a Mention    |
+-----------+----------------------------------------------------+
| {victim2} | The user is passed to the command, as normal text  |
+-----------+----------------------------------------------------+

.. tip::

    **Examples**
    
    .. code-block:: none

        [p]killset add {killer} slayed {victim}
        [p]killset add {victim} has spontanously combusted

**Arguments**

* ``<message>``: The kill message you want to add

~~~
killset bot
~~~

**Syntax**

.. code-block:: none

    [p]killset bot <message>

**Description**

Set the message for when the user attempts to kill the bot
Default message is "Wow, how original. I laugh at your feeble attempt to kill me"

**Context Parameters**

You can enhance message by leaving spaces for the bot to substitute.

+-----------+----------------------------------------------------+
| Argument  | Substitute                                         |
+===========+====================================================+
| {killer}  | The user who called the command, as a Mention      |
+-----------+----------------------------------------------------+
| {killer2} | The user who called the command, as normal text    |
+-----------+----------------------------------------------------+
| {victim}  | The user is passed to the command, as a Mention    |
+-----------+----------------------------------------------------+
| {victim2} | The user is passed to the command, as normal text  |
+-----------+----------------------------------------------------+

.. tip::

    **Examples**
    
    .. code-block:: none

        [p]killset bot *My eyes glow bright red as he stares at the knife {victim} is holding. {victim} wets their pants and runs away screaming for their mommy*

**Arguments**

* ``<message>``: The kill message you want to set

~~~
killset list
~~~

**Syntax**

.. code-block:: none

    [p]killset list

**Description**

Shows the currently configured messages in an embed

**Bot Permissions**

Embed Links

.. tip::

    **Examples**
    
    .. code-block:: none

        [p]killset list

~~~
killset self
~~~

**Syntax**

.. code-block:: none

    [p]killset self <message>

**Description**

Set the message for when the user attempts to kill themself
Default message is "Per the Laws of Robotics, I cannot assist you in killing yourself"

**Context Parameters**

You can enhance message by leaving spaces for the bot to substitute.

+-----------+----------------------------------------------------+
| Argument  | Substitute                                         |
+===========+====================================================+
| {killer}  | The user who called the command, as a Mention      |
+-----------+----------------------------------------------------+
| {killer2} | The user who called the command, as normal text    |
+-----------+----------------------------------------------------+
| {victim}  | The user is passed to the command, as a Mention    |
+-----------+----------------------------------------------------+
| {victim2} | The user is passed to the command, as normal text  |
+-----------+----------------------------------------------------+

.. tip::

    **Examples**
    
    .. code-block:: none

        [p]killset self *Mourns the lose of {killer}

**Arguments**

* ``<message>``: The kill message you want to set