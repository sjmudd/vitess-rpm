# vitess rpm builder

This script is intended to build rpms for vitess.
* See: https://vitess.io/
* Currently using a user and group name `vitess` and the base directory under `/vt` which is the typical location used by vitess.

# A note on versioning

As written vitess basically works out of git so doesn't have
very good version semantics. To compensate this for rpm building
I've made the following workaround which is to use the latest
tagged release in vitess and to follow that with the latest
commit on the master branch. This should be more flexible but
seems to work so far providing a version of the following at
the moment: v2.2.0.rc.1.20180614.110325.

# How to use this

My layout is slightly odd but keeps source and specfiles in the same location.

From `~/.rpmmacros`:
```
# %_topdir defines the top directory to be used for RPM building purposes
%_topdir        %(echo $HOME)/RPM
%_sourcedir     %{_topdir}/SRC/%{name}
%_specdir       %{_topdir}/SRC/%{name}
%_tmppath       %{_topdir}/TMP
%_builddir      %{_topdir}/TMP
%_rpmdir        %{_topdir}/PKG
%_srcrpmdir     %{_topdir}/PKG
%_buildroot     %{_topdir}/TMP/%{name}-%{version}-root
# careful about the UPPER case
%_rpmfilename   %{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm
%tmpdir         %{_topdir}/TMP
```

# Building rpms

* Setup your rpm environment and checkout this repo under `~/RPM/PKG/vitess`.
* Build a tarball from the upstream git repo.
  * `./specfile_helper git2tar # builds a file like vitess-v2.2.0.rc.1.20180614.110325.tar.gz`
* Build the rpm:
  * `rpmbuild -ba vitess.spec` # to build the rpms

# Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

# Authors

* **Simon J Mudd** - *Initial work* - [Simon Mudd](https://github.com/sjmudd)
