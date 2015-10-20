# fabric_vms

An addon for managing OpenVMS hosts with [`Fabric`](http://www.fabfile.org).
It wraps some of the methods available in Fabric enabling a user to execute
commands on an OpenVMS (tested with OVMS 7.3 and 8.x releases) host.

There are no special requirements for the host, i.e.
[GNV](http://gnv.sourceforge.net/),
[vmspython](http://www.vmspython.org/doku.php) are **not required**.


As an additional feature, it allows to run arbitrary commands on
[Xura](http://www.xura.com/)'s v5 SMSC platform `PML` interpreter if the
appropriate submodule is imported:

```python
from fabric_vms import pml

