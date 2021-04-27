.. _rolenotify:

==========
RoleNotify
==========

This is the cog guide for the rolenotify cog. You will
find detailed docs about usage and commands.

``[p]`` is considered as your prefix.

.. note:: To use this cog, load it by typing this::

        [p]load rolenotify

.. note:: 
    This cog requires the Members Intent

.. _rolenotify-usage:

-----
Usage
-----

Notify a user when they have a Role added or removed from them


.. _rolenotify-commands:

--------
Commands
--------

.. _rolenotify-command-rolenotify:

^^^^^^^^^^
rolenotify
^^^^^^^^^^

**User Permissions**

Bot Admin or Manage Roles

**Syntax**

.. code-block:: none

    [p]rolenotify 

**Description**

Configure RoleNotify

.. _rolenotify-command-rolenotify-channel:

"""""""
channel
"""""""

**User Permissions**

Bot Admin or Manage Roles

**Syntax**

.. code-block:: none

    [p]rolenotify channel <channel>

**Description**

Set the channel to output Role Notifications to

Pass 0 to clear the channel

.. _rolenotify-command-rolenotify-role:

""""
role
""""

**User Permissions**

Bot Admin or Manage Roles

**Syntax**

.. code-block:: none

    [p]rolenotify role 

**Description**

Configure settings for a Role

.. _rolenotify-command-rolenotify-role-info:

""""
info
""""

**User Permissions**

Bot Admin or Manage Roles

**Syntax**

.. code-block:: none

    [p]rolenotify role info <role>

**Description**

Display the configured settings for a Role

.. _rolenotify-command-rolenotify-role-method:

""""""
method
""""""

**User Permissions**

Bot Admin or Manage Roles

**Syntax**

.. code-block:: none

    [p]rolenotify role method <role> <method>

**Description**

Set the notification method

Valid options are `dm` and `channel`

.. _rolenotify-command-rolenotify-role-add:

"""
add
"""

**User Permissions**

Bot Admin or Manage Roles

**Syntax**

.. code-block:: none

    [p]rolenotify role add <role> <state>

**Description**

Set if the notification should be sent on Role Add

.. _rolenotify-command-rolenotify-role-remove:

""""""
remove
""""""

**User Permissions**

Bot Admin or Manage Roles

**Syntax**

.. code-block:: none

    [p]rolenotify role remove <role> <state>

**Description**

Set if the notification should be sent on Role Remove
