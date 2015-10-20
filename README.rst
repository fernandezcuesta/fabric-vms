**fabric_vms** - An addon for managing OpenVMS hosts with fabric_
###############################################################################

An addon for managing OpenVMS hosts with fabric_.
It wraps some of the methods available in Fabric enabling a user to execute
commands on an OpenVMS (tested with OVMS 7.3 and 8.x releases) host.

Install
*******************************************************************************
fabric_vms is on PyPI, so run:

.. code-block:: bash

    pip install fabric_vms

Compatibility
===============================================================================

There are no special requirements for the managed hosts, in particular
GNV_, vmspython_ are **not required**.

Only a subset of fabric_'s commands are ported, pull requests are more than
welcome.

As an additional feature, an extra module allows to run arbitrary commands on
`Xura <http://www.xura.com/>`__'s v5 SMSC platform `PML` interpreter if
imported as follows:

.. code-block:: py
    from fabric_vms import pml


Usage examples
*******************************************************************************
An example of ``fabfile`` using ``fabric_vms.safe_run()`` wrapper:

fabfile.py
===============================================================================
.. code-block:: py

    from fabric.api import env, task
    from fabric.utils import puts

    from fabric_vms import *
    from fabric_vms import safe_run as run  # override fabric_vms.run

    # Environmental settings
    env.use_ssh_config = True
    env.colorize_errors = True
    env.hosts = ['menta']
    env.user = 'SYSTEM'

    @task(default=True)
    def test():
        run('show device dsa /size /units=bytes')
        with cd('DSA0:[DELIVERABLES]'):
            run('md5sum packed_file.zip')

    @task
    def restart_snmp():
        run_clusterwide(['@SYS$STARTUP:TCPIP$SNMP_SHUTDOWN',
                         '@SYS$STARTUP:TCPIP$SNMP_STARTUP'])

    @task
    def stop_custom_services():
        run_clusterwide(['@SYS$STARTUP:STOP_SERVICES'])
        run('@T4$SYS:T4$STOP ALL')
        my_job = queue_job('HOUSEKEEPER')
        watchdog = queue_job('WATCHDOG')

        my_job.stop_queued_job()
        watchdog.stop_queued_job()

        # Check open files in DSA2, DSA3:
        for shadow_set in ['DSA2', 'DSA3']:
            open_files = lsof(shadow_set)
            if open_files:
                for _file in open_files:
                    puts(_file)


.. _fabric: http://www.fabfile.org
.. _GNV: http://gnv.sourceforge.net
.. _vmspython: http://www.vmspython.org
