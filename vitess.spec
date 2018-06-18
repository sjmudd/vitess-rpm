###########################################################################
#                                                                         #
#                      build vitess rpms from source                      #
#                                                                         #
###########################################################################

%define whinge /usr/bin/logger -p system.info -t vitess/rpm
%define vtroot /vt
%define vtbin %{vtroot}/bin
%define vtweb %{vtroot}/web
# UID/GID setup              # Fix this to make it configurable from an input define setting
%define vitess_uid   299     # set unless vitess_uid is set in which case we use that value
%define vitess_gid   299     # set unless vitess_gid is set in which case we use that value
%define vitess_version v2.2.0.rc.1.20180614.110325
##define vitess_version %(cat %SOURCE_DIR/RPM_VERSION)

Name: vitess
Summary: Vitess is a database clustering system for horizontal scaling of MySQL.
Group: System Environment/Daemons
Release: 1
License: Apache License - Version 2.0, January 2004

#GitSource: https://github.com/vitessio/vitess.git
#GitBranch: master 
Source: https://github.com/vitessio/vitess-%{version}.tar.gz
Patch: dev.env.patch
Version: %vitess_version

BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

# Determine package build requirements
BuildRequires: golang >= 1.9
BuildRequires: git
BuildRequires: python-virtualenv
BuildRequires: MySQL-python
BuildRequires: automake
BuildRequires: bison
BuildRequires: curl
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: golang
BuildRequires: libtool
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: python-devel
BuildRequires: python-virtualenv
BuildRequires: unzip

#Requires: FIXME this needs filling in and is missing at the moment

%description
Vitess is a database solution for deploying, scaling and managing large
clusters of MySQL instances. It's architected to run as effectively in a
public or private cloud architecture as it does on dedicated hardware. It
combines and extends many important MySQL features with the scalability
of a NoSQL database. Vitess can help you with the following problems:

* Scaling a MySQL database by allowing you to shard it, while keeping
  application changes to a minimum.
* Migrating from baremetal to a private or public cloud.
* Deploying and managing a large number of MySQL instances.

Vitess includes compliant JDBC and Go database drivers using a native
query protocol. Additionally, it implements the MySQL server protocol
which is compatible with virtually any other language.

Vitess has been serving all YouTube database traffic since 2011, and
has now been adopted by many enterprises for their production needs.

############################################################################

%prep
umask 022
%setup
%patch -p1

############################################################################

%build
umask 022

# we have to move things about a bit
mv $RPM_BUILD_DIR/vitess-%{version} $RPM_BUILD_DIR/vitess-%{version}-TEMP
mkdir -p $RPM_BUILD_DIR/vitess-%{version}
cd ..
cd -

# move the exported tree to the right location
mkdir -p src/vitess.io
mv $RPM_BUILD_DIR/vitess-%{version}-TEMP src/vitess.io/vitess
cd src/vitess.io/vitess

export MYSQL_FLAVOR=MySQL56
export VT_MYSQL_ROOT=/usr

# Ensure that govendor will be found
export PATH=$RPM_BUILD_DIR/vitess-%{version}/bin:$PATH

# run the bootstrap script
./bootstrap.sh

. ./dev.env
make

############################################################################

%pre
umask 022

# create vitess user and groups if missing
/usr/bin/getent group vitess >/dev/null || {
    %whinge "Adding vitess group to system"
    %{_sbindir}/groupadd -r -g %{vitess_gid} -r vitess 
}

/usr/bin/getent passwd vitess >/dev/null || {
    %whinge "Adding vitess user to system"
    %{_sbindir}/useradd -d %{_var}/spool/vitess -s /bin/bash -u %{vitess_uid} -g vitess -M -r vitess
}

############################################################################

%post
umask 022

############################################################################

%postun
umask 022

############################################################################

%clean
umask 022
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && {
    rm -rf ${RPM_BUILD_ROOT}
} || :

############################################################################

%install
umask 022

