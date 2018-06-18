vitess rpm builder
-------------------

This script is intended to build rpms for vitess.
See: https://vitess.io/

Currently using user/group vitess and the base directory
under /vt which is the typical location used by vitess.

A note on versioning
--------------------

As written vitess basically works out of git so doesn't have
very good version semantics. To compensate this for rpm building
I've made the following workaround which is to use the latest
tagged release in vitess and to follow that with the latest
commit on the master branch. This should be more flexible but
seems to work so far providing a version of the following at
the moment: v2.2.0.rc.1.20180614.110325.