[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && {
    rm -rf   ${RPM_BUILD_ROOT}
    mkdir -p ${RPM_BUILD_ROOT}
}

mkdir -p ${RPM_BUILD_ROOT}/vt/bin
for file in bin/*; do
	test -f $file && cp -p $file $RPM_BUILD_ROOT/vt/bin/
done
for d in src/vitess.io/vitess/web; do
	cp -pr $d $RPM_BUILD_ROOT/vt/
done

############################################################################

%files
%defattr(-, vitess, vitess)

# directories
%dir %attr(0755, vitess, vitess) %{vtweb}
%dir %attr(0755, vitess, vitess) %{vtbin}

# binaries
# - note there's currently other junk in here which should be removed
%attr(0755, vitess, vitess) %{vtbin}/automation_client
%attr(0755, vitess, vitess) %{vtbin}/automation_server
%attr(0755, vitess, vitess) %{vtbin}/consul
%attr(0755, vitess, vitess) %{vtbin}/cover
%attr(0755, vitess, vitess) %{vtbin}/demo
%attr(0755, vitess, vitess) %{vtbin}/etcd
%attr(0755, vitess, vitess) %{vtbin}/goimports
%attr(0755, vitess, vitess) %{vtbin}/golint
%attr(0755, vitess, vitess) %{vtbin}/govendor
%attr(0755, vitess, vitess) %{vtbin}/goyacc
%attr(0755, vitess, vitess) %{vtbin}/mockgen
%attr(0755, vitess, vitess) %{vtbin}/mysqlctl
%attr(0755, vitess, vitess) %{vtbin}/mysqlctld
%attr(0755, vitess, vitess) %{vtbin}/query_analyzer
%attr(0755, vitess, vitess) %{vtbin}/topo2topo
%attr(0755, vitess, vitess) %{vtbin}/unused
%attr(0755, vitess, vitess) %{vtbin}/vtaclcheck
%attr(0755, vitess, vitess) %{vtbin}/vtclient
%attr(0755, vitess, vitess) %{vtbin}/vtcombo
%attr(0755, vitess, vitess) %{vtbin}/vtctl
%attr(0755, vitess, vitess) %{vtbin}/vtctlclient
%attr(0755, vitess, vitess) %{vtbin}/vtctld
%attr(0755, vitess, vitess) %{vtbin}/vtexplain
%attr(0755, vitess, vitess) %{vtbin}/vtgate
%attr(0755, vitess, vitess) %{vtbin}/vtgateclienttest
%attr(0755, vitess, vitess) %{vtbin}/vtqueryserver
%attr(0755, vitess, vitess) %{vtbin}/vttablet
%attr(0755, vitess, vitess) %{vtbin}/vttestserver
%attr(0755, vitess, vitess) %{vtbin}/vttlstest
%attr(0755, vitess, vitess) %{vtbin}/vtworker
%attr(0755, vitess, vitess) %{vtbin}/vtworkerclient
%attr(0755, vitess, vitess) %{vtbin}/zk
%attr(0755, vitess, vitess) %{vtbin}/zkctl
%attr(0755, vitess, vitess) %{vtbin}/zkctld
%attr(0755, vitess, vitess) %{vtbin}/zksrv.sh
# web stuff
%attr(0644, vitess, vitess) %{vtweb}/vtctld/action-dialog.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld/actions.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld/api.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld/app.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld/app.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld/config.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld/index.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld/keyspaces.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld/keyspaces.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld/schema.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld/schema.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld/shard.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld/shard.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld/topo.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld/topo.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/.editorconfig
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/.gitignore
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/README.md
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/angular-cli.json
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/16e1d930cf13fb7a956372044b6d02d0.woff
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/38861cba61c66739c1452c3a71e39852.ttf
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/3d3a53586bd78d1069ae4b89a3b9aa98.svg
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/7e367be02cd17a96d513ab74846bafb3.woff2
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/9f916e330c478bbfa2a0dd6614042046.eot
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/favicon.ico
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/index.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/inline.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/main.0c2b4cdefdf7cd5afe91.bundle.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/main.0c2b4cdefdf7cd5afe91.bundle.js.gz
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/plotly-latest.min.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/primeui-ng-all.min.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/styles.07f8743f5392cfdfbcb5.bundle.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/app/styles.07f8743f5392cfdfbcb5.bundle.js.gz
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/config/karma.conf.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/config/protractor.conf.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/e2e/app.e2e-spec.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/e2e/app.po.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/e2e/tsconfig.json
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/e2e/typings.d.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/package.json
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/features.service.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/keyspace.service.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/keyspace.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/realtime-stats.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/shard.service.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/tablet-status.service.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/tablet.service.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/tablet.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/topo-data.service.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/topology-info.service.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/vtctl.service.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/api/workflow.service.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/app.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/app.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/app.component.spec.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/app.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/app.module.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/app.routes.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/dashboard.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/dashboard.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/dashboard.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/keyspace.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/keyspace.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/keyspace.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/shard.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/shard.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/shard.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/tablet.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/tablet.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/dashboard/tablet.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/index.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/rxjs-operators.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/schema/schema.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/schema/schema.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/schema/schema.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/breadcrumbs.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/breadcrumbs.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/breadcrumbs.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/can-deactivate-guard.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/dialog/dialog-content.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/dialog/dialog-settings.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/dialog/dialog.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/dialog/dialog.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/dialog/dialog.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/flags/flag.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/flags/keyspace.flags.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/flags/shard.flags.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/flags/tablet.flags.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/flags/workflow.flags.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/index.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/prepare-response.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/shared/proto.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/heatmap.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/heatmap.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/heatmap.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/status.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/status.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/status.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/tablet-popup.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/tablet-popup.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/tablet-popup.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/status/tablet.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/styles/vt.style.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/topo/topo-browser.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/topo/topo-browser.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/topo/topo-browser.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/workflows/node.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/workflows/workflow-list.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/workflows/workflow-list.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/workflows/workflow-list.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/workflows/workflow.component.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/workflows/workflow.component.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/app/workflows/workflow.component.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/assets/.gitignore
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/assets/.npmignore
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/environments/environment.dev.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/environments/environment.prod.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/environments/environment.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/favicon.ico
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/index.html
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/main.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/main.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/plotly-latest.min.js
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/polyfills.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/primeui-ng-all.min.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/styles.css
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/test.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/tsconfig.json
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/src/typings.d.ts
%attr(0644, vitess, vitess) %{vtweb}/vtctld2/tslint.json

############################################################################

%changelog
* Tue Jun 12 2018 Simon J Mudd <sjmudd@pobox.com> 0.20180612-1
  - first version
