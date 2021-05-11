#
# spec file for package xen
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
# needssslcertforbuild


#Compat macro for new _fillupdir macro introduced in Nov 2017
%if ! %{defined _fillupdir}
  %define _fillupdir /var/adm/fillup-templates
%endif

# Tumbleweed now defines _libexecdir as /usr/libexec
# Keep it at the original location (/usr/lib) for backward compatibility
%define _libexecdir /usr/lib

Name:           xen
ExclusiveArch:  %ix86 x86_64 aarch64
%define changeset 41121
%define xen_build_dir xen-4.14.1-testing
#
%define with_gdbsx 0
%define with_dom0_support 0
%bcond_with    xen_oxenstored
%ifarch x86_64
%bcond_without xen_debug
%bcond_without xen_stubdom
%else
%bcond_with    xen_debug
%bcond_with    xen_stubdom
%endif
#
%define qemu_arch i386
%ifarch x86_64
%define with_gdbsx 1
%define with_dom0_support 1
%endif
#
%ifarch %arm aarch64
%define with_dom0_support 1
%define qemu_arch aarch64
%endif
#
%define xen_install_suffix %{nil}
%ifarch x86_64
%define xen_install_suffix .gz
%endif
# EFI requires gcc 4.6 or newer
# gcc46 is available in 12.1 or sles11sp2
# gcc47 is available in sles11sp3
# gcc48 is available in sles11sp4
# 12.2+ have gcc 4.7 as default compiler
%define with_gcc47 0
%define with_gcc48 0
%define _fwdefdir /etc/sysconfig/SuSEfirewall2.d/services
%systemd_requires
BuildRequires:  pkgconfig(libsystemd)
%define with_systemd_modules_load %{_prefix}/lib/modules-load.d
PreReq:         %fillup_prereq
%ifarch %arm aarch64
%if 0%{?suse_version} > 1320 || ( 0%{?suse_version} == 1315 && 0%{?sle_version} > 120200 )
BuildRequires:  libfdt-devel
%else
BuildRequires:  libfdt1-devel
%endif
%endif
BuildRequires:  bison
BuildRequires:  fdupes
%if 0%{?suse_version} > 1315
BuildRequires:  figlet
%endif
BuildRequires:  flex
BuildRequires:  glib2-devel
BuildRequires:  libaio-devel
BuildRequires:  libbz2-devel
BuildRequires:  libnl3-devel
BuildRequires:  libpixman-1-0-devel
BuildRequires:  libuuid-devel
BuildRequires:  libxml2-devel
BuildRequires:  libyajl-devel
%if %{with xen_stubdom}
%if 0%{?suse_version} < 1230
BuildRequires:  texinfo
%else
BuildRequires:  makeinfo
%endif
%endif
BuildRequires:  ncurses-devel
%if %{?with_dom0_support}0
%if %{with xen_oxenstored}
BuildRequires:  ocaml
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-runtime
%endif
%endif
BuildRequires:  acpica
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  xz-devel
BuildRequires:  pkgconfig(systemd)
%ifarch x86_64
BuildRequires:  gcc-32bit
BuildRequires:  gcc-c++
%if %{?with_gcc47}0
BuildRequires:  gcc47
%endif
%if %{?with_gcc48}0
BuildRequires:  gcc48
%endif
BuildRequires:  glibc-32bit
BuildRequires:  glibc-devel-32bit
BuildRequires:  makeinfo
%endif
%ifarch x86_64
BuildRequires:  pesign-obs-integration
%endif
Provides:       installhint(reboot-needed)

Version:        4.14.1_16_rpi4
Release:        0 
Summary:        Xen Virtualization: Hypervisor (aka VMM aka Microkernel)
License:        GPL-2.0-only
Group:          System/Kernel
Source0:        xen-4.14.1-testing-src.tar.bz2
Source1:        stubdom.tar.bz2
Source2:        ipxe.tar.bz2
Source3:        mini-os.tar.bz2
Source4:        xen-utils-0.1.tar.bz2
Source9:        xen.changes
Source10:       README.SUSE
Source11:       boot.xen
Source12:       boot.local.xenU
Source13:       xen-supportconfig
Source14:       logrotate.conf
Source21:       block-npiv-common.sh
Source22:       block-npiv
Source23:       block-npiv-vport
Source24:       block-dmmd
Source28:       init.xen_loop
# Xen API remote authentication sources
Source30:       etc_pam.d_xen-api
Source31:       xenapiusers
# Init script and sysconf file for pciback
Source34:       init.pciback
Source35:       sysconfig.pciback
Source36:       xen2libvirt.py
# Systemd service files
Source41:       xencommons.service
Source42:       xen-dom0-modules.service
Source10172:    xendomains-wait-disks.sh
Source10173:    xendomains-wait-disks.LICENSE
Source10174:    xendomains-wait-disks.README.md
Source10183:    xen_maskcalc.py
# For xen-libs
Source99:       baselibs.conf
# Upstream patches
Patch1:         5fca3b32-tools-libs-ctrl-fix-dumping-of-ballooned-guest.patch
Patch2:         5fedf9f4-x86-hpet_setup-fix-retval.patch
Patch3:         5ff458f2-x86-vPCI-tolerate-disabled-MSI-X-entry.patch
Patch4:         5ff71655-x86-dpci-EOI-regardless-of-masking.patch
Patch5:         5ffc58c4-ACPI-reduce-verbosity-by-default.patch
Patch6:         5ffc58e8-x86-ACPI-dont-overwrite-FADT.patch
Patch7:         600999ad-x86-dpci-do-not-remove-pirqs-from.patch
Patch8:         600ab341-x86-vioapic-EOI-check-IRR-before-inject.patch
Patch9:         6011bbc7-x86-timer-fix-boot-without-PIT.patch
Patch10:        6013e4bd-memory-bail-from-page-scrub-when-CPU-offline.patch
Patch11:        6013e546-x86-HVM-reorder-domain-init-error-path.patch
Patch12:        601d4396-x86-EFI-suppress-ld-2-36-debug-info.patch
Patch13:        602bd768-page_alloc-only-flush-after-scrubbing.patch
Patch14:        602cfe3d-IOMMU-check-if-initialized-before-teardown.patch
Patch15:        602e5a8c-gnttab-never-permit-mapping-transitive-grants.patch
Patch16:        602e5abb-gnttab-bypass-IOMMU-when-mapping-own-grant.patch
Patch17:        602ffae9-tools-libs-light-fix-xl-save--c-handling.patch
Patch18:        6037b02e-x86-EFI-suppress-ld-2-36-base-relocs.patch
Patch19:        60410127-gcc11-adjust-rijndaelEncrypt.patch
Patch20:        60422428-x86-shadow-avoid-fast-fault-path.patch
Patch21:        604b9070-VT-d-disable-QI-IR-before-init.patch
Patch22:        60535c11-libxl-domain-soft-reset.patch
Patch23:        60700077-x86-vpt-avoid-pt_migrate-rwlock.patch
Patch24:        60787714-x86-HPET-factor-legacy-replacement-mode-enabling.patch
Patch25:        60787714-x86-HPET-avoid-legacy-replacement-mode.patch
# libxc
Patch300:       libxc-sr-3cccdae45242dab27198b8e150be0c85acd5d3c9.patch
Patch301:       libxc-sr-readv_exact.patch
Patch302:       libxc-sr-add-xc_is_known_page_type.patch
Patch303:       libxc-sr-use-xc_is_known_page_type.patch
Patch304:       libxc-sr-page_type_has_stream_data.patch
Patch305:       libxc-sr-save-show_transfer_rate.patch
Patch306:       libxc-sr-arrays.patch
Patch307:       libxc-sr-batch_pfns.patch
Patch308:       libxc-sr-save-mfns.patch
Patch309:       libxc-sr-save-types.patch
Patch310:       libxc-sr-save-errors.patch
Patch311:       libxc-sr-save-iov.patch
Patch312:       libxc-sr-save-rec_pfns.patch
Patch313:       libxc-sr-save-guest_data.patch
Patch314:       libxc-sr-save-local_pages.patch
Patch315:       libxc-sr-restore-pfns.patch
Patch316:       libxc-sr-restore-types.patch
Patch317:       libxc-sr-restore-mfns.patch
Patch318:       libxc-sr-restore-map_errs.patch
Patch319:       libxc-sr-restore-populate_pfns-mfns.patch
Patch320:       libxc-sr-restore-populate_pfns-pfns.patch
Patch321:       libxc-sr-restore-read_record.patch
Patch322:       libxc-sr-restore-handle_buffered_page_data.patch
Patch323:       libxc-sr-restore-handle_incoming_page_data.patch
Patch324:       libxc-bitmap-50a5215f30e964a6f16165ab57925ca39f31a849.patch
Patch325:       libxc-bitmap-longs.patch
Patch326:       libxc-bitmap-long.patch
# Our platform specific patches
Patch400:       xen-destdir.patch
Patch401:       vif-bridge-no-iptables.patch
Patch402:       vif-bridge-tap-fix.patch
Patch403:       xl-conf-default-bridge.patch
Patch404:       xl-conf-disable-autoballoon.patch
Patch405:       xen-arch-kconfig-nr_cpus.patch
Patch406:       suse-xendomains-service.patch
Patch407:       replace-obsolete-network-configuration-commands-in-s.patch
Patch408:       disable-building-pv-shim.patch
Patch409:       xenstore-launch.patch
Patch410:       ignore-ip-command-script-errors.patch
# Needs to go upstream
Patch420:       suspend_evtchn_lock.patch
Patch422:       stubdom-have-iovec.patch
Patch423:       vif-route.patch
Patch424:       gcc11-fixes.patch
# Other bug fixes or features
Patch451:       xenconsole-no-multiple-connections.patch
Patch452:       hibernate.patch
Patch453:       stdvga-cache.patch
Patch454:       ipxe-enable-nics.patch
Patch456:       pygrub-boot-legacy-sles.patch
Patch457:       pygrub-handle-one-line-menu-entries.patch
Patch458:       aarch64-rename-PSR_MODE_ELxx-to-match-linux-headers.patch
Patch459:       aarch64-maybe-uninitialized.patch
Patch461:       libxl.max_event_channels.patch
Patch462:       libxc.sr.superpage.patch
Patch463:       libxl.add-option-to-disable-disk-cache-flushes-in-qdisk.patch
Patch464:       libxl.pvscsi.patch
Patch465:       xen.libxl.dmmd.patch
Patch466:       libxl.set-migration-constraints-from-cmdline.patch
Patch467:       xenstore-run-in-studomain.patch
Patch468:       libxl.fix-libacpi-dependency.patch
Patch469:       libxl.helper_done-crash.patch
Patch470:       libxl.LIBXL_HOTPLUG_TIMEOUT.patch
Patch471:       libxc.migrate_tracking.patch
# python3 conversion patches
Patch500:       build-python3-conversion.patch
Patch501:       migration-python3-conversion.patch
Patch502:       bin-python3-conversion.patch
# Hypervisor and PV driver Patches
Patch600:       xen.bug1026236.suse_vtsc_tolerance.patch
Patch601:       x86-ioapic-ack-default.patch
Patch602:       x86-cpufreq-report.patch
Patch603:       xenwatchdogd-options.patch
Patch604:       xenwatchdogd-restart.patch
Patch621:       xen.build-compare.doc_html.patch
Patch623:       ipxe-no-error-logical-not-parentheses.patch
Patch624:       ipxe-use-rpm-opt-flags.patch
# Build patches
Patch99996:     xen.stubdom.newlib.patch
Patch99999:     reproducible.patch
Patch100000:    xen-dt-generation-failed.patch

URL:            http://www.cl.cam.ac.uk/Research/SRG/netos/xen/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%define pyver %(python3 -c "import sys; print(sys.version[:3])")

%description
Xen is a virtual machine monitor for x86 that supports execution of
multiple guest operating systems with unprecedented levels of
performance and resource isolation.

This package contains the Xen Hypervisor. (tm)

[Hypervisor is a trademark of IBM]

%package libs
Summary:        Xen Virtualization: Libraries
License:        GPL-2.0-only
Group:          System/Kernel

%description libs
Xen is a virtual machine monitor for x86 that supports execution of
multiple guest operating systems with unprecedented levels of
performance and resource isolation.

This package contains the libraries used to interact with the Xen
virtual machine monitor.

In addition to this package you need to install xen and xen-tools
to use Xen.


Authors:
--------
    Ian Pratt <ian.pratt@cl.cam.ac.uk>


%if %{?with_dom0_support}0

%package tools
Summary:        Xen Virtualization: Control tools for domain 0
License:        GPL-2.0-only
Group:          System/Kernel
%ifarch x86_64
%if 0%{?suse_version} >= 1315
Requires:       grub2-x86_64-xen
%endif
Recommends:     qemu-ovmf-x86_64
Requires:       qemu-x86
%endif
%ifarch %arm aarch64
Requires:       qemu-arm
%endif
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Recommends:     multipath-tools
Requires:       python3
Requires:       python3-curses
%ifarch %{ix86} x86_64
Requires:       qemu-seabios
%endif
# subpackage existed in 10.3
Provides:       xen-tools-ioemu = %{version}
Obsoletes:      xen-tools-ioemu < %{version}
Conflicts:      libvirt < 1.0.5

%description tools
Xen is a virtual machine monitor for x86 that supports execution of
multiple guest operating systems with unprecedented levels of
performance and resource isolation.

This package contains the control tools that allow you to start, stop,
migrate, and manage virtual machines.

In addition to this package you need to install xen and xen-libs
to use Xen.


Authors:
--------
    Ian Pratt <ian.pratt@cl.cam.ac.uk>


%ifarch x86_64
%package tools-xendomains-wait-disk
Summary:        Adds a new xendomains-wait-disks.service
License:        GPL-3.0-or-later
Group:          System/Kernel
Requires:       %{name}-tools = %{version}-%{release}
Requires:       coreutils
Requires:       sed
Requires:       vim
BuildArch:      noarch

%description tools-xendomains-wait-disk
This package adds a new service named xendomains-wait-disks.service,
that simply calls xendomains-wait-disks. xendomains-wait-disks script
loops checking for the presence of every disk used by domU that
xendomains.service will try to launch. The script returns when
all disks become available or xendomains-wait-disks.service expires.

xendomains-wait-disks.service has the same dependencies as
xendomains.service, but it adds itself as a Wanted service for xendomains.
If xendomains-wait-disks.service fails, xendomains.service is launched anyway.

https://github.com/luizluca/xen-tools-xendomains-wait-disk
%endif

%endif

%package tools-domU
Summary:        Xen Virtualization: Control tools for domain U
License:        GPL-2.0-only
Group:          System/Kernel
Conflicts:      %{name}-tools
Requires:       %{name}-libs = %{version}-%{release}

%description tools-domU
Xen is a virtual machine monitor for x86 that supports execution of
multiple guest operating systems with unprecedented levels of
performance and resource isolation.

This package contains tools that allow unprivileged domains to query
the virtualized environment.



Authors:
--------
    Ian Pratt <ian.pratt@cl.cam.ac.uk>

%package devel
Summary:        Xen Virtualization: Headers and libraries for development
License:        GPL-2.0-only
Group:          System/Kernel
Requires:       %{name}-libs = %{version}
Requires:       libuuid-devel

%description devel
Xen is a virtual machine monitor for x86 that supports execution of
multiple guest operating systems with unprecedented levels of
performance and resource isolation.

This package contains the libraries and header files needed to create
tools to control virtual machines.



Authors:
--------
    Ian Pratt <ian.pratt@cl.cam.ac.uk>

%if %{?with_dom0_support}0

%package doc-html
Summary:        Xen Virtualization: HTML documentation
License:        GPL-2.0-only
Group:          Documentation/HTML

%description doc-html
Xen is a virtual machine monitor for x86 that supports execution of
multiple guest operating systems with unprecedented levels of
performance and resource isolation.

xen-doc-html contains the online documentation in HTML format. Point
your browser at file:/usr/share/doc/packages/xen/html/



Authors:
--------
    Ian Pratt <ian.pratt@cl.cam.ac.uk>
%endif

%prep
%setup -q -n %xen_build_dir -a 1 -a 2 -a 3 -a 4
%autosetup -D -T -n %xen_build_dir -p1

%build
%define _lto_cflags %{nil}

# we control the version info of this package
# to gain control of filename of xen.gz
XEN_VERSION=%{version}
XEN_VERSION=${XEN_VERSION%%%%.*}
XEN_SUBVERSION=%{version}
XEN_SUBVERSION=${XEN_SUBVERSION#*.}
XEN_SUBVERSION=${XEN_SUBVERSION%%%%.*}
XEN_EXTRAVERSION="%version-%release"
XEN_EXTRAVERSION="${XEN_EXTRAVERSION#*.}"
XEN_EXTRAVERSION="${XEN_EXTRAVERSION#*.}"
# remove trailing B_CNT to reduce build-compare noise
XEN_EXTRAVERSION="${XEN_EXTRAVERSION%%.*}"
XEN_FULLVERSION="$XEN_VERSION.$XEN_SUBVERSION.$XEN_EXTRAVERSION"
XEN_BUILD_DATE="`date -u -d '1970-01-01'`"
XEN_BUILD_TIME="`date -u -d '1970-01-01' +%%T`"
SMBIOS_REL_DATE="`date -u -d '1970-01-01' +%%m/%%d/%%Y`"
RELDATE="`date -u -d '1970-01-01' '+%%d %%b %%Y'`"
if test -r %{S:9}
then
	XEN_BUILD_DATE="` date -u -d \"$(sed -n '/@/{s/ - .*$//p;q}' %{S:9})\" `"
	XEN_BUILD_TIME="` date -u -d \"$(sed -n '/@/{s/ - .*$//p;q}' %{S:9})\" +%%T`"
	SMBIOS_REL_DATE="` date -u -d \"$(sed -n '/@/{s/ - .*$//p;q}' %{S:9})\" +%%m/%%d/%%Y`"
	RELDATE="` date -u -d \"$(sed -n '/@/{s/ - .*$//p;q}' %{S:9})\" '+%%d %%b %%Y'`"
fi
cat > .our_xenversion <<_EOV_
export WGET=$(type -P false)
export FTP=$(type -P false)
export GIT=$(type -P false)
%ifarch aarch64
# GCC10+ enables outline-atomics option by default and breaks the build, so disable it
%if 0%{?suse_version} >= 1550
export CFLAGS="%{optflags} -mno-outline-atomics"
%endif
%endif
export EXTRA_CFLAGS_XEN_TOOLS="%{optflags}"
export EXTRA_CFLAGS_QEMU_TRADITIONAL="%{optflags}"
export SMBIOS_REL_DATE="$SMBIOS_REL_DATE"
export RELDATE="$RELDATE"
XEN_VERSION=$XEN_VERSION
XEN_SUBVERSION=$XEN_SUBVERSION
XEN_EXTRAVERSION=$XEN_EXTRAVERSION
XEN_FULLVERSION=$XEN_FULLVERSION
_EOV_
source ./.our_xenversion
echo "%{changeset}" > xen/.scmversion
sed -i~ "
s/XEN_VERSION[[:blank:]]*=.*/XEN_VERSION = $XEN_VERSION/
s/XEN_SUBVERSION[[:blank:]]*=.*/XEN_SUBVERSION = $XEN_SUBVERSION/
s/XEN_EXTRAVERSION[[:blank:]]*?=.*/XEN_EXTRAVERSION = .$XEN_EXTRAVERSION/
s/XEN_FULLVERSION[[:blank:]]*=.*/XEN_FULLVERSION = $XEN_FULLVERSION/
s/XEN_BUILD_DATE[[:blank:]]*?=.*/XEN_BUILD_DATE = $XEN_BUILD_DATE/
s/XEN_BUILD_TIME[[:blank:]]*?=.*/XEN_BUILD_TIME = $XEN_BUILD_TIME/
s/XEN_BUILD_HOST[[:blank:]]*?=.*/XEN_BUILD_HOST = buildhost/
s/XEN_DOMAIN[[:blank:]]*?=.*/XEN_DOMAIN = suse.de/
" xen/Makefile
if diff -u xen/Makefile~ xen/Makefile
then
	: no changes?
fi

configure_flags=
configure_flags="--with-system-qemu=%{_bindir}/qemu-system-%{qemu_arch}"
%if %{with xen_stubdom}
configure_flags="${configure_flags} --enable-stubdom"
%else
# change the/our default to daemon due to lack of stubdom
sed -i~ 's/ XENSTORETYPE=domain$/ XENSTORETYPE=daemon/' tools/hotplug/Linux/launch-xenstore.in
configure_flags="${configure_flags} --disable-stubdom"
%endif
export PYTHON="/usr/bin/python3"
configure_flags="${configure_flags} --disable-qemu-traditional"
./configure \
        --disable-xen \
        --enable-tools \
        --enable-docs \
        --prefix=/usr \
        --exec_prefix=/usr \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --with-libexec-leaf-dir=%{name} \
        --datadir=%{_datadir} \
        --mandir=%{_mandir} \
        --includedir=%{_includedir} \
        --docdir=%{_defaultdocdir}/xen \
	--with-initddir=%{_initddir} \
	--with-rundir=%{_rundir} \
%if %{?with_dom0_support}0
%if %{with xen_oxenstored}
	--with-xenstored=oxenstored \
%endif
%endif
	--enable-systemd \
	--with-systemd=%{_unitdir} \
	--with-systemd-modules-load=%{with_systemd_modules_load} \
	--with-system-ovmf=%{_datadir}/qemu/ovmf-x86_64-ms.bin \
	--with-system-seabios=%{_datadir}/qemu/bios-256k.bin \
        ${configure_flags}
make -C tools/include/xen-foreign %{?_smp_mflags}
make %{?_smp_mflags}
%if %{?with_dom0_support}0
make -C tools/xen-utils-0.1 XEN_INTREE_BUILD=yes XEN_ROOT=$PWD
%endif
#

%install
source ./.our_xenversion
# tools
make \
	DESTDIR=%{buildroot} \
	SYSCONFIG_DIR=%{_fillupdir} \
	PKG_INSTALLDIR=%{_libdir}/pkgconfig \
	%{?_smp_mflags} \
	install
find %{buildroot} -ls
for i in %{buildroot}/%{_fillupdir}/*
do
	mv -v $i ${i%%/*}/sysconfig.${i##*/}
done

#
udev_rulesdir=%{buildroot}/%{_udevrulesdir}
tools_domU_dir=%{buildroot}/%{_libexecdir}/%{name}-tools-domU
mkdir -p ${udev_rulesdir}
mkdir -p ${tools_domU_dir}
#
tee ${udev_rulesdir}/80-%{name}-tools-domU.rules <<'_EOR_'
# XenSource, Inc. Xen Platform Device
SUBSYSTEM=="pci", ATTR{modalias}=="pci:v00005853d00000001sv00005853sd00000001bcFFsc80i00", TAG+="systemd", ENV{SYSTEMD_WANTS}+="%{name}-vcpu-watch.service"
_EOR_
#
tee %{buildroot}/%{_unitdir}/%{name}-vcpu-watch.service <<'_EOS_'
[Unit]
Description=Listen to CPU online/offline events from dom0 toolstack

[Service]
Type=simple
ExecStart=%{_libexecdir}/%{name}-tools-domU/%{name}-vcpu-watch.sh
Restart=always
RestartSec=2
_EOS_
#
tee %{buildroot}/%{_libexecdir}/%{name}-tools-domU/%{name}-vcpu-watch.sh <<'_EOS_'
#!/bin/bash
unset LANG
unset ${!LC_*}
echo "$0 starting" >&2
xenstore-watch cpu | while read
do
  : xenstore event: ${REPLY}
  case "${REPLY}" in
    cpu)
      : just started
      ;;
    cpu/[0-9]/availability|cpu/[0-9][0-9]/availability)
      vcpu="${REPLY%%/*}"
      vcpu="${vcpu#*/}"
      sysfs="/sys/devices/system/cpu/cpu${vcpu}/online"
      if test -f "${sysfs}"
      then
        availability="`xenstore-read \"${REPLY}\"`"
        case "${availability}" in
          online|offline)
            if test "${availability}" = "online"
            then
              new_sysfs_state=1
            else
              new_sysfs_state=0
            fi
            read cur_sysfs_state rest < "${sysfs}"
            if test "${cur_sysfs_state}" = "${new_sysfs_state}"
            then
              : the vcpu "${vcpu}" already has state "${availability}" via "${sysfs}"
            else
              : setting vcpu "${vcpu}" to "${availability}" via "${sysfs}"
              echo "setting vcpu ${vcpu} to ${availability}" >&2
              echo "${new_sysfs_state}" > "${sysfs}"
            fi
          ;;
        esac
      fi
    ;;
    *)
      : unhandled
    ;;
  esac
done
exit 1
_EOS_
chmod 755 %{buildroot}/%{_libexecdir}/%{name}-tools-domU/%{name}-vcpu-watch.sh
#
tee ${udev_rulesdir}/60-persistent-xvd.rules <<'_EOR_'
ACTION=="remove", GOTO="xvd_aliases_end"
SUBSYSTEM!="block", GOTO="xvd_aliases_end"
KERNEL=="xvd*[!0-9]", IMPORT{program}=="%{name}-tools-domU.sh --devpath %%p --devtype $env{DEVTYPE}"
KERNEL=="xvd*[0-9]",  IMPORT{program}=="%{name}-tools-domU.sh --devpath %%p --devtype $env{DEVTYPE}"
KERNEL=="xvd*[!0-9]", ENV{VBD_HD_SYMLINK}=="hd[a-d]", SYMLINK+="$env{VBD_HD_SYMLINK}"
KERNEL=="xvd*[0-9]",  ENV{VBD_HD_SYMLINK}=="hd[a-d]", SYMLINK+="$env{VBD_HD_SYMLINK}%%n"
LABEL="xvd_aliases_end"
_EOR_
#
tee ${udev_rulesdir}/80-%{name}-channel-setup.rules <<'_EOF_'
SUBSYSTEM=="xen", DEVPATH=="/devices/console-[0-9]", IMPORT{program}=="xen-channel-setup.sh $attr{nodename} %%n"

SUBSYSTEM=="xen", DEVPATH=="/devices/console-[0-9]", ENV{XEN_CHANNEL_NAME}=="org.qemu.guest_agent.0", TAG+="systemd", ENV{SYSTEMD_WANTS}+="qemu-ga@hvc%%n.service"
_EOF_
#
dracut_moduledir=%{buildroot}/usr/lib/dracut/modules.d/50%{name}-tools-domU
mkdir -p ${dracut_moduledir}
tee ${dracut_moduledir}/module-setup.sh <<'_EOS_'
#!/bin/bash
check() {
  require_binaries xenstore-read || return 1
  return 0
}

depends() {
  return 0
}
install() {
  inst_multiple xenstore-read
  inst_multiple ${udevdir}/%{name}-tools-domU.sh
  inst_rules 60-persistent-xvd.rules
}
_EOS_
chmod 755 ${dracut_moduledir}/module-setup.sh
#
udev_programdir=%{buildroot}/usr/lib/udev
mkdir -p ${udev_programdir}
tee ${udev_programdir}/%{name}-tools-domU.sh <<'_EOS_'
#!/bin/bash
set -e
devpath=
devtype=
dev=
while test "$#" -gt 0
do
  : "$1"
  case "$1" in
    --devpath) devpath=$2 ; shift ;;
    --devtype) devtype=$2 ; shift ;;
    *) echo "$0: Unknown option $1" >&2 ; exit 1 ;;
  esac
  shift
done
test -n "${devpath}" || exit 1
test -n "${devtype}" || exit 1
cd "/sys/${devpath}"
case "${devtype}" in
  partition) cd .. ;;
esac
cd -P device
d="${PWD##*/}"
d="${d/-/\/}"
backend="`xenstore-read device/${d}/backend`"
dev="`xenstore-read \"${backend}\"/dev`"
test -n "${dev}" && echo "VBD_HD_SYMLINK=${dev}"
_EOS_
#
tee ${udev_programdir}/%{name}-channel-setup.sh <<'_EOF_'
#!/bin/bash

if test "$#" -ne 2; then
    exit 1
fi

channel_path="$1"
channel_num="$2"

name="`xenstore-read \"$channel_path\"/name`"
test -z "$name" && exit 1

if test $name != "org.qemu.guest_agent.0"; then
    exit 1
fi

mkdir -p /dev/xenchannel
devname=/dev/xenchannel/$name
# Xen's console devices are used for channels. See xen-pv-channel(7)
# for more details
ln -sfn /dev/hvc$channel_num $devname

echo "XEN_CHANNEL_NAME=$name"
_EOF_
chmod 755 ${udev_programdir}/*.sh

# EFI
%if %{?with_dom0_support}0
arch=`uname -m`
install_xen()
{
    local ext=""
    find %{buildroot}/boot -ls
    if [ -n "$1" ]; then
        ext="-$1"
        mv %{buildroot}/boot/xen-syms-${XEN_FULLVERSION} \
           %{buildroot}/boot/xen-syms${ext}-${XEN_FULLVERSION}
        mv %{buildroot}/boot/xen-${XEN_FULLVERSION}%{xen_install_suffix} \
           %{buildroot}/boot/xen${ext}-${XEN_FULLVERSION}%{xen_install_suffix}
        if test -d %{buildroot}/%{_libdir}/efi; then
            mv %{buildroot}/%{_libdir}/efi/xen-${XEN_FULLVERSION}.efi %{buildroot}/%{_libdir}/efi/xen${ext}-${XEN_FULLVERSION}.efi
            ln -sf xen${ext}-${XEN_FULLVERSION}.efi %{buildroot}/%{_libdir}/efi/xen${ext}-$XEN_VERSION.$XEN_SUBVERSION.efi
            ln -sf xen${ext}-${XEN_FULLVERSION}.efi %{buildroot}/%{_libdir}/efi/xen${ext}-$XEN_VERSION.efi
            ln -sf xen${ext}-${XEN_FULLVERSION}.efi %{buildroot}/%{_libdir}/efi/xen${ext}.efi
            gzip -c %{buildroot}/boot/xen${ext}-${XEN_FULLVERSION}%{xen_install_suffix}
        fi
    elif test -d %{buildroot}/%{_libdir}/efi; then
        # Move the efi files to /usr/share/efi/<arch> (fate#326960)
        mkdir -p %{buildroot}/%{_datadir}/efi/$arch
        mv %{buildroot}/%{_libdir}/efi/xen*.efi %{buildroot}/%{_datadir}/efi/$arch/
        ln -s %{_datadir}/efi/$arch/xen-${XEN_FULLVERSION}.efi %{buildroot}/%{_libdir}/efi/xen.efi
    fi
    rm %{buildroot}/boot/xen-$XEN_VERSION.$XEN_SUBVERSION%{xen_install_suffix}
    rm %{buildroot}/boot/xen-$XEN_VERSION%{xen_install_suffix}
    rm %{buildroot}/boot/xen%{xen_install_suffix}
    # Do not link to links; grub cannot follow.
    ln -s xen${ext}-${XEN_FULLVERSION}%{xen_install_suffix} %{buildroot}/boot/xen${ext}-$XEN_VERSION.$XEN_SUBVERSION%{xen_install_suffix}
    ln -s xen${ext}-${XEN_FULLVERSION}%{xen_install_suffix} %{buildroot}/boot/xen${ext}-$XEN_VERSION%{xen_install_suffix}
    ln -s xen${ext}-${XEN_FULLVERSION}%{xen_install_suffix} %{buildroot}/boot/xen${ext}%{xen_install_suffix}
    if test -f xen-syms${ext}-${XEN_FULLVERSION}; then
        ln -sf xen-syms${ext}-${XEN_FULLVERSION} %{buildroot}/boot/xen-syms${ext}
    fi
    find %{buildroot}/boot -ls
}
export BRP_PESIGN_FILES="*.efi /lib/firmware"
CC=gcc
%if %{?with_gcc47}0
CC=gcc-4.7
%endif
%if %{?with_gcc48}0
CC=gcc-4.8
%endif
rm -fv xen/.config
%if %{with xen_debug}
echo CONFIG_DEBUG=y > xen/.config
echo "CONFIG_DOM0_MEM=\"1G+10%%,max:64G\"" >> xen/.config
yes '' | make -C xen oldconfig
make -C xen install DEBUG_DIR=/boot DESTDIR=%{buildroot} CC=$CC %{?_smp_mflags}
install_xen dbg
make -C xen clean
%endif
echo CONFIG_DEBUG=n > xen/.config
echo "CONFIG_DOM0_MEM=\"1G+10%%,max:64G\"" >> xen/.config
yes '' | make -C xen oldconfig
make -C xen install DEBUG_DIR=/boot DESTDIR=%{buildroot} CC=$CC %{?_smp_mflags}
install_xen
make -C xen clean
%endif

# On x86_64, qemu-xen was installed as /usr/lib/xen/bin/qemu-system-i386
# and advertised as the <emulator> in libvirt capabilities. Tool such as
# virt-install include <emulator> in domXML they produce, so we need to
# preserve the path. For x86_64, create a simple wrapper that invokes
# /usr/bin/qemu-system-i386
# Using qemu-system-x86_64 will result in an incompatible VM
%ifarch x86_64 aarch64
hardcoded_path_in_existing_domU_xml='%{_libexecdir}/%{name}/bin'
mkdir -vp %{buildroot}${hardcoded_path_in_existing_domU_xml}
tee %{buildroot}${hardcoded_path_in_existing_domU_xml}/qemu-system-%{qemu_arch} << 'EOF'
#!/bin/sh

exec %{_bindir}/qemu-system-%{qemu_arch} "$@"
EOF
chmod 0755 %{buildroot}${hardcoded_path_in_existing_domU_xml}/qemu-system-%{qemu_arch}

#
unit='%{_libexecdir}/%{name}/bin/xendomains-wait-disks'
mkdir -vp '%{buildroot}%{_libexecdir}/%{name}/bin'
cp -avL '%{SOURCE10172}' "%{buildroot}${unit}"
mkdir xendomains-wait-disk
cp -avL '%{SOURCE10173}' xendomains-wait-disk/LICENSE
cp -avL '%{SOURCE10174}' xendomains-wait-disk/README.md
tee %{buildroot}%{_unitdir}/xendomains-wait-disks.service <<'_EOS_'
[Unit]
Description=Xendomains - for those machines that will start, wait for their disks to apear
Requires=proc-xen.mount xenstored.service
After=proc-xen.mount xenstored.service xenconsoled.service xen-init-dom0.service
After=network-online.target
After=remote-fs.target
Before=xendomains.service
ConditionPathExists=/proc/xen/capabilities

[Service]
Type=oneshot
ExecStart=${unit}
TimeoutSec=5min

[Install]
WantedBy=xendomains.service
_EOS_
#
%endif

# Stubdom
%if %{?with_dom0_support}0
# Docs
mkdir -p %{buildroot}/%{_defaultdocdir}/xen/misc
for name in COPYING %SOURCE10 %SOURCE11 %SOURCE12; do
    install -m 644 $name %{buildroot}/%{_defaultdocdir}/xen/
done
for name in vtpm-platforms.txt crashdb.txt xenpaging.txt \
    xen-command-line.pandoc xenstore-paths.pandoc; do
    install -m 644 docs/misc/$name %{buildroot}/%{_defaultdocdir}/xen/misc/
done

mkdir -p %{buildroot}/etc/modprobe.d
install -m644 %SOURCE28 %{buildroot}/etc/modprobe.d/xen_loop.conf

# xen-utils
make -C tools/xen-utils-0.1 install DESTDIR=%{buildroot} XEN_INTREE_BUILD=yes XEN_ROOT=$PWD
install -m755 %SOURCE36 %{buildroot}/usr/sbin/xen2libvirt
install -m755 %SOURCE10183 %{buildroot}/usr/sbin/xen_maskcalc

rm -f %{buildroot}/etc/xen/README*
# Example config
mkdir -p %{buildroot}/etc/xen/{vm,examples,scripts}
mv %{buildroot}/etc/xen/xlexample* %{buildroot}/etc/xen/examples
rm -f %{buildroot}/etc/xen/examples/*nbd
install -m644 tools/xentrace/formats %{buildroot}/etc/xen/examples/xentrace_formats.txt

# Scripts
rm -f %{buildroot}/etc/xen/scripts/block-*nbd
install -m755 %SOURCE21 %SOURCE22 %SOURCE23 %SOURCE24 %{buildroot}/etc/xen/scripts/
mkdir -p %{buildroot}/usr/lib/supportconfig/plugins
install -m 755 %SOURCE13 %{buildroot}/usr/lib/supportconfig/plugins/xen

# Xen API remote authentication files
install -d %{buildroot}/etc/pam.d
install -m644 %SOURCE30 %{buildroot}/etc/pam.d/xen-api
install -m644 %SOURCE31 %{buildroot}/etc/xen/

# Logrotate
install -m644 -D %SOURCE14 %{buildroot}/etc/logrotate.d/xen

# Directories
mkdir -p %{buildroot}/var/lib/xenstored
mkdir -p %{buildroot}/var/lib/xen/images
mkdir -p %{buildroot}/var/lib/xen/jobs
mkdir -p %{buildroot}/var/lib/xen/save
mkdir -p %{buildroot}/var/lib/xen/dump
mkdir -p %{buildroot}/var/log/xen
mkdir -p %{buildroot}/var/log/xen/console

# Systemd
cp -bavL %{S:41} %{buildroot}/%{_unitdir}
bn=`basename %{S:42}`
cp -bavL %{S:42} %{buildroot}/%{_unitdir}/${bn}
mods="`
for conf in $(ls %{buildroot}/%{with_systemd_modules_load}/*.conf)
do
	grep -v ^# $conf
	echo -n > $conf
done
`"
> mods
for mod in $mods
do
	# load by alias, if possible, to handle pvops and xenlinux
	alias="$mod"
	case "$mod" in
		xen-evtchn) ;;
		xen-gntdev) ;;
		xen-gntalloc) ;;
		xen-blkback) alias='xen-backend:vbd' ;;
		xen-netback) alias='xen-backend:vif' ;;
		xen-pciback) alias='xen-backend:pci' ;;
		evtchn) unset alias ;;
		gntdev) unset alias ;;
		netbk) alias='xen-backend:vif' ;;
		blkbk) alias='xen-backend:vbd' ;;
		xen-scsibk) unset alias ;;
		usbbk) unset alias ;;
		pciback) alias='xen-backend:pci' ;;
		xen-acpi-processor) ;;
		blktap2) unset alias ;;
		*) ;;
	esac
	if test -n "${alias}"
	then
		echo "ExecStart=-/bin/sh -c 'modprobe $alias || :'" >> mods
	fi
done
sort -u mods | tee -a %{buildroot}/%{_unitdir}/${bn}
rm -rfv %{buildroot}/%{_initddir}
install -m644 %SOURCE35 %{buildroot}/%{_fillupdir}/sysconfig.pciback

# Clean up unpackaged files
find %{buildroot} \( \
	-name .deps -o \
	-name README.blktap -o \
	-name README.xenmon -o \
	-name target-x86_64.conf -o \
	-name xen-mfndump -o \
	-name qcow-create -o \
	-name img2qcow -o \
	-name qcow2raw -o \
	-name qemu-bridge-helper -o \
	-name qemu-img-xen -o \
	-name qemu-nbd-xen -o \
	-name palcode-clipper -o \
	-name xen-shim-syms -o \
	-name "*.dtb" -o \
	-name "openbios-*" -o \
	-name "petalogix*" -o \
	-name "ppc*" -o \
	-name "*.pyc" -o \
	-name "s390*" -o \
	-name "slof*" -o \
	-name "spapr*" -o \
	-name "*.egg-info" \) \
	-print -delete
# Wipe empty directories
if find %{buildroot}/usr -type d -print0 | xargs -0n1 rmdir -p 2>/dev/null
then
	:
fi

# "xl devd" has to be called manually in a driver domain
find %{buildroot} -name xendriverdomain.service -print -delete

# Create hardlinks for 3 .txt files and 1 .py
%fdupes %{buildroot}/%{_prefix}
find %{buildroot} -type f -size 0 -delete -print

%else
# !with_dom0_support

# 32 bit hypervisor no longer supported.  Remove dom0 tools.
rm -rf %{buildroot}/%{_datadir}/doc
rm -rf %{buildroot}/%{_datadir}/man
rm -rf %{buildroot}/%{_libexecdir}/%{name}
rm -rf %{buildroot}/%{_libdir}/python*
rm -rf %{buildroot}/%{_libdir}/ocaml*
rm -rf %{buildroot}/%{_unitdir}
rm -rf %{buildroot}/%{_fillupdir}
rm -rf %{buildroot}/%{with_systemd_modules_load}
rm -rf %{buildroot}/usr/sbin
rm -rf %{buildroot}/etc/xen
rm -rf %{buildroot}/var
rm -f  %{buildroot}/%{_sysconfdir}/bash_completion.d/xl.sh
rm -f  %{buildroot}/%{_sysconfdir}/init.d/xen*
rm -f  %{buildroot}/%{_bindir}/*trace*
rm -f  %{buildroot}/%{_bindir}/vchan-socket-proxy
rm -f  %{buildroot}/%{_bindir}/xenalyze*
rm -f  %{buildroot}/%{_bindir}/xenco*
rm -f  %{buildroot}/%{_bindir}/xen-cpuid
rm -f  %{buildroot}/%{_bindir}/pygrub
rm -f  %{buildroot}/%{_bindir}/remus
rm -f  %{buildroot}/usr/etc/qemu/target-x86_64.conf
rm -f  %{buildroot}/usr/libexec/qemu-bridge-helper
%endif

%if %{?with_dom0_support}0

%files
%defattr(-,root,root)
/boot/*
%{_libdir}/efi
%{_datadir}/efi

%endif

%files libs
%defattr(-,root,root)
%{_libdir}/xenfsimage/
%{_libdir}/*.so.*

%if %{?with_dom0_support}0

%files tools
%defattr(-,root,root)
/usr/bin/xenalyze
/usr/bin/xencons
/usr/bin/xenstore*
/usr/bin/pygrub
/usr/bin/vchan-socket-proxy
/usr/bin/xencov_split
/usr/bin/xentrace_format
%ifarch x86_64
/usr/bin/xen-cpuid
/usr/sbin/xen-ucode
%endif
/usr/sbin/xenbaked
/usr/sbin/xenconsoled
/usr/sbin/xencov
/usr/sbin/xenlockprof
/usr/sbin/xenmon
/usr/sbin/xenperf
/usr/sbin/xenpm
/usr/sbin/xenpmd
/usr/sbin/xenstored
/usr/sbin/xentop
/usr/sbin/xentrace
/usr/sbin/xentrace_setsize
/usr/sbin/xentrace_setmask
/usr/sbin/xenwatchdogd
/usr/sbin/flask-get-bool
/usr/sbin/flask-getenforce
/usr/sbin/flask-label-pci
/usr/sbin/flask-loadpolicy
/usr/sbin/flask-set-bool
/usr/sbin/flask-setenforce
%if %{?with_gdbsx}0
/usr/sbin/gdbsx
%endif
/usr/sbin/xl
/usr/sbin/xen2libvirt
/usr/sbin/xen_maskcalc
%ifarch %ix86 x86_64
/usr/sbin/xen-hptool
/usr/sbin/xen-hvmcrash
/usr/sbin/xen-hvmctx
/usr/sbin/xen-lowmemd
/usr/sbin/xen-kdd
%endif
/usr/sbin/xenhypfs
/usr/sbin/xen-list
/usr/sbin/xen-destroy
/usr/sbin/xen-livepatch
/usr/sbin/xen-diag
%dir %attr(700,root,root) /etc/xen
%dir /etc/xen/scripts
/etc/xen/scripts/block*
/etc/xen/scripts/external-device-migrate
/etc/xen/scripts/hotplugpath.sh
/etc/xen/scripts/launch-xenstore
/etc/xen/scripts/locking.sh
/etc/xen/scripts/logging.sh
/etc/xen/scripts/vif2
/etc/xen/scripts/vif-*
/etc/xen/scripts/vscsi
/etc/xen/scripts/xen-hotplug-*
/etc/xen/scripts/xen-network-common.sh
/etc/xen/scripts/xen-script-common.sh
/etc/xen/scripts/colo-proxy-setup
/etc/xen/scripts/remus-netbuf-setup
%dir /usr/lib/supportconfig
%dir /usr/lib/supportconfig/plugins
/usr/lib/supportconfig/plugins/xen
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/bin
%exclude %{_libexecdir}/%{name}-tools-domU
%ifarch x86_64
%{_libexecdir}/%{name}/boot
%exclude %{_libexecdir}/%{name}/bin/xendomains-wait-disks
%endif
%{_fillupdir}/sysconfig.pciback
%{_fillupdir}/sysconfig.xencommons
%{_fillupdir}/sysconfig.xendomains
%dir /var/lib/xen
%dir %attr(700,root,root) /var/lib/xen/images
%dir %attr(700,root,root) /var/lib/xen/save
%dir %attr(700,root,root) /var/lib/xen/dump
%ifarch %ix86 x86_64
%dir %attr(700,root,root) /var/lib/xen/xenpaging
%endif
%dir /var/lib/xenstored
%dir /var/log/xen
%dir /var/log/xen/console
%config /etc/logrotate.d/xen
/etc/xen/auto
%config /etc/xen/examples
%config /etc/xen/cpupool
%config /etc/xen/vm
%config(noreplace) /etc/xen/xenapiusers
%config(noreplace) /etc/xen/xl.conf
%config /etc/pam.d/xen-api
%config /etc/modprobe.d/xen_loop.conf
%config %{_unitdir}
%exclude %{_unitdir}/%{name}-vcpu-watch.service
%exclude %{_unitdir}/xendomains-wait-disks.service
%config %{with_systemd_modules_load}
%dir /etc/modprobe.d
/etc/bash_completion.d/xl.sh
%dir %{_libdir}/python%{pyver}/site-packages/grub
%dir %{_libdir}/python%{pyver}/site-packages/xen
%dir %{_libdir}/python%{pyver}/site-packages/xen/lowlevel
%dir %{_libdir}/python%{pyver}/site-packages/xen/migration
%{_libdir}/python%{pyver}/site-packages/grub/*
%{_libdir}/python%{pyver}/site-packages/xen/util.py
%{_libdir}/python%{pyver}/site-packages/xen/lowlevel/*
%{_libdir}/python%{pyver}/site-packages/xen/migration/*
%{_libdir}/python%{pyver}/site-packages/*.so
%dir %{_defaultdocdir}/xen
%{_defaultdocdir}/xen/COPYING
%{_defaultdocdir}/xen/README.SUSE
%{_defaultdocdir}/xen/boot.local.xenU
%{_defaultdocdir}/xen/boot.xen
%{_mandir}/man*/*

%if %{with xen_oxenstored}
/usr/sbin/oxenstored
/etc/xen/oxenstored.conf
%dir %{_libdir}/ocaml
%dir %{_libdir}/ocaml/xenbus
%dir %{_libdir}/ocaml/xenctrl
%dir %{_libdir}/ocaml/xeneventchn
%dir %{_libdir}/ocaml/xenlight
%dir %{_libdir}/ocaml/xenmmap
%dir %{_libdir}/ocaml/xenstore
%dir %{_libdir}/ocaml/xentoollog
%{_libdir}/ocaml/xenbus/META
%{_libdir}/ocaml/xenbus/*.so
%{_libdir}/ocaml/xenbus/*.cma
%{_libdir}/ocaml/xenbus/*.cmi
%{_libdir}/ocaml/xenbus/*.cmo
%{_libdir}/ocaml/xenctrl/META
%{_libdir}/ocaml/xenctrl/*.so
%{_libdir}/ocaml/xenctrl/*.cma
%{_libdir}/ocaml/xenctrl/*.cmi
%{_libdir}/ocaml/xeneventchn/META
%{_libdir}/ocaml/xeneventchn/*.so
%{_libdir}/ocaml/xeneventchn/*.cma
%{_libdir}/ocaml/xeneventchn/*.cmi
%{_libdir}/ocaml/xenlight/META
%{_libdir}/ocaml/xenlight/*.so
%{_libdir}/ocaml/xenlight/*.cma
%{_libdir}/ocaml/xenlight/*.cmi
%{_libdir}/ocaml/xenmmap/META
%{_libdir}/ocaml/xenmmap/*.so
%{_libdir}/ocaml/xenmmap/*.cma
%{_libdir}/ocaml/xenmmap/*.cmi
%{_libdir}/ocaml/xenstore/META
%{_libdir}/ocaml/xenstore/*.cma
%{_libdir}/ocaml/xenstore/*.cmi
%{_libdir}/ocaml/xenstore/*.cmo
%{_libdir}/ocaml/xentoollog/META
%{_libdir}/ocaml/xentoollog/*.so
%{_libdir}/ocaml/xentoollog/*.cma
%{_libdir}/ocaml/xentoollog/*.cmi
%endif

%ifarch x86_64
%files tools-xendomains-wait-disk
%license xendomains-wait-disk/LICENSE
%doc xendomains-wait-disk/README.md
%config %{_unitdir}/xendomains-wait-disks.service
%config %attr(0755,root,root) %{_libexecdir}/%{name}/bin/xendomains-wait-disks
%endif
# with_dom0_support
%endif

%posttrans -n %{name}-tools-domU
%{?regenerate_initrd_posttrans}

%files tools-domU
%defattr(-,root,root)
%ifarch %ix86 x86_64
/usr/bin/xen-detect
%exclude /usr/bin/xenstore-control
%endif
/usr/bin/xenstore*
%if %{?with_dom0_support}0
%config %{_unitdir}/%{name}-vcpu-watch.service
%endif
%{_libexecdir}/%{name}-tools-domU
/usr/lib/udev
/usr/lib/dracut

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%if %{?with_dom0_support}0
%if %{with xen_oxenstored}
%{_libdir}/ocaml/xenbus/*.a
%{_libdir}/ocaml/xenbus/*.cmx*
%{_libdir}/ocaml/xenctrl/*.a
%{_libdir}/ocaml/xenctrl/*.cmx*
%{_libdir}/ocaml/xeneventchn/*.a
%{_libdir}/ocaml/xeneventchn/*.cmx*
%{_libdir}/ocaml/xenlight/*.a
%{_libdir}/ocaml/xenlight/*.cmx*
%{_libdir}/ocaml/xenmmap/*.a
%{_libdir}/ocaml/xenmmap/*.cmx*
%{_libdir}/ocaml/xenstore/*.a
%{_libdir}/ocaml/xenstore/*.cmx*
%{_libdir}/ocaml/xentoollog/*.a
%{_libdir}/ocaml/xentoollog/*.cmx*
%endif
%endif
/usr/include/*
%{_libdir}/pkgconfig/xenlight.pc
%{_libdir}/pkgconfig/xlutil.pc
%{_libdir}/pkgconfig/xencall.pc
%{_libdir}/pkgconfig/xencontrol.pc
%{_libdir}/pkgconfig/xendevicemodel.pc
%{_libdir}/pkgconfig/xenevtchn.pc
%{_libdir}/pkgconfig/xenforeignmemory.pc
%{_libdir}/pkgconfig/xengnttab.pc
%{_libdir}/pkgconfig/xenguest.pc
%{_libdir}/pkgconfig/xenhypfs.pc
%{_libdir}/pkgconfig/xenstat.pc
%{_libdir}/pkgconfig/xenstore.pc
%{_libdir}/pkgconfig/xentoolcore.pc
%{_libdir}/pkgconfig/xentoollog.pc
%{_libdir}/pkgconfig/xenvchan.pc

%if %{?with_dom0_support}0

%files doc-html
%defattr(-,root,root)
%dir %{_defaultdocdir}/xen
%{_defaultdocdir}/xen/misc
%{_defaultdocdir}/xen/html

%post
if [ -x /sbin/update-bootloader ]; then
    /sbin/update-bootloader --refresh; exit 0
fi

%pre tools
%service_add_pre xencommons.service
%service_add_pre xendomains.service
%service_add_pre xen-watchdog.service
%service_add_pre xenstored.service
%service_add_pre xen-dom0-modules.service
%service_add_pre xenconsoled.service
%service_add_pre xen-init-dom0.service
%service_add_pre xen-qemu-dom0-disk-backend.service

%post tools
xen_tools_first_arg=$1
%{fillup_only -n xencommons xencommons}
%{fillup_only -n xendomains xendomains}
%service_add_post xencommons.service
%service_add_post xendomains.service
%service_add_post xen-watchdog.service
%service_add_post xenstored.service
%service_add_post xen-dom0-modules.service
%service_add_post xenconsoled.service
%service_add_post xen-init-dom0.service
%service_add_post xen-qemu-dom0-disk-backend.service

if [ -f /etc/default/grub ] && ! (/usr/bin/grep GRUB_CMDLINE_XEN /etc/default/grub >/dev/null); then
    echo '# Xen boot parameters for all Xen boots' >> /etc/default/grub
    echo 'GRUB_CMDLINE_XEN=""' >> /etc/default/grub
    echo '# Xen boot parameters for non-recovery Xen boots (in addition to GRUB_CMDLINE_XEN)' >> /etc/default/grub
    echo 'GRUB_CMDLINE_XEN_DEFAULT=""' >> /etc/default/grub
fi
if [ -f %{_datadir}/grub2/i386-xen/grub.xen ] && [ ! -f %{_libexecdir}/%{name}/boot/pvgrub32.bin ]; then
 ln -sv %{_datadir}/grub2/i386-xen/grub.xen             %{_libexecdir}/%{name}/boot/pvgrub32.bin
fi
if [ -f %{_datadir}/grub2/x86_64-xen/grub.xen ] && [ ! -f %{_libexecdir}/%{name}/boot/pvgrub64.bin ]; then
 ln -sv %{_datadir}/grub2/x86_64-xen/grub.xen             %{_libexecdir}/%{name}/boot/pvgrub64.bin
fi

%preun tools
%service_del_preun xencommons.service
%service_del_preun xendomains.service
%service_del_preun xen-watchdog.service
%service_del_preun xenstored.service
%service_del_preun xen-dom0-modules.service
%service_del_preun xenconsoled.service
%service_del_preun xen-init-dom0.service
%service_del_preun xen-qemu-dom0-disk-backend.service

%postun tools
%if %{defined service_del_postun_without_restart}
%service_del_postun_without_restart xencommons.service
%service_del_postun_without_restart xendomains.service
%service_del_postun_without_restart xen-watchdog.service
%service_del_postun_without_restart xenstored.service
%service_del_postun_without_restart xen-dom0-modules.service
%service_del_postun_without_restart xenconsoled.service
%service_del_postun_without_restart xen-init-dom0.service
%service_del_postun_without_restart xen-qemu-dom0-disk-backend.service
%else
export DISABLE_RESTART_ON_UPDATE=yes
%service_del_postun xencommons.service
%service_del_postun xendomains.service
%service_del_postun xen-watchdog.service
%service_del_postun xenstored.service
%service_del_postun xen-dom0-modules.service
%service_del_postun xenconsoled.service
%service_del_postun xen-init-dom0.service
%service_del_postun xen-qemu-dom0-disk-backend.service
%endif

%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%changelog
* Mon Apr 19 2021 carnold@suse.com
- bsc#1180491 - "Panic on CPU 0: IO-APIC + timer doesn't work!"
  60787714-x86-HPET-avoid-legacy-replacement-mode.patch
  60787714-x86-HPET-factor-legacy-replacement-mode-enabling.patch
- Upstream bug fixes (bsc#1027519)
  60410127-gcc11-adjust-rijndaelEncrypt.patch
  60422428-x86-shadow-avoid-fast-fault-path.patch
  604b9070-VT-d-disable-QI-IR-before-init.patch
  60535c11-libxl-domain-soft-reset.patch (Replaces xsa368.patch)
  60700077-x86-vpt-avoid-pt_migrate-rwlock.patch
* Thu Mar 25 2021 ohering@suse.de
- bsc#1137251 - Restore changes for xen-dom0-modules.service which
  were silently removed on 2019-10-17
* Fri Mar 12 2021 ohering@suse.de
- bsc#1177112 - Fix libxc.sr.superpage.patch
  The receiving side did detect holes in a to-be-allocated superpage,
  but allocated a superpage anyway. This resulted to over-allocation.
* Mon Mar  8 2021 ohering@suse.de
- bsc#1167608 - adjust limit for max_event_channels
  A previous change allowed an unbound number of event channels
  to make sure even large domUs can start of of the box.
  This may have a bad side effect in the light of XSA-344.
  Adjust the built-in limit based on the number of vcpus.
  In case this is not enough, max_event_channels=/maxEventChannels=
  has to be used to set the limit as needed for large domUs
  adjust libxl.max_event_channels.patch
* Fri Mar  5 2021 carnold@suse.com
- bsc#1183072 - VUL-0: CVE-2021-28687: xen: HVM soft-reset crashes
  toolstack (XSA-368). Also resolves,
  bsc#1179148 - kdump of HVM fails, soft-reset not handled by libxl
  bsc#1181989 - openQA job causes libvirtd to dump core when
  running kdump inside domain
  xsa368.patch
* Fri Feb 26 2021 jbeulich@suse.com
- bsc#1177204 - L3-Question: conring size for XEN HV's with huge
  memory to small. Inital Xen logs cut
  5ffc58c4-ACPI-reduce-verbosity-by-default.patch
- Upstream bug fixes (bsc#1027519)
  601d4396-x86-EFI-suppress-ld-2-36-debug-info.patch
  602bd768-page_alloc-only-flush-after-scrubbing.patch
  602cfe3d-IOMMU-check-if-initialized-before-teardown.patch
  602e5a8c-gnttab-never-permit-mapping-transitive-grants.patch
  602e5abb-gnttab-bypass-IOMMU-when-mapping-own-grant.patch
  6037b02e-x86-EFI-suppress-ld-2-36-base-relocs.patch
- bsc#1181921 - GCC 11: xen package fails
  gcc11-fixes.patch
* Tue Feb 23 2021 carnold@suse.com
- bsc#1182576 - L3: XEN domU crashed on resume when using the xl
  unpause command
  602ffae9-tools-libs-light-fix-xl-save--c-handling.patch
* Thu Feb 18 2021 carnold@suse.com
- Start using the %%autosetup macro to simplify patch management
  xen.spec
* Wed Feb 10 2021 carnold@suse.com
- bsc#1181921 - GCC 11: xen package fails
  gcc11-fixes.patch
- Drop gcc10-fixes.patch
* Tue Feb  2 2021 carnold@suse.com
- Upstream bug fixes (bsc#1027519)
  5fedf9f4-x86-hpet_setup-fix-retval.patch
  5ff458f2-x86-vPCI-tolerate-disabled-MSI-X-entry.patch
  5ff71655-x86-dpci-EOI-regardless-of-masking.patch
  5ffc58e8-x86-ACPI-dont-overwrite-FADT.patch
  600999ad-x86-dpci-do-not-remove-pirqs-from.patch (Replaces xsa360.patch)
  600ab341-x86-vioapic-EOI-check-IRR-before-inject.patch
  6013e4bd-memory-bail-from-page-scrub-when-CPU-offline.patch
  6013e546-x86-HVM-reorder-domain-init-error-path.patch
- bsc#1180491 - "Panic on CPU 0: IO-APIC + timer doesn't work!"
  6011bbc7-x86-timer-fix-boot-without-PIT.patch
* Thu Jan 21 2021 carnold@suse.com
- bsc#1181254 - VUL-0: xen: IRQ vector leak on x86 (XSA-360)
  xsa360.patch
* Wed Jan 13 2021 carnold@suse.com
- bsc#1180794 - bogus qemu binary path used when creating fv guest
  under xen
  xen.spec
* Wed Jan 13 2021 carnold@suse.com
- bsc#1180690 - L3-Question: xen: no needsreboot flag set
  Add Provides: installhint(reboot-needed) in xen.spec for libzypp
* Mon Jan  4 2021 ohering@suse.de
- Update libxl.set-migration-constraints-from-cmdline.patch
  Remove code which handled --max_factor. The total amount of
  transferred data is no indicator to trigger the final stop+copy.
  This should have been removed during upgrade to Xen 4.7.
  Fix off-by-one in --max_iters, it caused one additional copy cycle.
  Reduce default value of --max_iters from 5 to 2.
  The workload within domU will continue to produce dirty pages.
  It is unreasonable to expect any slowdown during migration.
  Now there is one initial copy of all memory, one instead of four
  iteration for dirty memory, and a final copy iteration prior move.
* Thu Dec 17 2020 carnold@suse.com
- Update to Xen 4.14.1 bug fix release (bsc#1027519)
  xen-4.14.1-testing-src.tar.bz2
  Contains the following recent security fixes
  bsc#1179516 XSA-359 - CVE-2020-29571
  bsc#1179514 XSA-358 - CVE-2020-29570
  bsc#1179513 XSA-356 - CVE-2020-29567
  bsc#1178963 XSA-355 - CVE-2020-29040
  bsc#1178591 XSA-351 - CVE-2020-28368
  bsc#1179506 XSA-348 - CVE-2020-29566
  bsc#1179502 XSA-325 - CVE-2020-29483
  bsc#1179501 XSA-324 - CVE-2020-29484
  bsc#1179498 XSA-322 - CVE-2020-29481
  bsc#1179496 XSA-115 - CVE-2020-29480
- Dropped patches contained in new tarball
  5f1a9916-x86-S3-put-data-sregs-into-known-state.patch
  5f21b9fd-x86-cpuid-APIC-bit-clearing.patch
  5f479d9e-x86-begin-to-support-MSR_ARCH_CAPS.patch
  5f4cf06e-x86-Dom0-expose-MSR_ARCH_CAPS.patch
  5f4cf96a-x86-PV-fix-SEGBASE_GS_USER_SEL.patch
  5f560c42-x86-PV-64bit-segbase-consistency.patch
  5f560c42-x86-PV-rewrite-segment-ctxt-switch.patch
  5f5b6b7a-hypfs-fix-custom-param-writes.patch
  5f607915-x86-HVM-more-consistent-IO-completion.patch
  5f6a002d-x86-PV-handle-MSR_MISC_ENABLE-correctly.patch
  5f6a0049-memory-dont-skip-RCU-unlock-in-acquire_resource.patch
  5f6a0067-x86-vPT-fix-race-when-migrating-timers.patch
  5f6a008e-x86-MSI-drop-read_msi_msg.patch
  5f6a00aa-x86-MSI-X-restrict-reading-of-PBA-bases.patch
  5f6a00c4-evtchn-relax-port_is_valid.patch
  5f6a00df-x86-PV-avoid-double-exception-injection.patch
  5f6a00f4-evtchn-add-missing-barriers.patch
  5f6a0111-evtchn-x86-enforce-correct-upper-limit.patch
  5f6a013f-evtchn_reset-shouldnt-succeed-with.patch
  5f6a0160-evtchn-IRQ-safe-per-channel-lock.patch
  5f6a0178-evtchn-address-races-with-evtchn_reset.patch
  5f6a01a4-evtchn-preempt-in-evtchn_destroy.patch
  5f6a01c6-evtchn-preempt-in-evtchn_reset.patch
  5f6cfb5b-x86-PV-dont-GP-for-SYSENTER-with-NT-set.patch
  5f6cfb5b-x86-PV-dont-clobber-NT-on-return-to-guest.patch
  5f71a21e-x86-S3-fix-shadow-stack-resume.patch
  5f76ca65-evtchn-Flask-prealloc-for-send.patch
  5f76caaf-evtchn-FIFO-use-stable-fields.patch
  5f897c25-x86-traps-fix-read_registers-for-DF.patch
  5f897c7b-x86-smpboot-restrict-memguard_guard_stack.patch
  5f8ed5d3-x86-mm-map_pages_to_xen-single-exit-path.patch
  5f8ed5eb-x86-mm-modify_xen_mappings-one-exit-path.patch
  5f8ed603-x86-mm-prevent-races-in-mapping-updates.patch
  5f8ed635-IOMMU-suppress-iommu_dont_flush_iotlb-when.patch
  5f8ed64c-IOMMU-hold-page-ref-until-TLB-flush.patch
  5f8ed682-AMD-IOMMU-convert-amd_iommu_pte.patch
  5f8ed69c-AMD-IOMMU-update-live-PTEs-atomically.patch
  5f8ed6b0-AMD-IOMMU-suitably-order-DTE-mods.patch
  xsa286-1.patch
  xsa286-2.patch
  xsa286-3.patch
  xsa286-4.patch
  xsa286-5.patch
  xsa286-6.patch
  xsa351-1.patch
  xsa351-2.patch
  xsa351-3.patch
  xsa355.patch
* Wed Dec 16 2020 ohering@suse.de
- Pass --with-rundir to configure to get rid of /var/run
* Tue Dec 15 2020 ohering@suse.de
- bsc#1178736 - allow restart of xenwatchdogd, enable tuning of
  keep-alive interval and timeout options via XENWATCHDOGD_ARGS=
  add xenwatchdogd-options.patch
  add xenwatchdogd-restart.patch
* Tue Dec 15 2020 ohering@suse.de
- bsc#1177112 - Fix libxc.sr.superpage.patch
  The receiving side may punch holes incorrectly into optimistically
  allocated superpages. Also reduce overhead in bitmap handling.
  add libxc-bitmap-50a5215f30e964a6f16165ab57925ca39f31a849.patch
  add libxc-bitmap-long.patch
  add libxc-bitmap-longs.patch
* Mon Dec 14 2020 carnold@suse.com
- boo#1029961 - Move files in xen-tools-domU to /usr/bin from /bin
  xen-destdir.patch
  Drop tmp_build.patch
* Fri Dec  4 2020 carnold@suse.com
- bsc#1176782 - L3: xl dump-core shows missing nr_pages during
  core. If maxmem and current are the same the issue doesn't happen
  5fca3b32-tools-libs-ctrl-fix-dumping-of-ballooned-guest.patch
* Fri Nov 20 2020 carnold@suse.com
- bsc#1178963 - VUL-0: xen: stack corruption from XSA-346 change
  (XSA-355)
  xsa355.patch
* Fri Nov 20 2020 ohering@suse.de
- Fix build error with libxl.fix-libacpi-dependency.patch
* Fri Nov 20 2020 ohering@suse.de
- Enhance libxc.migrate_tracking.patch
  Hide SUSEINFO messages from pause/unpause/resume from xl command.
  They are intended for libvirt logging, but lacked info about
  execution context.
  Remove extra logging about dirty pages in each iteration, the
  number of transferred pages + protocol overhead is already
  reported elsewhere.
* Fri Nov 20 2020 ohering@suse.de
- Remove libxl.libxl__domain_pvcontrol.patch
  It is already part of 4.14.0-rc1
* Tue Nov 10 2020 carnold@suse.com
- bsc#1178591 - VUL-0: CVE-2020-28368: xen: Intel RAPL sidechannel
  attack aka PLATYPUS attack aka XSA-351
  xsa351-1.patch
  xsa351-2.patch
  xsa351-3.patch
* Mon Nov  2 2020 ohering@suse.de
- bsc#1177950 - adjust help for --max_iters, default is 5
  libxl.set-migration-constraints-from-cmdline.patch
* Fri Oct 30 2020 ohering@suse.de
- jsc#SLE-16899 - improve performance of live migration
  remove allocations and memcpy from hotpaths on sending and
  receiving side to get more throughput on 10Gbs+ connections
  libxc-sr-3cccdae45242dab27198b8e150be0c85acd5d3c9.patch
  libxc-sr-add-xc_is_known_page_type.patch
  libxc-sr-arrays.patch
  libxc-sr-batch_pfns.patch
  libxc-sr-page_type_has_stream_data.patch
  libxc-sr-readv_exact.patch
  libxc-sr-restore-handle_buffered_page_data.patch
  libxc-sr-restore-handle_incoming_page_data.patch
  libxc-sr-restore-map_errs.patch
  libxc-sr-restore-mfns.patch
  libxc-sr-restore-pfns.patch
  libxc-sr-restore-populate_pfns-mfns.patch
  libxc-sr-restore-populate_pfns-pfns.patch
  libxc-sr-restore-read_record.patch
  libxc-sr-restore-types.patch
  libxc-sr-save-errors.patch
  libxc-sr-save-guest_data.patch
  libxc-sr-save-iov.patch
  libxc-sr-save-local_pages.patch
  libxc-sr-save-mfns.patch
  libxc-sr-save-rec_pfns.patch
  libxc-sr-save-show_transfer_rate.patch
  libxc-sr-save-types.patch
  libxc-sr-use-xc_is_known_page_type.patch
  adjust libxc.sr.superpage.patch
  adjust libxc.migrate_tracking.patch
* Wed Oct 21 2020 carnold@suse.com
- Upstream bug fixes (bsc#1027519)
  5f479d9e-x86-begin-to-support-MSR_ARCH_CAPS.patch
  5f4cf06e-x86-Dom0-expose-MSR_ARCH_CAPS.patch
  5f4cf96a-x86-PV-fix-SEGBASE_GS_USER_SEL.patch
  5f560c42-x86-PV-rewrite-segment-ctxt-switch.patch
  5f5b6b7a-hypfs-fix-custom-param-writes.patch
  5f607915-x86-HVM-more-consistent-IO-completion.patch
  5f6cfb5b-x86-PV-dont-GP-for-SYSENTER-with-NT-set.patch
  5f6cfb5b-x86-PV-dont-clobber-NT-on-return-to-guest.patch
  5f71a21e-x86-S3-fix-shadow-stack-resume.patch
  5f76ca65-evtchn-Flask-prealloc-for-send.patch
  5f76caaf-evtchn-FIFO-use-stable-fields.patch
  5f897c25-x86-traps-fix-read_registers-for-DF.patch
  5f897c7b-x86-smpboot-restrict-memguard_guard_stack.patch
- Renamed patches
  5f560c42-x86-PV-64bit-segbase-consistency.patch
    Replaces 5f5b6951-x86-PV-64bit-segbase-consistency.patch
  5f6a002d-x86-PV-handle-MSR_MISC_ENABLE-correctly.patch
    Replaces 5f6a05a0-pv-Handle-the-Intel-specific-MSR_MISC_ENABLE-correctly.patch
  5f6a0049-memory-dont-skip-RCU-unlock-in-acquire_resource.patch
    Replaces 5f6a05b7-xen-memory-Dont-skip-the-RCU-unlock-path-in-acquire_resource.patch
  5f6a0067-x86-vPT-fix-race-when-migrating-timers.patch
    Replaces 5f6a05dd-vpt-fix-race-when-migrating-timers-between-vCPUs.patch
  5f6a008e-x86-MSI-drop-read_msi_msg.patch
    Replaces 5f6a05fa-msi-get-rid-of-read_msi_msg.patch
  5f6a00aa-x86-MSI-X-restrict-reading-of-PBA-bases.patch
    Replaces 5f6a061a-MSI-X-restrict-reading-of-table-PBA-bases-from-BARs.patch
  5f6a00c4-evtchn-relax-port_is_valid.patch
    Replaces 5f6a062c-evtchn-relax-port_is_valid.patch
  5f6a00df-x86-PV-avoid-double-exception-injection.patch
    Replaces 5f6a065c-pv-Avoid-double-exception-injection.patch
  5f6a00f4-evtchn-add-missing-barriers.patch
    Replaces 5f6a0674-xen-evtchn-Add-missing-barriers-when-accessing-allocating-an-event-channel.patch
  5f6a0111-evtchn-x86-enforce-correct-upper-limit.patch
    Replaces 5f6a068e-evtchn-x86-enforce-correct-upper-limit-for-32-bit-guests.patch
  5f6a013f-evtchn_reset-shouldnt-succeed-with.patch
    Replaces 5f6a06be-evtchn-evtchn_reset-shouldnt-succeed-with-still-open-ports.patch
  5f6a0160-evtchn-IRQ-safe-per-channel-lock.patch
    Replaces 5f6a06e0-evtchn-convert-per-channel-lock-to-be-IRQ-safe.patch
  5f6a0178-evtchn-address-races-with-evtchn_reset.patch
    Replaces 5f6a06f2-evtchn-address-races-with-evtchn_reset.patch
  5f6a01a4-evtchn-preempt-in-evtchn_destroy.patch
    Replaces 5f6a071f-evtchn-arrange-for-preemption-in-evtchn_destroy.patch
  5f6a01c6-evtchn-preempt-in-evtchn_reset.patch
    Replaces 5f6a0754-evtchn-arrange-for-preemption-in-evtchn_reset.patch
* Tue Oct 13 2020 carnold@suse.com
- bsc#1177409 - VUL-0: CVE-2020-27674: xen: x86 PV guest
  INVLPG-like flushes may leave stale TLB entries (XSA-286)
  xsa286-1.patch
  xsa286-2.patch
  xsa286-3.patch
  xsa286-4.patch
  xsa286-5.patch
  xsa286-6.patch
- bsc#1177412 - VUL-0: CVE-2020-27672: xen: Race condition in Xen
  mapping code (XSA-345)
  5f8ed5d3-x86-mm-map_pages_to_xen-single-exit-path.patch
  5f8ed5eb-x86-mm-modify_xen_mappings-one-exit-path.patch
  5f8ed603-x86-mm-prevent-races-in-mapping-updates.patch
- bsc#1177413 - VUL-0: CVE-2020-27671: xen: undue deferral of IOMMU
  TLB flushes (XSA-346)
  5f8ed635-IOMMU-suppress-iommu_dont_flush_iotlb-when.patch
  5f8ed64c-IOMMU-hold-page-ref-until-TLB-flush.patch
- bsc#1177414 - VUL-0: CVE-2020-27670: xen: unsafe AMD IOMMU page
  table updates (XSA-347)
  5f8ed682-AMD-IOMMU-convert-amd_iommu_pte.patch
  5f8ed69c-AMD-IOMMU-update-live-PTEs-atomically.patch
  5f8ed6b0-AMD-IOMMU-suitably-order-DTE-mods.patch
* Mon Oct 12 2020 ohering@suse.de
- Update libxc.sr.superpage.patch
  set errno in x86_hvm_alloc_4k (bsc#1177112)
* Tue Sep 22 2020 carnold@suse.com
- bsc#1176339 - VUL-0: CVE-2020-25602: xen: x86 pv: Crash when
  handling guest access to MSR_MISC_ENABLE (XSA-333)
  5f6a05a0-pv-Handle-the-Intel-specific-MSR_MISC_ENABLE-correctly.patch
- bsc#1176341 - VUL-0: CVE-2020-25598: xen: Missing unlock in
  XENMEM_acquire_resource error path (XSA-334)
  5f6a05b7-xen-memory-Dont-skip-the-RCU-unlock-path-in-acquire_resource.patch
- bsc#1176343 - VUL-0: CVE-2020-25604: xen: race when migrating
  timers between x86 HVM vCPU-s (XSA-336)
  5f6a05dd-vpt-fix-race-when-migrating-timers-between-vCPUs.patch
- bsc#1176344 - VUL-0: CVE-2020-25595: xen: PCI passthrough code
  reading back hardware registers (XSA-337)
  5f6a05fa-msi-get-rid-of-read_msi_msg.patch
  5f6a061a-MSI-X-restrict-reading-of-table-PBA-bases-from-BARs.patch
- bsc#1176346 - VUL-0: CVE-2020-25597: xen: once valid event
  channels may not turn invalid (XSA-338)
  5f6a062c-evtchn-relax-port_is_valid.patch
- bsc#1176345 - VUL-0: CVE-2020-25596: xen: x86 pv guest kernel
  DoS via SYSENTER (XSA-339)
  5f6a065c-pv-Avoid-double-exception-injection.patch
- bsc#1176347 - VUL-0: CVE-2020-25603: xen: Missing barrier
  barriers when accessing/allocating an event channel (XSA-340)
  5f6a0674-xen-evtchn-Add-missing-barriers-when-accessing-allocating-an-event-channel.patch
- bsc#1176348 - VUL-0: CVE-2020-25600: xen: out of bounds event
  channels available to 32-bit x86 domains (XSA-342)
  5f6a068e-evtchn-x86-enforce-correct-upper-limit-for-32-bit-guests.patch
- bsc#1176349 - VUL-0: CVE-2020-25599: xen: races with
  evtchn_reset() (XSA-343)
  5f6a06be-evtchn-evtchn_reset-shouldnt-succeed-with-still-open-ports.patch
  5f6a06e0-evtchn-convert-per-channel-lock-to-be-IRQ-safe.patch
  5f6a06f2-evtchn-address-races-with-evtchn_reset.patch
- bsc#1176350 - VUL-0: CVE-2020-25601: xen: lack of preemption in
  evtchn_reset() / evtchn_destroy() (XSA-344)
  5f6a071f-evtchn-arrange-for-preemption-in-evtchn_destroy.patch
  5f6a0754-evtchn-arrange-for-preemption-in-evtchn_reset.patch
- Upstream bug fix (bsc#1027519)
  5f5b6951-x86-PV-64bit-segbase-consistency.patch
* Mon Sep 21 2020 carnold@suse.com
- Fix problems in xen.spec with building on aarch64
* Fri Sep 18 2020 carnold@suse.com
- Make use of %%service_del_postun_without_restart while preserving
  the old behavior for older distros.
- In %%post tools, remove unnecessary qemu symlinks.
* Thu Sep 17 2020 ohering@suse.de
- Fix error in xen-tools %%post when linking pvgrub64.bin
- Make paths below libexec more explicit
- Create symlink also for pvgrub32.bin
* Fri Sep 11 2020 ohering@suse.de
- Revert previous libexec change for qemu compat wrapper
  The path is used in existing domU.xml files in the emulator field
- Escape some %% chars in xen.spec, they have to appear verbatim
* Wed Sep  9 2020 ohering@suse.de
- Enhance libxc.migrate_tracking.patch
  Print number of allocated pages on sending side, this is more
  accurate than p2m_size.
* Wed Sep  2 2020 carnold@suse.com
- jsc#SLE-15926 - Dev: XEN: drop netware support
  Dropped the following patches
  pygrub-netware-xnloader.patch
  xnloader.py
  Refreshed pygrub-boot-legacy-sles.patch
* Tue Sep  1 2020 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Fix build on aarch64 with gcc10
- Package xenhypfs for aarch64
* Wed Aug  5 2020 Callum Farmer <callumjfarmer13@gmail.com>
- Correct license name
  * GPL-3.0+ is now GPL-3.0-or-later
* Mon Aug  3 2020 carnold@suse.com
- Upstream bug fixes (bsc#1027519)
  5f1a9916-x86-S3-put-data-sregs-into-known-state.patch
  5f21b9fd-x86-cpuid-APIC-bit-clearing.patch
* Fri Jul 24 2020 carnold@suse.com
- Update to Xen 4.14.0 FCS release
  xen-4.14.0-testing-src.tar.bz2
  * Linux stubdomains (contributed by QUBES OS)
  * Control-flow Enforcement Technology (CET) Shadow Stack support (contributed by Citrix)
  * Lightweight VM fork for fuzzing / introspection. (contributed by Intel)
  * Livepatch: buildid and hotpatch stack requirements
  * CONFIG_PV32
  * Hypervisor FS support
  * Running Xen as a Hyper-V Guest
  * Domain ID randomization, persistence across save / restore
  * Golang binding autogeneration
  * KDD support for Windows 7, 8.x and 10
- Dropped patches contained in new tarball
  5eb51be6-cpupool-fix-removing-cpu-from-pool.patch
  5eb51caa-sched-vcpu-pause-flags-atomic.patch
  5ec2a760-x86-determine-MXCSR-mask-always.patch
  5ec50b05-x86-idle-rework-C6-EOI-workaround.patch
  5ec7dcaa-x86-dont-enter-C6-with-in-service-intr.patch
  5ec7dcf6-x86-dont-enter-C3-C6-with-errata.patch
  5ec82237-x86-extend-ISR-C6-workaround-to-Haswell.patch
  5ece1b91-x86-clear-RDRAND-CPUID-bit-on-AMD-fam-15-16.patch
  5ece8ac4-x86-load_system_tables-NMI-MC-safe.patch
  5ed69804-x86-ucode-fix-start-end-update.patch
  5eda60cb-SVM-split-recalc-NPT-fault-handling.patch
  5edf6ad8-ioreq-pending-emulation-server-destruction-race.patch
  5edfbbea-x86-spec-ctrl-CPUID-MSR-defs-for-SRBDS.patch
  5edfbbea-x86-spec-ctrl-mitigate-SRBDS.patch
  5ee24d0e-x86-spec-ctrl-document-SRBDS-workaround.patch
  xsa317.patch
  xsa319.patch
  xsa321-1.patch
  xsa321-2.patch
  xsa321-3.patch
  xsa321-4.patch
  xsa321-5.patch
  xsa321-6.patch
  xsa321-7.patch
  xsa328-1.patch
  xsa328-2.patch
* Thu Jul 23 2020 carnold@suse.com
- bsc#1172356 - Not able to hot-plug NIC via virt-manager, asks to
  attach on next reboot while it should be live attached
  ignore-ip-command-script-errors.patch
* Fri Jul 17 2020 ohering@suse.de
- Enhance libxc.migrate_tracking.patch
  After transfer of domU memory, the target host has to assemble
  the backend devices. Track the time prior xc_domain_unpause.
* Tue Jun 30 2020 ohering@suse.de
- Add libxc.migrate_tracking.patch to track live migrations
  unconditionally in logfiles, especially in libvirt.
  This will track how long a domU was suspended during transit.
* Mon Jun 29 2020 carnold@suse.com
- bsc#1173376 - VUL-0: CVE-2020-15566: xen: XSA-317 - Incorrect
  error handling in event channel port allocation
  xsa317.patch
- bsc#1173377 - VUL-0: CVE-2020-15563: xen: XSA-319 - inverted code
  paths in x86 dirty VRAM tracking
  xsa319.patch
- bsc#1173378 - VUL-0: CVE-2020-15565: xen: XSA-321 - insufficient
  cache write- back under VT-d
  xsa321-1.patch
  xsa321-2.patch
  xsa321-3.patch
  xsa321-4.patch
  xsa321-5.patch
  xsa321-6.patch
  xsa321-7.patch
- bsc#1173380 - VUL-0: CVE-2020-15567: xen: XSA-328 - non-atomic
  modification of live EPT PTE
  xsa328-1.patch
  xsa328-2.patch
* Mon Jun 22 2020 carnold@suse.com
- bsc#1172205 - VUL-0: CVE-2020-0543: xen: Special Register Buffer
  Data Sampling (SRBDS) aka "CrossTalk" (XSA-320)
  5ee24d0e-x86-spec-ctrl-document-SRBDS-workaround.patch
  5edfbbea-x86-spec-ctrl-CPUID-MSR-defs-for-SRBDS.patch (Replaces xsa320-1.patch)
  5edfbbea-x86-spec-ctrl-mitigate-SRBDS.patch (Replaces xsa320-2.patch)
- Upstream bug fixes (bsc#1027519)
  5ec50b05-x86-idle-rework-C6-EOI-workaround.patch
  5ec7dcaa-x86-dont-enter-C6-with-in-service-intr.patch
  5ec7dcf6-x86-dont-enter-C3-C6-with-errata.patch
  5ec82237-x86-extend-ISR-C6-workaround-to-Haswell.patch
  5ece1b91-x86-clear-RDRAND-CPUID-bit-on-AMD-fam-15-16.patch
  5ece8ac4-x86-load_system_tables-NMI-MC-safe.patch
  5ed69804-x86-ucode-fix-start-end-update.patch
  5eda60cb-SVM-split-recalc-NPT-fault-handling.patch
  5edf6ad8-ioreq-pending-emulation-server-destruction-race.patch
* Fri Jun  5 2020 Callum Farmer <callumjfarmer13@gmail.com>
- Fixes for %%_libexecdir changing to /usr/libexec
* Thu May 28 2020 carnold@suse.com
- bsc#1172205 - VUL-0: CVE-2020-0543: xen: Special Register Buffer
  Data Sampling (SRBDS) aka "CrossTalk" (XSA-320)
  xsa320-1.patch
  xsa320-2.patch
* Mon May 18 2020 carnold@suse.com
- Update to Xen 4.13.1 bug fix release (bsc#1027519)
  xen-4.13.1-testing-src.tar.bz2
  5eb51be6-cpupool-fix-removing-cpu-from-pool.patch
  5eb51caa-sched-vcpu-pause-flags-atomic.patch
  5ec2a760-x86-determine-MXCSR-mask-always.patch
- Drop patches contained in new tarball
  5de65f84-gnttab-map-always-do-IOMMU-part.patch
  5de65fc4-x86-avoid-HPET-use-on-certain-Intel.patch
  5e15e03d-sched-fix-S3-resume-with-smt=0.patch
  5e16fb6a-x86-clear-per-cpu-stub-page-info.patch
  5e1da013-IRQ-u16-is-too-narrow-for-evtchn.patch
  5e1dcedd-Arm-place-speculation-barrier-after-ERET.patch
  5e21ce98-x86-time-update-TSC-stamp-after-deep-C-state.patch
  5e286cce-VT-d-dont-pass-bridges-to-domain_context_mapping_one.patch
  5e318cd4-x86-apic-fix-disabling-LVT0.patch
  5e344c11-x86-HVM-relinquish-resources-from-domain_destroy.patch
  5e3bd385-EFI-recheck-variable-name-strings.patch
  5e3bd3d1-EFI-dont-leak-heap-VIA-XEN_EFI_get_next_variable_name.patch
  5e3bd3f8-xmalloc-guard-against-overflow.patch
  5e46e090-x86-smp-reset-x2apic_enabled-in-smp_send_stop.patch
  5e4c00ef-VT-d-check-full-RMRR-for-E820-reserved.patch
  5e4d4f5b-sched-fix-get_cpu_idle_time-with-core-sched.patch
  5e4e614d-x86-spec-ctrl-no-xen-also-disables-branch-hardening.patch
  5e4ec20e-x86-virtualise-MSR_PLATFORM_ID-properly.patch
  5e5e7188-fix-error-path-in-cpupool_unassign_cpu_start.patch
  5e6f53dd-AMD-IOMMU-fix-off-by-one-get_paging_mode.patch
  5e7a371c-sched-fix-cpu-onlining-with-core-sched.patch
  5e7c90cf-sched-fix-cpu-offlining-with-core-sched.patch
  5e7cfb29-x86-ucode-AMD-fix-assert-in-compare_patch.patch
  5e7cfb29-x86-ucode-fix-error-paths-in-apply_microcode.patch
  5e7dd83b-libx86-CPUID-fix-not-just-leaf-7.patch
  5e7dfbf6-x86-ucode-AMD-potential-buffer-overrun-equiv-tab.patch
  5e846cce-x86-HVM-fix-AMD-ECS-handling-for-Fam10.patch
  5e84905c-x86-ucode-AMD-fix-more-potential-buffer-overruns.patch
  5e86f7b7-credit2-avoid-vCPUs-with-lower-creds-than-idle.patch
  5e86f7fd-credit2-fix-credit-too-few-resets.patch
  5e876b0f-tools-xenstore-fix-use-after-free-in-xenstored.patch
  5e95ad61-xenoprof-clear-buffer-intended-to-be-shared-with-guests.patch
  5e95ad8f-xenoprof-limit-consumption-of-shared-buffer-data.patch
  5e95ae77-Add-missing-memory-barrier-in-the-unlock-path-of-rwlock.patch
  5e95af5e-xen-gnttab-Fix-error-path-in-map_grant_ref.patch
  5e95afb8-gnttab-fix-GNTTABOP_copy-continuation-handling.patch
* Wed May 13 2020 James Fehlig <jfehlig@suse.com>
- spec: Remove invocation of autogen.sh
- spec: Recommend qemu-ovmf-x86_64 to provide UEFI firmwares
* Wed May 13 2020 carnold@suse.com
- bsc#1170968 - GCC 10: xen build fails on i586
  gcc10-fixes.patch
* Tue Apr 14 2020 carnold@suse.com
- bsc#1169392 - VUL-0: CVE-2020-11742: xen: Bad continuation
  handling in GNTTABOP_copy (XSA-318)
  5e95afb8-gnttab-fix-GNTTABOP_copy-continuation-handling.patch
* Mon Apr  6 2020 carnold@suse.com
- bsc#1168140 - VUL-0: CVE-2020-11740, CVE-2020-11741: xen: XSA-313
  multiple xenoprof issues
  5e95ad61-xenoprof-clear-buffer-intended-to-be-shared-with-guests.patch
  5e95ad8f-xenoprof-limit-consumption-of-shared-buffer-data.patch
- bsc#1168142 - VUL-0: CVE-2020-11739: xen: XSA-314 - Missing
  memory barriers in read-write unlock paths
  5e95ae77-Add-missing-memory-barrier-in-the-unlock-path-of-rwlock.patch
- bsc#1168143 - VUL-0: CVE-2020-11743: xen: XSA-316 - Bad error
  path in GNTTABOP_map_grant
  5e95af5e-xen-gnttab-Fix-error-path-in-map_grant_ref.patch
- bsc#1167152 - L3: Xenstored Crashed during VM install Need Core
  analyzed
  5e876b0f-tools-xenstore-fix-use-after-free-in-xenstored.patch
- bsc#1165206 - Xen 4.12 DomU hang / freeze / stall / NMI watchdog
  bug soft lockup CPU #0 stuck under high load / upstream with
  workaround. See also bsc#1134506
  5e86f7b7-credit2-avoid-vCPUs-with-lower-creds-than-idle.patch
  5e86f7fd-credit2-fix-credit-too-few-resets.patch
- Drop for upstream solution (bsc#1165206)
  01-xen-credit2-avoid-vcpus-to.patch
  default-to-credit1-scheduler.patch
- Upstream bug fixes (bsc#1027519)
  5e4ec20e-x86-virtualise-MSR_PLATFORM_ID-properly.patch
  5e5e7188-fix-error-path-in-cpupool_unassign_cpu_start.patch
  5e6f53dd-AMD-IOMMU-fix-off-by-one-get_paging_mode.patch
  5e7a371c-sched-fix-cpu-onlining-with-core-sched.patch
  5e7c90cf-sched-fix-cpu-offlining-with-core-sched.patch
  5e7cfb29-x86-ucode-AMD-fix-assert-in-compare_patch.patch
  5e7cfb29-x86-ucode-fix-error-paths-in-apply_microcode.patch
  5e7dd83b-libx86-CPUID-fix-not-just-leaf-7.patch
  5e7dfbf6-x86-ucode-AMD-potential-buffer-overrun-equiv-tab.patch
  5e846cce-x86-HVM-fix-AMD-ECS-handling-for-Fam10.patch
  5e84905c-x86-ucode-AMD-fix-more-potential-buffer-overruns.patch
* Wed Mar 25 2020 ohering@suse.de
- bsc#1167608 - unbound limit for max_event_channels
  domUs with many vcpus and/or resources fail to start
  libxl.max_event_channels.patch
* Wed Mar 18 2020 ohering@suse.de
- bsc#1161480 - Fix xl shutdown for HVM without PV drivers
  add libxl.libxl__domain_pvcontrol.patch
* Thu Mar 12 2020 carnold@suse.com
- bsc#1165206 - Xen 4.12 DomU hang / freeze / stall / NMI watchdog
  bug soft lockup CPU #0 stuck under high load / upstream with
  workaround. See also bsc#1134506
  01-xen-credit2-avoid-vcpus-to.patch
* Tue Mar 10 2020 carnold@suse.com
- bsc#1158414 - GCC 10: xen build fails
  gcc10-fixes.patch
* Wed Mar  4 2020 carnold@suse.com
- bsc#1165206 - Xen 4.12 DomU hang / freeze / stall / NMI watchdog
  bug soft lockup CPU #0 stuck under high load / upstream with
  workaround. See also bsc#1134506
  default-to-credit1-scheduler.patch
* Thu Feb 20 2020 carnold@suse.com
- bsc#1160932 - VUL-0: xen: XSA-312 v1: arm: a CPU may speculate
  past the ERET instruction
  5e1dcedd-Arm-place-speculation-barrier-after-ERET.patch
- bsc#1164425 - x86: "spec-ctrl=no-xen" should also disable branch
  hardening
  5e4e614d-x86-spec-ctrl-no-xen-also-disables-branch-hardening.patch
- Upstream bug fixes (bsc#1027519)
  5e21ce98-x86-time-update-TSC-stamp-after-deep-C-state.patch
  5e286cce-VT-d-dont-pass-bridges-to-domain_context_mapping_one.patch
  5e318cd4-x86-apic-fix-disabling-LVT0.patch
  5e344c11-x86-HVM-relinquish-resources-from-domain_destroy.patch
  5e3bd385-EFI-recheck-variable-name-strings.patch
  5e3bd3d1-EFI-dont-leak-heap-VIA-XEN_EFI_get_next_variable_name.patch
  5e3bd3f8-xmalloc-guard-against-overflow.patch
  5e46e090-x86-smp-reset-x2apic_enabled-in-smp_send_stop.patch
  5e4c00ef-VT-d-check-full-RMRR-for-E820-reserved.patch
  5e4d4f5b-sched-fix-get_cpu_idle_time-with-core-sched.patch
* Tue Feb 18 2020 ohering@suse.de
- bsc#1159755 - use fixed qemu-3.1 machine type for HVM
  This must be done in qemu to preserve PCI layout
  remove libxl.lock-qemu-machine-for-hvm.patch
* Fri Feb  7 2020 ohering@suse.de
- jsc#SLE-10183 - script to calculate cpuid= mask
  add helper script from https://github.com/twizted/xen_maskcalc
  domUs may be migrated between different cpus from the same vendor
  if their visible cpuid value has incompatible feature bits masked.
* Wed Feb  5 2020 ohering@suse.de
- jsc#SLE-10172, bsc#1055731 - handle degraded raid for xendomains
  add helper script and systemd service from
  https://github.com/luizluca/xen-tools-xendomains-wait-disk
  in new sub package xen-tools-xendomains-wait-disk
  See included README for usage instructions
  xendomains-wait-disks.LICENSE
  xendomains-wait-disks.README.md
  xendomains-wait-disks.sh
* Tue Jan 28 2020 ohering@suse.de
- bsc#1159755 - use fixed qemu-3.1 machine type for HVM
  qemu4 introduced incompatible changes in pc-i440fx, which revealed
  a design bug in 'xenfv'. Live migration from domUs started with
  qemu versions prior qemu4 can not be received with qemu4+.
  libxl.lock-qemu-machine-for-hvm.patch
* Tue Jan 14 2020 carnold@suse.com
- Upstream bug fixes (bsc#1027519)
  5de65f84-gnttab-map-always-do-IOMMU-part.patch
  5de65fc4-x86-avoid-HPET-use-on-certain-Intel.patch
  5e15e03d-sched-fix-S3-resume-with-smt=0.patch
  5e16fb6a-x86-clear-per-cpu-stub-page-info.patch
  5e1da013-IRQ-u16-is-too-narrow-for-evtchn.patch
* Wed Jan  8 2020 Dominique Leuenberger <dimstar@opensuse.org>
- BuildRequire pkgconfig(libsystemd) instead of systemd-devel:
  Allow OBS to shortcut through the -mini flavors.
* Wed Dec 18 2019 carnold@suse.com
- bsc#1159320 - Xen logrotate file needs updated
  logrotate.conf
* Wed Dec 18 2019 carnold@suse.com
- Update to Xen 4.13.0 FCS release
  xen-4.13.0-testing-src.tar.bz2
  * Core Scheduling (contributed by SUSE)
  * Branch hardening to mitigate against Spectre v1 (contributed by Citrix)
  * Late uCode loading (contributed by Intel)
  * Improved live-patching build tools (contributed by AWS)
  * OP-TEE support (contributed by EPAM)
  * Renesas R-CAR IPMMU-VMSA driver (contributed by EPAM)
  * Dom0-less passthrough and ImageBuilder (contributed by XILINX)
  * Support for new Hardware
* Tue Dec  3 2019 carnold@suse.com
- Update to Xen 4.13.0 RC4 release
  xen-4.13.0-testing-src.tar.bz2
- Rebase libxl.pvscsi.patch
* Mon Nov 25 2019 carnold@suse.com
- Update to Xen 4.13.0 RC3 release
  xen-4.13.0-testing-src.tar.bz2
- Drop python38-build.patch
* Tue Nov 12 2019 carnold@suse.com
- Update to Xen 4.13.0 RC2 release
  xen-4.13.0-testing-src.tar.bz2
* Tue Oct 29 2019 Matej Cepl <mcepl@suse.com>
- Add python38-build.patch fixing build with Python 3.8 (add
  - -embed to python-config call)
* Mon Oct 14 2019 carnold@suse.com
- Update to Xen 4.13.0 RC1 release
  xen-4.13.0-testing-src.tar.bz2
- Drop patches contained in new tarball or invalid
  5ca7660f-x86-entry-drop-unused-includes.patch
  5cab2a6b-x86-ACPI-also-parse-AMD-tables-early.patch
  5cab2ab7-x86-IOMMU-introduce-init-ops.patch
  5cab2ae8-x86-IOMMU-abstract-iommu_supports_eim.patch
  5cab2b4e-x86-IOMMU-abstract-iommu_enable_x2apic_IR.patch
  5cab2b95-x86-IOMMU-initialize-iommu_ops-in.patch
  5cac9a4b-x86-IOMMU-abstract-adjust_vtd_irq_affinities.patch
  5cdeac7f-AMD-IOMMU-adjust-IOMMU-list-head-init.patch
  5cf8da09-adjust-sysdom-creation-call-earlier-on-x86.patch
  5d0cf4e4-AMD-IOMMU-initialize-IRQ-tasklet-once.patch
  5d149bb0-AMD-IOMMU-dont-add-IOMMUs.patch
  5d1b3fab-AMD-IOMMU-restrict-feature-logging.patch
  5d358508-x86-IRQ-desc-affinity-represents-request.patch
  5d358534-x86-IRQ-consolidate-arch-cpu_mask-use.patch
  5d358a67-AMD-IOMMU-pass-IOMMU-to-iterate_ivrs_entries-cb.patch
  5d358a92-AMD-IOMMU-pass-IOMMU-to-amd_iommu_alloc_intremap_table.patch
  5d39811c-x86-IOMMU-dont-restrict-IRQ-affinities.patch
  5d417813-AMD-IOMMU-bitfield-extended-features.patch
  5d417838-AMD-IOMMU-bitfield-control-reg.patch
  5d41785b-AMD-IOMMU-bitfield-IRTE.patch
  5d41787e-AMD-IOMMU-pass-IOMMU-to-gfu-intremap-entry.patch
  5d4178ad-AMD-IOMMU-128bit-non-guest-APIC-IRTE.patch
  5d4178fc-AMD-IOMMU-split-amd_iommu_init_one.patch
  5d41793f-AMD-IOMMU-allow-enabling-without-IRQ.patch
  5d417a16-AMD-IOMMU-adjust-IRQ-setup-for-x2APIC.patch
  5d417ab6-AMD-IOMMU-enable-x2APIC-mode.patch
  5d417b38-AMD-IOMMU-correct-IRTE-updating.patch
  5d417b6a-AMD-IOMMU-dont-needlessly-log-headers.patch
  5d419d49-x86-spec-ctrl-report-proper-status.patch
  5d43253c-x86-ucode-always-collect_cpu_info-at-boot.patch
  5d4a9d25-AMD-IOMMU-drop-not-found-message.patch
  5d4aa36f-x86-apic-enable-x2APIC-mode-earlier.patch
  5d4afa7a-credit2-fix-memory-leak.patch
  5d4d850a-introduce-bss-percpu-page-aligned.patch
  5d516531-x86-xpti-dont-leak-TSS-adjacent-data.patch
  5d5bf475-x86-PV-fix-handling-of-iommu-mappings.patch
  5d6524ca-x86-mm-correctly-init-M2P-entries.patch
  5d67ceaf-x86-properly-gate-PKU-clearing.patch
  5d70bfba-x86-shadow-dont-enable-with-too-small-allocation.patch
  5d779811-x86-fix-CPUID7-0-eax-levelling-MSR.patch
  5d77b40f-fix-hvm_all_ioreq_servers_add_vcpu-cleanup.patch
  5d80e7c0-AMD-IOMMU-free-shared-IRT-once.patch
  5d80e80d-AMD-IOMMU-valid-flag-for-IVRS-mappings.patch
  5d80e82e-AMD-IOMMU-alloc_intremap_table-callers-handle-errors.patch
  5d80e857-x86-PCI-read-MSI-X-table-entry-count-early.patch
  5d80ea13-vpci-honor-read-only-devices.patch
  5d89d8d9-libxc-x86-avoid-overflow-in-CPUID-APIC-ID.patch
  5d8b715f-ACPI-cpuidle-bump-max-num-of-states.patch
  5d8b72e5-AMD-IOMMU-dont-blindly-alloc-intremap-tables.patch
  5d8b730e-AMD-IOMMU-phantom-funcs-share-intremap-tables.patch
  5d8b733b-x86-PCI-read-max-MSI-vector-count-early.patch
  5d8b736d-AMD-IOMMU-replace-INTREMAP_ENTRIES.patch
  5d8b7393-AMD-IOMMU-restrict-intremap-table-sizes.patch
  5d9ee2a8-AMD-IOMMU-alloc-1-devtab-per-PCI-seg.patch
  5d9ee2f0-AMD-IOMMU-allocate_buffer-avoid-memset.patch
  5d9ee312-AMD-IOMMU-prefill-all-DTEs.patch
  CVE-2014-0222-blktap-qcow1-validate-l2-table-size.patch
  blktap2-no-uninit.patch
  libxl.prepare-environment-for-domcreate_stream_done.patch
  pygrub-python3-conversion.patch
  fix-xenpvnetboot.patch
* Thu Oct 10 2019 carnold@suse.com
- bsc#1135799 - Partner-L3: Xen crashes on AMD ROME based machines
  5d9ee2a8-AMD-IOMMU-alloc-1-devtab-per-PCI-seg.patch
  5d9ee2f0-AMD-IOMMU-allocate_buffer-avoid-memset.patch
  5d9ee312-AMD-IOMMU-prefill-all-DTEs.patch
* Wed Oct  2 2019 ohering@suse.de
- bsc#1120095 - add code to change LIBXL_HOTPLUG_TIMEOUT at runtime
  The included README has details about the impact of this change
  libxl.LIBXL_HOTPLUG_TIMEOUT.patch
* Mon Sep 30 2019 carnold@suse.com
- bsc#1135799 - Partner-L3: Xen crashes on AMD ROME based machines
  5ca7660f-x86-entry-drop-unused-includes.patch
  5cf8da09-adjust-sysdom-creation-call-earlier-on-x86.patch
  5cab2a6b-x86-ACPI-also-parse-AMD-tables-early.patch
  5cab2ab7-x86-IOMMU-introduce-init-ops.patch
  5cab2ae8-x86-IOMMU-abstract-iommu_supports_eim.patch
  5cab2b4e-x86-IOMMU-abstract-iommu_enable_x2apic_IR.patch
  5cab2b95-x86-IOMMU-initialize-iommu_ops-in.patch
  5cac9a4b-x86-IOMMU-abstract-adjust_vtd_irq_affinities.patch
  5cdeac7f-AMD-IOMMU-adjust-IOMMU-list-head-init.patch
  5d0cf4e4-AMD-IOMMU-initialize-IRQ-tasklet-once.patch
  5d149bb0-AMD-IOMMU-dont-add-IOMMUs.patch
  5d1b3fab-AMD-IOMMU-restrict-feature-logging.patch
  5d358508-x86-IRQ-desc-affinity-represents-request.patch
  5d358534-x86-IRQ-consolidate-arch-cpu_mask-use.patch
  5d358a67-AMD-IOMMU-pass-IOMMU-to-iterate_ivrs_entries-cb.patch
  5d358a92-AMD-IOMMU-pass-IOMMU-to-amd_iommu_alloc_intremap_table.patch
  5d39811c-x86-IOMMU-dont-restrict-IRQ-affinities.patch
  5d417813-AMD-IOMMU-bitfield-extended-features.patch
  5d417838-AMD-IOMMU-bitfield-control-reg.patch
  5d41785b-AMD-IOMMU-bitfield-IRTE.patch
  5d41787e-AMD-IOMMU-pass-IOMMU-to-gfu-intremap-entry.patch
  5d4178ad-AMD-IOMMU-128bit-non-guest-APIC-IRTE.patch
  5d4178fc-AMD-IOMMU-split-amd_iommu_init_one.patch
  5d41793f-AMD-IOMMU-allow-enabling-without-IRQ.patch
  5d417a16-AMD-IOMMU-adjust-IRQ-setup-for-x2APIC.patch
  5d417ab6-AMD-IOMMU-enable-x2APIC-mode.patch
  5d417b38-AMD-IOMMU-correct-IRTE-updating.patch
  5d417b6a-AMD-IOMMU-dont-needlessly-log-headers.patch
  5d4a9d25-AMD-IOMMU-drop-not-found-message.patch
  5d80e7c0-AMD-IOMMU-free-shared-IRT-once.patch
  5d80e80d-AMD-IOMMU-valid-flag-for-IVRS-mappings.patch
  5d80e82e-AMD-IOMMU-alloc_intremap_table-callers-handle-errors.patch
  5d80e857-x86-PCI-read-MSI-X-table-entry-count-early.patch
  5d8b72e5-AMD-IOMMU-dont-blindly-alloc-intremap-tables.patch
  5d8b730e-AMD-IOMMU-phantom-funcs-share-intremap-tables.patch
  5d8b733b-x86-PCI-read-max-MSI-vector-count-early.patch
  5d8b736d-AMD-IOMMU-replace-INTREMAP_ENTRIES.patch
  5d8b7393-AMD-IOMMU-restrict-intremap-table-sizes.patch
- bsc#1145240 - [Migration]Can't pre-allocate 1 shadow pages
  5d70bfba-x86-shadow-dont-enable-with-too-small-allocation.patch
- bsc#1137717 - [HPS Bug] Unable to install Windows Server 2016
  with 2 CPUs setting (or above) under SLES12 SP4 Xen Server on AMD
  ROME platform
  5d89d8d9-libxc-x86-avoid-overflow-in-CPUID-APIC-ID.patch
- Upstream bug fixes (bsc#1027519)
  5d67ceaf-x86-properly-gate-PKU-clearing.patch
  5d779811-x86-fix-CPUID7-0-eax-levelling-MSR.patch
  5d77b40f-fix-hvm_all_ioreq_servers_add_vcpu-cleanup.patch
  5d80ea13-vpci-honor-read-only-devices.patch
  5d8b715f-ACPI-cpuidle-bump-max-num-of-states.patch
* Fri Sep 27 2019 ohering@suse.de
- bsc#1145774 - Libivrtd segfaults when trying to live migrate a VM
  Fix crash in an error path of libxl_domain_suspend with
  libxl.helper_done-crash.patch
* Wed Aug 28 2019 carnold@suse.com
- Upstream bug fixes (bsc#1027519)
  5d419d49-x86-spec-ctrl-report-proper-status.patch
  5d43253c-x86-ucode-always-collect_cpu_info-at-boot.patch
  5d4aa36f-x86-apic-enable-x2APIC-mode-earlier.patch
  5d4afa7a-credit2-fix-memory-leak.patch
  5d4d850a-introduce-bss-percpu-page-aligned.patch
  5d516531-x86-xpti-dont-leak-TSS-adjacent-data.patch
  5d5bf475-x86-PV-fix-handling-of-iommu-mappings.patch
  5d6524ca-x86-mm-correctly-init-M2P-entries.patch
- Drop 5d419d49-x86-spec-ctrl-facilities-report-wrong-status.patch
* Wed Aug 28 2019 ohering@suse.de
- Preserve modified files which used to be marked as %%config,
  rename file.rpmsave to file
* Fri Aug  9 2019 carnold@suse.com
- Update to Xen 4.12.1 bug fix release (bsc#1027519)
  xen-4.12.1-testing-src.tar.bz2
- Drop patches contained in new tarball
  5c87b644-IOMMU-leave-enabled-for-kexec-crash.patch
  5c87b6a2-x86-HVM-dont-crash-guest-in-find_mmio_cache.patch
  5c87b6c8-drop-arch_evtchn_inject.patch
  5c87b6e8-avoid-atomic-rmw-accesses-in-map_vcpu_info.patch
  5c87e6d1-x86-TSX-controls-for-RTM-force-abort-mode.patch
  5c8f752c-x86-e820-build-with-gcc9.patch
  5c8fb92d-x86-HVM-split-linear-reads-and-writes.patch
  5c8fb951-x86-HVM-finish-IOREQs-correctly-on-completion.patch
  5c8fc6c0-x86-MSR-shorten-ARCH_CAPABILITIES.patch
  5c8fc6c0-x86-SC-retpoline-safety-calculations-for-eIBRS.patch
  5c9e63c5-credit2-SMT-idle-handling.patch
  5ca46b68-x86emul-no-GPR-update-upon-AVX-gather-failures.patch
  5ca773d1-x86emul-dont-read-mask-reg-without-AVX512F.patch
  5cab1f66-timers-fix-memory-leak-with-cpu-plug.patch
  5cac6cba-vmx-Fixup-removals-of-MSR-load-save-list-entries.patch
  5cd921fb-trace-fix-build-with-gcc9.patch
  5cd9224b-AMD-IOMMU-disable-upon-init-fail.patch
  5cd922c5-x86-MTRR-recalc-p2mt-when-iocaps.patch
  5cd9230f-VMX-correctly-get-GS_SHADOW-for-current.patch
  5cd926d0-bitmap_fill-zero-sized.patch
  5cd92724-drivers-video-drop-constraints.patch
  5cd93a69-x86-MSR_INTEL_CORE_THREAD_COUNT.patch
  5cd93a69-x86-boot-detect-Intel-SMT-correctly.patch
  5cd93a69-x86-spec-ctrl-reposition-XPTI-parsing.patch
  5cd981ff-x86-IRQ-tracing-avoid-UB-or-worse.patch
  5cdad090-x86-spec-ctrl-CPUID-MSR-definitions-for-MDS.patch
  5cdad090-x86-spec-ctrl-infrastructure-for-VERW-flush.patch
  5cdad090-x86-spec-ctrl-misc-non-functional-cleanup.patch
  5cdad090-x86-spec-ctrl-opts-to-control-VERW-flush.patch
  5cdeb9fd-sched-fix-csched2_deinit_pdata.patch
  5ce7a92f-x86-IO-APIC-fix-build-with-gcc9.patch
  5cf0f6a4-x86-vhpet-resume-avoid-small-diff.patch
  5cf16e51-x86-spec-ctrl-Knights-retpoline-safe.patch
  5d03a0c4-1-Arm-add-an-isb-before-reading-CNTPCT_EL0.patch
  5d03a0c4-2-gnttab-rework-prototype-of-set_status.patch
  5d03a0c4-3-Arm64-rewrite-bitops-in-C.patch
  5d03a0c4-4-Arm32-rewrite-bitops-in-C.patch
  5d03a0c4-5-Arm-bitops-consolidate-prototypes.patch
  5d03a0c4-6-Arm64-cmpxchg-simplify.patch
  5d03a0c4-7-Arm32-cmpxchg-simplify.patch
  5d03a0c4-8-Arm-bitops-helpers-with-timeout.patch
  5d03a0c4-9-Arm-cmpxchg-helper-with-timeout.patch
  5d03a0c4-A-Arm-turn-on-SILO-mode-by-default.patch
  5d03a0c4-B-bitops-guest-helpers.patch
  5d03a0c4-C-cmpxchg-guest-helpers.patch
  5d03a0c4-D-use-guest-atomics-helpers.patch
  5d03a0c4-E-Arm-add-perf-counters-in-guest-atomic-helpers.patch
  5d03a0c4-F-Arm-protect-gnttab_clear_flag.patch
- Refreshed patches
  libxl.pvscsi.patch
* Thu Aug  1 2019 carnold@suse.com
- bsc#1143563 - Speculative mitigation facilities report wrong status
  5d419d49-x86-spec-ctrl-facilities-report-wrong-status.patch
* Wed Jul 17 2019 ohering@suse.de
- Update xen-dom0-modules.service (bsc#1137251)
  Map backend module names from pvops and xenlinux kernels to a
  module alias. This avoids errors from modprobe about unknown
  modules. Ignore a few xenlinux modules that lack aliases.
* Mon Jul 15 2019 carnold@suse.com
- Gcc9 warnings seem to be cleared up with upstream fixes.
  Drop gcc9-ignore-warnings.patch
* Tue Jun 25 2019 carnold@suse.com
- bsc#1138563 - L3: xenpvnetboot improperly ported to Python 3
  fix-xenpvnetboot.patch
* Mon Jun 24 2019 ohering@suse.de
- Move /etc/modprobe.d/xen_loop.conf to /lib/modprobe.d/xen_loop.conf
* Mon Jun 24 2019 ohering@suse.de
- Remove /etc/xen/xenapiusers and /etc/pam.d/xen-api
* Fri Jun 21 2019 ohering@suse.de
- Remove all upstream provided files in /etc/xen
  They are not required at runtime. The host admin is now
  responsible if he really needs anything in this subdirectory.
* Fri Jun 21 2019 ohering@suse.de
- In our effort to make /etc fully admin controlled, move /etc/xen/scripts
  to libexec/xen/scripts with xen-tools.etc_pollution.patch
* Wed Jun 19 2019 ohering@suse.de
- Move /etc/bash_completion.d/xl.sh to %%{_datadir}/bash-completion/completions
* Mon Jun 17 2019 carnold@suse.com
- bsc#1138294 - VUL-0: CVE-2019-17349: XSA-295: Unlimited Arm
  Atomics Operations
  5d03a0c4-1-Arm-add-an-isb-before-reading-CNTPCT_EL0.patch
  5d03a0c4-2-gnttab-rework-prototype-of-set_status.patch
  5d03a0c4-3-Arm64-rewrite-bitops-in-C.patch
  5d03a0c4-4-Arm32-rewrite-bitops-in-C.patch
  5d03a0c4-5-Arm-bitops-consolidate-prototypes.patch
  5d03a0c4-6-Arm64-cmpxchg-simplify.patch
  5d03a0c4-7-Arm32-cmpxchg-simplify.patch
  5d03a0c4-8-Arm-bitops-helpers-with-timeout.patch
  5d03a0c4-9-Arm-cmpxchg-helper-with-timeout.patch
  5d03a0c4-A-Arm-turn-on-SILO-mode-by-default.patch
  5d03a0c4-B-bitops-guest-helpers.patch
  5d03a0c4-C-cmpxchg-guest-helpers.patch
  5d03a0c4-D-use-guest-atomics-helpers.patch
  5d03a0c4-E-Arm-add-perf-counters-in-guest-atomic-helpers.patch
  5d03a0c4-F-Arm-protect-gnttab_clear_flag.patch
- Upstream bug fixes (bsc#1027519)
  5c87b6c8-drop-arch_evtchn_inject.patch
  5c87b6e8-avoid-atomic-rmw-accesses-in-map_vcpu_info.patch
  5cd921fb-trace-fix-build-with-gcc9.patch
  5cd9224b-AMD-IOMMU-disable-upon-init-fail.patch
  5cd922c5-x86-MTRR-recalc-p2mt-when-iocaps.patch
  5cd9230f-VMX-correctly-get-GS_SHADOW-for-current.patch
  5cd926d0-bitmap_fill-zero-sized.patch
  5cd92724-drivers-video-drop-constraints.patch
  5cd93a69-x86-spec-ctrl-reposition-XPTI-parsing.patch (Replaces xsa297-0a.patch)
  5cd93a69-x86-MSR_INTEL_CORE_THREAD_COUNT.patch (Replaces xsa297-0b.patch)
  5cd93a69-x86-boot-detect-Intel-SMT-correctly.patch (Replaces xsa297-0c.patch)
  5cdad090-x86-spec-ctrl-misc-non-functional-cleanup.patch (Replaces xsa297-0d.patch)
  5cdad090-x86-spec-ctrl-CPUID-MSR-definitions-for-MDS.patch (Replaces xsa297-1.patch)
  5cdad090-x86-spec-ctrl-infrastructure-for-VERW-flush.patch (Replaces xsa297-2.patch)
  5cdad090-x86-spec-ctrl-opts-to-control-VERW-flush.patch (Replaces xsa297-3.patch)
  5cd981ff-x86-IRQ-tracing-avoid-UB-or-worse.patch
  5cdeb9fd-sched-fix-csched2_deinit_pdata.patch
  5ce7a92f-x86-IO-APIC-fix-build-with-gcc9.patch
  5cf0f6a4-x86-vhpet-resume-avoid-small-diff.patch
  5cf16e51-x86-spec-ctrl-Knights-retpoline-safe.patch
* Fri Jun 14 2019 carnold@suse.com
- Fix some outdated information in the readme
  README.SUSE
* Tue Jun 11 2019 Jim Fehlig <jfehlig@suse.com>
- spec: xen-tools: require matching version of xen package
  bsc#1137471
* Fri May 17 2019 ohering@suse.de
- Remove two stale patches
  xen.build-compare.man.patch
  xenpaging.doc.patch
* Tue May 14 2019 Martin Liška <mliska@suse.cz>
- Disable LTO (boo#1133296).
* Mon May 13 2019 ohering@suse.de
- Remove arm32 from ExclusiveArch to fix build
* Mon Apr 29 2019 carnold@suse.com
- bsc#1111331 - VUL-0: CPU issues Q2 2019 aka "Group 4".
  CVE-2018-12126, CVE-2018-12127, CVE-2018-12130, CVE-2019-11091
  xsa297-0a.patch
  xsa297-0b.patch
  xsa297-0c.patch
  xsa297-0d.patch
  xsa297-1.patch
  xsa297-2.patch
  xsa297-3.patch
- Update 5cab1f66-timers-fix-memory-leak-with-cpu-plug.patch and
  drop 5cac6219-xen-cpu-Fix-ARM-build-following-cs-597fbb8.patch
  Refresh 5cac6cba-vmx-Fixup-removals-of-MSR-load-save-list-entries.patch
* Wed Apr 17 2019 carnold@suse.com
- bsc#1131811 - [XEN] internal error: libxenlight failed to create
  new domain. This patch is a workaround for a systemd issue. See
  patch header for additional comments.
  xenstore-launch.patch
* Thu Apr 11 2019 carnold@suse.com
- bsc#1125378 - [xen][pygrub] Can not restore sle11sp4 pv guest
  after upgrading host from sle11sp4 to sle15sp1
  pygrub-python3-conversion.patch
- Fix "TypeError: virDomainDefineXML() argument 2 must be str or
  None, not bytes" when converting VMs from using the xm/xend
  toolstack to the libxl/libvirt toolstack. (bsc#1123378)
  xen2libvirt.py
* Mon Apr  8 2019 carnold@suse.com
- bsc#1124560 - Fully virtualized guests crash on boot
  5cac6cba-vmx-Fixup-removals-of-MSR-load-save-list-entries.patch
- bsc#1121391 - GCC 9: xen build fails
  5c8f752c-x86-e820-build-with-gcc9.patch
- Upstream bug fixes (bsc#1027519)
  5c87b644-IOMMU-leave-enabled-for-kexec-crash.patch
  5c87b6a2-x86-HVM-dont-crash-guest-in-find_mmio_cache.patch
  5c87e6d1-x86-TSX-controls-for-RTM-force-abort-mode.patch
  5c8fb92d-x86-HVM-split-linear-reads-and-writes.patch
  5c8fb951-x86-HVM-finish-IOREQs-correctly-on-completion.patch
  5c8fc6c0-x86-MSR-shorten-ARCH_CAPABILITIES.patch
  5c8fc6c0-x86-SC-retpoline-safety-calculations-for-eIBRS.patch
  5c9e63c5-credit2-SMT-idle-handling.patch
  5ca46b68-x86emul-no-GPR-update-upon-AVX-gather-failures.patch
  5ca773d1-x86emul-dont-read-mask-reg-without-AVX512F.patch
  5cab1f66-timers-fix-memory-leak-with-cpu-plug.patch
  5cac6219-xen-cpu-Fix-ARM-build-following-cs-597fbb8.patch
* Thu Apr  4 2019 ohering@suse.de
- Install pkgconfig files into libdir instead of datadir
* Tue Apr  2 2019 carnold@suse.com
- Update to Xen 4.12.0 FCS release (fate#325107, fate#323901)
  xen-4.12.0-testing-src.tar.bz2
  * HVM/PVH and PV only Hypervisor: The Xen 4.12 release separates
    the HVM/PVH and PV code paths in Xen and provides KCONFIG
    options to build a PV only or HVM/PVH only hypervisor.
  * QEMU Deprivilege (DM_RESTRICT): In Xen 4.12, this feature has
    been vastly improved.
  * Argo - Hypervisor-Mediated data eXchange: Argo is a new inter-
    domain communication mechanism.
  * Improvements to Virtual Machine Introspection: The VMI subsystem
    which allows detection of 0-day vulnerabilities has seen many
    functional and performance improvements.
  * Credit 2 Scheduler: The Credit2 scheduler is now the Xen Project
    default scheduler.
  * PVH Support: Grub2 boot support has been added to Xen and Grub2.
  * PVH Dom0: PVH Dom0 support has now been upgraded from experimental
    to tech preview.
  * The Xen 4.12 upgrade also includes improved IOMMU mapping code,
    which is designed to significantly improve the startup times of
    AMD EPYC based systems.
  * The upgrade also features Automatic Dom0 Sizing which allows the
    setting of Dom0 memory size as a percentage of host memory (e.g.
    10%%) or with an offset (e.g. 1G+10%%).
* Tue Mar 26 2019 carnold@suse.com
- bsc#1130485 - Please drop Requires on multipath-tools in
  xen-tools. Now using Recommends multipath-tools.
  xen.spec
* Mon Mar 25 2019 carnold@suse.com
- Update to Xen 4.12.0 RC7 release (fate#325107, fate#323901)
  xen-4.12.0-testing-src.tar.bz2
* Wed Mar 20 2019 carnold@suse.com
- Update to Xen 4.12.0 RC6 release (fate#325107, fate#323901)
  xen-4.12.0-testing-src.tar.bz2
* Fri Mar 15 2019 ohering@suse.de
- bsc#1026236 - add Xen cmdline option "suse_vtsc_tolerance" to
  avoid TSC emulation for HVM domUs if their expected frequency
  does not match exactly the frequency of the receiving host
  xen.bug1026236.suse_vtsc_tolerance.patch
* Mon Mar 11 2019 carnold@suse.com
- Update to Xen 4.12.0 RC5 release (fate#325107, fate#323901)
  xen-4.12.0-testing-src.tar.bz2
* Mon Mar 11 2019 carnold@suse.com
- jsc#SLE-3059 - Disable Xen auto-ballooning
- Add CONFIG_DOM0_MEM to the spec file for managing dom0 memory.
  xen.spec
- Disable autoballooning in xl.con
  xl-conf-disable-autoballoon.patch
* Thu Mar  7 2019 ohering@suse.de
- Update gcc9-ignore-warnings.patch to fix build in SLE12
* Thu Mar  7 2019 ohering@suse.de
- bsc#1126325 - fix crash in libxl in error path
  Setup of grant_tables and other variables may fail
  libxl.prepare-environment-for-domcreate_stream_done.patch
* Wed Mar  6 2019 carnold@suse.com
- bsc#1127620 - Documentation for the xl configuration file allows
  for firmware=pvgrub64 but we don't ship pvgrub64.
  Create a link from grub.xen to pvgrub64
  xen.spec
* Mon Mar  4 2019 carnold@suse.com
- Update to Xen 4.12.0 RC4 release (fate#325107, fate#323901)
  xen-4.12.0-testing-src.tar.bz2
- Tarball also contains additional post RC4 security fixes for
  Xen Security Advisories 287, 288, and 290 through 294.
* Tue Feb 19 2019 carnold@suse.com
- Update to Xen 4.12.0 RC3 release (fate#325107, fate#323901)
  xen-4.12.0-testing-src.tar.bz2
* Mon Feb  4 2019 carnold@suse.com
- Update to Xen 4.12.0 RC2 release (fate#325107, fate#323901)
  xen-4.12.0-testing-src.tar.bz2
* Fri Jan 25 2019 carnold@suse.com
- bsc#1121391 - GCC 9: xen build fails
  gcc9-ignore-warnings.patch
* Thu Jan 24 2019 carnold@suse.com
- bsc#1122563 - Virtualization/xen: Bug no Xen on boot, missing
  /proc/xen, after 4.11 -> 4.12 upgrade on X86_64/efi.
  Keep xen.efi in /usr/lib64/efi for booting older distros.
  xen.spec
* Fri Jan 18 2019 carnold@suse.com
- fate#326960: Package grub2 as noarch.
  As part of the effort to have a unified bootloader across
  architectures, modify the xen.spec file to move the Xen efi files
  to /usr/share/efi/$(uname -m) from /usr/lib64/efi.
* Wed Jan 16 2019 carnold@suse.com
- Update to Xen 4.12.0 RC1 release (fate#325107, fate#323901)
  xen-4.12.0-testing-src.tar.bz2
- Drop
  5b505d59-tools-xentop-replace-use-of-deprecated-vwprintw.patch
  5b76ec82-libxl-arm-Fix-build-on-arm64-acpi-w-gcc-8.2.patch
  5b8fae26-tools-libxl-correct-vcpu-affinity-output-with-sparse-physical-cpu-map.patch
  5b8fae26-xen-fill-topology-info-for-all-present-cpus.patch
  5b8fb5af-tools-xl-refuse-to-set-number-of-vcpus-to-0-via-xl-vcpu-set.patch
  5b9784ad-x86-HVM-drop-hvm_fetch_from_guest_linear.patch
  5b9784d2-x86-HVM-add-known_gla-helper.patch
  5b9784f2-x86-HVM-split-page-straddling-accesses.patch
  5bdc31d5-VMX-fix-vmx_handle_eoi.patch
  gcc8-fix-array-warning-on-i586.patch
  gcc8-fix-format-warning-on-i586.patch
  gcc8-inlining-failed.patch
  xen.bug1079730.patch
* Tue Jan 15 2019 carnold@suse.com
- bsc#1121960 - xen: sync with Factory
  xen.spec
  xen.changes
* Sat Jan 12 2019 Jan Engelhardt <jengelh@inai.de>
- Replace old $RPM_* shell vars.
- Run fdupes for all architectures, and not crossing
  subvolume boundaries.
* Thu Jan 10 2019 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Do not run %%fdupes on aarch64 to avoid the hardlink-across-partition
  rpmlint error
* Tue Jan  8 2019 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Require qemu-seabios only on x86* as it is not available on non-x86
  systems
* Thu Dec 27 2018 Bernhard Wiedemann <bwiedemann@suse.com>
- Avoid creating dangling symlinks (bsc#1116524)
  This reverts the revert of tmp_build.patch
* Tue Dec  4 2018 carnold@suse.com
- Update to Xen 4.11.1 bug fix release (bsc#1027519)
  xen-4.11.1-testing-src.tar.bz2
- 5b505d59-tools-xentop-replace-use-of-deprecated-vwprintw.patch
  replaces xen.2b50cdbc444c637575580dcfa6c9525a84d5cc62.patch
- 5b76ec82-libxl-arm-Fix-build-on-arm64-acpi-w-gcc-8.2.patch
  replaces xen.b8f33431f3dd23fb43a879f4bdb4283fdc9465ad.patch
- Drop the following patches contained in the new tarball
  5b34b8fe-VMX-defer-vmx_vmcs_exit-as-long-as-possible.patch
  5b3cab8e-1-VMX-MSR_DEBUGCTL-handling.patch
  5b3cab8e-2-VMX-improve-MSR-load-save-API.patch
  5b3cab8e-3-VMX-cleanup-MSR-load-save-infra.patch
  5b3cab8f-1-VMX-factor-out-locate_msr_entry.patch
  5b3cab8f-2-VMX-remote-access-to-MSR-lists.patch
  5b3cab8f-3-VMX-improve-LBR-MSR-handling.patch
  5b3cab8f-4-VMX-pass-MSR-value-into-vmx_msr_add.patch
  5b3cab8f-5-VMX-load-only-guest-MSR-entries.patch
  5b3f8fa5-port-array_index_nospec-from-Linux.patch
  5b4321f6-x86-correctly-set-nonlazy_xstate_used-when-loading-full-state.patch
  5b4488e7-x86-spec-ctrl-cmdline-handling.patch
  5b471517-page_alloc-correct-first_dirty-calc-in-block-merging.patch
  5b4c9a60-allow-cpu_down-to-be-called-earlier.patch
  5b4db308-SVM-fix-cleanup-svm_inject_event.patch
  5b5040c3-cpupools-fix-state-when-downing-a-CPU-failed.patch
  5b5040f2-x86-AMD-distinguish-CU-from-HT.patch
  5b505fe5-VMX-fix-find-msr-build.patch
  5b508775-1-x86-distinguish-CPU-offlining-and-removal.patch
  5b508775-2-x86-possibly-bring-up-all-CPUs.patch
  5b508775-3-x86-cmdline-opt-to-avoid-use-of-secondary-HTs.patch
  5b508ce8-VMX-dont-clobber-dr6-while-debug-state-is-lazy.patch
  5b50df16-1-x86-xstate-use-guest-CPUID-policy.patch
  5b50df16-2-x86-make-xstate-calculation-errors-more-obvious.patch
  5b56feb1-hvm-Disallow-unknown-MSR_EFER-bits.patch
  5b56feb2-spec-ctrl-Fix-the-parsing-of-xpti--on-fixed-Intel-hardware.patch
  5b62ca93-VMX-avoid-hitting-BUG_ON.patch
  5b6d84ac-x86-fix-improve-vlapic-read-write.patch
  5b6d8ce2-x86-XPTI-parsing.patch
  5b72fbbe-ARM-disable-grant-table-v2.patch
  5b72fbbe-oxenstored-eval-order.patch
  5b72fbbe-vtx-Fix-the-checking-for-unknown-invalid-MSR_DEBUGCTL-bits.patch
  5b72fbbf-1-spec-ctrl-Calculate-safe-PTE-addresses-for-L1TF-mitigations.patch
  5b72fbbf-2-spec-ctrl-Introduce-an-option-to-control-L1TF-mitigation-for-PV-guests.patch
  5b72fbbf-3-shadow-Infrastructure-to-force-a-PV-guest-into-shadow-mode.patch
  5b72fbbf-4-mm-Plumbing-to-allow-any-PTE-update-to-fail-with--ERESTART.patch
  5b72fbbf-5-pv-Force-a-guest-into-shadow-mode-when-it-writes-an-L1TF-vulnerable-PTE.patch
  5b72fbbf-6-spec-ctrl-CPUID-MSR-definitions-for-L1D_FLUSH.patch
  5b72fbbf-7-msr-Virtualise-MSR_FLUSH_CMD-for-guests.patch
  5b72fbbf-8-spec-ctrl-Introduce-an-option-to-control-L1D_FLUSH-for-HVM-HAP-guests.patch
  5b72fbbf-x86-Make-spec-ctrl-no-a-global-disable-of-all-mitigations.patch
  5b72fbbf-xl.conf-Add-global-affinity-masks.patch
  5b74190e-x86-hvm-ioreq-MMIO-range-check-honor-DF.patch
  5b752762-x86-hvm-emul-rep-IO-should-not-cross-GFN-boundaries.patch
  5b75afef-x86-setup-avoid-OoB-E820-lookup.patch
  5b76b780-rangeset-inquiry-functions-tolerate-NULL.patch
  5b83c654-VT-d-dmar-iommu-mem-leak-fix.patch
  5b8d5832-x86-assorted-array_index_nospec-insertions.patch
  5ba11ed4-credit2-fix-moving-CPUs-between-cpupools.patch
  5bacae4b-x86-boot-allocate-extra-module-slot.patch
  5bae44ce-x86-silence-false-log-messages.patch
  5bb60c12-x86-split-opt_xpti.patch
  5bb60c4f-x86-split-opt_pv_l1tf.patch
  5bb60c74-x86-fix-xpti-and-pv-l1tf.patch
  5bcf0722-x86-boot-enable-NMIs.patch
  5bd076e9-dombuilder-init-vcpu-debug-regs-correctly.patch
  5bd076e9-x86-boot-init-debug-regs-correctly.patch
  5bd076e9-x86-init-vcpu-debug-regs-correctly.patch
  5bd0e0cf-vvmx-Disallow-the-use-of-VT-x-instructions-when-nested-virt-is-disabled.patch
  5bd0e11b-x86-disallow-VT-x-insns-without-nested-virt.patch
  5bd85bfd-x86-fix-crash-on-xl-set-parameter-pcid.patch
  5be2a308-x86-extend-get_platform_badpages.patch
  5be2a354-x86-work-around-HLE-host-lockup-erratum.patch
  xsa275-1.patch
  xsa275-2.patch
  xsa276-1.patch
  xsa276-2.patch
  xsa277.patch
  xsa279.patch
  xsa280-1.patch
  xsa280-2.patch
* Wed Nov 21 2018 carnold@suse.com
- bsc#1116524 - Package xen-tools-4.11.0_09-2.1.x86_64 broken:
  Missing /bin/domu-xenstore.  This was broken because "make
  package build reproducible" change. (boo#1047218, boo#1062303)
  This fix reverses the change to this patch.
  tmp_build.patch
* Mon Nov 12 2018 carnold@suse.com
- bsc#1115040 - VUL-0: CVE-2018-19961 CVE-2018-19962: xen:
  insufficient TLB flushing / improper large page mappings with AMD
  IOMMUs (XSA-275)
  xsa275-1.patch
  xsa275-2.patch
- bsc#1115043 - VUL-0: CVE-2018-19963: xen: resource accounting
  issues in x86 IOREQ server handling (XSA-276)
  xsa276-1.patch
  xsa276-2.patch
- bsc#1115044 - VUL-0: CVE-2018-19964: xen: x86: incorrect error
  handling for guest p2m page removals (XSA-277)
  xsa277.patch
- bsc#1114405 - VUL-0: CVE-2018-18883: xen: Nested VT-x usable even
  when disabled (XSA-278)
  5bd0e11b-x86-disallow-VT-x-insns-without-nested-virt.patch
- bsc#1115045 - VUL-0: xen: CVE-2018-19965: x86: DoS from attempting
  to use INVPCID with a non-canonical addresses (XSA-279)
  xsa279.patch
- bsc#1115047 - VUL-0: CVE-2018-19966: xen: Fix for XSA-240
  conflicts with shadow paging (XSA-280)
  xsa280-1.patch
  xsa280-2.patch
- bsc#1114988 - VUL-0: CVE-2018-19967: xen: guest use of HLE
  constructs may lock up host (XSA-282)
  5be2a308-x86-extend-get_platform_badpages.patch
  5be2a354-x86-work-around-HLE-host-lockup-erratum.patch
- bsc#1108940 - L3: XEN SLE12-SP1 domU hang on SLE12-SP3 HV
  5bdc31d5-VMX-fix-vmx_handle_eoi.patch
- Upstream bug fixes (bsc#1027519)
  5b752762-x86-hvm-emul-rep-IO-should-not-cross-GFN-boundaries.patch
  5ba11ed4-credit2-fix-moving-CPUs-between-cpupools.patch
  5bacae4b-x86-boot-allocate-extra-module-slot.patch
  5bae44ce-x86-silence-false-log-messages.patch
  5bb60c12-x86-split-opt_xpti.patch
  5bb60c4f-x86-split-opt_pv_l1tf.patch
  5bb60c74-x86-fix-xpti-and-pv-l1tf.patch
  5bcf0722-x86-boot-enable-NMIs.patch
  5bd076e9-dombuilder-init-vcpu-debug-regs-correctly.patch
  5bd076e9-x86-boot-init-debug-regs-correctly.patch
  5bd076e9-x86-init-vcpu-debug-regs-correctly.patch
  5bd85bfd-x86-fix-crash-on-xl-set-parameter-pcid.patch
* Tue Nov  6 2018 carnold@suse.com
- bsc#1114405 - VUL-0: CVE-2018-18883: xen: Nested VT-x usable even
  when disabled (XSA-278)
  5bd0e0cf-vvmx-Disallow-the-use-of-VT-x-instructions-when-nested-virt-is-disabled.patch
* Wed Oct 24 2018 ohering@suse.de
- Use SMBIOS_REL_DATE instead of SMBIOS_DATE for reproducible binaries
* Wed Oct 24 2018 Bernhard Wiedemann <bwiedemann@suse.com>
- make package build reproducible (boo#1047218, boo#1062303)
  * Set SMBIOS_REL_DATE
  * Update tmp_build.patch to use SHA instead of random build-id
  * Add reproducible.patch to use --no-insert-timestamp
* Mon Oct 15 2018 ohering@suse.de
- Building with ncurses 6.1 will fail without
  xen.2b50cdbc444c637575580dcfa6c9525a84d5cc62.patch
- Building libxl acpi support on aarch64 with gcc 8.2 will fail without
  xen.b8f33431f3dd23fb43a879f4bdb4283fdc9465ad.patch
* Tue Sep 11 2018 carnold@suse.com
- bsc#1106263 - L3: The affinity reporting via 'xl vcpu-list' is
  apparently broken
  5b8fae26-tools-libxl-correct-vcpu-affinity-output-with-sparse-physical-cpu-map.patch
  5b8fae26-xen-fill-topology-info-for-all-present-cpus.patch
  5b8fb5af-tools-xl-refuse-to-set-number-of-vcpus-to-0-via-xl-vcpu-set.patch
* Tue Sep 11 2018 carnold@suse.com
- bsc#1094508 - L3: Kernel oops in fs/dcache.c called by
  d_materialise_unique()
  5b9784ad-x86-HVM-drop-hvm_fetch_from_guest_linear.patch
  5b9784d2-x86-HVM-add-known_gla-helper.patch
  5b9784f2-x86-HVM-split-page-straddling-accesses.patch
- bsc#1103279 - (CVE-2018-15470) VUL-0: CVE-2018-15470: xen:
  oxenstored does not apply quota-maxentity (XSA-272)
  5b72fbbe-oxenstored-eval-order.patch
- bsc#1103275 - (CVE-2018-15469) VUL-0: CVE-2018-15469: xen: Use of
  v2 grant tables may cause crash on ARM (XSA-268)
  5b72fbbe-ARM-disable-grant-table-v2.patch
- Upstream patches from Jan (bsc#1027519)
  5b6d84ac-x86-fix-improve-vlapic-read-write.patch
  5b74190e-x86-hvm-ioreq-MMIO-range-check-honor-DF.patch
  5b75afef-x86-setup-avoid-OoB-E820-lookup.patch
  5b76b780-rangeset-inquiry-functions-tolerate-NULL.patch
  5b83c654-VT-d-dmar-iommu-mem-leak-fix.patch
  5b8d5832-x86-assorted-array_index_nospec-insertions.patch
- Drop 5b741962-x86-write-to-correct-variable-in-parse_pv_l1tf.patch
* Tue Aug 28 2018 carnold@suse.com
- bsc#1078292 - rpmbuild -ba SPECS/xen.spec with xen-4.9.1 failed
  xen.spec
* Fri Aug 17 2018 carnold@suse.com
- bsc#1091107 - VUL-0: CVE-2018-3646: xen: L1 Terminal Fault -VMM
  (XSA-273)
  5b72fbbf-1-spec-ctrl-Calculate-safe-PTE-addresses-for-L1TF-mitigations.patch
  5b72fbbf-2-spec-ctrl-Introduce-an-option-to-control-L1TF-mitigation-for-PV-guests.patch
  5b72fbbf-3-shadow-Infrastructure-to-force-a-PV-guest-into-shadow-mode.patch
  5b72fbbf-4-mm-Plumbing-to-allow-any-PTE-update-to-fail-with--ERESTART.patch
  5b72fbbf-5-pv-Force-a-guest-into-shadow-mode-when-it-writes-an-L1TF-vulnerable-PTE.patch
  5b72fbbf-6-spec-ctrl-CPUID-MSR-definitions-for-L1D_FLUSH.patch
  5b72fbbf-7-msr-Virtualise-MSR_FLUSH_CMD-for-guests.patch
  5b72fbbf-8-spec-ctrl-Introduce-an-option-to-control-L1D_FLUSH-for-HVM-HAP-guests.patch
- bsc#1103276 - VUL-0: CVE-2018-15468: xen: x86: Incorrect
  MSR_DEBUGCTL handling lets guests enable BTS (XSA-269)
  5b72fbbe-vtx-Fix-the-checking-for-unknown-invalid-MSR_DEBUGCTL-bits.patch
- Upstream prereq patches for XSA-273 and other upstream fixes
  (bsc#1027519)
  5b34b8fe-VMX-defer-vmx_vmcs_exit-as-long-as-possible.patch
  5b3cab8e-1-VMX-MSR_DEBUGCTL-handling.patch
  5b3cab8e-2-VMX-improve-MSR-load-save-API.patch
  5b3cab8e-3-VMX-cleanup-MSR-load-save-infra.patch
  5b3cab8f-1-VMX-factor-out-locate_msr_entry.patch
  5b3cab8f-2-VMX-remote-access-to-MSR-lists.patch
  5b3cab8f-3-VMX-improve-LBR-MSR-handling.patch
  5b3cab8f-4-VMX-pass-MSR-value-into-vmx_msr_add.patch
  5b3cab8f-5-VMX-load-only-guest-MSR-entries.patch
  5b4321f6-x86-correctly-set-nonlazy_xstate_used-when-loading-full-state.patch
  5b505fe5-VMX-fix-find-msr-build.patch
  5b56feb1-hvm-Disallow-unknown-MSR_EFER-bits.patch
  5b56feb2-spec-ctrl-Fix-the-parsing-of-xpti--on-fixed-Intel-hardware.patch
  5b62ca93-VMX-avoid-hitting-BUG_ON.patch
  5b6d8ce2-x86-XPTI-parsing.patch
  5b72fbbf-x86-Make-spec-ctrl-no-a-global-disable-of-all-mitigations.patch
  5b72fbbf-xl.conf-Add-global-affinity-masks.patch
  5b741962-x86-write-to-correct-variable-in-parse_pv_l1tf.patch
* Tue Jul 24 2018 carnold@suse.com
- Upstream patches from Jan (bsc#1027519)
  5b3f8fa5-port-array_index_nospec-from-Linux.patch
  5b4488e7-x86-spec-ctrl-cmdline-handling.patch
  5b471517-page_alloc-correct-first_dirty-calc-in-block-merging.patch
  5b4c9a60-allow-cpu_down-to-be-called-earlier.patch
  5b4db308-SVM-fix-cleanup-svm_inject_event.patch
  5b5040c3-cpupools-fix-state-when-downing-a-CPU-failed.patch
  5b5040f2-x86-AMD-distinguish-CU-from-HT.patch
  5b508775-1-x86-distinguish-CPU-offlining-and-removal.patch
  5b508775-2-x86-possibly-bring-up-all-CPUs.patch
  5b508775-3-x86-cmdline-opt-to-avoid-use-of-secondary-HTs.patch
  5b508ce8-VMX-dont-clobber-dr6-while-debug-state-is-lazy.patch
  5b50df16-1-x86-xstate-use-guest-CPUID-policy.patch
  5b50df16-2-x86-make-xstate-calculation-errors-more-obvious.patch
  gcc8-fix-format-warning-on-i586.patch
  gcc8-fix-array-warning-on-i586.patch
- Drop xen.fuzz-_FORTIFY_SOURCE.patch
  gcc8-fix-warning-on-i586.patch
* Mon Jul  9 2018 carnold@suse.com
- Update to Xen 4.11.0 FCS (fate#325202, fate#325123)
  xen-4.11.0-testing-src.tar.bz2
  disable-building-pv-shim.patch
- Dropped patches
  5a33a12f-domctl-improve-locking-during-domain-destruction.patch
  5a6703cb-x86-move-invocations-of-hvm_flush_guest_tlbs.patch
  5a79d7ed-libxc-packed-initrd-dont-fail-domain-creation.patch
  5a9985bd-x86-invpcid-support.patch
  5ac72a48-gcc8.patch
  5ac72a5f-gcc8.patch
  5ac72a64-gcc8.patch
  5ac72a69-gcc8.patch
  5ac72a6e-gcc8.patch
  5ac72a74-gcc8.patch
  5ac72a7b-gcc8.patch
  5ad4923e-x86-correct-S3-resume-ordering.patch
  5ad49293-x86-suppress-BTI-mitigations-around-S3.patch
  5ad600d4-x86-pv-introduce-x86emul_read_dr.patch
  5ad600d4-x86-pv-introduce-x86emul_write_dr.patch
  5ad8c3a7-x86-spec_ctrl-update-retpoline-decision-making.patch
  5adda097-x86-HPET-fix-race-triggering-ASSERT.patch
  5adda0d5-x86-HVM-never-retain-emulated-insn-cache.patch
  5adde9ed-xpti-fix-double-fault-handling.patch
  5ae06fad-SVM-fix-intercepts-for-SYS-CALL-ENTER-MSRs.patch
  5ae31917-x86-cpuidle-init-stats-lock-once.patch
  5aeaeae4-introduce-vcpu_sleep_nosync_locked.patch
  5aeaeaf0-sched-fix-races-in-vcpu-migration.patch
  5aeb2c57-x86-retval-checks-of-set-guest-trapbounce.patch
  5aec7393-1-x86-xpti-avoid-copy.patch
  5aec7393-2-x86-xpti-write-cr3.patch
  5aec744a-3-x86-xpti-per-domain-flag.patch
  5aec744a-4-x86-xpti-use-invpcid.patch
  5aec744a-5-x86-xpti-no-global-pages.patch
  5aec744a-6-x86-xpti-cr3-valid-flag.patch
  5aec744a-7-x86-xpti-pv_guest_cr4_to_real_cr4.patch
  5aec744b-8-x86-xpti-cr3-helpers.patch
  5aec74a8-9-x86-xpti-use-pcid.patch
  5af1daa9-1-x86-traps-fix-dr6-handing-in-DB-handler.patch
  5af1daa9-2-x86-pv-move-exception-injection-into-test_all_events.patch
  5af1daa9-3-x86-traps-use-IST-for-DB.patch
  5af1daa9-4-x86-traps-fix-handling-of-DB-in-hypervisor-context.patch
  5af1daa9-x86-HVM-guard-against-bogus-emulator-ioreq-state.patch
  5af1daa9-x86-vpt-support-IO-APIC-routed-intr.patch
  5af97999-viridian-cpuid-leaf-40000003.patch
  5afc13ae-1-x86-read-MSR_ARCH_CAPABILITIES-once.patch
  5afc13ae-2-x86-express-Xen-SPEC_CTRL-choice-as-variable.patch
  5afc13ae-3-x86-merge-bti_ist_info-use_shadow_spec_ctrl.patch
  5afc13ae-4-x86-fold-XEN_IBRS-ALTERNATIVES.patch
  5afc13ae-5-x86-rename-bits-of-spec_ctrl-infrastructure.patch
  5afc13ae-6-x86-elide-MSR_SPEC_CTRL-handling-in-idle.patch
  5afc13ae-7-x86-split-X86_FEATURE_SC_MSR.patch
  5afc13ae-8-x86-explicitly-set-Xen-default-SPEC_CTRL.patch
  5afc13ae-9-x86-cpuid-improve-guest-policies-for-speculative.patch
  5afc13ae-A-x86-introduce-spec-ctrl-cmdline-opt.patch
  5b02c786-x86-AMD-mitigations-for-GPZ-SP4.patch
  5b02c786-x86-Intel-mitigations-for-GPZ-SP4.patch
  5b02c786-x86-msr-virtualise-SPEC_CTRL-SSBD.patch
  5b0bc9da-x86-XPTI-fix-S3-resume.patch
  5b0d2286-libxc-x86-PV-dont-hand-through-CPUID-leaf-0x80000008.patch
  5b0d2d91-x86-suppress-sync-when-XPTI-off.patch
  5b0d2dbc-x86-correct-default_xen_spec_ctrl.patch
  5b0d2ddc-x86-CPUID-dont-override-tool-stack-hidden-STIBP.patch
  5b150ef9-x86-fix-error-handling-of-pv-dr7-shadow.patch
  5b21825d-1-x86-support-fully-eager-FPU-context-switching.patch
  5b21825d-2-x86-spec-ctrl-mitigations-for-LazyFPU.patch
  5b238b92-x86-HVM-account-for-fully-eager-FPU.patch
  5b2b7172-x86-EFI-fix-FPU-state-handling-around-runtime-calls.patch
  5b31e004-x86-HVM-emul-attempts-FPU-set-fpu_initialised.patch
  5b323e3c-x86-EFI-fix-FPU-state-handling-around-runtime-calls.patch
  5b34882d-x86-mm-dont-bypass-preemption-checks.patch
  5b348874-x86-refine-checks-in-DB-handler.patch
  5b348897-libxl-qemu_disk_scsi_drive_string-break-out-common.patch
  5b3488a2-libxl-restore-passing-ro-to-qemu-for-SCSI-disks.patch
  5b34891a-x86-HVM-dont-cause-NM-to-be-raised.patch
  5b348954-x86-guard-against-NM.patch
  libxl.Add-a-version-check-of-QEMU-for-QMP-commands.patch
  libxl.LIBXL_DESTROY_TIMEOUT.patch
  libxl.qmp-Tell-QEMU-about-live-migration-or-snapshot.patch
  xen_fix_build_with_acpica_20180427_and_new_packages.patch
* Wed Jul  4 2018 trenn@suse.de
- Submit upstream patch libacpi: fixes for iasl >= 20180427
  git commit 858dbaaeda33b05c1ac80aea0ba9a03924e09005
  xen_fix_build_with_acpica_20180427_and_new_packages.patch
  This is needed for acpica package to get updated in our build service
* Fri Jun 29 2018 carnold@suse.com
- Upstream patches from Jan (bsc#1027519)
  5b02c786-x86-AMD-mitigations-for-GPZ-SP4.patch (Replaces Spectre-v4-1.patch)
  5b02c786-x86-Intel-mitigations-for-GPZ-SP4.patch (Replaces Spectre-v4-2.patch)
  5b02c786-x86-msr-virtualise-SPEC_CTRL-SSBD.patch (Replaces Spectre-v4-3.patch)
  5b0bc9da-x86-XPTI-fix-S3-resume.patch
  5b0d2286-libxc-x86-PV-dont-hand-through-CPUID-leaf-0x80000008.patch
  5b0d2d91-x86-suppress-sync-when-XPTI-off.patch
  5b0d2dbc-x86-correct-default_xen_spec_ctrl.patch
  5b0d2ddc-x86-CPUID-dont-override-tool-stack-hidden-STIBP.patch
  5b150ef9-x86-fix-error-handling-of-pv-dr7-shadow.patch
  5b21825d-1-x86-support-fully-eager-FPU-context-switching.patch (Replaces xsa267-1.patch)
  5b21825d-2-x86-spec-ctrl-mitigations-for-LazyFPU.patch (Replaces xsa267-2.patch)
  5b238b92-x86-HVM-account-for-fully-eager-FPU.patch
  5b2b7172-x86-EFI-fix-FPU-state-handling-around-runtime-calls.patch
  5b31e004-x86-HVM-emul-attempts-FPU-set-fpu_initialised.patch
  5b323e3c-x86-EFI-fix-FPU-state-handling-around-runtime-calls.patch
  5b34882d-x86-mm-dont-bypass-preemption-checks.patch (Replaces xsa264.patch)
  5b348874-x86-refine-checks-in-DB-handler.patch (Replaces xsa265.patch)
  5b348897-libxl-qemu_disk_scsi_drive_string-break-out-common.patch (Replaces xsa266-1-<>.patch)
  5b3488a2-libxl-restore-passing-ro-to-qemu-for-SCSI-disks.patch (Replaces xsa266-2-<>.patch)
  5b34891a-x86-HVM-dont-cause-NM-to-be-raised.patch
  5b348954-x86-guard-against-NM.patch
* Mon Jun 25 2018 ohering@suse.de
- Fix more build gcc8 related failures with xen.fuzz-_FORTIFY_SOURCE.patch
* Mon Jun 25 2018 ohering@suse.de
- bsc#1098403 - fix regression introduced by changes for bsc#1079730
  a PV domU without qcow2 and/or vfb has no qemu attached.
  Ignore QMP errors for PV domUs to handle PV domUs with and without
  an attached qemu-xen.
  xen.bug1079730.patch
* Mon Jun 18 2018 carnold@suse.com
- bsc#1097521 - VUL-0: CVE-2018-12891: xen: preemption checks
  bypassed in x86 PV MM handling (XSA-264)
  xsa264.patch
- bsc#1097522 - VUL-0: CVE-2018-12893: xen: x86: #DB exception
  safety check can be triggered by a guest (XSA-265)
  xsa265.patch
- bsc#1097523 - VUL-0: CVE-2018-12892: xen: libxl fails to honour
  readonly flag on HVM emulated SCSI disks (XSA-266)
  xsa266-1-libxl-qemu_disk_scsi_drive_string-Break-out-common-p.patch
  xsa266-2-libxl-restore-passing-readonly-to-qemu-for-SCSI-disk.patch
* Wed Jun 13 2018 carnold@suse.com
- bsc#1095242 - VUL-0: CVE-2018-3665: xen: Lazy FP Save/Restore
  (XSA-267)
  xsa267-1.patch
  xsa267-2.patch
* Fri Jun  1 2018 carnold@suse.com
- bsc#1092543 - GCC 8: xen build fails
  gcc8-fix-warning-on-i586.patch
* Fri May 18 2018 carnold@suse.com
- bsc#1092631 - VUL-0: CVE-2018-3639: xen: V4 – Speculative Store
  Bypass aka "Memory Disambiguation" (XSA-263)
  5ad4923e-x86-correct-S3-resume-ordering.patch
  5ad49293-x86-suppress-BTI-mitigations-around-S3.patch
  5afc13ae-1-x86-read-MSR_ARCH_CAPABILITIES-once.patch
  5afc13ae-2-x86-express-Xen-SPEC_CTRL-choice-as-variable.patch
  5afc13ae-3-x86-merge-bti_ist_info-use_shadow_spec_ctrl.patch
  5afc13ae-4-x86-fold-XEN_IBRS-ALTERNATIVES.patch
  5afc13ae-5-x86-rename-bits-of-spec_ctrl-infrastructure.patch
  5afc13ae-6-x86-elide-MSR_SPEC_CTRL-handling-in-idle.patch
  5afc13ae-7-x86-split-X86_FEATURE_SC_MSR.patch
  5afc13ae-8-x86-explicitly-set-Xen-default-SPEC_CTRL.patch
  5afc13ae-9-x86-cpuid-improve-guest-policies-for-speculative.patch
  5afc13ae-A-x86-introduce-spec-ctrl-cmdline-opt.patch
  Spectre-v4-1.patch
  Spectre-v4-2.patch
  Spectre-v4-3.patch
* Thu May 17 2018 ohering@suse.de
- Always call qemus xen-save-devices-state in suspend/resume to
  fix migration with qcow2 images (bsc#1079730)
  libxl.Add-a-version-check-of-QEMU-for-QMP-commands.patch
  libxl.qmp-Tell-QEMU-about-live-migration-or-snapshot.patch
  xen.bug1079730.patch
* Wed May 16 2018 carnold@suse.com
- bsc#1087289 - L3: Xen BUG at sched_credit.c:1663
  5aeaeae4-introduce-vcpu_sleep_nosync_locked.patch
  5aeaeaf0-sched-fix-races-in-vcpu-migration.patch
- Upstream patches from Jan (bsc#1027519)
  5ad600d4-x86-pv-introduce-x86emul_read_dr.patch
  5ad600d4-x86-pv-introduce-x86emul_write_dr.patch
  5ad8c3a7-x86-spec_ctrl-update-retpoline-decision-making.patch
  5adda097-x86-HPET-fix-race-triggering-ASSERT.patch
  5adda0d5-x86-HVM-never-retain-emulated-insn-cache.patch
  5ae06fad-SVM-fix-intercepts-for-SYS-CALL-ENTER-MSRs.patch
  5ae31917-x86-cpuidle-init-stats-lock-once.patch
  5aeb2c57-x86-retval-checks-of-set-guest-trapbounce.patch
  5af1daa9-1-x86-traps-fix-dr6-handing-in-DB-handler.patch (Replaces xsa260-1.patch)
  5af1daa9-2-x86-pv-move-exception-injection-into-test_all_events.patch (Replaces xsa260-2.patch)
  5af1daa9-3-x86-traps-use-IST-for-DB.patch (Replaces xsa260-3.patch)
  5af1daa9-4-x86-traps-fix-handling-of-DB-in-hypervisor-context.patch (Replaces xsa260-4.patch)
  5af1daa9-x86-HVM-guard-against-bogus-emulator-ioreq-state.patch (Replaces xsa262.patch)
  5af1daa9-x86-vpt-support-IO-APIC-routed-intr.patch (Replaces xsa261.patch)
  5af97999-viridian-cpuid-leaf-40000003.patch
* Fri May 11 2018 carnold@suse.com
- Fixes related to Page Table Isolation (XPTI). bsc#1074562 XSA-254
  5a6703cb-x86-move-invocations-of-hvm_flush_guest_tlbs.patch
  5a9985bd-x86-invpcid-support.patch
  5adde9ed-xpti-fix-double-fault-handling.patch
  5aec7393-1-x86-xpti-avoid-copy.patch
  5aec7393-2-x86-xpti-write-cr3.patch
  5aec744a-3-x86-xpti-per-domain-flag.patch
  5aec744a-4-x86-xpti-use-invpcid.patch
  5aec744a-5-x86-xpti-no-global-pages.patch
  5aec744a-6-x86-xpti-cr3-valid-flag.patch
  5aec744a-7-x86-xpti-pv_guest_cr4_to_real_cr4.patch
  5aec744b-8-x86-xpti-cr3-helpers.patch
  5aec74a8-9-x86-xpti-use-pcid.patch
* Wed May  9 2018 carnold@suse.com
- bsc#1092543 - GCC 8: xen build fails
  5ac72a48-gcc8.patch
  5ac72a5f-gcc8.patch
  5ac72a64-gcc8.patch
  5ac72a69-gcc8.patch
  5ac72a6e-gcc8.patch
  5ac72a74-gcc8.patch
  5ac72a7b-gcc8.patch
  gcc8-inlining-failed.patch
* Tue May  8 2018 carnold@suse.com
- Update to Xen 4.10.1 bug fix release (bsc#1027519)
  xen-4.10.1-testing-src.tar.bz2
  disable-building-pv-shim.patch
- Drop the following patches contained in the new tarball
  5a21a77e-x86-pv-construct-d0v0s-GDT-properly.patch
  5a2fda0d-x86-mb2-avoid-Xen-when-looking-for-module-crashkernel-pos.patch
  5a2ffc1f-x86-mm-drop-bogus-paging-mode-assertion.patch
  5a313972-x86-microcode-add-support-for-AMD-Fam17.patch
  5a32bd79-x86-vmx-dont-use-hvm_inject_hw_exception-in-.patch
  5a4caa5e-x86-IRQ-conditionally-preserve-access-perm.patch
  5a4caa8c-x86-E820-don-t-overrun-array.patch
  5a4e2bca-x86-free-msr_vcpu_policy-during-destruction.patch
  5a4e2c2c-x86-upcall-inject-spurious-event-after-setting-vector.patch
  5a4fd893-1-x86-break-out-alternative-asm-into-separate-header.patch
  5a4fd893-2-x86-introduce-ALTERNATIVE_2-macros.patch
  5a4fd893-3-x86-hvm-rename-update_guest_vendor-to-cpuid_policy_changed.patch
  5a4fd893-4-x86-introduce-cpuid_policy_updated.patch
  5a4fd893-5-x86-entry-remove-partial-cpu_user_regs.patch
  5a4fd894-1-x86-rearrange-RESTORE_ALL-to-restore-in-stack-order.patch
  5a4fd894-2-x86-hvm-use-SAVE_ALL-after-VMExit.patch
  5a4fd894-3-x86-erase-guest-GPRs-on-entry-to-Xen.patch
  5a4fd894-4-clarifications-to-wait-infrastructure.patch
  5a534c78-x86-dont-use-incorrect-CPUID-values-for-topology.patch
  5a5cb24c-x86-mm-always-set-_PAGE_ACCESSED-on-L4-updates.patch
  5a5e2cff-x86-Meltdown-band-aid.patch
  5a5e2d73-x86-Meltdown-band-aid-conditional.patch
  5a5e3a4e-1-x86-support-compiling-with-indirect-branch-thunks.patch
  5a5e3a4e-2-x86-support-indirect-thunks-from-asm.patch
  5a5e3a4e-3-x86-report-speculative-mitigation-details.patch
  5a5e3a4e-4-x86-AMD-set-lfence-as-Dispatch-Serialising.patch
  5a5e3a4e-5-x86-introduce-alternative-indirect-thunks.patch
  5a5e3a4e-6-x86-definitions-for-Indirect-Branch-Controls.patch
  5a5e3a4e-7-x86-cmdline-opt-to-disable-IBRS-IBPB-STIBP.patch
  5a5e459c-1-x86-SVM-offer-CPUID-faulting-to-AMD-HVM-guests.patch
  5a5e459c-2-x86-report-domain-id-on-CPUID.patch
  5a68bc16-x86-acpi-process-softirqs-logging-Cx.patch
  5a69c0b9-x86-fix-GET_STACK_END.patch
  5a6b36cd-1-x86-cpuid-handling-of-IBRS-IBPB-STIBP-and-IBRS-for-guests.patch
  5a6b36cd-2-x86-msr-emulation-of-SPEC_CTRL-PRED_CMD.patch
  5a6b36cd-3-x86-migrate-MSR_SPEC_CTRL.patch
  5a6b36cd-4-x86-hvm-permit-direct-access-to-SPEC_CTRL-PRED_CMD.patch
  5a6b36cd-5-x86-use-SPEC_CTRL-on-entry.patch
  5a6b36cd-6-x86-clobber-RSB-RAS-on-entry.patch
  5a6b36cd-7-x86-no-alternatives-in-NMI-MC-paths.patch
  5a6b36cd-8-x86-boot-calculate-best-BTI-mitigation.patch
  5a6b36cd-9-x86-issue-speculation-barrier.patch
  5a6b36cd-A-x86-offer-Indirect-Branch-Controls-to-guests.patch
  5a6b36cd-B-x86-clear-SPEC_CTRL-while-idle.patch
  5a7b1bdd-x86-reduce-Meltdown-band-aid-IPI-overhead.patch
  5a843807-x86-spec_ctrl-fix-bugs-in-SPEC_CTRL_ENTRY_FROM_INTR_IST.patch
  5a856a2b-x86-emul-fix-64bit-decoding-of-segment-overrides.patch
  5a856a2b-x86-use-32bit-xors-for-clearing-GPRs.patch
  5a856a2b-x86-xpti-hide-almost-all-of-Xen-image-mappings.patch
  5a8be788-x86-nmi-start-NMI-watchdog-on-CPU0-after-SMP.patch
  5a95373b-x86-PV-avoid-leaking-other-guests-MSR_TSC_AUX.patch
  5a95571f-memory-dont-implicitly-unpin-in-decrease-res.patch
  5a95576c-gnttab-ARM-dont-corrupt-shared-GFN-array.patch
  5a955800-gnttab-dont-free-status-pages-on-ver-change.patch
  5a955854-x86-disallow-HVM-creation-without-LAPIC-emul.patch
  5a956747-x86-HVM-dont-give-wrong-impression-of-WRMSR-success.patch
  5a9eb7f1-x86-xpti-dont-map-stack-guard-pages.patch
  5a9eb85c-x86-slightly-reduce-XPTI-overhead.patch
  5a9eb890-x86-remove-CR-reads-from-exit-to-guest-path.patch
  5aa2b6b9-cpufreq-ondemand-CPU-offlining-race.patch
  5aaa9878-x86-vlapic-clear-TMR-bit-for-edge-triggered-intr.patch
  xsa258.patch
  xsa259.patch
* Wed Apr 25 2018 carnold@suse.com
- bsc#1090820 - VUL-0: CVE-2018-8897: xen: x86: mishandling of
  debug exceptions (XSA-260)
  xsa260-1.patch
  xsa260-2.patch
  xsa260-3.patch
  xsa260-4.patch
- bsc#1090822 - VUL-0: CVE-2018-10982: xen: x86 vHPET interrupt
  injection errors (XSA-261)
  xsa261.patch
- bsc#1090823 - VUL-0: CVE-2018-10981: xen: qemu may drive Xen into
  unbounded loop (XSA-262)
  xsa262.patch
* Mon Apr 16 2018 carnold@suse.com
- bsc#1089152 - VUL-0: CVE-2018-10472: xen: Information leak via
  crafted user-supplied CDROM (XSA-258)
  xsa258.patch
- bsc#1089635 - VUL-0: CVE-2018-10471: xen: x86: PV guest may crash
  Xen with XPTI (XSA-259)
  xsa259.patch
* Wed Mar 28 2018 ohering@suse.de
- Preserve xen-syms from xen-dbg.gz to allow processing vmcores
  with crash(1) (bsc#1087251)
* Mon Mar 26 2018 carnold@suse.com
- Upstream patches from Jan (bsc#1027519) and fixes related to
  Page Table Isolation (XPTI). See also bsc#1074562 XSA-254
  5a856a2b-x86-xpti-hide-almost-all-of-Xen-image-mappings.patch
  5a9eb7f1-x86-xpti-dont-map-stack-guard-pages.patch
  5a9eb85c-x86-slightly-reduce-XPTI-overhead.patch
  5a9eb890-x86-remove-CR-reads-from-exit-to-guest-path.patch
  5aa2b6b9-cpufreq-ondemand-CPU-offlining-race.patch
  5aaa9878-x86-vlapic-clear-TMR-bit-for-edge-triggered-intr.patch
* Thu Mar  1 2018 carnold@suse.com
- bsc#1072834 - Xen HVM: unchecked MSR access error: RDMSR from
  0xc90 at rIP: 0xffffffff93061456 (native_read_msr+0x6/0x30)
  5a956747-x86-HVM-dont-give-wrong-impression-of-WRMSR-success.patch
- Upstream patches from Jan (bsc#1027519)
  5a79d7ed-libxc-packed-initrd-dont-fail-domain-creation.patch
  5a7b1bdd-x86-reduce-Meltdown-band-aid-IPI-overhead.patch
  5a843807-x86-spec_ctrl-fix-bugs-in-SPEC_CTRL_ENTRY_FROM_INTR_IST.patch
  5a856a2b-x86-emul-fix-64bit-decoding-of-segment-overrides.patch
  5a856a2b-x86-use-32bit-xors-for-clearing-GPRs.patch
  5a8be788-x86-nmi-start-NMI-watchdog-on-CPU0-after-SMP.patch
  5a95373b-x86-PV-avoid-leaking-other-guests-MSR_TSC_AUX.patch
  5a95571f-memory-dont-implicitly-unpin-in-decrease-res.patch (Replaces xsa252.patch)
  5a95576c-gnttab-ARM-dont-corrupt-shared-GFN-array.patch (Replaces xsa255-1.patch)
  5a955800-gnttab-dont-free-status-pages-on-ver-change.patch (Replaces xsa255-2.patch)
  5a955854-x86-disallow-HVM-creation-without-LAPIC-emul.patch (Replaces xsa256.patch)
- Drop
  xsa252.patch
  xsa255-1.patch
  xsa255-2.patch
  xsa256.patch
* Mon Feb 12 2018 carnold@suse.com
- bsc#1080635 - VUL-0: CVE-2018-7540: xen: DoS via non-preemptable
  L3/L4 pagetable freeing (XSA-252)
  xsa252.patch
- bsc#1080662 - VUL-0: CVE-2018-7541: xen: grant table v2 -> v1
  transition may crash Xen (XSA-255)
  xsa255-1.patch
  xsa255-2.patch
- bsc#1080634 - VUL-0: CVE-2018-7542: xen: x86 PVH guest without
  LAPIC may DoS the host (XSA-256)
  xsa256.patch
* Fri Feb  9 2018 ohering@suse.de
- Remove stale systemd presets code for 13.2 and older
* Fri Feb  9 2018 ohering@suse.de
- fate#324965 - add script, udev rule and systemd service to watch
  for vcpu online/offline events in a HVM domU
  They are triggered via xl vcpu-set domU N
* Fri Feb  9 2018 ohering@suse.de
- Replace hardcoded xen with Name tag when refering to subpkgs
* Fri Feb  9 2018 ohering@suse.de
- Make sure tools and tools-domU require libs from the very same build
* Wed Feb  7 2018 jfehlig@suse.com
- tools-domU: Add support for qemu guest agent. New files
  80-xen-channel-setup.rules and xen-channel-setup.sh configure a
  xen-pv-channel for use by the guest agent
  FATE#324963
* Wed Feb  7 2018 ohering@suse.de
- Remove outdated /etc/xen/README*
* Mon Jan 29 2018 carnold@suse.com
- bsc#1073961 - VUL-0: CVE-2018-5244: xen: x86: memory leak with
  MSR emulation (XSA-253)
  5a4e2bca-x86-free-msr_vcpu_policy-during-destruction.patch
- bsc#1074562 - VUL-0: CVE-2017-5753,CVE-2017-5715,CVE-2017-5754
  xen: Information leak via side effects of speculative execution
  (XSA-254). Includes Spectre v2 mitigation.
  5a4caa5e-x86-IRQ-conditionally-preserve-access-perm.patch
  5a4caa8c-x86-E820-don-t-overrun-array.patch
  5a4e2c2c-x86-upcall-inject-spurious-event-after-setting-vector.patch
  5a4fd893-1-x86-break-out-alternative-asm-into-separate-header.patch
  5a4fd893-2-x86-introduce-ALTERNATIVE_2-macros.patch
  5a4fd893-3-x86-hvm-rename-update_guest_vendor-to-cpuid_policy_changed.patch
  5a4fd893-4-x86-introduce-cpuid_policy_updated.patch
  5a4fd893-5-x86-entry-remove-partial-cpu_user_regs.patch
  5a4fd894-1-x86-rearrange-RESTORE_ALL-to-restore-in-stack-order.patch
  5a4fd894-2-x86-hvm-use-SAVE_ALL-after-VMExit.patch
  5a4fd894-3-x86-erase-guest-GPRs-on-entry-to-Xen.patch
  5a4fd894-4-clarifications-to-wait-infrastructure.patch
  5a534c78-x86-dont-use-incorrect-CPUID-values-for-topology.patch
  5a5cb24c-x86-mm-always-set-_PAGE_ACCESSED-on-L4-updates.patch
  5a5e2cff-x86-Meltdown-band-aid.patch
  5a5e2d73-x86-Meltdown-band-aid-conditional.patch
  5a5e3a4e-1-x86-support-compiling-with-indirect-branch-thunks.patch
  5a5e3a4e-2-x86-support-indirect-thunks-from-asm.patch
  5a5e3a4e-3-x86-report-speculative-mitigation-details.patch
  5a5e3a4e-4-x86-AMD-set-lfence-as-Dispatch-Serialising.patch
  5a5e3a4e-5-x86-introduce-alternative-indirect-thunks.patch
  5a5e3a4e-6-x86-definitions-for-Indirect-Branch-Controls.patch
  5a5e3a4e-7-x86-cmdline-opt-to-disable-IBRS-IBPB-STIBP.patch
  5a5e459c-1-x86-SVM-offer-CPUID-faulting-to-AMD-HVM-guests.patch
  5a5e459c-2-x86-report-domain-id-on-CPUID.patch
  5a68bc16-x86-acpi-process-softirqs-logging-Cx.patch
  5a69c0b9-x86-fix-GET_STACK_END.patch
  5a6b36cd-1-x86-cpuid-handling-of-IBRS-IBPB-STIBP-and-IBRS-for-guests.patch
  5a6b36cd-2-x86-msr-emulation-of-SPEC_CTRL-PRED_CMD.patch
  5a6b36cd-3-x86-migrate-MSR_SPEC_CTRL.patch
  5a6b36cd-4-x86-hvm-permit-direct-access-to-SPEC_CTRL-PRED_CMD.patch
  5a6b36cd-5-x86-use-SPEC_CTRL-on-entry.patch
  5a6b36cd-6-x86-clobber-RSB-RAS-on-entry.patch
  5a6b36cd-7-x86-no-alternatives-in-NMI-MC-paths.patch
  5a6b36cd-8-x86-boot-calculate-best-BTI-mitigation.patch
  5a6b36cd-9-x86-issue-speculation-barrier.patch
  5a6b36cd-A-x86-offer-Indirect-Branch-Controls-to-guests.patch
  5a6b36cd-B-x86-clear-SPEC_CTRL-while-idle.patch
* Fri Jan 26 2018 carnold@suse.com
- Fix python3 deprecated atoi call (bsc#1067224)
  pygrub-python3-conversion.patch
- Drop xenmon-python3-conversion.patch
* Wed Jan 10 2018 ohering@suse.de
- bsc#1067317 - pass cache=writeback|unsafe|directsync to qemu,
  depending on the libxl disk settings
  libxl.add-option-to-disable-disk-cache-flushes-in-qdisk.patch
* Mon Jan  8 2018 ohering@suse.de
- Remove libxl.LIBXL_DESTROY_TIMEOUT.debug.patch
* Fri Jan  5 2018 carnold@suse.com
- bsc#1067224 - xen-tools have hard dependency on Python 2
  build-python3-conversion.patch
  bin-python3-conversion.patch
* Wed Dec 20 2017 carnold@suse.com
- bsc#1070165 - xen crashes after aborted localhost migration
  5a2ffc1f-x86-mm-drop-bogus-paging-mode-assertion.patch
- bsc#1035442 - L3: libxl: error: libxl.c:1676:devices_destroy_cb:
  libxl__devices_destroy failed
  5a33a12f-domctl-improve-locking-during-domain-destruction.patch
- Upstream patches from Jan (bsc#1027519)
  5a21a77e-x86-pv-construct-d0v0s-GDT-properly.patch
  5a2fda0d-x86-mb2-avoid-Xen-when-looking-for-module-crashkernel-pos.patch
  5a313972-x86-microcode-add-support-for-AMD-Fam17.patch
  5a32bd79-x86-vmx-dont-use-hvm_inject_hw_exception-in-.patch
* Wed Dec 13 2017 carnold@suse.com
- Update to Xen 4.10.0 FCS (fate#321394, fate#322686)
  xen-4.10.0-testing-src.tar.bz2
* Mon Dec 11 2017 ohering@suse.de
- Rebuild initrd if xen-tools-domU is updated
* Tue Dec  5 2017 carnold@suse.com
- Update to Xen 4.10.0-rc8 (fate#321394, fate#322686)
  xen-4.10.0-testing-src.tar.bz2
* Tue Nov 28 2017 ohering@suse.de
- Increase the value of LIBXL_DESTROY_TIMEOUT from 10 to 100 seconds
  If many domUs shutdown in parallel the backends can not keep up
  Add some debug output to track how long backend shutdown takes (bsc#1035442)
  libxl.LIBXL_DESTROY_TIMEOUT.patch
  libxl.LIBXL_DESTROY_TIMEOUT.debug.patch
* Tue Nov 28 2017 ohering@suse.de
- Adjust xenstore-run-in-studomain.patch to change the defaults
  in the code instead of changing the sysconfig template, to also
  cover the upgrade case
* Fri Nov 24 2017 carnold@suse.com
- Update to Xen 4.10.0-rc6 (fate#321394, fate#322686)
  xen-4.10.0-testing-src.tar.bz2
* Fri Nov 24 2017 ohering@suse.de
- Since xen switched to Kconfig, building a debug hypervisor
  was done by default. Adjust make logic to build a non-debug
  hypervisor by default, and continue to provide one as xen-dbg.gz
* Fri Nov 24 2017 ohering@suse.de
- fate#316614: set migration constraints from cmdline
  fix libxl.set-migration-constraints-from-cmdline.patch for xen-4.10
* Thu Nov 23 2017 ohering@suse.de
- Document the suse-diskcache-disable-flush option in
  xl-disk-configuration(5) (bsc#879425,bsc#1067317)
* Thu Nov 23 2017 rbrown@suse.com
- Replace references to /var/adm/fillup-templates with new
  %%_fillupdir macro (boo#1069468)
* Thu Nov 16 2017 carnold@suse.com
- Update to Xen 4.10.0-rc5 (fate#321394, fate#322686)
  xen-4.10.0-testing-src.tar.bz2
- fate#323663 - Run Xenstore in stubdomain
  xenstore-run-in-studomain.patch
* Thu Nov  9 2017 carnold@suse.com
- bsc#1067224 - xen-tools have hard dependency on Python 2
  pygrub-python3-conversion.patch
  xenmon-python3-conversion.patch
  migration-python3-conversion.patch
  xnloader.py
  xen2libvirt.py
* Wed Nov  8 2017 ohering@suse.de
- Remove xendriverdomain.service (bsc#1065185)
  Driver domains must be configured manually with custom .service file
* Thu Nov  2 2017 carnold@suse.com
- Update to Xen 4.10.0-rc3 (fate#321394, fate#322686)
  xen-4.10.0-testing-src.tar.bz2
- Drop 59f31268-libxc-remove-stale-error-check-for-domain-size.patch
* Thu Nov  2 2017 ohering@suse.de
- Adjust xen-dom0-modules.service to ignore errors (bsc#1065187)
* Fri Oct 27 2017 carnold@suse.com
- fate#324052 Support migration of Xen HVM domains larger than 1TB
  59f31268-libxc-remove-stale-error-check-for-domain-size.patch
* Wed Oct 25 2017 carnold@suse.com
- Update to Xen 4.10.0-rc2 (fate#321394, fate#322686)
  xen-4.10.0-testing-src.tar.bz2
* Mon Oct 16 2017 carnold@suse.com
- Update to Xen 4.10.0-rc1 (fate#321394, fate#322686)
  xen-4.10.0-testing-src.tar.bz2
- Drop patches included in new tarball
  592fd5f0-stop_machine-fill-result-only-in-case-of-error.patch
  596f257e-x86-fix-hvmemul_insn_fetch.patch
  5982fd99-VT-d-don-t-panic-warn-on-iommu-no-igfx.patch
  598c3630-VT-d-PI-disable-when-CPU-side-PI-is-off.patch
  598c3706-cpufreq-only-stop-ondemand-governor-if-started.patch
  5992f1e5-x86-grant-disallow-misaligned-PTEs.patch
  5992f20d-gnttab-split-maptrack-lock-to-make-it-useful-again.patch
  5992f233-gnttab-correct-pin-status-fixup-for-copy.patch
  59958e76-gnttab-dont-use-possibly-unbounded-tail-calls.patch
  59958ebf-gnttab-fix-transitive-grant-handling.patch
  59958edd-gnttab-avoid-spurious-maptrack-handle-alloc-failures.patch
  599da329-arm-mm-release-grant-lock-on-xatp1-error-paths.patch
  59a01223-x86-check-for-alloc-errors-in-modify_xen_mappings.patch
  59a0130c-x86-efi-dont-write-relocs-in-efi_arch_relocate_image-1st-pass.patch
  59a9221f-VT-d-use-correct-BDF-for-VF-to-search-VT-d-unit.patch
  59ae9177-x86-emul-fix-handling-of-unimplemented-Grp7-insns.patch
  59aec335-x86emul-correct-VEX-W-handling-for-VPINSRD.patch
  59aec375-x86emul-correct-VEX-L-handling-for-VCVTx2SI.patch
  59afcea0-x86-introduce-and-use-setup_force_cpu_cap.patch
  59b2a7f2-x86-HVM-correct-repeat-count-update-linear-phys.patch
  59b7d664-mm-make-sure-node-is-less-than-MAX_NUMNODES.patch
  59b7d69b-grant_table-fix-GNTTABOP_cache_flush-handling.patch
  59b7d6c8-xenstore-dont-unlink-connection-object-twice.patch
  59b7d6d9-gnttab-also-validate-PTE-perms-upon-destroy-replace.patch
  gcc7-arm.patch
  gcc7-mini-os.patch
* Tue Oct  3 2017 carnold@suse.com
- bsc#1061084 - VUL-0: xen: page type reference leak on x86
  (XSA-242)
  xsa242.patch
- bsc#1061086 - VUL-0: xen: x86: Incorrect handling of self-linear
  shadow mappings with translated guests (XSA-243)
  xsa243.patch
- bsc#1061087 - VUL-0: xen: x86: Incorrect handling of IST settings
  during CPU hotplug (XSA-244)
  xsa244.patch
* Mon Oct  2 2017 carnold@suse.com
- bsc#1061077 - VUL-0: xen: DMOP map/unmap missing argument checks
  (XSA-238)
  xsa238.patch
- bsc#1061080 - VUL-0: xen: hypervisor stack leak in x86 I/O
  intercept code (XSA-239)
  xsa239.patch
- bsc#1061081 - VUL-0: xen: Unlimited recursion in linear pagetable
  de-typing (XSA-240)
  xsa240-1.patch
  xsa240-2.patch
- bsc#1061082 - VUL-0: xen: Stale TLB entry due to page type
  release race (XSA-241)
  xsa241.patch
* Fri Sep 29 2017 carnold@suse.com
- bsc#1061075 - VUL-0: xen: pin count / page reference race in
  grant table code (XSA-236)
  xsa236.patch
- bsc#1061076 - VUL-0: xen: multiple MSI mapping issues on x86
  (XSA-237)
  xsa237-1.patch
  xsa237-2.patch
  xsa237-3.patch
  xsa237-4.patch
  xsa237-5.patch
* Tue Sep 26 2017 carnold@suse.com
- bsc#1056278 - VUL-0: xen: Missing NUMA node parameter
  verification (XSA-231)
  59b7d664-mm-make-sure-node-is-less-than-MAX_NUMNODES.patch
- bsc#1056280 - VUL-0: xen: Missing check for grant table (XSA-232)
  59b7d69b-grant_table-fix-GNTTABOP_cache_flush-handling.patch
- bsc#1056281 - VUL-0: xen: cxenstored: Race in domain cleanup
  (XSA-233)
  59b7d6c8-xenstore-dont-unlink-connection-object-twice.patch
- bsc#1056282 - VUL-0: xen: insufficient grant unmapping checks for
  x86 PV guests (XSA-234)
  59b7d6d9-gnttab-also-validate-PTE-perms-upon-destroy-replace.patch
- bsc#1055321 - VUL-0: xen: add-to-physmap error paths fail to
  release lock on ARM (XSA-235)
  599da329-arm-mm-release-grant-lock-on-xatp1-error-paths.patch
- Upstream patches from Jan (bsc#1027519)
  59a01223-x86-check-for-alloc-errors-in-modify_xen_mappings.patch
  59a0130c-x86-efi-dont-write-relocs-in-efi_arch_relocate_image-1st-pass.patch
  59a9221f-VT-d-use-correct-BDF-for-VF-to-search-VT-d-unit.patch
  59ae9177-x86-emul-fix-handling-of-unimplemented-Grp7-insns.patch
  59aec335-x86emul-correct-VEX-W-handling-for-VPINSRD.patch
  59aec375-x86emul-correct-VEX-L-handling-for-VCVTx2SI.patch
  59afcea0-x86-introduce-and-use-setup_force_cpu_cap.patch
  59b2a7f2-x86-HVM-correct-repeat-count-update-linear-phys.patch
- Dropped gcc7-xen.patch
* Thu Sep  7 2017 carnold@suse.com
- bsc#1057358 - Cannot Boot into SLES12.3 with Xen hypervisor when
  Secure Boot is Enabled
  xen.spec
* Tue Sep  5 2017 ohering@suse.de
- bsc#1055695 - XEN: 11SP4 and 12SP3 HVM guests can not be restored
  update from v6 to v9 to cover more cases for ballooned domUs
  libxc.sr.superpage.patch
* Mon Aug 28 2017 ohering@suse.de
- bsc#1026236 - remove suse_vtsc_tolerance= cmdline option for Xen
  drop the patch because it is not upstream acceptable
  remove xen.suse_vtsc_tolerance.patch
* Sat Aug 26 2017 ohering@suse.de
- bsc#1055695 - XEN: 11SP4 and 12SP3 HVM guests can not be restored
  after the save using xl stack
  libxc.sr.superpage.patch
* Tue Aug 22 2017 ohering@suse.de
- Unignore gcc-PIE
  the toolstack disables PIE for firmware builds as needed
* Mon Aug 21 2017 carnold@suse.com
- Upstream patches from Jan (bsc#1027519)
  592fd5f0-stop_machine-fill-result-only-in-case-of-error.patch
  596f257e-x86-fix-hvmemul_insn_fetch.patch
  5982fd99-VT-d-don-t-panic-warn-on-iommu-no-igfx.patch
  598c3630-VT-d-PI-disable-when-CPU-side-PI-is-off.patch
  598c3706-cpufreq-only-stop-ondemand-governor-if-started.patch
  5992f1e5-x86-grant-disallow-misaligned-PTEs.patch (Replaces xsa227.patch)
  5992f20d-gnttab-split-maptrack-lock-to-make-it-useful-again.patch (Replaces xsa228.patch)
  5992f233-gnttab-correct-pin-status-fixup-for-copy.patch (Replaces xsa230.patch)
  59958e76-gnttab-dont-use-possibly-unbounded-tail-calls.patch (Replaces xsa226-1.patch)
  59958ebf-gnttab-fix-transitive-grant-handling.patch (Replaces xsa226-2.patch)
  59958edd-gnttab-avoid-spurious-maptrack-handle-alloc-failures.patch
* Wed Aug 16 2017 carnold@suse.com
- bsc#1044974 - xen-tools require python-pam
  xen.spec
* Fri Aug 11 2017 carnold@suse.com
- Clean up spec file errors and a few warnings. (bsc#1027519)
- Removed conditional 'with_systemd' and some old deprecated
  'sles_version' checks.
  xen.spec
* Thu Aug 10 2017 jfehlig@suse.com
- Remove use of brctl utiltiy from supportconfig plugin
  FATE#323639
* Thu Aug 10 2017 ohering@suse.de
- Use upstream variant of mini-os __udivmoddi4 change
  gcc7-mini-os.patch
* Wed Aug  9 2017 carnold@suse.com
- fate#323639 Move bridge-utils to legacy
  replace-obsolete-network-configuration-commands-in-s.patch
* Tue Aug  8 2017 carnold@suse.com
- bsc#1052686 - VUL-0: xen: grant_table: possibly premature
  clearing of GTF_writing / GTF_reading (XSA-230)
  xsa230.patch
* Mon Aug  7 2017 ohering@suse.de
- bsc#1035231 - migration of HVM domU does not use superpages
  on destination dom0
  libxc.sr.superpage.patch
* Thu Aug  3 2017 carnold@suse.com
- bsc#1051787 - VUL-0: CVE-2017-12135: xen: possibly unbounded
  recursion in grant table code (XSA-226)
  xsa226-1.patch
  xsa226-2.patch
- bsc#1051788 - VUL-0: CVE-2017-12137: xen: x86: PV privilege
  escalation via map_grant_ref (XSA-227)
  xsa227.patch
- bsc#1051789 - VUL-0: CVE-2017-12136: xen: grant_table: Race
  conditions with maptrack free list handling (XSA-228)
  xsa228.patch
* Tue Aug  1 2017 jfehlig@suse.com
- Add a supportconfig plugin
  xen-supportconfig
  FATE#323661
* Tue Jul 25 2017 ohering@suse.de
- bsc#1026236 - add suse_vtsc_tolerance= cmdline option for Xen
  To avoid emulation of TSC access from a domU after live migration
  add a global tolerance for the measured host kHz
  xen.suse_vtsc_tolerance.patch
* Thu Jul 20 2017 carnold@suse.com
- fate#323662 Drop qemu-dm from xen-tools package
  The following tarball and patches have been removed
  qemu-xen-traditional-dir-remote.tar.bz2
  VNC-Support-for-ExtendedKeyEvent-client-message.patch
  0001-net-move-the-tap-buffer-into-TAPState.patch
  0002-net-increase-tap-buffer-size.patch
  0003-e1000-fix-access-4-bytes-beyond-buffer-end.patch
  0004-e1000-secrc-support.patch
  0005-e1000-multi-buffer-packet-support.patch
  0006-e1000-clear-EOP-for-multi-buffer-descriptors.patch
  0007-e1000-verify-we-have-buffers-upfront.patch
  0008-e1000-check-buffer-availability.patch
  CVE-2013-4533-qemut-pxa2xx-buffer-overrun-on-incoming-migration.patch
  CVE-2013-4534-qemut-openpic-buffer-overrun-on-incoming-migration.patch
  CVE-2013-4537-qemut-ssi-sd-fix-buffer-overrun-on-invalid-state-load.patch
  CVE-2013-4538-qemut-ssd0323-fix-buffer-overun-on-invalid-state.patch
  CVE-2013-4539-qemut-tsc210x-fix-buffer-overrun-on-invalid-state-load.patch
  CVE-2014-0222-qemut-qcow1-validate-l2-table-size.patch
  CVE-2014-3640-qemut-slirp-NULL-pointer-deref-in-sosendto.patch
  CVE-2015-4037-qemut-smb-config-dir-name.patch
  CVE-2015-5154-qemut-fix-START-STOP-UNIT-command-completion.patch
  CVE-2015-5278-qemut-Infinite-loop-in-ne2000_receive-function.patch
  CVE-2015-6815-qemut-e1000-fix-infinite-loop.patch
  CVE-2015-7512-qemut-net-pcnet-buffer-overflow-in-non-loopback-mode.patch
  CVE-2015-8345-qemut-eepro100-infinite-loop-fix.patch
  CVE-2015-8504-qemut-vnc-avoid-floating-point-exception.patch
  CVE-2016-1714-qemut-fw_cfg-add-check-to-validate-current-entry-value.patch
  CVE-2016-1981-qemut-e1000-eliminate-infinite-loops-on-out-of-bounds-transfer.patch
  CVE-2016-2391-qemut-usb-null-pointer-dereference-in-ohci-module.patch
  CVE-2016-2841-qemut-ne2000-infinite-loop-in-ne2000_receive.patch
  CVE-2016-4439-qemut-scsi-esp-OOB-write-while-writing-to-cmdbuf-in-esp_reg_write.patch
  CVE-2016-4441-qemut-scsi-esp-OOB-write-while-writing-to-cmdbuf-in-get_cmd.patch
  CVE-2016-5238-qemut-scsi-esp-OOB-write-when-using-non-DMA-mode-in-get_cmd.patch
  CVE-2016-5338-qemut-scsi-esp-OOB-rw-access-while-processing-ESP_FIFO.patch
  CVE-2016-6351-qemut-scsi-esp-make-cmdbuf-big-enough-for-maximum-CDB-size.patch
  CVE-2016-7908-qemut-net-Infinite-loop-in-mcf_fec_do_tx.patch
  CVE-2016-7909-qemut-net-pcnet-infinite-loop-in-pcnet_rdra_addr.patch
  CVE-2016-8667-qemut-dma-rc4030-divide-by-zero-error-in-set_next_tick.patch
  CVE-2016-8669-qemut-char-divide-by-zero-error-in-serial_update_parameters.patch
  CVE-2016-8910-qemut-net-rtl8139-infinite-loop-while-transmit-in-Cplus-mode.patch
  CVE-2016-9921-qemut-display-cirrus_vga-divide-by-zero-in-cirrus_do_copy.patch
  CVE-2017-6505-qemut-usb-an-infinite-loop-issue-in-ohci_service_ed_list.patch
  CVE-2017-8309-qemut-audio-host-memory-leakage-via-capture-buffer.patch
  CVE-2017-9330-qemut-usb-ohci-infinite-loop-due-to-incorrect-return-value.patch
  blktap.patch
  cdrom-removable.patch
  xen-qemu-iscsi-fix.patch
  qemu-security-etch1.patch
  xen-disable-qemu-monitor.patch
  xen-hvm-default-bridge.patch
  qemu-ifup-set-mtu.patch
  ioemu-vnc-resize.patch
  capslock_enable.patch
  altgr_2.patch
  log-guest-console.patch
  bdrv_open2_fix_flags.patch
  bdrv_open2_flags_2.patch
  ioemu-7615-qcow2-fix-alloc_cluster_link_l2.patch
  qemu-dm-segfault.patch
  bdrv_default_rwflag.patch
  kernel-boot-hvm.patch
  ioemu-watchdog-support.patch
  ioemu-watchdog-linkage.patch
  ioemu-watchdog-ib700-timer.patch
  ioemu-hvm-pv-support.patch
  pvdrv_emulation_control.patch
  ioemu-disable-scsi.patch
  ioemu-disable-emulated-ide-if-pv.patch
  xenpaging.qemu.flush-cache.patch
  ioemu-devicemodel-include.patch
- Cleanup spec file and remove unused KMP patches
  kmp_filelist
  supported_module.patch
  xen_pvonhvm.xen_emul_unplug.patch
* Mon Jul 17 2017 carnold@suse.com
- bsc#1002573 - Optimize LVM functions in block-dmmd
  block-dmmd
* Fri Jul 14 2017 ohering@suse.de
- Record initial Xen dmesg in /var/log/xen/xen-boot.log for
  supportconfig. Keep previous log in /var/log/xen/xen-boot.prev.log
* Fri Jul 14 2017 ohering@suse.de
- Remove storytelling from description in xen.rpm
* Wed Jun 28 2017 carnold@suse.com
- Update to Xen 4.9.0 FCS (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
* Wed Jun 21 2017 carnold@suse.com
- Update block-dmmd script (bsc#1002573)
  block-dmmd
* Tue Jun 20 2017 carnold@suse.com
- Update to Xen 4.9.0-rc8+ (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
  gcc7-arm.patch
- Drop gcc7-error-xenpmd.patch
* Mon Jun  5 2017 carnold@suse.com
- Update to Xen 4.9.0-rc8 (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
* Thu Jun  1 2017 carnold@suse.com
- bsc#1042160 - VUL-1: CVE-2017-9330: xen: usb: ohci: infinite loop
  due to incorrect return value
  CVE-2017-9330-qemut-usb-ohci-infinite-loop-due-to-incorrect-return-value.patch
* Tue May 30 2017 carnold@suse.com
- bsc#1037243 - VUL-1: CVE-2017-8309: xen: audio: host memory
  leakage via capture buffer
  CVE-2017-8309-qemut-audio-host-memory-leakage-via-capture-buffer.patch
* Fri May 26 2017 carnold@suse.com
- Update to Xen 4.9.0-rc7 (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
* Mon May 22 2017 carnold@suse.com
- Update to Xen 4.9.0-rc6 (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
* Thu May 18 2017 carnold@suse.com
- bsc#1031343 - xen fails to build with GCC 7
  gcc7-mini-os.patch
  gcc7-xen.patch
* Wed May 17 2017 carnold@suse.com
- bsc#1031343 - xen fails to build with GCC 7
  gcc7-error-xenpmd.patch
* Tue May 16 2017 carnold@suse.com
- Update to Xen 4.9.0-rc5 (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
- Drop xen-tools-pkgconfig-xenlight.patch
* Wed May 10 2017 carnold@suse.com
- bsc#1037779 - xen breaks kexec-tools build
  xen-tools-pkgconfig-xenlight.patch
* Tue May  9 2017 carnold@suse.com
- Update to Xen 4.9.0-rc4 (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
* Tue May  2 2017 carnold@suse.com
- bsc#1036146 - sles12sp2 xen VM dumps core to wrong path
  xen.spec
* Fri Apr 28 2017 carnold@suse.com
- Update to Xen 4.9.0-rc3 (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
  aarch64-maybe-uninitialized.patch
* Fri Apr 21 2017 carnold@suse.com
- Update to Xen 4.9.0-rc2 (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
* Wed Apr 19 2017 carnold@suse.com
- Update to Xen 4.9.0-rc1 (fate#321394, fate#323108)
  xen-4.9.0-testing-src.tar.bz2
  ioemu-devicemodel-include.patch
- Dropped patches contained in new tarball
  xen-4.8.0-testing-src.tar.bz2
  0001-xenstore-let-write_node-and-some-callers-return-errn.patch
  0002-xenstore-undo-function-rename.patch
  0003-xenstore-rework-of-transaction-handling.patch
  584806ce-x86emul-correct-PUSHF-POPF.patch
  584fc649-fix-determining-when-domain-creation-is-complete.patch
  58510c06-x86emul-CMPXCHGnB-ignore-prefixes.patch
  58510cac-x86emul-MOVNTI-no-REP-prefixes.patch
  58526ccc-x86emul-64bit-ignore-most-segment-bases-in-align-check.patch
  5853ed37-VT-d-correct-dma_msi_set_affinity.patch
  5853ee07-x86emul-CMPXCHG16B-aligned-operand.patch
  58580060-x86-emul-correct-SYSCALL-eflags-handling.patch
  585aa3c5-x86-force-EFLAGS-IF-on-upon-exit-to-PV.patch
  585aa407-x86-HVM-NULL-check-before-using-VMFUNC-hook.patch
  585bd5fe-x86-emul-correct-VMFUNC-return-value-handling.patch
  586ba81c-x86-cpu-dont-update-this_cpu-for-guest-get_cpu_vendor.patch
  587d04d6-x86-xstate-fix-array-overrun-with-LWP.patch
  587de4a9-x86emul-VEX-B-ignored-in-compat-mode.patch
  5882129d-x86emul-LOCK-check-adjustments.patch
  58821300-x86-segment-attribute-handling.patch
  58873c1f-x86emul-correct-FPU-stub-asm-constraints.patch
  58873c80-x86-hvm-do-not-set-msr_tsc_adjust-on-.patch
  5887888f-credit2-fix-shutdown-suspend-with-cpupools.patch
  5887888f-credit2-never-consider-CPUs-outside-of-pool.patch
  5887888f-credit2-use-the-correct-scratch-cpumask.patch
  5888b1b3-x86-emulate-dont-assume-addr_size-32-implies-protmode.patch
  5899cbd9-EPT-allow-wrcomb-MMIO-mappings-again.patch
  589b3272-libxl-dont-segfault-when-creating-domain-with-invalid-pvusb-device.patch
  58a44771-IOMMU-always-call-teardown-callback.patch
  58a48ccc-x86-fix-p2m_flush_table-for-non-nested.patch
  58a59f4b-libxl-correct-xenstore-entry-for-empty-cdrom.patch
  58a70d94-VMX-fix-VMCS-race-on-cswitch-paths.patch
  58ac1f3f-VMX-dont-leak-host-syscall-MSRs.patch
  58b5a2de-x86-correct-Xens-idea-of-its-memory-layout.patch
  58b6fd42-credit2-always-mark-a-tickled-pCPU-as-tickled.patch
  58b6fd42-credit2-dont-miss-accounting-during-credit-reset.patch
  58cbf682-x86-EFI-avoid-overrunning-mb_modules.patch
  58cf9200-x86-EFI-avoid-IOMMU-faults-on-tail-gap.patch
  58cf9260-x86-EFI-avoid-Xen-when-looking-for-mod-kexec-pos.patch
  58cf9277-x86-time-dont-use-vTSC-if-host-guest-freqs-match.patch
  58d25ea2-xenstore-add-missing-checks-for-allocation-failure.patch
  58d91365-sched-dont-call-wrong-hook-via-VCPU2OP.patch
  CVE-2017-2615-qemut-display-cirrus-oob-access-while-doing-bitblt-copy-backward-mode.patch
  CVE-2017-2620-xsa209-qemut-cirrus_bitblt_cputovideo-does-not-check-if-memory-region-safe.patch
  glibc-2.25-compatibility-fix.patch
  xs-09-add_change_node-params.patch
  xs-10-call-add_change_node.patch
  xs-11-tdb-record-header.patch
  xs-12-node-gen-count.patch
  xs-13-read-directory-part-support.patch
  xs-14-command-array.patch
  xs-15-command-return-val.patch
  xs-16-function-static.patch
  xs-17-arg-parsing.patch
  xs-18-default-buffer.patch
  xs-19-handle-alloc-failures.patch
  xs-20-tdb-version.patch
  xs-21-empty-tdb-database.patch
  xs-22-reopen_log-fix.patch
  xs-23-XS_DEBUG-rename.patch
  xs-24-xenstored_control.patch
  xs-25-control-enhance.patch
  xs-26-log-control.patch
  xs-27-memory-report.patch
  xs-28-remove-talloc-report.patch
  xs-29-define-off_t.patch
  xsa206-0001-xenstored-apply-a-write-transaction-rate-limit.patch
  xsa206-0002-xenstored-Log-when-the-write-transaction-rate-limit.patch
* Wed Apr  5 2017 carnold@suse.com
- bsc#1022703 - Xen HVM guest with OVMF hangs with unattached CDRom
  58a59f4b-libxl-correct-xenstore-entry-for-empty-cdrom.patch
* Wed Mar 29 2017 jfehlig@suse.com
- bsc#1015348 - L3: libvirtd does not start during boot
  suse-xendomains-service.patch
* Wed Mar 22 2017 carnold@suse.com
- bsc#1014136 - Partner-L3: kdump can't dump a kernel on SLES12-SP2
  with Xen hypervisor.
  58cf9260-x86-EFI-avoid-Xen-when-looking-for-mod-kexec-pos.patch
- bsc#1026236 - L3: Paravirtualized vs. fully virtualized migration
  - latter one much faster
  58cf9277-x86-time-dont-use-vTSC-if-host-guest-freqs-match.patch
- Upstream patch from Jan
  58cbf682-x86-EFI-avoid-overrunning-mb_modules.patch
  58cf9200-x86-EFI-avoid-IOMMU-faults-on-tail-gap.patch
  58d91365-sched-dont-call-wrong-hook-via-VCPU2OP.patch
* Mon Mar 20 2017 carnold@suse.com
- bsc#1022555 - L3: Timeout in "execution of /etc/xen/scripts/block
  add"
  58d25ea2-xenstore-add-missing-checks-for-allocation-failure.patch
  0001-xenstore-let-write_node-and-some-callers-return-errn.patch
  0002-xenstore-undo-function-rename.patch
  0003-xenstore-rework-of-transaction-handling.patch
- bsc#1030144 - VUL-0: xen: xenstore denial of service via repeated
  update (XSA-206)
  xsa206-0001-xenstored-apply-a-write-transaction-rate-limit.patch
  xsa206-0002-xenstored-Log-when-the-write-transaction-rate-limit.patch
- bsc#1029827 - Forward port xenstored
  xs-09-add_change_node-params.patch
  xs-10-call-add_change_node.patch
  xs-11-tdb-record-header.patch
  xs-12-node-gen-count.patch
  xs-13-read-directory-part-support.patch
  xs-14-command-array.patch
  xs-15-command-return-val.patch
  xs-16-function-static.patch
  xs-17-arg-parsing.patch
  xs-18-default-buffer.patch
  xs-19-handle-alloc-failures.patch
  xs-20-tdb-version.patch
  xs-21-empty-tdb-database.patch
  xs-22-reopen_log-fix.patch
  xs-23-XS_DEBUG-rename.patch
  xs-24-xenstored_control.patch
  xs-25-control-enhance.patch
  xs-26-log-control.patch
  xs-27-memory-report.patch
  xs-28-remove-talloc-report.patch
  xs-29-define-off_t.patch
* Tue Mar 14 2017 ohering@suse.de
- bsc#1029128 - fix make xen to really produce xen.efi with gcc48
* Wed Mar  8 2017 carnold@suse.com
- bsc#1028235 - VUL-0: CVE-2017-6505: xen: qemu: usb: an infinite
  loop issue in ohci_service_ed_list
  CVE-2017-6505-qemut-usb-an-infinite-loop-issue-in-ohci_service_ed_list.patch
- Upstream patches from Jan (bsc#1027519)
  5887888f-credit2-fix-shutdown-suspend-with-cpupools.patch
  5887888f-credit2-use-the-correct-scratch-cpumask.patch
  5899cbd9-EPT-allow-wrcomb-MMIO-mappings-again.patch
  589b3272-libxl-dont-segfault-when-creating-domain-with-invalid-pvusb-device.patch
  58a44771-IOMMU-always-call-teardown-callback.patch
  58a48ccc-x86-fix-p2m_flush_table-for-non-nested.patch
  58a70d94-VMX-fix-VMCS-race-on-cswitch-paths.patch
  58ac1f3f-VMX-dont-leak-host-syscall-MSRs.patch
  58b5a2de-x86-correct-Xens-idea-of-its-memory-layout.patch
  58b6fd42-credit2-always-mark-a-tickled-pCPU-as-tickled.patch
  58b6fd42-credit2-dont-miss-accounting-during-credit-reset.patch
* Thu Mar  2 2017 carnold@suse.com
- bsc#1027654 - XEN fails to build against glibc 2.25
  glibc-2.25-compatibility-fix.patch
  libxl.pvscsi.patch
* Thu Feb 16 2017 ohering@suse.de
- fate#316613: Refresh and enable libxl.pvscsi.patch
* Fri Feb 10 2017 carnold@suse.com
- bsc#1024834 - VUL-0: CVE-2017-2620: xen: cirrus_bitblt_cputovideo
  does not check if memory region is safe (XSA-209)
  CVE-2017-2620-xsa209-qemut-cirrus_bitblt_cputovideo-does-not-check-if-memory-region-safe.patch
* Wed Feb  8 2017 carnold@suse.com
- bsc#1023948 - [pvusb][sles12sp3][openqa] Segmentation fault
  happened when adding usbctrl devices via xl
  589b3272-libxl-dont-segfault-when-creating-domain-with-invalid-pvusb-device.patch
* Thu Feb  2 2017 carnold@suse.com
- Upstream patches from Jan (bsc#1027519)
  587d04d6-x86-xstate-fix-array-overrun-with-LWP.patch
  587de4a9-x86emul-VEX-B-ignored-in-compat-mode.patch
  5882129d-x86emul-LOCK-check-adjustments.patch
  58821300-x86-segment-attribute-handling.patch
  58873c1f-x86emul-correct-FPU-stub-asm-constraints.patch
  58873c80-x86-hvm-do-not-set-msr_tsc_adjust-on-.patch
  5887888f-credit2-use-the-correct-scratch-cpumask.patch
  5887888f-credit2-never-consider-CPUs-outside-of-pool.patch
  5887888f-credit2-fix-shutdown-suspend-with-cpupools.patch
  5888b1b3-x86-emulate-dont-assume-addr_size-32-implies-protmode.patch
* Wed Feb  1 2017 carnold@suse.com
- bsc#1023004 - VUL-0: CVE-2017-2615: qemu: display: cirrus: oob
  access while doing bitblt copy backward mode
  CVE-2017-2615-qemut-display-cirrus-oob-access-while-doing-bitblt-copy-backward-mode.patch
* Thu Jan 26 2017 carnold@suse.com
- fate#322313 and fate#322150 require the acpica package ported to
  aarch64 which Xen 4.8 needs to build. Temporarily disable aarch64
  until these fates are complete.
  xen.spec
* Wed Jan 25 2017 carnold@suse.com
- bsc#1021952 - Virutalization/xen: Bug xen-tools missing
  /usr/bin/domu-xenstore; guests fail to launch
  tmp_build.patch
  xen.spec
* Wed Jan 18 2017 ohering@suse.de
- No systemd presets for 42.3+ and SLE12SP3+ (bsc#1012842)
* Thu Jan 12 2017 carnold@suse.com
- bsc#1007224 - broken symlinks in /usr/share/doc/packages/xen/misc/
  xen.spec
* Mon Jan  9 2017 carnold@suse.com
- 585aa3c5-x86-force-EFLAGS-IF-on-upon-exit-to-PV.patch
  Replaces xsa202.patch (bsc#1014298)
- 585aa407-x86-HVM-NULL-check-before-using-VMFUNC-hook.patch
  Replaces xsa203.patch (bsc#1014300)
- 58580060-x86-emul-correct-SYSCALL-eflags-handling.patch
  Replaces xsa204.patch (bsc#1016340)
- Upstream patches from Jan
  58526ccc-x86emul-64bit-ignore-most-segment-bases-in-align-check.patch
  5853ed37-VT-d-correct-dma_msi_set_affinity.patch
  5853ee07-x86emul-CMPXCHG16B-aligned-operand.patch
  585bd5fe-x86-emul-correct-VMFUNC-return-value-handling.patch
  586ba81c-x86-cpu-dont-update-this_cpu-for-guest-get_cpu_vendor.patch
* Wed Jan  4 2017 carnold@suse.com
- bsc#1015169 - VUL-0: CVE-2016-9921, CVE-2016-9922: xen: qemu:
  display: cirrus_vga: a divide by zero in cirrus_do_copy
  CVE-2016-9921-qemut-display-cirrus_vga-divide-by-zero-in-cirrus_do_copy.patch
* Mon Dec 19 2016 carnold@suse.com
- bsc#1016340 - VUL-0: CVE-2016-10013: xen: x86: Mishandling of
  SYSCALL singlestep during emulation (XSA-204)
  xsa204.patch
* Thu Dec 15 2016 carnold@suse.com
- bsc#1012651 - VUL-0: CVE-2016-9932: xen: x86 CMPXCHG8B emulation
  fails to ignore operand size override (XSA-200)
  58510c06-x86emul-CMPXCHGnB-ignore-prefixes.patch
* Wed Dec 14 2016 carnold@suse.com
- bsc#1014298 - VUL-0: CVE-2016-10024: xen: x86 PV guests may be
  able to mask interrupts (XSA-202)
  xsa202.patch
- bsc#1014300 - VUL-0: CVE-2016-10025: xen: x86: missing NULL
  pointer check in VMFUNC emulation (XSA-203)
  xsa203.patch
- Upstream patches from Jan
  584806ce-x86emul-correct-PUSHF-POPF.patch
  584fc649-fix-determining-when-domain-creation-is-complete.patch
  58510c06-x86emul-CMPXCHGnB-ignore-prefixes.patch
  58510cac-x86emul-MOVNTI-no-REP-prefixes.patch
* Mon Dec  5 2016 carnold@suse.com
- Update to Xen 4.8 FCS
  xen-4.8.0-testing-src.tar.bz2
- Dropped
  xen-4.7.1-testing-src.tar.bz2
  0001-libxc-Rework-extra-module-initialisation.patch
  0002-libxc-Prepare-a-start-info-structure-for-hvmloader.patch
  0003-configure-define-SEABIOS_PATH-and-OVMF_PATH.patch
  0004-firmware-makefile-install-BIOS-blob.patch
  0005-libxl-Load-guest-BIOS-from-file.patch
  0006-xen-Move-the-hvm_start_info-C-representation-from-li.patch
  0007-hvmloader-Grab-the-hvm_start_info-pointer.patch
  0008-hvmloader-Locate-the-BIOS-blob.patch
  0009-hvmloader-Check-modules-whereabouts-in-perform_tests.patch
  0010-hvmloader-Load-SeaBIOS-from-hvm_start_info-modules.patch
  0011-hvmloader-Load-OVMF-from-modules.patch
  0012-hvmloader-Specific-bios_load-function-required.patch
  0013-hvmloader-Always-build-in-SeaBIOS-and-OVMF-loader.patch
  0014-configure-do-not-depend-on-SEABIOS_PATH-or-OVMF_PATH.patch
  57580bbd-kexec-allow-relaxed-placement-via-cmdline.patch
  576001df-x86-time-use-local-stamp-in-TSC-calibration-fast-path.patch
  5769106e-x86-generate-assembler-equates-for-synthesized.patch
  57a1e603-x86-time-adjust-local-system-time-initialization.patch
  57a1e64c-x86-time-introduce-and-use-rdtsc_ordered.patch
  57a2f6ac-x86-time-calibrate-TSC-against-platform-timer.patch
  57a30261-x86-support-newer-Intel-CPU-models.patch
  5810a9cc-x86-emul-Correct-decoding-of-SReg3-operands.patch
  581b2c3b-x86-emul-reject-LGDT-LIDT-with-non-canonical-addresses.patch
  581b647a-x86emul-L-S-G-I-DT-ignore-opsz-overrides-in-64-bit-mode.patch
  58249392-x86-svm-dont-clobber-eax-edx-if-RDMSR-intercept-fails.patch
  582c35d6-x86-vmx-correct-long-mode-check-in-vmx_cpuid_intercept.patch
  582c35ee-x86-traps-dont-call-hvm_hypervisor_cpuid_leaf-for-PV.patch
  58343dc2-x86-hvm-Fix-the-handling-of-non-present-segments.patch
  58343df8-x86-HVM-dont-load-LDTR-with-VM86-mode-attrs-during-task-switch.patch
  58343e24-x86-PV-writes-of-fs-and-gs-base-MSRs-require-canonical-addresses.patch
  58343e9e-libelf-fix-stack-memory-leak-when-loading-32-bit-symbol-tables.patch
  58343ec2-x86emul-fix-huge-bit-offset-handling.patch
  58343f29-x86-emul-correct-the-IDT-entry-calculation-in-inject_swint.patch
  58343f44-x86-svm-fix-injection-of-software-interrupts.patch
  58343f79-pygrub-Properly-quote-results-when-returning-them-to-the-caller.patch
  CVE-2016-9381-xsa197-qemut.patch
  CVE-2016-9637-xsa199-qemut.patch
* Tue Nov 22 2016 carnold@suse.com
- bsc#1011652 - VUL-0: xen: qemu ioport array overflow
  CVE-2016-9637-xsa199-qemut.patch
* Fri Nov 18 2016 carnold@suse.com
- bsc#1009100 - VUL-0: CVE-2016-9386: XSA-191: xen: x86 null
  segments not always treated as unusable
  58343dc2-x86-hvm-Fix-the-handling-of-non-present-segments.patch
- bsc#1009103 - VUL-0: CVE-2016-9382: XSA-192: xen: x86 task switch
  to VM86 mode mis-handled
  58343df8-x86-HVM-dont-load-LDTR-with-VM86-mode-attrs-during-task-switch.patch
- bsc#1009104 - VUL-0: CVE-2016-9385: XSA-193: xen: x86 segment base
  write emulation lacking canonical address checks
  58343e24-x86-PV-writes-of-fs-and-gs-base-MSRs-require-canonical-addresses.patch
- bsc#1009105 - VUL-0: CVE-2016-9384: XSA-194: xen: guest 32-bit
  ELF symbol table load leaking host data
  58343e9e-libelf-fix-stack-memory-leak-when-loading-32-bit-symbol-tables.patch
- bsc#1009107 - VUL-0: CVE-2016-9383: XSA-195: xen: x86 64-bit bit
  test instruction emulation broken
  58343ec2-x86emul-fix-huge-bit-offset-handling.patch
- bsc#1009108 - VUL-0: CVE-2016-9377,CVE-2016-9378: XSA-196: xen:
  x86 software interrupt injection mis-handled
  58343f29-x86-emul-correct-the-IDT-entry-calculation-in-inject_swint.patch
  58343f44-x86-svm-fix-injection-of-software-interrupts.patch
- bsc#1009109 - VUL-0: CVE-2016-9381: XSA-197: xen: qemu incautious
  about shared ring processing
  CVE-2016-9381-xsa197-qemut.patch
- bsc#1009111 - VUL-0: CVE-2016-9379,CVE-2016-9380: XSA-198: xen:
  delimiter injection vulnerabilities in pygrub
  58343f79-pygrub-Properly-quote-results-when-returning-them-to-the-caller.patch
- Upstream patches from Jan
  581b2c3b-x86-emul-reject-LGDT-LIDT-with-non-canonical-addresses.patch
  581b647a-x86emul-L-S-G-I-DT-ignore-opsz-overrides-in-64-bit-mode.patch
  58249392-x86-svm-dont-clobber-eax-edx-if-RDMSR-intercept-fails.patch
  582c35d6-x86-vmx-correct-long-mode-check-in-vmx_cpuid_intercept.patch
  582c35ee-x86-traps-dont-call-hvm_hypervisor_cpuid_leaf-for-PV.patch
* Tue Nov 15 2016 carnold@suse.com
- Update to Xen Version 4.7.1
  xen-4.7.1-testing-src.tar.bz2
- Dropped patches contained in new tarball
  xen-4.7.0-testing-src.tar.bz2
  575e9ca0-nested-vmx-Validate-host-VMX-MSRs-before-accessing-them.patch
  57640448-xen-sched-use-default-scheduler-upon-an-invalid-sched.patch
  57973099-have-schedulers-revise-initial-placement.patch
  579730e6-remove-buggy-initial-placement-algorithm.patch
  57976073-x86-remove-unsafe-bits-from-mod_lN_entry-fastpath.patch
  57976078-x86-avoid-SMAP-violation-in-compat_create_bounce_frame.patch
  57ac6316-don-t-restrict-DMA-heap-to-node-0.patch
  57b71fc5-x86-EFI-don-t-apply-relocations-to-l-2-3-_bootmap.patch
  57b7447b-dont-permit-guest-to-populate-PoD-pages-for-itself.patch
  57c4412b-x86-HVM-add-guarding-logic-for-VMX-specific-code.patch
  57c57f73-libxc-correct-max_pfn-calculation-for-saving-domain.patch
  57c805bf-x86-levelling-restrict-non-architectural-OSXSAVE-handling.patch
  57c805c1-x86-levelling-pass-vcpu-to-ctxt_switch_levelling.patch
  57c805c3-x86-levelling-provide-architectural-OSXSAVE-handling.patch
  57c82be2-x86-32on64-adjust-call-gate-emulation.patch
  57c93e52-fix-error-in-libxl_device_usbdev_list.patch
  57c96df3-credit1-fix-a-race-when-picking-initial-pCPU.patch
  57c96e2c-x86-correct-PT_NOTE-file-position.patch
  57cfed43-VMX-correct-feature-checks-for-MPX-and-XSAVES.patch
  57d1563d-x86-32on64-don-t-allow-recursive-page-tables-from-L3.patch
  57d15679-x86-emulate-Correct-boundary-interactions-of-emulated-insns.patch
  57d1569a-x86-shadow-Avoid-overflowing-sh_ctxt-seg_reg.patch
  57d18642-hvm-fep-Allow-test-insns-crossing-1-0-boundary.patch
  57d18642-x86-segment-Bounds-check-accesses-to-emulation-ctxt-seg_reg.patch
  57d7ca5f-x86-domctl-fix-TOCTOU-race-in-XEN_DOMCTL_getvcpuextstate.patch
  57d7ca64-x86-domctl-fix-migration-of-guests-not-using-xsave.patch
  57da8883-credit1-fix-mask-to-be-used-for-tickling.patch
  57da8883-credit2-properly-schedule-migration-of-running-vcpu.patch
  57dfb1c5-x86-Intel-hide-CPUID-faulting-capability-from-guests.patch
  57e93e1d-x86emul-correct-loading-of-ss.patch
  57e93e4a-x86emul-don-t-allow-null-selector-for-LTR.patch
  57e93e89-x86-AMD-apply-erratum-665-workaround.patch
  57ee6cbc-credit1-return-time-remaining-to-limit-as-next-timeslice.patch
  57f3a8ee-x86emul-honor-guest-CR0-TS-and-CR0-EM.patch
  57fb6a91-x86-defer-not-present-segment-checks.patch
  5800c51d-x86-hvm-Clobber-cs-L-when-LME-becomes-set.patch
  5800caec-x86emul-fix-pushing-of-selector-registers.patch
  5800cb06-x86-Viridian-don-t-depend-on-undefined-register-state.patch
  580e29f9-x86-MISALIGNSSE-feature-depends-on-SSE.patch
  57dfb2ff-x86-Intel-Broadwell-no-PKG_C8-10_RESIDENCY-MSRs.patch
* Mon Nov  7 2016 carnold@suse.com
- bsc#1004981 - Xen RPM doesn't contain debug hypervisor for EFI
  systems
  xen.spec
* Thu Nov  3 2016 carnold@suse.com
- bsc#1000106 - VUL-0: CVE-2016-7777: xen: CR0.TS and CR0.EM not
  always honored for x86 HVM guests (XSA-190)
  57f3a8ee-x86emul-honor-guest-CR0-TS-and-CR0-EM.patch
- bsc#996191 - [XEN][acpi]residency -n 88 -c will cause xen panic
  on broadwell-ep
  57dfb2ff-x86-Intel-Broadwell-no-PKG_C8-10_RESIDENCY-MSRs.patch
- Upstream patches from Jan
  57d7ca5f-x86-domctl-fix-TOCTOU-race-in-XEN_DOMCTL_getvcpuextstate.patch
  57d7ca64-x86-domctl-fix-migration-of-guests-not-using-xsave.patch
  57da8883-credit1-fix-mask-to-be-used-for-tickling.patch
  57da8883-credit2-properly-schedule-migration-of-running-vcpu.patch
  57dfb1c5-x86-Intel-hide-CPUID-faulting-capability-from-guests.patch
  57e93e1d-x86emul-correct-loading-of-ss.patch
  57e93e4a-x86emul-don-t-allow-null-selector-for-LTR.patch
  57e93e89-x86-AMD-apply-erratum-665-workaround.patch
  57ee6cbc-credit1-return-time-remaining-to-limit-as-next-timeslice.patch
  57fb6a91-x86-defer-not-present-segment-checks.patch
  5800c51d-x86-hvm-Clobber-cs-L-when-LME-becomes-set.patch
  5800caec-x86emul-fix-pushing-of-selector-registers.patch
  5800cb06-x86-Viridian-don-t-depend-on-undefined-register-state.patch
  580e29f9-x86-MISALIGNSSE-feature-depends-on-SSE.patch
  5810a9cc-x86-emul-Correct-decoding-of-SReg3-operands.patch
* Wed Nov  2 2016 carnold@suse.com
- bsc#1007941 - Xen tools limit the number of vcpus to 256 when the
  system has 384
  xen-arch-kconfig-nr_cpus.patch
* Tue Nov  1 2016 carnold@suse.com
- bsc#1007157 - VUL-0: CVE-2016-8910: xen: net: rtl8139: infinite
  loop while transmit in C+ mode
  CVE-2016-8910-qemut-net-rtl8139-infinite-loop-while-transmit-in-Cplus-mode.patch
* Mon Oct 17 2016 carnold@suse.com
- bsc#1005004 - CVE-2016-8667: xen: dma: rc4030 divide by zero
  error in set_next_tick
  CVE-2016-8667-qemut-dma-rc4030-divide-by-zero-error-in-set_next_tick.patch
- bsc#1005005 - VUL-0: CVE-2016-8669: xen: char: divide by zero
  error in serial_update_parameters
  CVE-2016-8669-qemut-char-divide-by-zero-error-in-serial_update_parameters.patch
* Wed Oct  5 2016 carnold@suse.com
- bsc#1003030 - VUL-0: CVE-2016-7908: xen: net: Infinite loop in
  mcf_fec_do_tx
  CVE-2016-7908-qemut-net-Infinite-loop-in-mcf_fec_do_tx.patch
- bsc#1003032 - VUL-0: CVE-2016-7909: xen: net: pcnet: infinite
  loop in pcnet_rdra_addr
  CVE-2016-7909-qemut-net-pcnet-infinite-loop-in-pcnet_rdra_addr.patch
* Mon Sep 12 2016 carnold@suse.com
- bsc#995785 - VUL-0: CVE-2016-7092: xen: x86: Disallow L3
  recursive pagetable for 32-bit PV guests (XSA-185)
  57d1563d-x86-32on64-don-t-allow-recursive-page-tables-from-L3.patch
- bsc#995789 - VUL-0: CVE-2016-7093: xen: x86: Mishandling of
  instruction pointer truncation during emulation (XSA-186)
  57d15679-x86-emulate-Correct-boundary-interactions-of-emulated-insns.patch
  57d18642-hvm-fep-Allow-test-insns-crossing-1-0-boundary.patch
- bsc#995792 - VUL-0: CVE-2016-7094: xen: x86 HVM: Overflow of
  sh_ctxt->seg_reg[] (XSA-187)
  57d1569a-x86-shadow-Avoid-overflowing-sh_ctxt-seg_reg.patch
  57d18642-x86-segment-Bounds-check-accesses-to-emulation-ctxt-seg_reg.patch
- bsc#991934 - xen hypervisor crash in csched_acct
  57c96df3-credit1-fix-a-race-when-picking-initial-pCPU.patch
- Upstream patches from Jan
  57c4412b-x86-HVM-add-guarding-logic-for-VMX-specific-code.patch
  57c57f73-libxc-correct-max_pfn-calculation-for-saving-domain.patch
  57c805bf-x86-levelling-restrict-non-architectural-OSXSAVE-handling.patch
  57c805c1-x86-levelling-pass-vcpu-to-ctxt_switch_levelling.patch
  57c805c3-x86-levelling-provide-architectural-OSXSAVE-handling.patch
  57c82be2-x86-32on64-adjust-call-gate-emulation.patch
  57c96e2c-x86-correct-PT_NOTE-file-position.patch
  57cfed43-VMX-correct-feature-checks-for-MPX-and-XSAVES.patch
* Mon Sep 12 2016 ohering@suse.de
- bsc#979002 - add 60-persistent-xvd.rules and helper script
  also to initrd, add the relevant dracut helper
* Mon Sep  5 2016 ohering@suse.de
- bnc#953518 - unplug also SCSI disks in qemu-xen-traditional for
  upstream unplug protocol
* Fri Sep  2 2016 carnold@suse.com
- bsc#989679 - [pvusb feature] USB device not found when
  'virsh detach-device guest usb.xml'
  57c93e52-fix-error-in-libxl_device_usbdev_list.patch
* Tue Aug 23 2016 carnold@suse.com
- bsc#992224 - [HPS Bug] During boot of Xen Hypervisor, Failed to
  get contiguous memory for DMA from Xen
  57ac6316-don-t-restrict-DMA-heap-to-node-0.patch
- bsc#978755 - xen uefi systems fail to boot
- bsc#983697 - SLES12 SP2 Xen UEFI mode cannot boot
  57b71fc5-x86-EFI-don-t-apply-relocations-to-l-2-3-_bootmap.patch
- Upstream patch from Jan
  57b7447b-dont-permit-guest-to-populate-PoD-pages-for-itself.patch
* Mon Aug  8 2016 jfehlig@suse.com
- spec: to stay compatible with the in-tree qemu-xen binary, use
  /usr/bin/qemu-system-i386 instead of /usr/bin/qemu-system-x86_64
  bsc#986164
* Thu Aug  4 2016 carnold@suse.com
- bsc#970135 - new virtualization project clock test randomly fails
  on Xen
  576001df-x86-time-use-local-stamp-in-TSC-calibration-fast-path.patch
  5769106e-x86-generate-assembler-equates-for-synthesized.patch
  57a1e603-x86-time-adjust-local-system-time-initialization.patch
  57a1e64c-x86-time-introduce-and-use-rdtsc_ordered.patch
  57a2f6ac-x86-time-calibrate-TSC-against-platform-timer.patch
- bsc#991934 - xen hypervisor crash in csched_acct
  57973099-have-schedulers-revise-initial-placement.patch
  579730e6-remove-buggy-initial-placement-algorithm.patch
- bsc#988675 - VUL-0: CVE-2016-6258: xen: x86: Privilege escalation
  in PV guests (XSA-182)
  57976073-x86-remove-unsafe-bits-from-mod_lN_entry-fastpath.patch
- bsc#988676 - VUL-0: CVE-2016-6259: xen: x86: Missing SMAP
  whitelisting in 32-bit exception / event delivery (XSA-183)
  57976078-x86-avoid-SMAP-violation-in-compat_create_bounce_frame.patch
- Upstream patches from Jan
  57a30261-x86-support-newer-Intel-CPU-models.patch
* Mon Aug  1 2016 carnold@suse.com
- bsc#985503 - vif-route broken
  vif-route.patch
* Thu Jul 28 2016 carnold@suse.com
- bsc#978413 - PV guest upgrade from sles11sp4 to sles12sp2 alpha3
  failed on sles11sp4 xen host.
  pygrub-handle-one-line-menu-entries.patch
* Wed Jul 27 2016 carnold@suse.com
- bsc#990843 - VUL-1: CVE-2016-6351: xen: qemu: scsi: esp: OOB
  write access in esp_do_dma
  CVE-2016-6351-qemut-scsi-esp-make-cmdbuf-big-enough-for-maximum-CDB-size.patch
* Thu Jun 23 2016 carnold@suse.com
- bsc#900418 - Dump cannot be performed on SLES12 XEN
  57580bbd-kexec-allow-relaxed-placement-via-cmdline.patch
- Upstream patches from Jan
  575e9ca0-nested-vmx-Validate-host-VMX-MSRs-before-accessing-them.patch
  57640448-xen-sched-use-default-scheduler-upon-an-invalid-sched.patch
* Tue Jun 21 2016 carnold@suse.com
- fate#319989 - Update to Xen 4.7 FCS
  xen-4.7.0-testing-src.tar.bz2
- Drop CVE-2014-3672-qemut-xsa180.patch
* Thu Jun 16 2016 carnold@suse.com
- bsc#954872 - script block-dmmd not working as expected - libxl:
  error: libxl_dm.c (Additional fixes)
  block-dmmd
* Fri Jun 10 2016 ohering@suse.de
- Convert with_stubdom into build_conditional to allow adjusting
  via prjconf
- Convert with_debug into build_conditional to allow adjusting
  via prjconf
* Fri Jun 10 2016 ohering@suse.de
- bsc#979002 - add 60-persistent-xvd.rules and helper script to
  xen-tools-domU to simplify transition to pvops based kernels
* Fri Jun 10 2016 ohering@suse.de
- Convert with_oxenstored into build_conditional to allow
  adjusting via prjconf (fate#320836)
* Thu Jun  9 2016 carnold@suse.com
- bsc#983984 - VUL-0: CVE-2016-5338: xen: qemu: scsi: esp: OOB r/w
  access while processing ESP_FIFO
  CVE-2016-5338-qemut-scsi-esp-OOB-rw-access-while-processing-ESP_FIFO.patch
- bsc#982960 - VUL-0: CVE-2016-5238: xen: qemu: scsi: esp: OOB
  write when using non-DMA mode in get_cmd
  CVE-2016-5238-qemut-scsi-esp-OOB-write-when-using-non-DMA-mode-in-get_cmd.patch
* Tue Jun  7 2016 carnold@suse.com
- fate#319989 - Update to Xen 4.7 RC5
  xen-4.7.0-testing-src.tar.bz2
* Wed May 25 2016 carnold@suse.com
- fate#319989 - Update to Xen 4.7 RC4
  xen-4.7.0-testing-src.tar.bz2
- Dropped
  xen.pkgconfig-4.7.patch
  xsa164.patch
* Mon May 23 2016 carnold@suse.com
- bsc#981264 - VUL-0: CVE-2014-3672: xen: Unrestricted qemu logging
  (XSA-180)
  CVE-2014-3672-qemut-xsa180.patch
* Thu May 19 2016 carnold@suse.com
- bsc#980724 - VUL-0: CVE-2016-4441: Qemu: scsi: esp: OOB write
  while writing to 's->cmdbuf' in get_cmd
  CVE-2016-4441-qemut-scsi-esp-OOB-write-while-writing-to-cmdbuf-in-get_cmd.patch
- bsc#980716 - VUL-0: CVE-2016-4439: xen: scsi: esp: OOB write
  while writing to 's->cmdbuf' in esp_reg_write
  CVE-2016-4439-qemut-scsi-esp-OOB-write-while-writing-to-cmdbuf-in-esp_reg_write.patch
* Tue May 17 2016 carnold@suse.com
- fate#319989 - Update to Xen 4.7 RC3
  xen-4.7.0-testing-src.tar.bz2
- Dropped
  libxl-remove-cdrom-cachemode.patch
  x86-PoD-only-reclaim-if-needed.patch
  gcc6-warnings-as-errors.patch
* Wed May 11 2016 carnold@suse.com
- bsc#954872 - script block-dmmd not working as expected - libxl:
  error: libxl_dm.c (another modification)
  block-dmmd
* Tue May 10 2016 carnold@suse.com
- fate#319989 - Update to Xen 4.7 RC2
  xen-4.7.0-testing-src.tar.bz2
* Tue May 10 2016 carnold@suse.com
- bsc#961600 - L3: poor performance when Xen HVM domU configured
  with max memory > current memory
  x86-PoD-only-reclaim-if-needed.patch
* Fri May  6 2016 ohering@suse.de
- Mark SONAMEs and pkgconfig as xen 4.7
  xen.pkgconfig-4.7.patch
* Tue May  3 2016 jfehlig@suse.com
- bsc#977329 - Xen: Cannot boot HVM guests with empty cdrom
  libxl-remove-cdrom-cachemode.patch
* Tue May  3 2016 carnold@suse.com
- fate#319989 - Update to Xen 4.7 RC1
  xen-4.7.0-testing-src.tar.bz2
* Tue May  3 2016 ohering@suse.de
- fate#316614: set migration constraints from cmdline
  restore libxl.set-migration-constraints-from-cmdline.patch
* Tue May  3 2016 ohering@suse.de
- Remove obsolete patch for xen-kmp
  magic_ioport_compat.patch
* Tue May  3 2016 ohering@suse.de
- fate#316613: update to v12
  libxl.pvscsi.patch
* Fri Apr 29 2016 carnold@suse.com
- Update to the latest Xen 4.7 pre-release c2994f86
  Drop libxl.migrate-legacy-stream-read.patch
* Fri Apr 15 2016 ohering@suse.de
- bnc#972756 - Can't migrate HVM guest from SLES12SP1 Xen host
  to SLES12SP2 Alpha 1 host using xl migrate
  libxl.migrate-legacy-stream-read.patch
* Fri Apr  1 2016 jfehlig@suse.com
- Add patches from proposed upstream series to load BIOS's from
  the toolstack instead of embedding in hvmloader
  http://lists.xenproject.org/archives/html/xen-devel/2016-03/msg01626.html
  0001-libxc-Rework-extra-module-initialisation.patch,
  0002-libxc-Prepare-a-start-info-structure-for-hvmloader.patch,
  0003-configure-define-SEABIOS_PATH-and-OVMF_PATH.patch,
  0004-firmware-makefile-install-BIOS-blob.patch,
  0005-libxl-Load-guest-BIOS-from-file.patch,
  0006-xen-Move-the-hvm_start_info-C-representation-from-li.patch,
  0007-hvmloader-Grab-the-hvm_start_info-pointer.patch,
  0008-hvmloader-Locate-the-BIOS-blob.patch,
  0009-hvmloader-Check-modules-whereabouts-in-perform_tests.patch,
  0010-hvmloader-Load-SeaBIOS-from-hvm_start_info-modules.patch,
  0011-hvmloader-Load-OVMF-from-modules.patch,
  0012-hvmloader-Specific-bios_load-function-required.patch,
  0013-hvmloader-Always-build-in-SeaBIOS-and-OVMF-loader.patch,
  0014-configure-do-not-depend-on-SEABIOS_PATH-or-OVMF_PATH.patch
- Enable support for UEFI on x86_64 using the ovmf-x86_64-ms.bin
  firmware from qemu-ovmf-x86_64. The firmware is preloaded with
  Microsoft keys to more closely resemble firmware on real hardware
  FATE#320490
* Fri Mar 25 2016 carnold@suse.com
- fate#319989: Update to Xen 4.7 (pre-release)
  xen-4.7.0-testing-src.tar.bz2
- Dropped:
  xen-4.6.1-testing-src.tar.bz2
  55f7f9d2-libxl-slightly-refine-pci-assignable-add-remove-handling.patch
  5628fc67-libxl-No-emulated-disk-driver-for-xvdX-disk.patch
  5644b756-x86-HVM-don-t-inject-DB-with-error-code.patch
  5649bcbe-libxl-relax-readonly-check-introduced-by-XSA-142-fix.patch
  hotplug-Linux-block-performance-fix.patch
  set-mtu-from-bridge-for-tap-interface.patch
  xendomains-libvirtd-conflict.patch
  xsa154.patch
  xsa155-xen-0001-xen-Add-RING_COPY_REQUEST.patch
  xsa155-xen-0002-blktap2-Use-RING_COPY_REQUEST.patch
  xsa155-xen-0003-libvchan-Read-prod-cons-only-once.patch
  xsa170.patch
* Tue Mar 22 2016 jfehlig@suse.com
- Use system SeaBIOS instead of building/installing another one
  FATE#320638
  Dropped files:
  seabios-dir-remote.tar.bz2
  xen-c99-fix.patch
  xen.build-compare.seabios.patch
* Wed Mar 16 2016 jfehlig@suse.com
- spec: drop BuildRequires that were only needed for qemu-xen
* Fri Mar  4 2016 carnold@suse.com
- bsc#969377 - xen does not build with GCC 6
  ipxe-use-rpm-opt-flags.patch
  gcc6-warnings-as-errors.patch
* Thu Mar  3 2016 carnold@suse.com
- bsc#969351 - VUL-0: CVE-2016-2841: xen: net: ne2000: infinite
  loop in ne2000_receive
  CVE-2016-2841-qemut-ne2000-infinite-loop-in-ne2000_receive.patch
- Drop xsa154-fix.patch
* Wed Mar  2 2016 jfehlig@suse.com
- Use system qemu instead of building/installing yet another qemu
  FATE#320638
- Dropped files
  qemu-xen-dir-remote.tar.bz2
  CVE-2014-0222-qemuu-qcow1-validate-l2-table-size.patch
  CVE-2015-1779-qemuu-incrementally-decode-websocket-frames.patch
  CVE-2015-1779-qemuu-limit-size-of-HTTP-headers-from-websockets-clients.patch
  CVE-2015-4037-qemuu-smb-config-dir-name.patch
  CVE-2015-7512-qemuu-net-pcnet-buffer-overflow-in-non-loopback-mode.patch
  CVE-2015-7549-qemuu-pci-null-pointer-dereference-issue.patch
  CVE-2015-8345-qemuu-eepro100-infinite-loop-fix.patch
  CVE-2015-8504-qemuu-vnc-avoid-floating-point-exception.patch
  CVE-2015-8558-qemuu-usb-infinite-loop-in-ehci_advance_state-results-in-DoS.patch
  CVE-2015-8568-qemuu-net-vmxnet3-avoid-memory-leakage-in-activate_device.patch
  CVE-2015-8613-qemuu-scsi-initialise-info-object-with-appropriate-size.patch
  CVE-2015-8743-qemuu-ne2000-OOB-memory-access-in-ioport-rw-functions.patch
  CVE-2015-8744-qemuu-net-vmxnet3-incorrect-l2-header-validation-leads-to-crash.patch
  CVE-2015-8745-qemuu-net-vmxnet3-read-IMR-registers-instead-of-assert.patch
  CVE-2016-1568-qemuu-ide-ahci-reset-ncq-object-to-unused-on-error.patch
  CVE-2016-1714-qemuu-fw_cfg-add-check-to-validate-current-entry-value.patch
  CVE-2014-7815-qemut-vnc-sanitize-bits_per_pixel-from-the-client.patch
  CVE-2016-1981-qemuu-e1000-eliminate-infinite-loops-on-out-of-bounds-transfer.patch
  CVE-2016-2538-qemuu-usb-integer-overflow-in-remote-NDIS-message-handling.patch
  CVE-2015-8619-qemuu-stack-based-OOB-write-in-hmp_sendkey-routine.patch
  qemu-xen-enable-spice-support.patch
  qemu-xen-upstream-qdisk-cache-unsafe.patch
  tigervnc-long-press.patch
  xsa162-qemuu.patch
* Mon Feb 29 2016 carnold@suse.com
- bsc#962321 - VUL-0: CVE-2016-1922: xen: i386: null pointer
  dereference in vapic_write()
  CVE-2016-1922-qemuu-i386-null-pointer-dereference-in-vapic_write.patch
* Wed Feb 24 2016 carnold@suse.com
- bsc#968004 - VUL-0: CVE-2016-2538: xen: usb: integer overflow in
  remote NDIS control message handling
  CVE-2016-2538-qemuu-usb-integer-overflow-in-remote-NDIS-message-handling.patch
* Thu Feb 18 2016 carnold@suse.com
- bsc#954872 - L3: script block-dmmd not working as expected -
  libxl: error: libxl_dm.c
  block-dmmd
- Update libxl to recognize dmmd and npiv prefix in disk spec
  xen.libxl.dmmd.patch
* Wed Feb 17 2016 carnold@suse.com
- bsc#967101 - VUL-0: CVE-2016-2391: xen: usb: multiple eof_timers
  in ohci module leads to null pointer dereference
  CVE-2016-2391-qemuu-usb-null-pointer-dereference-in-ohci-module.patch
  CVE-2016-2391-qemut-usb-null-pointer-dereference-in-ohci-module.patch
- bsc#967090 - VUL-0: CVE-2016-2392: xen: usb: null pointer
  dereference in remote NDIS control message handling
  CVE-2016-2392-qemuu-usb-null-pointer-dereference-in-NDIS-message-handling.patch
* Thu Feb 11 2016 carnold@suse.com
- Update to Xen Version 4.6.1
  xen-4.6.1-testing-src.tar.bz2
- Dropped patches now contained in tarball or unnecessary
  xen-4.6.0-testing-src.tar.bz2
  5604f239-x86-PV-properly-populate-descriptor-tables.patch
  561bbc8b-VT-d-don-t-suppress-invalidation-address-write-when-it-is-zero.patch
  561d2046-VT-d-use-proper-error-codes-in-iommu_enable_x2apic_IR.patch
  561d20a0-x86-hide-MWAITX-from-PV-domains.patch
  561e3283-x86-NUMA-fix-SRAT-table-processor-entry-parsing-and-consumption.patch
  5632118e-arm-Support-hypercall_create_continuation-for-multicall.patch
  56321222-arm-rate-limit-logging-from-unimplemented-PHYSDEVOP-and-HVMOP.patch
  56321249-arm-handle-races-between-relinquish_memory-and-free_domheap_pages.patch
  5632127b-x86-guard-against-undue-super-page-PTE-creation.patch
  5632129c-free-domain-s-vcpu-array.patch
  563212c9-x86-PoD-Eager-sweep-for-zeroed-pages.patch
  563212e4-xenoprof-free-domain-s-vcpu-array.patch
  563212ff-x86-rate-limit-logging-in-do_xen-oprof-pmu-_op.patch
  56323737-libxl-adjust-PoD-target-by-memory-fudge-too.patch
  56377442-x86-PoD-Make-p2m_pod_empty_cache-restartable.patch
  5641ceec-x86-HVM-always-intercept-AC-and-DB.patch
  56549f24-x86-vPMU-document-as-unsupported.patch
  5677f350-x86-make-debug-output-consistent-in-hvm_set_callback_via.patch
  xsa155-qemut-qdisk-double-access.patch
  xsa155-qemut-xenfb.patch
  xsa155-qemuu-qdisk-double-access.patch
  xsa155-qemuu-xenfb.patch
  xsa159.patch
  xsa160.patch
  xsa162-qemut.patch
  xsa165.patch
  xsa166.patch
  xsa167.patch
  xsa168.patch
* Fri Feb  5 2016 carnold@suse.com
- bsc#965315 - VUL-0: CVE-2016-2270: xen: x86: inconsistent
  cachability flags on guest mappings (XSA-154)
  xsa154.patch
- bsc#965317 - VUL-0: CVE-2016-2271: xen: VMX: guest user mode may
  crash guest with non-canonical RIP (XSA-170)
  xsa170.patch
* Fri Feb  5 2016 carnold@suse.com
- bsc#965269 - VUL-1: CVE-2015-8619: xen: stack based OOB write in
  hmp_sendkey routine
  CVE-2015-8619-qemuu-stack-based-OOB-write-in-hmp_sendkey-routine.patch
* Thu Feb  4 2016 carnold@suse.com
- bsc#965156 - VUL-0: CVE-2015-6855: xen: ide: divide by zero issue
  CVE-2015-6855-qemuu-ide-divide-by-zero-issue.patch
- bsc#965112 - VUL-0: CVE-2014-3640: xen: slirp: NULL pointer deref
  in sosendto()
  CVE-2014-3640-qemut-slirp-NULL-pointer-deref-in-sosendto.patch
* Wed Feb  3 2016 carnold@suse.com
- bsc#964947 - VUL-0: CVE-2015-5278: xen: Infinite loop in
  ne2000_receive() function
  CVE-2015-5278-qemut-Infinite-loop-in-ne2000_receive-function.patch
- bsc#956832 - VUL-0: CVE-2015-8345: xen: qemu: net: eepro100:
  infinite loop in processing command block list
  CVE-2015-8345-qemuu-eepro100-infinite-loop-fix.patch
  CVE-2015-8345-qemut-eepro100-infinite-loop-fix.patch
* Tue Feb  2 2016 carnold@suse.com
- bsc#964644 - VUL-0: CVE-2013-4533: xen pxa2xx: buffer overrun on
  incoming migration
  CVE-2013-4533-qemut-pxa2xx-buffer-overrun-on-incoming-migration.patch
- bsc#964925 - VUL-0: CVE-2014-0222: xen: qcow1: validate L2 table
  size to avoid integer overflows
  CVE-2014-0222-blktap-qcow1-validate-l2-table-size.patch
- Dropped CVE-2014-0222-qemuu-qcow1-validate-l2-table-size.patch
* Mon Feb  1 2016 carnold@suse.com
- bsc#964415 - VUL-1: CVE-2016-2198: xen: usb: ehci null pointer
  dereference in ehci_caps_write
  CVE-2016-2198-qemuu-usb-ehci-null-pointer-dereference-in-ehci_caps_write.patch
- bsc#964452 - VUL-0: CVE-2013-4534: xen: openpic: buffer overrun
  on incoming migration
  CVE-2013-4534-qemut-openpic-buffer-overrun-on-incoming-migration.patch
* Wed Jan 27 2016 carnold@suse.com
- bsc#963783 - VUL-1: CVE-2016-1981: xen: net: e1000 infinite loop
  in start_xmit and e1000_receive_iov routines
  CVE-2016-1981-qemuu-e1000-eliminate-infinite-loops-on-out-of-bounds-transfer.patch
  CVE-2016-1981-qemut-e1000-eliminate-infinite-loops-on-out-of-bounds-transfer.patch
* Wed Jan 20 2016 carnold@suse.com
- bsc#962758 - VUL-0: CVE-2013-4539: xen: tsc210x: buffer overrun
  on invalid state load
  CVE-2013-4539-qemut-tsc210x-fix-buffer-overrun-on-invalid-state-load.patch
* Tue Jan 19 2016 carnold@suse.com
- bsc#962632 - VUL-0: CVE-2015-1779: xen: vnc: insufficient
  resource limiting in VNC websockets decoder
  CVE-2015-1779-qemuu-limit-size-of-HTTP-headers-from-websockets-clients.patch
  CVE-2015-1779-qemuu-incrementally-decode-websocket-frames.patch
- bsc#962642 - VUL-0: CVE-2013-4537: xen: ssi-sd: buffer overrun on
  invalid state load
  CVE-2013-4537-qemut-ssi-sd-fix-buffer-overrun-on-invalid-state-load.patch
- bsc#962627 - VUL-0: CVE-2014-7815: xen: vnc: insufficient
  bits_per_pixel from the client sanitization
  CVE-2014-7815-qemut-vnc-sanitize-bits_per_pixel-from-the-client.patch
* Mon Jan 18 2016 carnold@suse.com
- bsc#962335 - VUL-0: CVE-2013-4538: xen: ssd0323: fix buffer
  overun on invalid state
  CVE-2013-4538-qemut-ssd0323-fix-buffer-overun-on-invalid-state.patch
- bsc#962360 - VUL-0: CVE-2015-7512: xen: net: pcnet: buffer
  overflow in non-loopback mode
  CVE-2015-7512-qemuu-net-pcnet-buffer-overflow-in-non-loopback-mode.patch
  CVE-2015-7512-qemut-net-pcnet-buffer-overflow-in-non-loopback-mode.patch
* Wed Jan 13 2016 carnold@suse.com
- bsc#961692 - VUL-0: CVE-2016-1714: xen: nvram: OOB r/w access in
  processing firmware configurations
  CVE-2016-1714-qemuu-fw_cfg-add-check-to-validate-current-entry-value.patch
  CVE-2016-1714-qemut-fw_cfg-add-check-to-validate-current-entry-value.patch
* Mon Jan 11 2016 carnold@suse.com
- bsc#961358 - VUL-0: CVE-2015-8613: xen: qemu: scsi: stack based
  buffer overflow in megasas_ctrl_get_info
  CVE-2015-8613-qemuu-scsi-initialise-info-object-with-appropriate-size.patch
- bsc#961332 - VUL-0: CVE-2016-1568: xen: Qemu: ide: ahci
  use-after-free vulnerability in aio port commands
  CVE-2016-1568-qemuu-ide-ahci-reset-ncq-object-to-unused-on-error.patch
* Thu Jan  7 2016 carnold@suse.com
- bsc#959695 - missing docs for xen
  xen.spec
* Wed Jan  6 2016 carnold@suse.com
- bsc#960862 - VUL-0: CVE-2016-1571: xen: VMX: intercept issue with
  INVLPG on non-canonical address (XSA-168)
  xsa168.patch
- bsc#960861 - VUL-0: CVE-2016-1570: xen: PV superpage
  functionality missing sanity checks (XSA-167)
  xsa167.patch
- bsc#960836 - VUL-0: CVE-2015-8744: xen: net: vmxnet3: incorrect
  l2 header validation leads to a crash via assert(2) call
  CVE-2015-8744-qemuu-net-vmxnet3-incorrect-l2-header-validation-leads-to-crash.patch
* Tue Jan  5 2016 carnold@suse.com
- bsc#960707 - VUL-0: CVE-2015-8745: xen: reading IMR registers
  leads to a crash via assert(2) call
  CVE-2015-8745-qemuu-net-vmxnet3-read-IMR-registers-instead-of-assert.patch
- bsc#960726 - VUL-0: CVE-2015-8743: xen: ne2000: OOB memory access
  in ioport r/w functions
  CVE-2015-8743-qemuu-ne2000-OOB-memory-access-in-ioport-rw-functions.patch
* Mon Jan  4 2016 carnold@suse.com
- bsc#960093 - VUL-0: CVE-2015-8615: xen: x86: unintentional
  logging upon guest changing callback method (XSA-169)
  5677f350-x86-make-debug-output-consistent-in-hvm_set_callback_via.patch
* Mon Dec 21 2015 ohering@suse.de
- Adjust xen-dom0-modules.service to run Before xenstored.service
  instead of proc-xen.mount to workaround a bug in systemd "design"
  (bnc#959845)
* Wed Dec 16 2015 carnold@suse.com
- bsc#959387 - VUL-0: CVE-2015-8568 CVE-2015-8567: xen: qemu: net:
  vmxnet3: host memory leakage
  CVE-2015-8568-qemuu-net-vmxnet3-avoid-memory-leakage-in-activate_device.patch
* Mon Dec 14 2015 carnold@suse.com
- bsc#957988 - VUL-0: CVE-2015-8550: xen: paravirtualized drivers
  incautious about shared memory contents (XSA-155)
  xsa155-xen-0001-xen-Add-RING_COPY_REQUEST.patch
  xsa155-xen-0002-blktap2-Use-RING_COPY_REQUEST.patch
  xsa155-xen-0003-libvchan-Read-prod-cons-only-once.patch
  xsa155-qemuu-qdisk-double-access.patch
  xsa155-qemut-qdisk-double-access.patch
  xsa155-qemuu-xenfb.patch
  xsa155-qemut-xenfb.patch
- bsc#959006 - VUL-0: CVE-2015-8558: xen: qemu: usb: infinite loop
  in ehci_advance_state results in DoS
  CVE-2015-8558-qemuu-usb-infinite-loop-in-ehci_advance_state-results-in-DoS.patch
- bsc#958918 - VUL-0: CVE-2015-7549: xen: qemu pci: null pointer
  dereference issue
  CVE-2015-7549-qemuu-pci-null-pointer-dereference-issue.patch
- bsc#958493 - VUL-0: CVE-2015-8504: xen: qemu: ui: vnc: avoid
  floating point exception
  CVE-2015-8504-qemuu-vnc-avoid-floating-point-exception.patch
  CVE-2015-8504-qemut-vnc-avoid-floating-point-exception.patch
- bsc#958007 - VUL-0: CVE-2015-8554: xen: qemu-dm buffer overrun in
  MSI-X handling (XSA-164)
  xsa164.patch
- bsc#958009 - VUL-0: CVE-2015-8555: xen: information leak in
  legacy x86 FPU/XMM initialization (XSA-165)
  xsa165.patch
- bsc#958523 - VUL-0: xen: ioreq handling possibly susceptible to
  multiple read issue (XSA-166)
  xsa166.patch
* Fri Nov 27 2015 carnold@suse.com
- bsc#956832 - VUL-0: CVE-2015-8345: xen: qemu: net: eepro100:
  infinite loop in processing command block list
  CVE-2015-8345-qemuu-eepro100-infinite-loop-fix.patch
  CVE-2015-8345-qemut-eepro100-infinite-loop-fix.patch
- Upstream patches from Jan
  56377442-x86-PoD-Make-p2m_pod_empty_cache-restartable.patch
  5641ceec-x86-HVM-always-intercept-AC-and-DB.patch (Replaces CVE-2015-5307-xsa156.patch)
  5644b756-x86-HVM-don-t-inject-DB-with-error-code.patch
  56544a57-VMX-fix-adjust-trap-injection.patch
  56546ab2-sched-fix-insert_vcpu-locking.patch
* Wed Nov 25 2015 carnold@suse.com
- bsc#956592 - VUL-0: xen: virtual PMU is unsupported (XSA-163)
  56549f24-x86-vPMU-document-as-unsupported.patch
- bsc#956408 - VUL-0: CVE-2015-8339, CVE-2015-8340: xen:
  XENMEM_exchange error handling issues (XSA-159)
  xsa159.patch
- bsc#956409 - VUL-0: CVE-2015-8341: xen: libxl leak of pv kernel
  and initrd on error (XSA-160)
  xsa160.patch
- bsc#956411 - VUL-0: CVE-2015-7504: xen: heap buffer overflow
  vulnerability in pcnet emulator (XSA-162)
  xsa162-qemuu.patch
  xsa162-qemut.patch
- bsc#947165 - VUL-0: CVE-2015-7311: xen: libxl fails to honour
  readonly flag on disks with qemu-xen (xsa-142)
  5628fc67-libxl-No-emulated-disk-driver-for-xvdX-disk.patch
  5649bcbe-libxl-relax-readonly-check-introduced-by-XSA-142-fix.patch
* Tue Nov 24 2015 carnold@suse.com
- fate#315712: XEN: Use the PVOPS kernel
  Turn off building the KMPs now that we are using the pvops kernel
  xen.spec
* Thu Nov 19 2015 carnold@suse.com
- Upstream patches from Jan
  561bbc8b-VT-d-don-t-suppress-invalidation-address-write-when-it-is-zero.patch
  561d20a0-x86-hide-MWAITX-from-PV-domains.patch
  561e3283-x86-NUMA-fix-SRAT-table-processor-entry-parsing-and-consumption.patch
  5632118e-arm-Support-hypercall_create_continuation-for-multicall.patch
  56321222-arm-rate-limit-logging-from-unimplemented-PHYSDEVOP-and-HVMOP.patch
  56321249-arm-handle-races-between-relinquish_memory-and-free_domheap_pages.patch
  5632127b-x86-guard-against-undue-super-page-PTE-creation.patch
  5632129c-free-domain-s-vcpu-array.patch (Replaces CVE-2015-7969-xsa149.patch)
  563212c9-x86-PoD-Eager-sweep-for-zeroed-pages.patch
  563212e4-xenoprof-free-domain-s-vcpu-array.patch
  563212ff-x86-rate-limit-logging-in-do_xen-oprof-pmu-_op.patch
  56323737-libxl-adjust-PoD-target-by-memory-fudge-too.patch
  56377442-x86-PoD-Make-p2m_pod_empty_cache-restartable.patch
  5641ceec-x86-HVM-always-intercept-AC-and-DB.patch (Replaces CVE-2015-5307-xsa156.patch)
  5644b756-x86-HVM-don-t-inject-DB-with-error-code.patch
- Dropped 55b0a2db-x86-MSI-track-guest-masking.patch
* Thu Nov 19 2015 ohering@suse.de
- Use upstream variants of block-iscsi and block-nbd
* Thu Nov 19 2015 ohering@suse.de
- Remove xenalyze.hg, its part of xen-4.6
* Tue Nov 10 2015 carnold@suse.com
- Update to Xen Version 4.6.0
  xen-4.6.0-testing-src.tar.bz2
  mini-os.tar.bz2
  blktap2-no-uninit.patch
  stubdom-have-iovec.patch
- Renamed
  xsa149.patch to CVE-2015-7969-xsa149.patch
- Dropped patches now contained in tarball or unnecessary
  xen-4.5.2-testing-src.tar.bz2
  54c2553c-grant-table-use-uint16_t-consistently-for-offset-and-length.patch
  54ca33bc-grant-table-refactor-grant-copy-to-reduce-duplicate-code.patch
  54ca340e-grant-table-defer-releasing-pages-acquired-in-a-grant-copy.patch
  54f4985f-libxl-fix-libvirtd-double-free.patch
  55103616-vm-assist-prepare-for-discontiguous-used-bit-numbers.patch
  551ac326-xentop-add-support-for-qdisk.patch
  552d0fd2-x86-hvm-don-t-include-asm-spinlock-h.patch
  552d0fe8-x86-mtrr-include-asm-atomic.h.patch
  552d293b-x86-vMSI-X-honor-all-mask-requests.patch
  552d2966-x86-vMSI-X-add-valid-bits-for-read-acceleration.patch
  5537a4d8-libxl-use-DEBUG-log-level-instead-of-INFO.patch
  5548e903-domctl-don-t-truncate-XEN_DOMCTL_max_mem-requests.patch
  5548e95d-x86-allow-to-suppress-M2P-user-mode-exposure.patch
  554c7aee-x86-provide-arch_fetch_and_add.patch
  554c7b00-arm-provide-arch_fetch_and_add.patch
  554cc211-libxl-add-qxl.patch 55534b0a-x86-provide-add_sized.patch
  55534b25-arm-provide-add_sized.patch
  5555a4f8-use-ticket-locks-for-spin-locks.patch
  5555a5b9-x86-arm-remove-asm-spinlock-h.patch
  5555a8ec-introduce-non-contiguous-allocation.patch
  556d973f-unmodified-drivers-tolerate-IRQF_DISABLED-being-undefined.patch
  5576f143-x86-adjust-PV-I-O-emulation-functions-types.patch
  55795a52-x86-vMSI-X-support-qword-MMIO-access.patch
  557eb55f-gnttab-per-active-entry-locking.patch
  557eb5b6-gnttab-introduce-maptrack-lock.patch
  557eb620-gnttab-make-the-grant-table-lock-a-read-write-lock.patch
  557ffab8-evtchn-factor-out-freeing-an-event-channel.patch
  5582bf43-evtchn-simplify-port_is_valid.patch
  5582bf81-evtchn-remove-the-locking-when-unmasking-an-event-channel.patch
  5583d9c5-x86-MSI-X-cleanup.patch
  5583da09-x86-MSI-track-host-and-guest-masking-separately.patch
  5583da64-gnttab-use-per-VCPU-maptrack-free-lists.patch
  5583da8c-gnttab-steal-maptrack-entries-from-other-VCPUs.patch
  5587d711-evtchn-clear-xen_consumer-when-clearing-state.patch
  5587d779-evtchn-defer-freeing-struct-evtchn-s-until-evtchn_destroy_final.patch
  5587d7b7-evtchn-use-a-per-event-channel-lock-for-sending-events.patch
  5587d7e2-evtchn-pad-struct-evtchn-to-64-bytes.patch
  55b0a218-x86-PCI-CFG-write-intercept.patch
  55b0a255-x86-MSI-X-maskall.patch 55b0a283-x86-MSI-X-teardown.patch
  55b0a2ab-x86-MSI-X-enable.patch blktapctrl-close-fifos.patch
  blktapctrl-default-to-ioemu.patch blktapctrl-disable-debug-printf.patch
  blktap-no-uninit.patch blktap-pv-cdrom.patch build-tapdisk-ioemu.patch
  ioemu-bdrv-open-CACHE_WB.patch ioemu-blktap-barriers.patch
  ioemu-blktap-fv-init.patch ioemu-blktap-image-format.patch
  ioemu-blktap-zero-size.patch libxl.set-migration-constraints-from-cmdline.patch
  local_attach_support_for_phy.patch pci-attach-fix.patch
  qemu-xen-upstream-megasas-buildtime.patch tapdisk-ioemu-logfile.patch
  tapdisk-ioemu-shutdown-fix.patch udev-rules.patch xen.build-compare.ipxe.patch
  xen.build-compare.mini-os.patch xen.build-compare.smbiosdate.patch
  xen.build-compare.vgabios.patch xen.build-compare.xen_compile_h.patch
  xl-coredump-file-location.patch
* Thu Nov  5 2015 carnold@suse.com
- bsc#954405 - VUL-0: CVE-2015-8104: Xen: guest to host DoS by
  triggering an infinite loop in microcode via #DB exception
- bsc#954018 - VUL-0: CVE-2015-5307: xen: x86: CPU lockup during
  fault delivery (XSA-156)
  CVE-2015-5307-xsa156.patch
* Wed Nov  4 2015 carnold@suse.com
- Update to Xen 4.5.2
  xen-4.5.2-testing-src.tar.bz2
- Drop the following
  xen-4.5.1-testing-src.tar.bz2
  552d0f49-x86-traps-identify-the-vcpu-in-context-when-dumping-regs.patch
  5576f178-kexec-add-more-pages-to-v1-environment.patch
  55780be1-x86-EFI-adjust-EFI_MEMORY_WP-handling-for-spec-version-2.5.patch
  558bfaa0-x86-traps-avoid-using-current-too-early.patch
  5592a116-nested-EPT-fix-the-handling-of-nested-EPT.patch
  559b9dd6-x86-p2m-ept-don-t-unmap-in-use-EPT-pagetable.patch
  559bc633-x86-cpupool-clear-proper-cpu_valid-bit-on-CPU-teardown.patch
  559bc64e-credit1-properly-deal-with-CPUs-not-in-any-pool.patch
  559bc87f-x86-hvmloader-avoid-data-corruption-with-xenstore-rw.patch
  559bdde5-pull-in-latest-linux-earlycpio.patch
  55a62eb0-xl-correct-handling-of-extra_config-in-main_cpupoolcreate.patch
  55a66a1e-make-rangeset_report_ranges-report-all-ranges.patch
  55a77e4f-dmar-device-scope-mem-leak-fix.patch
  55c1d83d-x86-gdt-Drop-write-only-xalloc-d-array.patch
  55c3232b-x86-mm-Make-hap-shadow-teardown-preemptible.patch
  55dc78e9-x86-amd_ucode-skip-updates-for-final-levels.patch
  55df2f76-IOMMU-skip-domains-without-page-tables-when-dumping.patch
  55e43fd8-x86-NUMA-fix-setup_node.patch
  55e43ff8-x86-NUMA-don-t-account-hotplug-regions.patch
  55e593f1-x86-NUMA-make-init_node_heap-respect-Xen-heap-limit.patch
  55f2e438-x86-hvm-fix-saved-pmtimer-and-hpet-values.patch
  55f9345b-x86-MSI-fail-if-no-hardware-support.patch
  5604f2e6-vt-d-fix-IM-bit-mask-and-unmask-of-FECTL_REG.patch
  560a4af9-x86-EPT-tighten-conditions-of-IOMMU-mapping-updates.patch
  560a7c36-x86-p2m-pt-delay-freeing-of-intermediate-page-tables.patch
  560a7c53-x86-p2m-pt-ignore-pt-share-flag-for-shadow-mode-guests.patch
  560bd926-credit1-fix-tickling-when-it-happens-from-a-remote-pCPU.patch
  560e6d34-x86-p2m-pt-tighten-conditions-of-IOMMU-mapping-updates.patch
  561bbc8b-VT-d-don-t-suppress-invalidation-address-write-when-0.patch
  561d20a0-x86-hide-MWAITX-from-PV-domains.patch
  561e3283-x86-NUMA-fix-SRAT-table-processor-entry-handling.patch
  563212c9-x86-PoD-Eager-sweep-for-zeroed-pages.patch
  CVE-2015-4106-xsa131-9.patch CVE-2015-3259-xsa137.patch
  CVE-2015-7311-xsa142.patch CVE-2015-7835-xsa148.patch
  xsa139-qemuu.patch xsa140-qemuu-1.patch xsa140-qemuu-2.patch
  xsa140-qemuu-3.patch xsa140-qemuu-4.patch xsa140-qemuu-5.patch
  xsa140-qemuu-6.patch xsa140-qemuu-7.patch xsa140-qemut-1.patch
  xsa140-qemut-2.patch xsa140-qemut-3.patch xsa140-qemut-4.patch
  xsa140-qemut-5.patch xsa140-qemut-6.patch xsa140-qemut-7.patch
  xsa151.patch xsa152.patch xsa153-libxl.patch
  CVE-2015-5154-qemuu-check-array-bounds-before-writing-to-io_buffer.patch
  CVE-2015-5154-qemuu-fix-START-STOP-UNIT-command-completion.patch
  CVE-2015-5154-qemuu-clear-DRQ-after-handling-all-expected-accesses.patch
  CVE-2015-5154-qemut-check-array-bounds-before-writing-to-io_buffer.patch
  CVE-2015-5154-qemut-clear-DRQ-after-handling-all-expected-accesses.patch
  CVE-2015-6815-qemuu-e1000-fix-infinite-loop.patch
  CVE-2015-5239-qemuu-limit-client_cut_text-msg-payload-size.patch
  CVE-2015-5239-qemut-limit-client_cut_text-msg-payload-size.patch"
* Mon Nov  2 2015 carnold@suse.com
- bsc#950704 - CVE-2015-7970 VUL-1: xen: x86: Long latency
  populate-on-demand operation is not preemptible (XSA-150)
  563212c9-x86-PoD-Eager-sweep-for-zeroed-pages.patch
* Wed Oct 28 2015 carnold@suse.com
- Upstream patches from Jan
  5604f239-x86-PV-properly-populate-descriptor-tables.patch
  561bbc8b-VT-d-don-t-suppress-invalidation-address-write-when-0.patch
  561d2046-VT-d-use-proper-error-codes-in-iommu_enable_x2apic_IR.patch
  561d20a0-x86-hide-MWAITX-from-PV-domains.patch
  561e3283-x86-NUMA-fix-SRAT-table-processor-entry-handling.patch
* Fri Oct 23 2015 carnold@suse.com
- bsc#951845 - VUL-0: CVE-2015-7972: xen: x86: populate-on-demand
  balloon size inaccuracy can crash guests (XSA-153)
  xsa153-libxl.patch
* Fri Oct 16 2015 carnold@suse.com
- bsc#950703 - VUL-1: CVE-2015-7969: xen: leak of main per-domain
  vcpu pointer array (DoS) (XSA-149)
  xsa149.patch
- bsc#950705 - VUL-1: CVE-2015-7969: xen: x86: leak of per-domain
  profiling-related vcpu pointer array (DoS) (XSA-151)
  xsa151.patch
- bsc#950706 - VUL-0: CVE-2015-7971: xen: x86: some pmu and
  profiling hypercalls log without rate limiting (XSA-152)
  xsa152.patch
- Dropped
  55dc7937-x86-IO-APIC-don-t-create-pIRQ-mapping-from-masked-RTE.patch
  5604f239-x86-PV-properly-populate-descriptor-tables.patch
* Thu Oct 15 2015 carnold@suse.com
- bsc#932267 - VUL-1: CVE-2015-4037: qemu,kvm,xen: insecure
  temporary file use in /net/slirp.c
  CVE-2015-4037-qemuu-smb-config-dir-name.patch
  CVE-2015-4037-qemut-smb-config-dir-name.patch
- bsc#877642 - VUL-0: CVE-2014-0222: qemu: qcow1: validate L2 table
  size to avoid integer overflows
  CVE-2014-0222-qemuu-qcow1-validate-l2-table-size.patch
  CVE-2014-0222-qemut-qcow1-validate-l2-table-size.patch
* Wed Oct 14 2015 carnold@suse.com
- bsc#950367 - VUL-0: CVE-2015-7835: xen: x86: Uncontrolled
  creation of large page mappings by PV guests (XSA-148)
  CVE-2015-7835-xsa148.patch
* Tue Oct  6 2015 jfehlig@suse.com
- bsc#949138 - Setting vcpu affinity under Xen causes libvirtd
  abort
  54f4985f-libxl-fix-libvirtd-double-free.patch
* Tue Oct  6 2015 carnold@suse.com
- bsc#949046 - Increase %%suse_version in SP1 to 1316
  xen.spec
- Update README.SUSE detailing dom0 ballooning recommendations
* Mon Oct  5 2015 carnold@suse.com
- bsc#945167 - Running command ’ xl pci-assignable-add 03:10.1’
  secondly show errors
  55f7f9d2-libxl-slightly-refine-pci-assignable-add-remove-handling.patch
- Upstream patches from Jan
  55f2e438-x86-hvm-fix-saved-pmtimer-and-hpet-values.patch
  55f9345b-x86-MSI-fail-if-no-hardware-support.patch
  5604f239-x86-PV-properly-populate-descriptor-tables.patch
  5604f2e6-vt-d-fix-IM-bit-mask-and-unmask-of-FECTL_REG.patch
  560a4af9-x86-EPT-tighten-conditions-of-IOMMU-mapping-updates.patch
  560a7c36-x86-p2m-pt-delay-freeing-of-intermediate-page-tables.patch
  560a7c53-x86-p2m-pt-ignore-pt-share-flag-for-shadow-mode-guests.patch
  560bd926-credit1-fix-tickling-when-it-happens-from-a-remote-pCPU.patch
  560e6d34-x86-p2m-pt-tighten-conditions-of-IOMMU-mapping-updates.patch
* Fri Oct  2 2015 mlatimer@suse.com
- bsc#941074 - VmError: Device 51728 (vbd) could not be connected.
  Hotplug scripts not working.
  hotplug-Linux-block-performance-fix.patch
* Wed Sep 23 2015 carnold@suse.com
- bsc#947165 - VUL-0: CVE-2015-7311: xen: libxl fails to honour
  readonly flag on disks with qemu-xen (xsa-142)
  CVE-2015-7311-xsa142.patch
* Wed Sep 16 2015 cyliu@suse.com
- bsc#945165 - Xl pci-attach show error with kernel of SLES 12 sp1
  pci-attach-fix.patch
* Tue Sep 15 2015 jfehlig@suse.com
- bsc#945164 - Xl destroy show error with kernel of SLES 12 sp1
  5537a4d8-libxl-use-DEBUG-log-level-instead-of-INFO.patch
* Wed Sep  9 2015 carnold@suse.com
- Upstream patches from Jan
  55dc78e9-x86-amd_ucode-skip-updates-for-final-levels.patch
  55dc7937-x86-IO-APIC-don-t-create-pIRQ-mapping-from-masked-RTE.patch
  55df2f76-IOMMU-skip-domains-without-page-tables-when-dumping.patch
  55e43fd8-x86-NUMA-fix-setup_node.patch
  55e43ff8-x86-NUMA-don-t-account-hotplug-regions.patch
  55e593f1-x86-NUMA-make-init_node_heap-respect-Xen-heap-limit.patch
  54c2553c-grant-table-use-uint16_t-consistently-for-offset-and-length.patch
  54ca33bc-grant-table-refactor-grant-copy-to-reduce-duplicate-code.patch
  54ca340e-grant-table-defer-releasing-pages-acquired-in-a-grant-copy.patch
* Tue Sep  8 2015 carnold@suse.com
- bsc#944463 - VUL-0: CVE-2015-5239: qemu-kvm: Integer overflow in
  vnc_client_read() and protocol_client_msg()
  CVE-2015-5239-qemuu-limit-client_cut_text-msg-payload-size.patch
  CVE-2015-5239-qemut-limit-client_cut_text-msg-payload-size.patch
- bsc#944697 - VUL-1: CVE-2015-6815: qemu: net: e1000: infinite
  loop issue
  CVE-2015-6815-qemuu-e1000-fix-infinite-loop.patch
  CVE-2015-6815-qemut-e1000-fix-infinite-loop.patch
* Wed Aug 26 2015 carnold@suse.com
- bnc#935634 - VUL-0: CVE-2015-3259: xen: XSA-137: xl command line
  config handling stack overflow
  55a62eb0-xl-correct-handling-of-extra_config-in-main_cpupoolcreate.patch
* Tue Aug 18 2015 carnold@suse.com
- bsc#907514 - Bus fatal error & sles12 sudden reboot has been
  observed
- bsc#910258 - SLES12 Xen host crashes with FATAL NMI after
  shutdown of guest with VT-d NIC
- bsc#918984 - Bus fatal error & sles11-SP4 sudden reboot has been
  observed
- bsc#923967 - Partner-L3: Bus fatal error & sles11-SP3 sudden
  reboot has been observed
  552d293b-x86-vMSI-X-honor-all-mask-requests.patch
  552d2966-x86-vMSI-X-add-valid-bits-for-read-acceleration.patch
  5576f143-x86-adjust-PV-I-O-emulation-functions-types.patch
  55795a52-x86-vMSI-X-support-qword-MMIO-access.patch
  5583d9c5-x86-MSI-X-cleanup.patch
  5583da09-x86-MSI-track-host-and-guest-masking-separately.patch
  55b0a218-x86-PCI-CFG-write-intercept.patch
  55b0a255-x86-MSI-X-maskall.patch
  55b0a283-x86-MSI-X-teardown.patch
  55b0a2ab-x86-MSI-X-enable.patch
  55b0a2db-x86-MSI-track-guest-masking.patch
- Upstream patches from Jan
  552d0f49-x86-traps-identify-the-vcpu-in-context-when-dumping-regs.patch
  559bc633-x86-cpupool-clear-proper-cpu_valid-bit-on-CPU-teardown.patch
  559bc64e-credit1-properly-deal-with-CPUs-not-in-any-pool.patch
  559bc87f-x86-hvmloader-avoid-data-corruption-with-xenstore-rw.patch
  55a66a1e-make-rangeset_report_ranges-report-all-ranges.patch
  55a77e4f-dmar-device-scope-mem-leak-fix.patch
  55c1d83d-x86-gdt-Drop-write-only-xalloc-d-array.patch
  55c3232b-x86-mm-Make-hap-shadow-teardown-preemptible.patch
- Dropped for upstream version
  x86-MSI-mask.patch
  x86-MSI-pv-unmask.patch
  x86-MSI-X-enable.patch
  x86-MSI-X-maskall.patch
  x86-MSI-X-teardown.patch
  x86-pci_cfg_okay.patch
  x86-PCI-CFG-write-intercept.patch
* Tue Jul 28 2015 carnold@suse.com
- bsc#939712 - VUL-0: XSA-140: QEMU leak of uninitialized heap
  memory in rtl8139 device model
  xsa140-qemuu-1.patch
  xsa140-qemuu-2.patch
  xsa140-qemuu-3.patch
  xsa140-qemuu-4.patch
  xsa140-qemuu-5.patch
  xsa140-qemuu-6.patch
  xsa140-qemuu-7.patch
  xsa140-qemut-1.patch
  xsa140-qemut-2.patch
  xsa140-qemut-3.patch
  xsa140-qemut-4.patch
  xsa140-qemut-5.patch
  xsa140-qemut-6.patch
  xsa140-qemut-7.patch
- bsc#939709 - VUL-0: XSA-139: xen: Use after free in QEMU/Xen
  block unplug protocol
  xsa139-qemuu.patch
* Tue Jul 21 2015 ohering@suse.de
- bsc#937371 - xen vm's running after reboot
  xendomains-libvirtd-conflict.patch
* Thu Jul 16 2015 carnold@suse.com
- bsc#938344 - VUL-0: CVE-2015-5154: qemu,kvm,xen: host code
  execution via IDE subsystem CD-ROM
  CVE-2015-5154-qemuu-check-array-bounds-before-writing-to-io_buffer.patch
  CVE-2015-5154-qemut-check-array-bounds-before-writing-to-io_buffer.patch
  CVE-2015-5154-qemuu-fix-START-STOP-UNIT-command-completion.patch
  CVE-2015-5154-qemut-fix-START-STOP-UNIT-command-completion.patch
  CVE-2015-5154-qemuu-clear-DRQ-after-handling-all-expected-accesses.patch
  CVE-2015-5154-qemut-clear-DRQ-after-handling-all-expected-accesses.patch
* Wed Jul 15 2015 ohering@suse.de
- Remove xendomains.service from systemd preset file because it
  conflicts with libvirt-guests.service (bnc#937371)
  Its up to the admin to run systemctl enable xendomains.service
* Wed Jul  8 2015 carnold@suse.com
- bnc#935634 - VUL-0: CVE-2015-3259: xen: XSA-137: xl command line
  config handling stack overflow
  CVE-2015-3259-xsa137.patch
- Upstream patches from Jan
  558bfaa0-x86-traps-avoid-using-current-too-early.patch
  5592a116-nested-EPT-fix-the-handling-of-nested-EPT.patch
  559b9dd6-x86-p2m-ept-don-t-unmap-in-use-EPT-pagetable.patch
  559bdde5-pull-in-latest-linux-earlycpio.patch
- Upstream patches from Jan pending review
  552d0fd2-x86-hvm-don-t-include-asm-spinlock-h.patch
  552d0fe8-x86-mtrr-include-asm-atomic.h.patch
  552d293b-x86-vMSI-X-honor-all-mask-requests.patch
  552d2966-x86-vMSI-X-add-valid-bits-for-read-acceleration.patch
  554c7aee-x86-provide-arch_fetch_and_add.patch
  554c7b00-arm-provide-arch_fetch_and_add.patch
  55534b0a-x86-provide-add_sized.patch
  55534b25-arm-provide-add_sized.patch
  5555a4f8-use-ticket-locks-for-spin-locks.patch
  5555a5b9-x86-arm-remove-asm-spinlock-h.patch
  5555a8ec-introduce-non-contiguous-allocation.patch
  55795a52-x86-vMSI-X-support-qword-MMIO-access.patch
  557eb55f-gnttab-per-active-entry-locking.patch
  557eb5b6-gnttab-introduce-maptrack-lock.patch
  557eb620-gnttab-make-the-grant-table-lock-a-read-write-lock.patch
  557ffab8-evtchn-factor-out-freeing-an-event-channel.patch
  5582bf43-evtchn-simplify-port_is_valid.patch
  5582bf81-evtchn-remove-the-locking-when-unmasking-an-event-channel.patch
  5583d9c5-x86-MSI-X-cleanup.patch
  5583da09-x86-MSI-track-host-and-guest-masking-separately.patch
  5583da64-gnttab-use-per-VCPU-maptrack-free-lists.patch
  5583da8c-gnttab-steal-maptrack-entries-from-other-VCPUs.patch
  5587d711-evtchn-clear-xen_consumer-when-clearing-state.patch
  5587d779-evtchn-defer-freeing-struct-evtchn-s-until-evtchn_destroy_final.patch
  5587d7b7-evtchn-use-a-per-event-channel-lock-for-sending-events.patch
  5587d7e2-evtchn-pad-struct-evtchn-to-64-bytes.patch
  x86-MSI-pv-unmask.patch
  x86-pci_cfg_okay.patch
  x86-PCI-CFG-write-intercept.patch
  x86-MSI-X-maskall.patch
  x86-MSI-X-teardown.patch
  x86-MSI-X-enable.patch
  x86-MSI-mask.patch
* Tue Jul  7 2015 ohering@suse.de
- Adjust more places to use br0 instead of xenbr0
* Tue Jun 30 2015 carnold@suse.com
- bnc#936516 - xen fails to build with kernel update(4.1.0 from
  stable)
  556d973f-unmodified-drivers-tolerate-IRQF_DISABLED-being-undefined.patch
* Fri Jun 26 2015 carnold@suse.com
- Update to Xen Version 4.5.1 FCS (fate#315675)
  xen-4.5.1-testing-src.tar.bz2
- Dropped patches now contained in tarball
  556c2cf2-x86-don-t-crash-mapping-a-page-using-EFI-rt-page-tables.patch
  556d9718-efi-fix-allocation-problems-if-ExitBootServices-fails.patch
  556eabf7-x86-apic-Disable-the-LAPIC-later-in-smp_send_stop.patch
  556eac15-x86-crash-don-t-use-set_fixmap-in-the-crash-path.patch
  55780aaa-efi-avoid-calling-boot-services-after-ExitBootServices.patch
  55780aff-x86-EFI-fix-EFI_MEMORY_WP-handling.patch
  55780b43-EFI-early-add-mapbs-to-map-EfiBootServices-Code-Data.patch
  55780b97-EFI-support-default-attributes-to-map-Runtime-service-areas.patch
  5513b458-allow-reboot-overrides-when-running-under-EFI.patch
  5513b4d1-dont-apply-reboot-quirks-if-reboot-set-by-user.patch
  5576f178-kexec-add-more-pages-to-v1-environment.patch
  5535f633-dont-leak-hypervisor-stack-to-toolstacks.patch
  CVE-2015-3456-xsa133-qemuu.patch
  CVE-2015-3456-xsa133-qemut.patch
  qemu-MSI-X-enable-maskall.patch
  qemu-MSI-X-latch-writes.patch
  x86-MSI-X-guest-mask.patch
* Thu Jun 25 2015 jfehlig@suse.com
- Replace 5124efbe-add-qxl-support.patch with the variant that
  finally made it upstream, 554cc211-libxl-add-qxl.patch
* Wed Jun 10 2015 carnold@suse.com
- bsc#931627 - VUL-0: CVE-2015-4105: XSA-130: xen: Guest triggerable
  qemu MSI-X pass-through error messages
  qemu-MSI-X-latch-writes.patch
- bsc#907514 - Bus fatal error & sles12 sudden reboot has been observed
- bsc#910258 - SLES12 Xen host crashes with FATAL NMI after shutdown
  of guest with VT-d NIC
- bsc#918984 - Bus fatal error & sles11-SP4 sudden reboot has been
  observed
- bsc#923967 - Partner-L3: Bus fatal error & sles11-SP3 sudden reboot
  has been observed
  x86-MSI-X-teardown.patch
  x86-MSI-X-enable.patch
  x86-MSI-X-guest-mask.patch
  x86-MSI-X-maskall.patch
  qemu-MSI-X-enable-maskall.patch
- Upstream patches from Jan
  55780aaa-efi-avoid-calling-boot-services-after-ExitBootServices.patch
  55780aff-x86-EFI-fix-EFI_MEMORY_WP-handling.patch
  55780b43-EFI-early-add-mapbs-to-map-EfiBootServices-Code-Data.patch
  55780b97-EFI-support-default-attributes-to-map-Runtime-service-areas.patch
  55780be1-x86-EFI-adjust-EFI_MEMORY_WP-handling-for-spec-version-2.5.patch
  55103616-vm-assist-prepare-for-discontiguous-used-bit-numbers.patch
  5548e95d-x86-allow-to-suppress-M2P-user-mode-exposure.patch
- Dropped the following patches now contained in the tarball
  xen-no-array-bounds.patch CVE-2015-4103-xsa128.patch
  CVE-2015-4104-xsa129.patch CVE-2015-4105-xsa130.patch
  CVE-2015-4106-xsa131-1.patch CVE-2015-4106-xsa131-2.patch
  CVE-2015-4106-xsa131-3.patch CVE-2015-4106-xsa131-4.patch
  CVE-2015-4106-xsa131-5.patch CVE-2015-4106-xsa131-6.patch
  CVE-2015-4106-xsa131-7.patch CVE-2015-4106-xsa131-8.patch
* Wed Jun  3 2015 carnold@suse.com
- Update to Xen 4.5.1 RC2
- bsc#931628 - VUL-0: CVE-2015-4106: XSA-131: xen: Unmediated PCI
  register access in qemu
  CVE-2015-4106-xsa131-1.patch
  CVE-2015-4106-xsa131-2.patch
  CVE-2015-4106-xsa131-3.patch
  CVE-2015-4106-xsa131-4.patch
  CVE-2015-4106-xsa131-5.patch
  CVE-2015-4106-xsa131-6.patch
  CVE-2015-4106-xsa131-7.patch
  CVE-2015-4106-xsa131-8.patch
  CVE-2015-4106-xsa131-9.patch
- bsc#931627 - VUL-0: CVE-2015-4105: XSA-130: xen: Guest triggerable
  qemu MSI-X pass-through error messages
  CVE-2015-4105-xsa130.patch
- bsc#931626 - VUL-0: CVE-2015-4104: XSA-129: xen: PCI MSI mask
  bits inadvertently exposed to guests
  CVE-2015-4104-xsa129.patch
- bsc#931625 - VUL-0: CVE-2015-4103: XSA-128: xen: Potential
  unintended writes to host MSI message data field via qemu
  CVE-2015-4103-xsa128.patch
- Upstream patches from Jan
  5548e903-domctl-don-t-truncate-XEN_DOMCTL_max_mem-requests.patch
  556c2cf2-x86-don-t-crash-mapping-a-page-using-EFI-rt-page-tables.patch
  556d9718-efi-fix-allocation-problems-if-ExitBootServices-fails.patch
  556d973f-unmodified-drivers-tolerate-IRQF_DISABLED-being-undefined.patch
  556eabf7-x86-apic-Disable-the-LAPIC-later-in-smp_send_stop.patch
  556eac15-x86-crash-don-t-use-set_fixmap-in-the-crash-path.patch
* Wed May 20 2015 ohering@suse.de
- Add DefaultDependencies=no to xen-dom0-modules.service because
  it has to run before proc-xen.mount
* Tue May 19 2015 carnold@suse.com
- Update to Xen 4.5.1 RC1
* Fri May 15 2015 ohering@suse.de
- Update blktap-no-uninit.patch to work with gcc-4.5
* Mon May 11 2015 carnold@suse.com
- bsc#927967 - VUL-0: CVE-2015-3340: xen: Information leak through
  XEN_DOMCTL_gettscinfo (XSA-132)
  5535f633-dont-leak-hypervisor-stack-to-toolstacks.patch
* Thu May  7 2015 carnold@suse.com
- bnc#929339 - VUL-0: CVE-2015-3456: qemu kvm xen: VENOM qemu
  floppy driver host code execution
  CVE-2015-3456-xsa133-qemuu.patch
  CVE-2015-3456-xsa133-qemut.patch
* Mon Apr 27 2015 carnold@suse.com
- bsc#928783 - Reboot failure; Request backport of upstream Xen
  patch to 4.5.0, or update pkgs to 4.5.1
  5513b458-allow-reboot-overrides-when-running-under-EFI.patch
  5513b4d1-dont-apply-reboot-quirks-if-reboot-set-by-user.patch
* Tue Apr 21 2015 ohering@suse.de
- bnc#927750 - Avoid errors reported by system-modules-load.service
* Wed Apr  8 2015 rguenther@suse.com
- Add xen-no-array-bounds.patch and blktap-no-uninit.patch to selectively
  turn errors back to warnings to fix build with GCC 5.
- Amend xen.stubdom.newlib.patch to pull in declaration of strcmp to
  avoid implicit-fortify-decl rpmlint error.
- Fix quoting of __SMBIOS_DATE__ in xen.build-compare.smbiosdate.patch.
* Fri Apr  3 2015 carnold@suse.com
- xentop: Fix memory leak on read failure
  551ac326-xentop-add-support-for-qdisk.patch
* Tue Mar 31 2015 carnold@suse.com
- Dropped xentop-add-support-for-qdisk.patch in favor of upstream
  version
  551ac326-xentop-add-support-for-qdisk.patch
* Mon Mar 16 2015 carnold@suse.com
- Enable spice support in qemu for x86_64
  5124efbe-add-qxl-support.patch
  qemu-xen-enable-spice-support.patch
* Thu Mar 12 2015 rguenther@suse.com
- Add xen-c99-fix.patch to remove pointless inline specifier on
  function declarations which break build with a C99 compiler which
  GCC 5 is by default. (bsc#921994)
- Add ipxe-no-error-logical-not-parentheses.patch to supply
  - Wno-logical-not-parentheses to the ipxe build to fix
  breakage with GCC 5. (bsc#921994)
* Wed Mar 11 2015 carnold@suse.com
- bnc#921842 - Xentop doesn't display disk statistics for VMs using
  qdisks
  xentop-add-support-for-qdisk.patch
* Tue Feb 24 2015 meissner@suse.com
- Disable the PIE enablement done for Factory, as the XEN code
  is not buildable with PIE and it does not make much sense
  to build the hypervisor code with it.
* Tue Feb 17 2015 carnold@suse.com
- bnc#918169 - XEN fixes required to work with Kernel 3.19.0
  xen.spec
* Tue Feb 10 2015 ohering@suse.de
- Package xen.changes because its referenced in xen.spec
* Wed Jan 28 2015 carnold@suse.com
- Update seabios to rel-1.7.5 which is the correct version for
  Xen 4.5
* Wed Jan 14 2015 carnold@suse.com
- Update to Xen 4.5.0 FCS
* Wed Jan 14 2015 ohering@suse.de
- Include systemd presets in 13.2 and older
* Mon Jan 12 2015 ohering@suse.de
- bnc#897352 - Enable xencommons/xendomains only during fresh install
- disable restart on upgrade because the toolstack is not restartable
* Tue Dec 16 2014 ohering@suse.de
- adjust seabios, vgabios, stubdom and hvmloader build to reduce
  build-compare noise
  xen.build-compare.mini-os.patch
  xen.build-compare.smbiosdate.patch
  xen.build-compare.ipxe.patch
  xen.build-compare.vgabios.patch
  xen.build-compare.seabios.patch
  xen.build-compare.man.patch
* Mon Dec 15 2014 carnold@suse.com
- Update to Xen 4.5.0 RC4
* Wed Dec 10 2014 ohering@suse.de
- Remove xend specific if-up scripts
  Recording bridge slaves is a generic task which should be handled
  by generic network code
* Tue Dec  9 2014 ohering@suse.de
- Use systemd features from upstream
  requires updated systemd-presets-branding package
* Thu Dec  4 2014 carnold@suse.com
- Update to Xen 4.5.0 RC3
* Thu Dec  4 2014 ohering@suse.de
- Set GIT, WGET and FTP to /bin/false
* Wed Dec  3 2014 ohering@suse.de
- Use new configure features instead of make variables
  xen.stubdom.newlib.patch
* Wed Nov 19 2014 ohering@suse.de
- adjust docs and xen build to reduce build-compare noise
  xen.build-compare.doc_html.patch
  xen.build-compare.xen_compile_h.patch
* Mon Nov 17 2014 ohering@suse.de
- Drop trailing B_CNT from XEN_EXTRAVERSION to reduce build-compare noise
* Tue Nov 11 2014 carnold@suse.com
- Update to Xen 4.5.0 RC2
* Thu Oct 23 2014 carnold@suse.com
- Update to Xen 4.5.0 RC1
  xen-4.5.0-testing-src.tar.bz2
- Remove all patches now contained in the new tarball
  xen-4.4.1-testing-src.tar.bz2
  5315a3bb-x86-don-t-propagate-acpi_skip_timer_override-do-Dom0.patch
  5315a43a-x86-ACPI-also-print-address-space-for-PM1x-fields.patch
  53299d8f-xenconsole-reset-tty-on-failure.patch
  53299d8f-xenconsole-tolerate-tty-errors.patch
  5346a7a0-x86-AMD-support-further-feature-masking-MSRs.patch
  53563ea4-x86-MSI-drop-workaround-for-insecure-Dom0-kernels.patch
  537c9c77-libxc-check-return-values-on-mmap-and-madvise.patch
  537cd0b0-hvmloader-also-cover-PCI-MMIO-ranges-above-4G-with-UC-MTRR-ranges.patch
  537cd0cc-hvmloader-PA-range-0xfc000000-0xffffffff-should-be-UC.patch
  539ebe62-x86-EFI-improve-boot-time-diagnostics.patch
  53aac342-x86-HVM-consolidate-and-sanitize-CR4-guest-reserved-bit-determination.patch
  53c9151b-Fix-xl-vncviewer-accesses-port-0-by-any-invalid-domid.patch
  53d124e7-fix-list_domain_details-check-config-data-length-0.patch
  53dba447-x86-ACPI-allow-CMOS-RTC-use-even-when-ACPI-says-there-is-none.patch
  53df727b-x86-HVM-extend-LAPIC-shortcuts-around-P2M-lookups.patch
  53e8be5f-x86-vHPET-use-rwlock-instead-of-simple-one.patch
  53f737b1-VMX-fix-DebugCtl-MSR-clearing.patch
  53f7386d-x86-irq-process-softirqs-in-irq-keyhandlers.patch
  53fcebab-xen-pass-kernel-initrd-to-qemu.patch
  53ff3659-x86-consolidate-boolean-inputs-in-hvm-and-p2m.patch
  53ff36ae-x86-hvm-treat-non-insn-fetch-NPF-also-as-read-violations.patch
  53ff36d5-x86-mem_event-deliver-gla-fault-EPT-violation-information.patch
  53ff3716-x86-ats-Disable-Address-Translation-Services-by-default.patch
  53ff3899-x86-NMI-allow-processing-unknown-NMIs-with-watchdog.patch
  54005472-EPT-utilize-GLA-GPA-translation-known-for-certain-faults.patch
  540effe6-evtchn-check-control-block-exists-when-using-FIFO-based-events.patch
  540f2624-x86-idle-add-barriers-to-CLFLUSH-workaround.patch
  541825dc-VMX-don-t-leave-x2APIC-MSR-intercepts-disabled.patch
  541ad385-x86-suppress-event-check-IPI-to-MWAITing-CPUs.patch
  541ad3ca-x86-HVM-batch-vCPU-wakeups.patch
  541ad81a-VT-d-suppress-UR-signaling-for-further-desktop-chipsets.patch
  54216833-x86-shadow-fix-race-when-sampling-dirty-vram-state.patch
  54216882-x86-emulate-check-cpl-for-all-privileged-instructions.patch
  542168ae-x86emul-only-emulate-swint-injection-for-real-mode.patch
  54228a37-x86-EFI-fix-freeing-of-uninitialized-pointer.patch
  5423e61c-x86emul-fix-SYSCALL-SYSENTER-SYSEXIT-emulation.patch
  5424057f-x86-HVM-fix-miscellaneous-aspects-of-x2APIC-emulation.patch
  542405b4-x86-HVM-fix-ID-handling-of-x2APIC-emulation.patch
  542bf997-x86-HVM-properly-bound-x2APIC-MSR-range.patch
  54325cc0-x86-MSI-fix-MSI-X-case-of-freeing-IRQ.patch
  54325d2f-x86-restore-reserving-of-IO-APIC-pages-in-XENMEM_machine_memory_map-output.patch
  54325d95-don-t-allow-Dom0-access-to-IOMMUs-MMIO-pages.patch
  54325ecc-AMD-guest_iommu-properly-disable-guest-iommu-support.patch
  54325f3c-x86-paging-make-log-dirty-operations-preemptible.patch
  54379e6d-x86-vlapic-don-t-silently-accept-bad-vectors.patch
  CVE-2013-4540-qemu.patch qemu-support-xen-hvm-direct-kernel-boot.patch
  qemu-xen-upstream-blkif-discard.patch change-vnc-passwd.patch
  libxc-pass-errno-to-callers-of-xc_domain_save.patch
  libxl.honor-more-top-level-vfb-options.patch
  libxl.add-option-for-discard-support-to-xl-disk-conf.patch
  libxl.introduce-an-option-to-disable-the-non-O_DIRECT-workaround.patch
  x86-dom-print.patch x86-extra-trap-info.patch tmp_build.patch
  xl-check-for-libvirt-managed-domain.patch disable-wget-check.patch
- Xend/xm is no longer supported and is not part of the upstream code. Remove
  all xend/xm specific patches, configs, and scripts
  xen-xmexample.patch bridge-opensuse.patch xmexample.disks xmclone.sh
  init.xend xend-relocation.sh xend.service xend-relocation-server.fw
  domUloader.py xmexample.domUloader xmexample.disks
  bridge-vlan.patch bridge-bonding.patch bridge-record-creation.patch
  network-nat-open-SuSEfirewall2-FORWARD.patch
  xend-set-migration-constraints-from-cmdline.patch
  xen.migrate.tools-xend_move_assert_to_exception_block.patch
  xend-pvscsi-recognize-also-SCSI-CDROM-devices.patch
  xend-config.patch xend-max-free-mem.patch xend-hvm-default-pae.patch
  xend-vif-route-ifup.patch xend-xenapi-console-protocol.patch xend-core-dump-loc.patch
  xend-xen-api-auth.patch xend-checkpoint-rename.patch xend-xm-save-check-file.patch
  xend-xm-create-xflag.patch xend-domu-usb-controller.patch xend-devid-or-name.patch
  xend-migration-domname-fix.patch xend-del_usb_xend_entry.patch xend-xen-domUloader.patch
  xend-multi-xvdp.patch xend-check_device_status.patch xend-change_home_server.patch
  xend-minimum-restart-time.patch xend-disable-internal-logrotate.patch xend-config-enable-dump-comment.patch
  xend-tools-watchdog-support.patch xend-console-port-restore.patch xend-vcpu-affinity-fix.patch
  xend-migration-bridge-check.patch xend-managed-pci-device.patch xend-hvm-firmware-passthrough.patch
  xend-cpuinfo-model-name.patch xend-xm-reboot-fix.patch xend-domain-lock.patch
  xend-domain-lock-sfex.patch xend-32on64-extra-mem.patch xend-hv_extid_compatibility.patch
  xend-xenpaging.autostart.patch xend-remove-xm-deprecation-warning.patch libxen_permissive.patch
  tmp-initscript-modprobe.patch init.xendomains xendomains.service
  xen-watchdog.service xen-updown.sh
* Thu Oct 16 2014 carnold@suse.com
- bnc#901317 - L3: increase limit domUloader to 32MB
  domUloader.py
* Tue Oct 14 2014 carnold@suse.com
- bnc#898772 - SLES 12 RC3 - XEN Host crashes when assigning non-VF
  device (SR-IOV) to guest
  54325cc0-x86-MSI-fix-MSI-X-case-of-freeing-IRQ.patch
- bnc#882089 - Windows 2012 R2 fails to boot up with greater than
  60 vcpus
  54325ecc-AMD-guest_iommu-properly-disable-guest-iommu-support.patch
- bnc#826717 - VUL-0: CVE-2013-3495: XSA-59: xen: Intel VT-d
  Interrupt Remapping engines can be evaded by native NMI interrupts
  541ad81a-VT-d-suppress-UR-signaling-for-further-desktop-chipsets.patch
- Upstream patches from Jan
  540effe6-evtchn-check-control-block-exists-when-using-FIFO-based-events.patch (Replaces xsa107.patch)
  54216833-x86-shadow-fix-race-when-sampling-dirty-vram-state.patch (Replaces xsa104.patch)
  54216882-x86-emulate-check-cpl-for-all-privileged-instructions.patch (Replaces xsa105.patch)
  542168ae-x86emul-only-emulate-swint-injection-for-real-mode.patch (Replaces xsa106.patch)
  54228a37-x86-EFI-fix-freeing-of-uninitialized-pointer.patch
  5423e61c-x86emul-fix-SYSCALL-SYSENTER-SYSEXIT-emulation.patch
  5424057f-x86-HVM-fix-miscellaneous-aspects-of-x2APIC-emulation.patch
  542405b4-x86-HVM-fix-ID-handling-of-x2APIC-emulation.patch
  542bf997-x86-HVM-properly-bound-x2APIC-MSR-range.patch (Replaces xsa108.patch)
  54325d2f-x86-restore-reserving-of-IO-APIC-pages-in-XENMEM_machine_memory_map-output.patch
  54325d95-don-t-allow-Dom0-access-to-IOMMUs-MMIO-pages.patch
  54325f3c-x86-paging-make-log-dirty-operations-preemptible.patch (Replaces xsa97.patch)
  54379e6d-x86-vlapic-don-t-silently-accept-bad-vectors.patch
* Sat Oct 11 2014 dmueller@suse.com
- restrict requires on grub2-x86_64-xen to x86_64 hosts
* Wed Oct  8 2014 jfehlig@suse.com
- bsc#900292 - xl: change default dump directory
  xl-coredump-file-location.patch
* Fri Oct  3 2014 mlatimer@suse.com
- Update xen2libvirt.py to better detect and handle file formats
* Tue Sep 30 2014 carnold@suse.com
- bnc#889526 - VUL-0: CVE-2014-5146, CVE-2014-5149: xen: XSA-97
  Long latency virtual-mmu operations are not preemptible
  xsa97.patch
- bnc#882089 - Windows 2012 R2 fails to boot up with greater than
  60 vcpus
  541ad385-x86-suppress-event-check-IPI-to-MWAITing-CPUs.patch
  541ad3ca-x86-HVM-batch-vCPU-wakeups.patch
- Upstream patches from Jan
  540f2624-x86-idle-add-barriers-to-CLFLUSH-workaround.patch
  541825dc-VMX-don-t-leave-x2APIC-MSR-intercepts-disabled.patch
* Tue Sep 30 2014 carnold@suse.com
- bnc#897657 - VUL-0: CVE-2014-7188: xen: XSA-108 Improper MSR
  range used for x2APIC emulation
  xsa108.patch
* Mon Sep 29 2014 carnold@suse.com
- bnc#897906 - libxc: check return values on mmap() and madvise()
  on xc_alloc_hypercall_buffer()
  537c9c77-libxc-check-return-values-on-mmap-and-madvise.patch
* Mon Sep 22 2014 carnold@suse.com
- bnc#897614 - Virtualization/xen: Bug `xen-tools` uninstallable;
  grub2-x86_64-xen dependency not available
  xen.spec
* Wed Sep 17 2014 jfehlig@suse.com
- More cleanup of README.SUSE
* Mon Sep 15 2014 cyliu@suse.com
- Update xen patch with upstream patch so that latest libvirt
  patch can work. (bnc#896044)
  + 53fcebab-xen-pass-kernel-initrd-to-qemu.patch
  - xen-pass-kernel-initrd-to-qemu.patch
* Wed Sep 10 2014 carnold@suse.com
- bnc#895804 - VUL-0: CVE-2014-6268: xen: XSA-107: Mishandling of
  uninitialised FIFO-based event channel control blocks
  xsa107.patch
- bnc#895802 - VUL-0: CVE-2014-7156: xen: XSA-106: Missing
  privilege level checks in x86 emulation of software interrupts
  xsa106.patch
- bnc#895799 - VUL-0: CVE-2014-7155: xen: XSA-105: Missing
  privilege level checks in x86 HLT, LGDT, LIDT, and LMSW emulation
  xsa105.patch
- bnc#895798 - VUL-0: CVE-2014-7154: xen: XSA-104: Race condition
  in HVMOP_track_dirty_vram
  xsa104.patch
* Thu Sep  4 2014 cyliu@suse.com
- bnc#882405 - Only one key-press event was generated while holding
  a key before key-release in pv guests through xl vncviewer
  tigervnc-long-press.patch
* Tue Sep  2 2014 carnold@suse.com
- Update to Xen Version 4.4.1 FCS
  xen-4.4.1-testing-src.tar.bz2
- Dropped patches now contained in tarball
  53d7b781-x86-cpu-undo-BIOS-CPUID-max_leaf-limit-earlier.patch
  53df71c7-lz4-check-for-underruns.patch
  53e47d6b-x86_emulate-properly-do-IP-updates-and-other-side-effects.patch
* Mon Sep  1 2014 carnold@suse.com
- bnc#882089 - Windows 2012 R2 fails to boot up with greater than
  60 vcpus
  53df727b-x86-HVM-extend-LAPIC-shortcuts-around-P2M-lookups.patch
  53e8be5f-x86-vHPET-use-rwlock-instead-of-simple-one.patch
  53ff3659-x86-consolidate-boolean-inputs-in-hvm-and-p2m.patch
  53ff36ae-x86-hvm-treat-non-insn-fetch-NPF-also-as-read-violations.patch
  53ff36d5-x86-mem_event-deliver-gla-fault-EPT-violation-information.patch
  54005472-EPT-utilize-GLA-GPA-translation-known-for-certain-faults.patch
- Upstream patches from Jan
  53f737b1-VMX-fix-DebugCtl-MSR-clearing.patch
  53f7386d-x86-irq-process-softirqs-in-irq-keyhandlers.patch
  53ff3716-x86-ats-Disable-Address-Translation-Services-by-default.patch
  53ff3899-x86-NMI-allow-processing-unknown-NMIs-with-watchdog.patch
* Fri Aug 29 2014 carnold@suse.com
- bnc#864801 - VUL-0: CVE-2013-4540: qemu: zaurus: buffer overrun
  on invalid state load
  CVE-2013-4540-qemu.patch
* Fri Aug 15 2014 carnold@suse.com
- Update README.SUSE with additional debug help
* Fri Aug  8 2014 carnold@suse.com
- bnc#883112 - Xen Panic during boot "System without CMOS RTC must
  be booted from EFI"
  53dba447-x86-ACPI-allow-CMOS-RTC-use-even-when-ACPI-says-there-is-none.patch
- Upstream patches from Jan
  53d7b781-x86-cpu-undo-BIOS-CPUID-max_leaf-limit-earlier.patch
  53df71c7-lz4-check-for-underruns.patch
  53df727b-x86-HVM-extend-LAPIC-shortcuts-around-P2M-lookups.patch
  53e47d6b-x86_emulate-properly-do-IP-updates-and-other-side-effects.patch
* Thu Aug  7 2014 carnold@suse.com
- Update to Xen Version 4.4.1-rc2
  xen-4.4.1-testing-src.tar.bz2
- Dropped the following upstream patches and xen-4.4.0-testing-src.tar.bz2
  537b5ede-move-domain-to-cpupool0-before-destroying-it.patch
  5327190a-x86-Intel-work-around-Xeon-7400-series-erratum-AAI65.patch
  534bdf47-x86-HAP-also-flush-TLB-when-altering-a-present-1G-or-intermediate-entry.patch
  535a354b-passthrough-allow-to-suppress-SERR-and-PERR-signaling.patch
  53636ebf-x86-fix-guest-CPUID-handling.patch
  5347b524-evtchn-eliminate-64k-ports-limitation.patch
  53a040c6-page-alloc-scrub-pages-used-by-hypervisor-upon-freeing.patch
  53a1990a-IOMMU-prevent-VT-d-device-IOTLB-operations-on-wrong-IOMMU.patch
  53732f4f-x86-MCE-bypass-uninitialized-vcpu-in-vMCE-injection.patch
  531dc0e2-xmalloc-handle-correctly-page-allocation-when-align-size.patch
  5331917d-x86-enforce-preemption-in-HVM_set_mem_access-p2m_set_mem_access.patch
  531d8e09-x86-HVM-fix-memory-type-merging-in-epte_get_entry_emt.patch
  538ee637-ACPI-Prevent-acpi_table_entries-from-falling-into-a-infinite-loop.patch
  535a34eb-VT-d-suppress-UR-signaling-for-server-chipsets.patch
  535e31bc-x86-HVM-correct-the-SMEP-logic-for-HVM_CR0_GUEST_RESERVED_BITS.patch
  53859956-timers-set-the-deadline-more-accurately.patch
  53636978-hvm_set_ioreq_page-releases-wrong-page-in-error-path.patch
  535a3516-VT-d-suppress-UR-signaling-for-desktop-chipsets.patch
  53cfdcc7-avoid-crash-when-doing-shutdown-with-active-cpupools.patch
  5383175e-VT-d-fix-mask-applied-to-DMIBAR-in-desktop-chipset-XSA-59-workaround.patch
  531d8e34-x86-HVM-consolidate-passthrough-handling-in-epte_get_entry_emt.patch
  532fff53-x86-fix-determination-of-bit-count-for-struct-domain-allocations.patch
  5357baff-x86-add-missing-break-in-dom0_pit_access.patch
  530c54c3-x86-mce-Reduce-boot-time-logspam.patch
  5383167d-ACPI-ERST-fix-table-mapping.patch
  5390927f-x86-fix-reboot-shutdown-with-running-HVM-guests.patch
  530b27fd-x86-MCE-Fix-race-condition-in-mctelem_reserve.patch
  53709b77-Nested-VMX-load-current_vmcs-only-when-it-exists.patch
  5396d818-avoid-crash-on-HVM-domain-destroy-with-PCI-passthrough.patch
  531d8fd0-kexec-identify-which-cpu-the-kexec-image-is-being-executed-on.patch
  5385956b-x86-don-t-use-VA-for-cache-flush-when-also-flushing-TLB.patch
  539ec004-x86-mce-don-t-spam-the-console-with-CPUx-Temperature-z.patch
  53909259-x86-domctl-two-functional-fixes-to-XEN_DOMCTL_-gs-etvcpuextstate.patch
  53859549-AMD-IOMMU-don-t-free-page-table-prematurely.patch
  533d413b-x86-mm-fix-checks-against-max_mapped_pfn.patch
  535fa503-x86-HVM-restrict-HVMOP_set_mem_type.patch
  53271880-VT-d-fix-RMRR-handling.patch
  5390917a-VT-d-honor-APEI-firmware-first-mode-in-XSA-59-workaround-code.patch
  538dcada-x86-HVM-eliminate-vulnerabilities-from-hvm_inject_msi.patch
  53455585-x86-AMD-feature-masking-is-unavailable-on-Fam11.patch
  537b5e50-VT-d-apply-quirks-at-device-setup-time-rather-than-only-at-boot.patch
  53a199d7-x86-EFI-allow-FPU-XMM-use-in-runtime-service-functions.patch
  53cfddaf-x86-mem_event-validate-the-response-vcpu_id-before-acting-on-it.patch
  53b16cd4-VT-d-ATS-correct-and-clean-up-dev_invalidate_iotlb.patch
  53cfdde4-x86-mem_event-prevent-underflow-of-vcpu-pause-counts.patch
  53356c1e-x86-HVM-correct-CPUID-leaf-80000008-handling.patch
  534bbd90-x86-nested-HAP-don-t-BUG-on-legitimate-error.patch
  530b28c5-x86-MSI-don-t-risk-division-by-zero.patch
  5396e805-x86-HVM-refine-SMEP-test-in-HVM_CR4_GUEST_RESERVED_BITS.patch
  5370e03b-pygrub-fix-error-handling-if-no-valid-partitions-are-found.patch
  5321b257-x86-make-hypercall-preemption-checks-consistent.patch
  5321b20b-common-make-hypercall-preemption-checks-consistent.patch
  538c338f-x86-amd_ucode-flip-revision-numbers-in-printk.patch
  537b5e79-VT-d-extend-error-report-masking-workaround-to-newer-chipsets.patch
  531d8db1-x86-hvm-refine-the-judgment-on-IDENT_PT-for-EMT.patch
  53b56de1-properly-reference-count-DOMCTL_-un-pausedomain-hypercalls.patch
  530b2880-Nested-VMX-update-nested-paging-mode-on-vmexit.patch
  533ad1ee-VMX-fix-PAT-value-seen-by-guest.patch
  53206661-pygrub-support-linux16-and-initrd16.patch
  5315a254-IOMMU-generalize-and-correct-softirq-processing.patch
* Fri Aug  1 2014 cyliu@suse.com
- bnc#820873 - The "long" option doesn't work with "xl list"
  53d124e7-fix-list_domain_details-check-config-data-length-0.patch
* Wed Jul 30 2014 carnold@suse.com
- bnc#888996 - Package 'xen-tool' contains 'SuSE' spelling in a
  filename and/or SPEC file
  Renamed README.SuSE -> README.SUSE
  Modified files: xen.spec, boot.local.xenU, init.pciback
  xend-config.patch, xend-vif-route-ifup.patch
* Tue Jul 29 2014 carnold@suse.com
- bnc#882673 - Dom0 memory should enforce a minimum memory size
  (e.g. dom0_mem=min:512M)
  xen.spec (Mike Latimer)
* Thu Jul 24 2014 carnold@suse.com
- Upstream patches from Jan
  5347b524-evtchn-eliminate-64k-ports-limitation.patch
  53aac342-x86-HVM-consolidate-and-sanitize-CR4-guest-reserved-bit-determination.patch
  53b16cd4-VT-d-ATS-correct-and-clean-up-dev_invalidate_iotlb.patch
  53b56de1-properly-reference-count-DOMCTL_-un-pausedomain-hypercalls.patch
  53cfdcc7-avoid-crash-when-doing-shutdown-with-active-cpupools.patch
  53cfddaf-x86-mem_event-validate-the-response-vcpu_id-before-acting-on-it.patch
  53cfdde4-x86-mem_event-prevent-underflow-of-vcpu-pause-counts.patch
* Sun Jul 20 2014 cyliu@suse.com
- bnc#886801 - xl vncviewer: The first domu can be accessed by any id
  53c9151b-Fix-xl-vncviewer-accesses-port-0-by-any-invalid-domid.patch
* Mon Jul 14 2014 carnold@suse.com
- Upstream pygrub bug fix
  5370e03b-pygrub-fix-error-handling-if-no-valid-partitions-are-found.patch
* Wed Jul  9 2014 carnold@suse.com
- Fix pygrub to handle old 32 bit VMs
  pygrub-boot-legacy-sles.patch (Mike Latimer)
* Mon Jul  7 2014 jfehlig@suse.com
- Remove xen-vmresync utility.  It is an old Platespin Orchestrate
  utility that should have never been included in the Xen package.
  Updated xen.spec
* Mon Jul  7 2014 jfehlig@suse.com
- Rework xen-destroy utility included in xen-utils
  bnc#885292 and bnc#886063
  Updated xen-utils-0.1.tar.bz2
* Mon Jul  7 2014 carnold@suse.com
- bnc#886063 - Xen monitor fails (xl list --long output different
  from xm list --long output)
- bnc#885292 - VirtualDomain: pid_status does not know how to check
  status on SLE12
  Re-enable building xen-utils for sle12 and include xen-list and
  xen-destroy in the xen-tools package for HA.
  xen.spec
* Fri Jun 27 2014 carnold@suse.com
- bnc#882127 - Xen kernel panics on booting SLES12 Beta 8
  53a199d7-x86-EFI-allow-FPU-XMM-use-in-runtime-service-functions.patch
- Upstream patches from Jan
  538c338f-x86-amd_ucode-flip-revision-numbers-in-printk.patch
  538ee637-ACPI-Prevent-acpi_table_entries-from-falling-into-a-infinite-loop.patch
  5390917a-VT-d-honor-APEI-firmware-first-mode-in-XSA-59-workaround-code.patch
  53909259-x86-domctl-two-functional-fixes-to-XEN_DOMCTL_-gs-etvcpuextstate.patch
  5390927f-x86-fix-reboot-shutdown-with-running-HVM-guests.patch
  5396d818-avoid-crash-on-HVM-domain-destroy-with-PCI-passthrough.patch
  5396e805-x86-HVM-refine-SMEP-test-in-HVM_CR4_GUEST_RESERVED_BITS.patch
  539ebe62-x86-EFI-improve-boot-time-diagnostics.patch
  539ec004-x86-mce-don-t-spam-the-console-with-CPUx-Temperature-z.patch
  53a040c6-page-alloc-scrub-pages-used-by-hypervisor-upon-freeing.patch (replaces xsa100.patch)
  53a1990a-IOMMU-prevent-VT-d-device-IOTLB-operations-on-wrong-IOMMU.patch
* Tue Jun 24 2014 jfehlig@suse.com
- Replace 'domUloader' with 'pygrub' when converting or importing
  Xen domains into libvirt with xen2libvirt.  domUloader is no
  longer provided in xen-tools.
  Modified: xen2libvirt.py
* Fri Jun 13 2014 cyliu@suse.com
- fate#310956: Support Direct Kernel Boot for FV guests
  patches would go to upstream:
  qemu side: qemu-support-xen-hvm-direct-kernel-boot.patch
  xen side: xen-pass-kernel-initrd-to-qemu.patch
* Fri Jun  6 2014 carnold@suse.com
- Modify how we check for libvirt managed domains
  xl-check-for-libvirt-managed-domain.patch
* Thu Jun  5 2014 carnold@suse.com
- bnc#880751 - VUL-0: xen: Hypervisor heap contents leaked to
  guests
  xsa100.patch
- bnc#878841 - VUL-0: XSA-96: Xen: Vulnerabilities in HVM MSI
  injection
  538dcada-x86-HVM-eliminate-vulnerabilities-from-hvm_inject_msi.patch
- Upstream patches from Jan
  537cd0b0-hvmloader-also-cover-PCI-MMIO-ranges-above-4G-with-UC-MTRR-ranges.patch
  537cd0cc-hvmloader-PA-range-0xfc000000-0xffffffff-should-be-UC.patch
  5383167d-ACPI-ERST-fix-table-mapping.patch
  5383175e-VT-d-fix-mask-applied-to-DMIBAR-in-desktop-chipset-XSA-59-workaround.patch
  53859549-AMD-IOMMU-don-t-free-page-table-prematurely.patch
  5385956b-x86-don-t-use-VA-for-cache-flush-when-also-flushing-TLB.patch
  53859956-timers-set-the-deadline-more-accurately.patch
* Tue May 27 2014 ohering@suse.de
- bnc#879425: handle cache=unsafe from libvirt to disable flush in qdisk
  libxl.add-option-to-disable-disk-cache-flushes-in-qdisk.patch
  qemu-xen-upstream-qdisk-cache-unsafe.patch
* Tue May 27 2014 ohering@suse.de
- libxl: introduce an option for disabling the non-O_DIRECT workaround
  recognize direct-io-safe in domU.cfg diskspec
  libxl.introduce-an-option-to-disable-the-non-O_DIRECT-workaround.patch
* Tue May 27 2014 ohering@suse.de
- fate#316071: add discard support for file backed storage (qdisk)
  update patch to allow more values in overloaded ->readwrite member
* Tue May 27 2014 carnold@suse.com
- bnc#826717 - VUL-0: CVE-2013-3495: XSA-59: xen: Intel VT-d
  Interrupt Remapping engines can be evaded by native NMI interrupts
  537b5e50-VT-d-apply-quirks-at-device-setup-time-rather-than-only-at-boot.patch
  537b5e79-VT-d-extend-error-report-masking-workaround-to-newer-chipsets.patch
- Upstream patches from Jan
  53709b77-Nested-VMX-load-current_vmcs-only-when-it-exists.patch
  53732f4f-x86-MCE-bypass-uninitialized-vcpu-in-vMCE-injection.patch
  537b5ede-move-domain-to-cpupool0-before-destroying-it.patch
* Tue May 20 2014 carnold@suse.com
- Update README.SuSE with information on the toolstack change
* Fri May 16 2014 ohering@suse.de
- fate#316071: add discard support for file backed storage (qdisk)
  update to recognize option discard/no-discard instead of discard=0,1
  to match upstream change
* Mon May 12 2014 ohering@suse.de
- fate#316613: Implement pvscsi in xl/libxl
  libxl.pvscsi.patch
* Fri May  9 2014 carnold@suse.com
- bnc#875668 - VUL-0: CVE-2014-3124: xen: XSA-92:
  HVMOP_set_mem_type allows invalid P2M entries to be created
  535fa503-x86-HVM-restrict-HVMOP_set_mem_type.patch (replaces xsa92.patch)
- bnc#826717 - VUL-0: CVE-2013-3495: XSA-59: xen: Intel VT-d
  Interrupt Remapping engines can be evaded by native NMI interrupts
  535a34eb-VT-d-suppress-UR-signaling-for-server-chipsets.patch
  535a3516-VT-d-suppress-UR-signaling-for-desktop-chipsets.patch
- Upstream patches from Jan
  535a354b-passthrough-allow-to-suppress-SERR-and-PERR-signaling.patch
  535e31bc-x86-HVM-correct-the-SMEP-logic-for-HVM_CR0_GUEST_RESERVED_BITS.patch
  53636978-hvm_set_ioreq_page-releases-wrong-page-in-error-path.patch
  53636ebf-x86-fix-guest-CPUID-handling.patch
* Tue May  6 2014 carnold@suse.com
- Fix pygrub to handle VM with no grub/menu.lst file.
- Don't use /var/run/xend/boot for temporary boot directory
  pygrub-boot-legacy-sles.patch
* Sat Apr 26 2014 carnold@suse.com
- When the xl command is used, check to see if the domain being
  modified is managed by libvirt and print warning if it is.
  xl-check-for-libvirt-managed-domain.patch
* Thu Apr 24 2014 carnold@suse.com
- Upstream patches from Jan
  53455585-x86-AMD-feature-masking-is-unavailable-on-Fam11.patch
  5346a7a0-x86-AMD-support-further-feature-masking-MSRs.patch
  534bbd90-x86-nested-HAP-don-t-BUG-on-legitimate-error.patch
  534bdf47-x86-HAP-also-flush-TLB-when-altering-a-present-1G-or-intermediate-entry.patch
  53563ea4-x86-MSI-drop-workaround-for-insecure-Dom0-kernels.patch
  5357baff-x86-add-missing-break-in-dom0_pit_access.patch
- XSA-92
  xsa92.patch
* Sat Apr 12 2014 mmarek@suse.cz
- Add # needssslcertforbuild to use the project's certificate when
  building in a home project. (bnc#872354)
* Wed Apr  9 2014 carnold@suse.com
- Upstream patches from Jan
  53356c1e-x86-HVM-correct-CPUID-leaf-80000008-handling.patch
  533ad1ee-VMX-fix-PAT-value-seen-by-guest.patch
  533d413b-x86-mm-fix-checks-against-max_mapped_pfn.patch
* Thu Apr  3 2014 carnold@suse.com
- bnc#862608 - SLES 11 SP3 vm-install should get RHEL 7 support
  when released
  53206661-pygrub-support-linux16-and-initrd16.patch
- Upstream bug fixes
  53299d8f-xenconsole-reset-tty-on-failure.patch
  53299d8f-xenconsole-tolerate-tty-errors.patch
* Thu Apr  3 2014 dmueller@suse.com
- fix build for armv7l and aarch64
* Thu Apr  3 2014 ohering@suse.de
- Remove compiletime strings from qemu-upstream
  qemu-xen-upstream-megasas-buildtime.patch
* Wed Apr  2 2014 carnold@suse.com
- bnc#871546 - KMPs are not signed in SUSE:SLE-12:GA?
  xen.spec
* Tue Apr  1 2014 carnold@suse.com
- Upstream patches from Jan
  532fff53-x86-fix-determination-of-bit-count-for-struct-domain-allocations.patch
  5331917d-x86-enforce-preemption-in-HVM_set_mem_access-p2m_set_mem_access.patch
- Drop xsa89.patch for upstream version (see bnc#867910, 5331917d-x86-enforce...)
* Fri Mar 28 2014 carnold@suse.com
- bnc#863821 - Xen unable to boot paravirtualized VMs installed
  with btrfs.  Add 'Requires: grub2-x86_64-xen' to xen-tools.
- Restore soft links for qemu-system-i386 and qemu-dm
- Cleanup inconsistency in which version of qemu-system-i386 is
  being used (Xen vs qemu-x86).  Use only Xen's version.
  xen.spec
* Thu Mar 27 2014 carnold@suse.com
- Add conditionals for SLE12 when defining xend and max_cpus
  xen.spec
* Wed Mar 19 2014 carnold@suse.com
- Upstream patches from Jan
  5321b20b-common-make-hypercall-preemption-checks-consistent.patch
  5321b257-x86-make-hypercall-preemption-checks-consistent.patch
  53271880-VT-d-fix-RMRR-handling.patch
  5327190a-x86-Intel-work-around-Xeon-7400-series-erratum-AAI65.patch
- Dropped the following as now part of 5321b257
  5310bac3-mm-ensure-useful-progress-in-decrease_reservation.patch
* Wed Mar 12 2014 carnold@suse.com
- bnc#867910 - VUL-0: EMBARGOED: xen: XSA-89: HVMOP_set_mem_access
  is not preemptible
  xsa89.patch
- Upstream patches from Jan
  530b27fd-x86-MCE-Fix-race-condition-in-mctelem_reserve.patch
  530b2880-Nested-VMX-update-nested-paging-mode-on-vmexit.patch
  530b28c5-x86-MSI-don-t-risk-division-by-zero.patch
  530c54c3-x86-mce-Reduce-boot-time-logspam.patch
  5310bac3-mm-ensure-useful-progress-in-decrease_reservation.patch
  5315a254-IOMMU-generalize-and-correct-softirq-processing.patch
  5315a3bb-x86-don-t-propagate-acpi_skip_timer_override-do-Dom0.patch
  5315a43a-x86-ACPI-also-print-address-space-for-PM1x-fields.patch
  531d8db1-x86-hvm-refine-the-judgment-on-IDENT_PT-for-EMT.patch
  531d8e09-x86-HVM-fix-memory-type-merging-in-epte_get_entry_emt.patch
  531d8e34-x86-HVM-consolidate-passthrough-handling-in-epte_get_entry_emt.patch
  531d8fd0-kexec-identify-which-cpu-the-kexec-image-is-being-executed-on.patch
  531dc0e2-xmalloc-handle-correctly-page-allocation-when-align-size.patch
* Tue Mar 11 2014 carnold@suse.com
- Add conversion tool for migrating xend/xm managed VMs to libvirt
  xen2libvirt.py (Jim Fehlig)
* Mon Mar 10 2014 carnold@suse.com
- Update to Xen 4.4.0 FCS
* Thu Mar  6 2014 mlatimer@suse.com
- bnc#865682 - Local attach support for PHY backends using scripts
  local_attach_support_for_phy.patch
* Tue Feb 25 2014 mlatimer@suse.com
- bnc#798770 - Improve multipath support for npiv devices
  block-npiv
  block-npiv-common.sh
* Wed Feb 19 2014 ohering@suse.de
- honor global keymap= option in libxl
  libxl.honor-more-top-level-vfb-options.patch
* Tue Feb 11 2014 carnold@suse.com
- Update to c/s 28381 to include libxl fork and event fixes for
  libvirt
  xen-4.4.0-testing-src.tar.bz2
* Tue Feb 11 2014 ohering@suse.de
- bnc#863297: xend/pvscsi: recognize also SCSI CDROM devices
  xend-pvscsi-recognize-also-SCSI-CDROM-devices.patch
* Tue Feb 11 2014 ohering@suse.de
- fate#316614: set migration constraints from cmdline
  fix xl migrate to print the actual error string
  libxc-pass-errno-to-callers-of-xc_domain_save.patch
* Mon Feb 10 2014 carnold@suse.com
- Include additional help docs for xl in xen-tools
- Apply all patches including those for unpackaged xend
  xen.spec
* Mon Feb 10 2014 ohering@suse.de
- fate#316614: set migration constraints from cmdline
  split existing changes into libxl and xend part
  added libxl.set-migration-constraints-from-cmdline.patch
  added xend-set-migration-constraints-from-cmdline.patch
  removed xen.migrate.tools_add_xm_migrate_--log_progress_option.patch
  removed xen.migrate.tools_set_number_of_dirty_pages_during_migration.patch
  removed xen.migrate.tools_set_migration_constraints_from_cmdline.patch
* Tue Feb  4 2014 carnold@suse.com
- Enable ix86 32bit build for xen-libs to be built to support
  xen-tools-domU on 32bit VMs and also vhostmd running in 32bit VMs
* Mon Feb  3 2014 carnold@suse.de
- Enable blktapctrl when qemu-traditional is required to satisfy
  build dependencies.  Remove binaries after build if xend is
  disabled
* Sun Feb  2 2014 ohering@suse.de
- update ifarch usage in xen.spec to cover also arm
- blktapctrl is used only by xend
- fix xend-tools-xend sub pkg handling
- default to gcc47 for sles11sp3 builds
- remove all latex packages from BuildRequires
- aarch64-rename-PSR_MODE_ELxx-to-match-linux-headers.patch
* Sun Feb  2 2014 ohering@suse.de
- add arch dependent install suffix for /boot/xen files
* Sat Feb  1 2014 ohering@suse.de
- Set max_cpus==4 for non-x86_64 builds
* Fri Jan 31 2014 carnold@suse.com
- Update to Xen 4.4.0 RC3 c/s 28321
* Thu Jan 30 2014 ohering@suse.de
- Add flex and bison to BuildRequires, needed by previous patch
* Thu Jan 30 2014 ohering@suse.de
- fate#316071: add discard support for file backed storage (qdisk)
  libxl.add-option-for-discard-support-to-xl-disk-conf.patch
* Mon Jan 27 2014 carnold@suse.com
- On platforms where xend is still supported don't output a
  deprecation warning when using xm.
  xend-remove-xm-deprecation-warning.patch
* Thu Jan 23 2014 carnold@suse.com
- Changed License to GPL-2.0 (from GPL-2.0+)
* Thu Jan 23 2014 carnold@suse.com
- Dropped xen-changeset.patch.  It is no longer needed.
* Sat Jan 18 2014 ohering@suse.de
- BuildRequire libfdt1-devel on ARM
* Fri Jan 17 2014 ohering@suse.de
- fate#311487: remove modprobe.conf files for autoloading of
  pv-on-hvm files.
  Rely on core kernel to skip initialization of emulated hardware
  Handle xen_emul_unplug= from xenlinux based core kernel-default
  xen_pvonhvm.xen_emul_unplug.patch
  Dropped xen_pvdrivers.conf
* Thu Jan 16 2014 carnold@suse.com
- Fix the spec file to build for old distros
  The xm/xend toolstack will continue to be contained in xen-tools
  for older openSUSE and sles distros but it will be contained in
  xend-tools for os13.x
* Wed Jan 15 2014 ohering@suse.de
- fate#316071: add discard support for file backed storage (qdisk)
  to qemu-upstream, enabled unconditionally
  qemu-xen-upstream-blkif-discard.patch
* Tue Jan 14 2014 carnold@suse.com
- Update to Xen 4.4.0 RC2 c/s 28287
* Thu Jan  9 2014 carnold@suse.com
- Restore 32bit ix86 support in spec file for kmps and domU tools
- Restore a few missing xend patches
  xend-config-enable-dump-comment.patch
  xend-tools-watchdog-support.patch
  xend-vif-route-ifup.patch
* Thu Jan  2 2014 carnold@suse.com
- fate#315692: XEN: Include Xen version 4.4 in SLES-12
  Update to Xen 4.4.0 RC1 c/s 28233
- Drop 32bit support from spec file
- Dropped numerous patches now included in the tarball
* Wed Jan  1 2014 coolo@suse.com
- gcc-32bit pulls in the right gcc bits, so better buildrequire that
* Tue Nov 26 2013 carnold@suse.com
- Upstream patches from Jan
  5281fad4-numa-sched-leave-node-affinity-alone-if-not-in-auto-mode.patch
  52820823-nested-SVM-adjust-guest-handling-of-structure-mappings.patch
  52820863-VMX-don-t-crash-processing-d-debug-key.patch
  5282492f-x86-eliminate-has_arch_mmios.patch
  52864df2-credit-Update-other-parameters-when-setting-tslice_ms.patch
  52864f30-fix-leaking-of-v-cpu_affinity_saved-on-domain-destruction.patch
  5289d225-nested-VMX-don-t-ignore-mapping-errors.patch
  528a0eb0-x86-consider-modules-when-cutting-off-memory.patch
  528f606c-x86-hvm-reset-TSC-to-0-after-domain-resume-from-S3.patch
  528f609c-x86-crash-disable-the-watchdog-NMIs-on-the-crashing-cpu.patch
  52932418-x86-xsave-fix-nonlazy-state-handling.patch
* Fri Nov 22 2013 carnold@suse.com
- bnc#851749 - Xen service file does not call xend properly
  xend.service
* Fri Nov 22 2013 adrian@suse.de
- Add missing requires to pciutils package for xend-tools
* Tue Nov 19 2013 carnold@suse.com
- bnc#851386 - VUL-0: xen: XSA-78: Insufficient TLB flushing in
  VT-d (iommu) code
  528a0e5b-TLB-flushing-in-dma_pte_clear_one.patch
* Tue Nov 19 2013 tbehrens@suse.com
- Make -devel package depend on libuuid-devel, since libxl.h
  includes uuid.h
* Mon Nov 11 2013 carnold@suse.com
- bnc#849667 - VUL-0: xen: XSA-74: Lock order reversal between
  page_alloc_lock and mm_rwlock
  CVE-2013-4553-xsa74.patch
- bnc#849665 - VUL-0: CVE-2013-4551: xen: XSA-75: Host crash due to
  guest VMX instruction execution
  52809208-nested-VMX-VMLANUCH-VMRESUME-emulation-must-check-permission-1st.patch
- bnc#849668 - VUL-0: xen: XSA-76: Hypercalls exposed to privilege
  rings 1 and 2 of HVM guests
  CVE-2013-4554-xsa76.patch
- Upstream patches from Jan
  52654798-x86-xsave-also-save-restore-XCR0-across-suspend-ACPI-S3.patch
  526e43d4-x86-refine-address-validity-checks-before-accessing-page-tables.patch
  526f786a-fix-locking-in-cpu_disable_scheduler.patch
  5277646c-x86-ACPI-x2APIC-guard-against-out-of-range-ACPI-or-APIC-IDs.patch
  5277a134-x86-make-sure-memory-block-is-RAM-before-passing-to-the-allocator.patch
  5278f7f9-x86-HVM-32-bit-IN-result-must-be-zero-extended-to-64-bits.patch
  527a0a05-call-sched_destroy_domain-before-cpupool_rm_domain.patch
  527cb7d2-x86-hvm-fix-restart-of-RTC-periodic-timer-with-vpt_align-1.patch
  527cb820-x86-EFI-make-trampoline-allocation-more-flexible.patch
  5280aae0-x86-idle-reduce-contention-on-ACPI-register-accesses.patch
* Mon Nov  4 2013 carnold@suse.com
- bnc#848657 - VUL-0: xen: CVE-2013-4494: XSA-73: Lock order
  reversal between page allocation and grant table locks
  5277639c-gnttab-correct-locking-order-reversal.patch
* Thu Oct 31 2013 carnold@suse.com
- Update to Xen 4.3.1
* Tue Oct 22 2013 carnold@suse.com
- domUloader can no longer be used with the xl toolstack to boot
  sles10. Patch pygrub to get the kernel and initrd from the image.
  pygrub-boot-legacy-sles.patch
* Mon Oct 21 2013 carnold@suse.com
- bnc#842515 - VUL-0: CVE-2013-4375: XSA-71: xen: qemu disk backend
  (qdisk) resource leak
  CVE-2013-4375-xsa71.patch
- bnc#845520 - VUL-0: CVE-2013-4416: xen: ocaml xenstored
  mishandles oversized message replies
  CVE-2013-4416-xsa72.patch
- Upstream patches from Jan
  52496bea-x86-properly-handle-hvm_copy_from_guest_-phys-virt-errors.patch (Replaces CVE-2013-4355-xsa63.patch)
  52496c11-x86-mm-shadow-Fix-initialization-of-PV-shadow-L4-tables.patch (Replaces CVE-2013-4356-xsa64.patch)
  52496c32-x86-properly-set-up-fbld-emulation-operand-address.patch (Replaces CVE-2013-4361-xsa66.patch)
  52497c6c-x86-don-t-blindly-create-L3-tables-for-the-direct-map.patch
  524e971b-x86-idle-Fix-get_cpu_idle_time-s-interaction-with-offline-pcpus.patch
  524e9762-x86-percpu-Force-INVALID_PERCPU_AREA-to-non-canonical.patch
  524e983e-Nested-VMX-check-VMX-capability-before-read-VMX-related-MSRs.patch
  524e98b1-Nested-VMX-fix-IA32_VMX_CR4_FIXED1-msr-emulation.patch
  524e9dc0-xsm-forbid-PV-guest-console-reads.patch
  5256a979-x86-check-segment-descriptor-read-result-in-64-bit-OUTS-emulation.patch
  5256be57-libxl-fix-vif-rate-parsing.patch
  5256be84-tools-ocaml-fix-erroneous-free-of-cpumap-in-stub_xc_vcpu_getaffinity.patch
  5256be92-libxl-fix-out-of-memory-error-handling-in-libxl_list_cpupool.patch
  5257a89a-x86-correct-LDT-checks.patch
  5257a8e7-x86-add-address-validity-check-to-guest_map_l1e.patch
  5257a944-x86-check-for-canonical-address-before-doing-page-walks.patch
  525b95f4-scheduler-adjust-internal-locking-interface.patch
  525b9617-sched-fix-race-between-sched_move_domain-and-vcpu_wake.patch
  525e69e8-credit-unpause-parked-vcpu-before-destroying-it.patch
  525faf5e-x86-print-relevant-tail-part-of-filename-for-warnings-and-crashes.patch
* Wed Oct  2 2013 jfehlig@suse.com
- Improvements to block-dmmd script
  bnc#828623
* Tue Oct  1 2013 carnold@suse.com
- bnc#840196 - L3: MTU size on Dom0 gets reset when booting DomU
  with e1000 device
  set-mtu-from-bridge-for-tap-interface.patch
* Mon Sep 30 2013 carnold@suse.com
- bnc#839596 - VUL-0: CVE-2013-1442: XSA-62: xen: Information leak
  on AVX and/or LWP capable CPUs
  5242a1b5-x86-xsave-initialize-extended-register-state-when-guests-enable-it.patch
- bnc#840592 - VUL-0: CVE-2013-4355: XSA-63: xen: Information leaks
  through I/O instruction emulation
  CVE-2013-4355-xsa63.patch
- bnc#840593 - VUL-0: CVE-2013-4356: XSA-64: xen: Memory accessible
  by 64-bit PV guests under live migration
  CVE-2013-4356-xsa64.patch
- bnc#841766 - VUL-1: CVE-2013-4361: XSA-66: xen: Information leak
  through fbld instruction emulation
  CVE-2013-4361-xsa66.patch
- bnc#833796 - L3: Xen: migration broken from xsave-capable to
  xsave-incapable host
  52205e27-x86-xsave-initialization-improvements.patch
  522dc0e6-x86-xsave-fix-migration-from-xsave-capable-to-xsave-incapable-host.patch
- bnc#839600 - [HP BCS SLES11 Bug]: In HP’s UEFI x86_64 platform and
  sles11sp3 with xen environment, xen hypervisor will panic on
  multiple blades nPar.
  523172d5-x86-fix-memory-cut-off-when-using-PFN-compression.patch
- bnc#833251 - [HP BCS SLES11 Bug]: In HP’s UEFI x86_64 platform
  and with xen environment, in booting stage ,xen hypervisor will
  panic.
  522d896b-x86-EFI-properly-handle-run-time-memory-regions-outside-the-1-1-map.patch
- bnc#834751 - [HP BCS SLES11 Bug]: In xen, “shutdown –y 0 –h”
  cannot power off system
  522d896b-x86-EFI-properly-handle-run-time-memory-regions-outside-the-1-1-map.patch
- Upstream patches from Jan
  520119fc-xen-conring-Write-to-console-ring-even-if-console-lock-is-busted.patch
  520a2705-watchdog-crash-Always-disable-watchdog-in-console_force_unlock.patch
  522d8a1f-x86-allow-guest-to-set-clear-MSI-X-mask-bit-try-2.patch
  522dc044-xmalloc-make-whole-pages-xfree-clear-the-order-field-ab-used-by-xmalloc.patch
  522f2f9f-Nested-VMX-Clear-bit-31-of-IA32_VMX_BASIC-MSR.patch
  522f37b2-sched-arinc653-check-for-guest-data-transfer-failures.patch
  5231e090-libxc-x86-fix-page-table-creation-for-huge-guests.patch
  5231f00c-cpufreq-missing-check-of-copy_from_guest.patch
  523304b6-x86-machine_restart-must-not-call-acpi_dmar_reinstate-twice.patch
  5239a064-x86-HVM-fix-failure-path-in-hvm_vcpu_initialise.patch
  5239a076-VMX-fix-failure-path-in-construct_vmcs.patch
  523c0ed4-x86-HVM-properly-handle-wide-MMIO.patch
  523c1758-sched_credit-filter-node-affinity-mask-against-online-cpus.patch
  523ff393-x86-HVM-linear-address-must-be-canonical-for-the-whole-accessed-range.patch
  523ff3e2-x86-HVM-refuse-doing-string-operations-in-certain-situations.patch
* Wed Sep 25 2013 ohering@suse.de
- Use upstream version of unplugging in PVonHVM guests
  add 523c1834-unmodified_drivers-enable-unplug-per-default.patch
  remove disable_emulated_device.patch
* Wed Sep 25 2013 ohering@suse.de
- fate#315714 - Support pvUSB in Xen HVM guests, add xen-usb.ko
* Mon Sep  9 2013 carnold@suse.com
- Upstream patches from Jan
  521c6d4a-x86-don-t-allow-Dom0-access-to-the-MSI-address-range.patch
  521c6d6c-x86-don-t-allow-Dom0-access-to-the-HT-address-range.patch
  521c6e23-x86-Intel-add-support-for-Haswell-CPU-models.patch
  521db25f-Fix-inactive-timer-list-corruption-on-second-S3-resume.patch
  521e1156-x86-AVX-instruction-emulation-fixes.patch
  521ef8d9-AMD-IOMMU-add-missing-checks.patch
  52205a7d-hvmloader-smbios-Correctly-count-the-number-of-tables-written.patch
  52205a90-public-hvm_xs_strings.h-Fix-ABI-regression-for-OEM-SMBios-strings.patch
  52205e27-x86-xsave-initialization-improvements.patch
  5226020f-xend-handle-extended-PCI-configuration-space-when-saving-state.patch
  52260214-xend-fix-file-descriptor-leak-in-pci-utilities.patch
  52285317-hvmloader-fix-SeaBIOS-interface.patch
* Tue Sep  3 2013 carnold@suse.com
- bnc#837585 - xen* pkg update DISables `xencommons` and
  `xendomains` systemd services
  xen.spec
* Fri Aug 30 2013 ohering@suse.de
- remove unneeded patch, autoload is handled by PCI device, without
  PCI device xen_platform_pci would not work anyway
  xen.sles11sp1.fate311487.xen_platform_pci.dmistring.patch
* Fri Aug 30 2013 ohering@suse.de
- Update our xen-3.0.4 version of unplug code in qemu-trad
  add comments about the usage of the code
  rename handler function
  reenable handlers for writing/reading from emulated PCI device
* Fri Aug 30 2013 ohering@suse.de
- Change unplugging of emulated devices in PVonHVM guests
  Since 3.0.4 xen-platform-pci.ko triggerd the unplug by writing
  to the PCI space of the emulated PCI device. 3.3 introduced an
  official unplug protocol. The option to unplug wit the official
  protocol is disabled per default.
  Remove our version and enable the unplug via official protocol
* Fri Aug 30 2013 carnold@suse.com
- Upstream patches from Jan
  51e517e6-AMD-IOMMU-allocate-IRTEs.patch
  51e5183f-AMD-IOMMU-untie-remap-and-vector-maps.patch
  51e63df6-VMX-fix-interaction-of-APIC-V-and-Viridian-emulation.patch
  52146070-ACPI-fix-acpi_os_map_memory.patch
  5214d26a-VT-d-warn-about-CFI-being-enabled-by-firmware.patch
  5215d094-Nested-VMX-Check-whether-interrupt-is-blocked-by-TPR.patch
  5215d0c5-Nested-VMX-Force-check-ISR-when-L2-is-running.patch
  5215d135-Nested-VMX-Clear-APIC-v-control-bit-in-vmcs02.patch
  5215d2d5-Nested-VMX-Update-APIC-v-RVI-SVI-when-vmexit-to-L1.patch
  5215d8b0-Correct-X2-APIC-HVM-emulation.patch
- Dropped 520d417d-xen-Add-stdbool.h-workaround-for-BSD.patch
* Mon Aug 26 2013 carnold@suse.com
- bnc#836239 - SLES 11 SP3 Xen security patch does not
  automatically update UEFI boot binary
  xen.spec
* Tue Aug 20 2013 carnold@suse.com
- Upstream patches from Jan
  51d5334e-x86-mm-Ensure-useful-progress-in-alloc_l2_table.patch
  51dd155c-adjust-x86-EFI-build.patch
  51e63d80-x86-cpuidle-Change-logging-for-unknown-APIC-IDs.patch
  51e6540d-x86-don-t-use-destroy_xen_mappings-for-vunmap.patch
  51e7963f-x86-time-Update-wallclock-in-shared-info-when-altering-domain-time-offset.patch
  51ffd577-fix-off-by-one-mistakes-in-vm_alloc.patch
  51ffd5fd-x86-refine-FPU-selector-handling-code-for-XSAVEOPT.patch
  520114bb-Nested-VMX-Flush-TLBs-and-Caches-if-paging-mode-changed.patch
  520a5504-VMX-add-boot-parameter-to-enable-disable-APIC-v-dynamically.patch
  520a24f6-x86-AMD-Fix-nested-svm-crash-due-to-assertion-in-__virt_to_maddr.patch
  520a2570-x86-AMD-Inject-GP-instead-of-UD-when-unable-to-map-vmcb.patch
  520b4b60-VT-d-protect-against-bogus-information-coming-from-BIOS.patch
  520b4bda-x86-MTRR-fix-range-check-in-mtrr_add_page.patch
  520cb8b6-x86-time-fix-check-for-negative-time-in-__update_vcpu_system_time.patch
  520d417d-xen-Add-stdbool.h-workaround-for-BSD.patch
* Fri Aug 16 2013 carnold@suse.com
- The xencommons.service file handles the starting of xenstored
  and xenconsoled.  Drop the following services files as
  unecessary. Update xendomains.service to reflect these changes.
  xenstored.service
  xenconsoled.service
  blktapctrl.service
* Fri Aug 16 2013 carnold@suse.com
- Add xencommons.service to xendomains.service 'After' tag
  xendomains.service
* Thu Aug 15 2013 carnold@suse.com
- Change the default bridge in xl.conf from xenbr0 to just br0
  xl-conf-default-bridge.patch
- Add network.target to xendomains.service 'After' tag
  xendomains.service
* Wed Jul 31 2013 carnold@suse.com
- Spec file cleanups
  xen.spec
- Renamed xend-sysconfig.patch to xencommons-sysconfig.patch
* Mon Jul 29 2013 carnold@suse.com
- Added support for systemd with the following service files
  xenstored.service
  blktapctrl.service
  xend.service
  xenconsoled.service
  xen-watchdog.service
  xendomains.service
  xencommons.service
* Fri Jul 12 2013 carnold@suse.com
- Upstream patches from Jan
  51d277a3-x86-don-t-pass-negative-time-to-gtime_to_gtsc-try-2.patch
  51d27807-iommu-amd-Fix-logic-for-clearing-the-IOMMU-interrupt-bits.patch
  51d27841-iommu-amd-Workaround-for-erratum-787.patch
  51daa074-Revert-hvmloader-always-include-HPET-table.patch
* Fri Jul 12 2013 carnold@suse.com
- Dropped deprecated or unnecessary patches
  pvdrv-import-shared-info.patch
  minios-fixups.patch
* Tue Jul  9 2013 carnold@suse.com
- Update to Xen 4.3.0 FCS
* Fri Jul  5 2013 agraf@suse.com
- Enable ARM targets for Xen
* Thu Jun 27 2013 carnold@suse.com
- Update to Xen 4.3.0-rc6
* Wed Jun 19 2013 carnold@suse.com
- Update to Xen 4.3.0-rc5
* Fri Jun 14 2013 carnold@suse.com
- Update to Xen 4.3.0-rc4
* Mon Jun 10 2013 carnold@suse.com
- Fix xen-utils compiler time warnings
  xen-utils-0.1.tar.bz2
* Fri Jun  7 2013 carnold@suse.com
- Enable building the KMPs
  xen.spec
* Wed Jun  5 2013 carnold@suse.com
- Update to Xen 4.3.0-rc3
* Fri May 31 2013 carnold@suse.com
- bnc#801663 - performance of mirror lvm unsuitable for production
  block-dmmd
* Thu May 30 2013 carnold@suse.com
- Update to Xen 4.3.0-rc2
* Wed May 15 2013 carnold@suse.com
- The xend toolstack is now deprecated and unsupported. Consolidate
  all xend and traditional qemu patches into one patch file.
  Rename '.diff' patches to '.patch' and reoder others.
  xend-traditional-qemu.patch
* Tue May 14 2013 carnold@suse.com
- Create a xend-tools package for the legacy xend toolstack and
  traditional qemu files.
* Mon May 13 2013 carnold@suse.com
- Update to Xen 4.3.0-rc1 c/s 27068
  Drop all upstream changeset patches now included in 4.3 tarball
- Removed the doc-pdf RPM as there are no more PDFs to include
  since the docs/xen-api sources were dropped.
* Tue May  7 2013 carnold@suse.com
- bnc#818183 - VUL-0: xen: CVE-2013-2007: XSA-51: qga set umask
  0077 when daemonizing
  CVE-2013-2007-xsa51-1.patch
  CVE-2013-2007-xsa51-2.patch
* Mon May  6 2013 ohering@suse.de
- add lndir to BuildRequires
* Mon May  6 2013 ohering@suse.de
- remove xen.migrate.tools_notify_restore_to_hangup_during_migration_--abort_if_busy.patch
  It changed migration protocol and upstream wants a different solution
* Sun May  5 2013 ohering@suse.de
- bnc#802221 - fix xenpaging
  readd xenpaging.qemu.flush-cache.patch
* Thu May  2 2013 carnold@suse.com
- bnc#808269 - Fully Virtualized Windows VM install is failed on
  Ivy Bridge platforms with Xen kernel
  26754-hvm-Improve-APIC-INIT-SIPI-emulation.patch
* Tue Apr 30 2013 carnold@suse.com
- Upstream patches from Jan
  26891-x86-S3-Fix-cpu-pool-scheduling-after-suspend-resume.patch
  26930-x86-EFI-fix-runtime-call-status-for-compat-mode-Dom0.patch
- Additional fix for bnc#816159
  CVE-2013-1918-xsa45-followup.patch
* Mon Apr 29 2013 cyliu@suse.com
- bnc#817068 - Xen guest with >1 sr-iov vf won't start
  xen-managed-pci-device.patch
* Mon Apr 29 2013 carnold@suse.com
- Update to Xen 4.2.2 c/s 26064
  The following recent security patches are included in the tarball
  CVE-2013-0151-xsa34.patch (bnc#797285)
  CVE-2012-6075-xsa41.patch (bnc#797523)
  CVE-2013-1917-xsa44.patch (bnc#813673)
  CVE-2013-1919-xsa46.patch (bnc#813675)
* Wed Apr 24 2013 carnold@suse.com
- Upstream patch from Jan
  26902-x86-EFI-pass-boot-services-variable-info-to-runtime-code.patch
* Fri Apr 19 2013 carnold@suse.com
- bnc#816159 - VUL-0: xen: CVE-2013-1918: XSA-45: Several long
  latency operations are not preemptible
  CVE-2013-1918-xsa45-1-vcpu-destroy-pagetables-preemptible.patch
  CVE-2013-1918-xsa45-2-new-guest-cr3-preemptible.patch
  CVE-2013-1918-xsa45-3-new-user-base-preemptible.patch
  CVE-2013-1918-xsa45-4-vcpu-reset-preemptible.patch
  CVE-2013-1918-xsa45-5-set-info-guest-preemptible.patch
  CVE-2013-1918-xsa45-6-unpin-preemptible.patch
  CVE-2013-1918-xsa45-7-mm-error-paths-preemptible.patch
- bnc#816163 - VUL-0: xen: CVE-2013-1952: XSA-49: VT-d interrupt
  remapping source validation flaw for bridges
  CVE-2013-1952-xsa49.patch
* Thu Apr 18 2013 cyliu@suse.com
- bnc#809662 - can't use pv-grub to start domU (pygrub does work)
  xen.spec
* Mon Apr 15 2013 carnold@suse.com
- bnc#814709 - Unable to create XEN virtual machines in SLED 11 SP2
  on Kyoto
  xend-cpuinfo-model-name.patch
* Mon Apr 15 2013 carnold@suse.com
- bnc#813673 - VUL-0: CVE-2013-1917: xen: Xen PV DoS vulnerability with
  SYSENTER
  CVE-2013-1917-xsa44.patch
- bnc#813675 - VUL-0: CVE-2013-1919: xen: Several access permission
  issues with IRQs for unprivileged guests
  CVE-2013-1919-xsa46.patch
- bnc#814059 - VUL-1: xen: qemu-nbd format-guessing due to missing
  format specification
  CVE-2013-1922-xsa48.patch
- Upstream patches from Jan
  26749-x86-reserve-pages-when-SandyBridge-integrated-graphics.patch
  26751-x86-EFI-permit-setting-variable-with-non-zero-attributes.patch
  26765-hvm-Clean-up-vlapic_reg_write-error-propagation.patch
  26770-x86-irq_move_cleanup_interrupt-must-ignore-legacy-vectors.patch
  26771-x86-S3-Restore-broken-vcpu-affinity-on-resume.patch
  26772-VMX-Always-disable-SMEP-when-guest-is-in-non-paging-mode.patch
  26773-x86-mm-shadow-spurious-warning-when-unmapping-xenheap-pages.patch
  26774-defer-event-channel-bucket-pointer-store-until-after-XSM-checks.patch
  26799-x86-don-t-pass-negative-time-to-gtime_to_gtsc.patch
* Thu Apr  4 2013 carnold@suse.com
- bnc#813156 - IndentationError in XendCheckpoint.py
  xend-domain-lock.patch
* Tue Apr  2 2013 ohering@suse.de
- bnc#797014 - no way to control live migrations
- bnc#803712 - after live migration rcu_sched_state detected stalls
  xen.migrate.tools-xend_move_assert_to_exception_block.patch
  xen.migrate.tools-libxc_print_stats_if_migration_is_aborted.patch
  xen.migrate.tools_set_number_of_dirty_pages_during_migration.patch
  xen.migrate.tools_notify_restore_to_hangup_during_migration_--abort_if_busy.patch
* Tue Mar 26 2013 carnold@suse.com
- bnc#811764 - XEN (hypervisor or kernel) has a problem with EFI
  variable services
  x86-EFI-set-variable-permit-attrs.patch
- Upstream patches from Jan
  26060-ACPI-ERST-table-size-checks.patch
  26692-x86-fully-protect-MSI-X-table-from-PV-guest-accesses.patch
  26702-powernow-add-fixups-for-AMD-P-state-figures.patch
  26704-x86-MCA-suppress-bank-clearing-for-certain-injected-events.patch (bnc#805579)
  26731-AMD-IOMMU-Process-softirqs-while-building-dom0-iommu-mappings.patch
  26733-VT-d-Enumerate-IOMMUs-when-listing-capabilities.patch
  26734-ACPI-ERST-Name-table-in-otherwise-opaque-error-messages.patch
  26736-ACPI-APEI-Unlock-apei_iomaps_lock-on-error-path.patch
  26737-ACPI-APEI-Add-apei_exec_run_optional.patch
  26742-IOMMU-properly-check-whether-interrupt-remapping-is-enabled.patch
  26743-VT-d-deal-with-5500-5520-X58-errata.patch (bnc#801910)
  26744-AMD-IOMMU-allow-disabling-only-interrupt-remapping.patch
* Thu Mar 14 2013 jfehlig@suse.com
- Load blktap module in xencommons init script.  blktap2 doesn't
  support qcow2, so blktap is needed to support domains with
  'tap:qcow2' disk configurations.
  modified tmp-initscript-modprobe.patch
* Thu Mar 14 2013 carnold@suse.com
- bnc#809203 - xen.efi isn't signed with SUSE Secure Boot key
  xen.spec
* Mon Mar 11 2013 jfehlig@suse.com
- Fix adding managed PCI device to an inactive domain
  modified xen-managed-pci-device.patch
* Mon Mar 11 2013 jfehlig@suse.com
- bnc#805094 - xen hot plug attach/detach fails
  modified blktap-pv-cdrom.patch
* Mon Mar 11 2013 jfehlig@suse.com
- bnc# 802690 - domain locking can prevent a live migration from
  completing
  modified xend-domain-lock.patch
* Fri Mar  8 2013 ohering@suse.de
- bnc#797014 - no way to control live migrations
  26675-tools-xentoollog_update_tty_detection_in_stdiostream_progress.patch
  xen.migrate.tools-xc_print_messages_from_xc_save_with_xc_report.patch
  xen.migrate.tools-xc_document_printf_calls_in_xc_restore.patch
  xen.migrate.tools-xc_rework_xc_save.cswitch_qemu_logdirty.patch
  xen.migrate.tools_set_migration_constraints_from_cmdline.patch
  xen.migrate.tools_add_xm_migrate_--log_progress_option.patch
* Thu Mar  7 2013 carnold@suse.com
- Upstream patches from Jan
  26585-x86-mm-Take-the-p2m-lock-even-in-shadow-mode.patch
  26595-x86-nhvm-properly-clean-up-after-failure-to-set-up-all-vCPU-s.patch
  26601-honor-ACPI-v4-FADT-flags.patch
  26656-x86-fix-null-pointer-dereference-in-intel_get_extended_msrs.patch
  26659-AMD-IOMMU-erratum-746-workaround.patch
  26660-x86-fix-CMCI-injection.patch
  26672-vmx-fix-handling-of-NMI-VMEXIT.patch
  26673-Avoid-stale-pointer-when-moving-domain-to-another-cpupool.patch
  26676-fix-compat-memory-exchange-op-splitting.patch
  26677-x86-make-certain-memory-sub-ops-return-valid-values.patch
  26678-SEDF-avoid-gathering-vCPU-s-on-pCPU0.patch
  26679-x86-defer-processing-events-on-the-NMI-exit-path.patch
  26683-credit1-Use-atomic-bit-operations-for-the-flags-structure.patch
  26689-fix-domain-unlocking-in-some-xsm-error-paths.patch
* Tue Mar  5 2013 carnold@suse.com
- fate#313584: pass bios information to XEN HVM guest
  xend-hvm-firmware-passthrough.patch
* Mon Mar  4 2013 ohering@suse.de
- bnc#806736: enabling xentrace crashes hypervisor
  26686-xentrace_fix_off-by-one_in_calculate_tbuf_size.patch
* Thu Feb 28 2013 ohering@suse.de
- update xenalyze to revision 149
  Make eip_list output more useful
  Use correct length when copying record into buffer
  decode PV_HYPERCALL_SUBCALL events
  decode PV_HYPERCALL_V2 records
  Analyze populate-on-demand reclamation patterns
  Handle 64-bit MMIO
  Also strip write bit when processing a generic event
  Make the warnigns in hvm_generic_postprocess more informative
  Don't warn about switching paging levels unless verbosity>=6
  Process NPFs as generic for summary purposes
  Add HVM_EVENT_VLAPIC
* Wed Feb 20 2013 jfehlig@suse.com
- Add upstream patch to fix vfb/vkb initialization in libxl
  26369-libxl-devid.patch
* Tue Feb 19 2013 carnold@suse.com
- fate##313584: pass bios information to XEN HVM guest
  26554-hvm-firmware-passthrough.patch
  26555-hvm-firmware-passthrough.patch
  26556-hvm-firmware-passthrough.patch
* Tue Feb 19 2013 carnold@suse.com
- Upstream patches from Jan
  26516-ACPI-parse-table-retval.patch (Replaces CVE-2013-0153-xsa36.patch)
  26517-AMD-IOMMU-clear-irtes.patch (Replaces CVE-2013-0153-xsa36.patch)
  26518-AMD-IOMMU-disable-if-SATA-combined-mode.patch (Replaces CVE-2013-0153-xsa36.patch)
  26519-AMD-IOMMU-perdev-intremap-default.patch (Replaces CVE-2013-0153-xsa36.patch)
  26526-pvdrv-no-devinit.patch
  26529-gcc48-build-fix.patch
  26531-AMD-IOMMU-IVHD-special-missing.patch (Replaces CVE-2013-0153-xsa36.patch)
  26532-AMD-IOMMU-phantom-MSI.patch
  26536-xenoprof-div-by-0.patch
  26576-x86-APICV-migration.patch
  26577-x86-APICV-x2APIC.patch
  26578-AMD-IOMMU-replace-BUG_ON.patch
* Mon Feb 18 2013 ohering@suse.de
- bnc#797014 - no way to control live migrations
  26547-tools-xc_fix_logic_error_in_stdiostream_progress.patch
  26548-tools-xc_handle_tty_output_differently_in_stdiostream_progress.patch
  26549-tools-xc_turn_XCFLAGS_*_into_shifts.patch
  26550-tools-xc_restore_logging_in_xc_save.patch
  26551-tools-xc_log_pid_in_xc_save-xc_restore_output.patch
* Mon Feb 11 2013 mmarek@suse.cz
- Set $BRP_PESIGN_FILES in the %%install section so that modules
  are signed in the buildservice (fate#314552).
* Mon Feb 11 2013 ohering@suse.de
- PVonHVM: __devinit was removed in linux-3.8
* Wed Feb  6 2013 jfehlig@suse.com
- Add 'managed' PCI passthrough support to xend, allowing support
  for the same through libvirt
  xen-managed-pci-device.patch
  FATE#313570
* Tue Feb  5 2013 carnold@suse.com
- Upstream patches from Jan
  26287-sched-credit-pick-idle.patch
  26340-VT-d-intremap-verify-legacy-bridge.patch (Replaces CVE-2012-5634-xsa33.patch)
  26370-libxc-x86-initial-mapping-fit.patch
  26395-x86-FPU-context-conditional.patch
  26404-x86-forward-both-NMI-kinds.patch
  26418-x86-trampoline-consider-multiboot.patch
  26427-x86-AMD-enable-WC+.patch
  26428-x86-HVM-RTC-update.patch
  26440-x86-forward-SERR.patch
  26443-ACPI-zap-DMAR.patch
  26444-x86-nHVM-no-self-enable.patch (Replaces CVE-2013-0152-xsa35.patch)
  26501-VMX-simplify-CR0-update.patch
  26502-VMX-disable-SMEP-when-not-paging.patch
* Fri Feb  1 2013 carnold@suse.com
- bnc#800275 - VUL-0: XSA-36: CVE-2013-0153: xen: interrupt remap
  entries shared and old ones not cleared on AMD IOMMUs
  CVE-2013-0153-xsa36.patch
* Wed Jan 30 2013 mmarek@suse.cz
- Add # needssslcertforbuild to the specfile, to make the UEFI
  signing certificate available during build (fate#314511, fate#314552).
* Fri Jan 25 2013 jfehlig@suse.com
- bnc#798188 - Add $network to xend initscript dependencies
* Thu Jan 24 2013 jfehlig@suse.com
- Add upstream patches to fix libxl bugs.  These patches have
  already been posted for inclusion in xen-4.2-testing.
  25912-partial-libxl.patch
  26372-tools-paths.patch
  26468-libxl-race.patch
  26469-libxl-race.patch
* Tue Jan 22 2013 carnold@novell.com
- bnc#797285 - VUL-0: Xen: XSA-34 (CVE-2013-0151) - nested
  virtualization on 32-bit exposes host crash
  CVE-2013-0151-xsa34.patch
- bnc#797287 - VUL-0: Xen: XSA-35 (CVE-2013-0152) - Nested HVM
  exposes host to being driven out of memory by guest
  CVE-2013-0152-xsa35.patch
* Thu Jan 17 2013 carnold@novell.com
- bnc#793717 - NetWare will not boot on Xen 4.2
  xnloader.py
  domUloader.py
  pygrub-netware-xnloader.patch
  Removed reverse-24757-use-grant-references.patch
* Wed Jan 16 2013 carnold@novell.com
- bnc#797523 - VUL-1: CVE-2012-6075: qemu / kvm-qemu: e1000
  overflows under some conditions
  CVE-2012-6075-xsa41.patch
* Tue Jan 15 2013 carnold@novell.com
- Mask the floating point exceptions for guests like NetWare on
  machines that support XSAVE.
  x86-fpu-context-conditional.patch
* Mon Jan 14 2013 carnold@novell.com
- fate##313584: pass bios information to XEN HVM guest
  26341-hvm-firmware-passthrough.patch
  26342-hvm-firmware-passthrough.patch
  26343-hvm-firmware-passthrough.patch
  26344-hvm-firmware-passthrough.patch
* Tue Jan  8 2013 carnold@novell.com
- bnc#787169 - L3: Marvell 88SE9125 disk controller not detecting
  disk in Xen kernel
  26133-IOMMU-defer-BM-disable.patch
  26324-IOMMU-assign-params.patch
  26325-IOMMU-add-remove-params.patch
  26326-VT-d-context-map-params.patch
  26327-AMD-IOMMU-flush-params.patch
  26328-IOMMU-pdev-type.patch
  26329-IOMMU-phantom-dev.patch
  26330-VT-d-phantom-MSI.patch
  26331-IOMMU-phantom-dev-quirk.patch
- Upstream patches from Jan
  26294-x86-AMD-Fam15-way-access-filter.patch
  26320-IOMMU-domctl-assign-seg.patch
  26332-x86-compat-show-guest-stack-mfn.patch
  26333-x86-get_page_type-assert.patch
* Mon Dec 17 2012 carnold@novell.com
- bnc#794316 - VUL-0: CVE-2012-5634: xen: VT-d interrupt remapping
  source validation flaw (XSA-33)
  CVE-2012-5634-xsa33.patch
* Mon Dec 17 2012 carnold@novell.com
- Update to Xen 4.2.1 c/s 25952
* Tue Dec 11 2012 carnold@novell.com
- Upstream patches from Jan
  26195-x86-compat-atp-gmfn-range-cont.patch
  26196-ACPI-set-PDC-bits-rc.patch
  26200-IOMMU-debug-verbose.patch
  26203-x86-HAP-dirty-vram-leak.patch
  26229-gnttab-version-switch.patch (Replaces CVE-2012-5510-xsa26.patch)
  26230-x86-HVM-limit-batches.patch (Replaces CVE-2012-5511-xsa27.patch)
  26231-memory-exchange-checks.patch (Replaces CVE-2012-5513-xsa29.patch)
  26232-x86-mark-PoD-error-path.patch (Replaces CVE-2012-5514-xsa30.patch)
  26233-memop-order-checks.patch (Replaces CVE-2012-5515-xsa31.patch)
  26234-x86-page-from-gfn-pv.patch (Replaces CVE-2012-5525-xsa32.patch)
  26235-IOMMU-ATS-max-queue-depth.patch
  26252-VMX-nested-rflags.patch
  26253-VMX-nested-rdtsc.patch
  26254-VMX-nested-dr.patch
  26255-VMX-nested-ia32e-mode.patch
  26258-VMX-nested-intr-delivery.patch
  26260-x86-mmuext-errors.patch
  26262-x86-EFI-secure-shim.patch
  26266-sched-ratelimit-check.patch
  26272-x86-EFI-makefile-cflags-filter.patch
* Mon Dec 10 2012 carnold@novell.com
- bnc#757525 - domain destroyed on live migration with missing vif
  on target machine
  xen-migration-bridge-check.patch
* Thu Dec  6 2012 carnold@novell.com
- NetWare will not boot or install on Xen 4.2
  reverse-24757-use-grant-references.patch
* Fri Nov 30 2012 cyliu@suse.com
- fate#313222 - xenstore-chmod should support 256 permissions
  26189-xenstore-chmod.patch
* Tue Nov 27 2012 carnold@novell.com
- bnc#789945 - VUL-0: CVE-2012-5510: xen: Grant table version
  switch list corruption vulnerability (XSA-26)
  CVE-2012-5510-xsa26.patch
- bnc#789944 - VUL-0: CVE-2012-5511: xen: Several HVM operations do
  not validate the range of their inputs (XSA-27)
  CVE-2012-5511-xsa27.patch
- bnc#789951 - VUL-0: CVE-2012-5513: xen: XENMEM_exchange may
  overwrite hypervisor memory (XSA-29)
  CVE-2012-5513-xsa29.patch
- bnc#789948 - VUL-0: CVE-2012-5514: xen: Missing unlock in
  guest_physmap_mark_populate_on_demand() (XSA-30)
  CVE-2012-5514-xsa30.patch
- bnc#789950 - VUL-0: CVE-2012-5515: xen: Several memory hypercall
  operations allow invalid extent order values (XSA-31)
  CVE-2012-5515-xsa31.patch
- bnc#789952 - VUL-0: CVE-2012-5525: xen: Several hypercalls do not
  validate input GFNs (XSA-32)
  CVE-2012-5525-xsa32.patch
- Upstream patches from Jan
  26129-ACPI-BGRT-invalidate.patch
  26132-tmem-save-NULL-check.patch
  26134-x86-shadow-invlpg-check.patch
  26139-cpumap-masking.patch
  26148-vcpu-timer-overflow.patch (Replaces CVE-2012-4535-xsa20.patch)
  26149-x86-p2m-physmap-error-path.patch (Replaces CVE-2012-4537-xsa22.patch)
  26150-x86-shadow-unhook-toplevel-check.patch (Replaces CVE-2012-4538-xsa23.patch)
  26151-gnttab-compat-get-status-frames.patch (Replaces CVE-2012-4539-xsa24.patch)
  26179-PCI-find-next-cap.patch
  26183-x86-HPET-masking.patch
  26188-x86-time-scale-asm.patch
* Wed Nov 21 2012 ohering@suse.de
- remove obsolete pv-driver-build.patch to fix build
* Sat Nov 17 2012 aj@suse.de
- Fix build with glibc 2.17: add patch xen-glibc217.patch, fix
  configure for librt.
* Tue Nov 13 2012 jfehlig@suse.com
- bnc#777628 - guest "disappears" after live migration
  Updated block-dmmd script
* Fri Nov  9 2012 carnold@novell.com
- Fix exception in balloon.py and osdep.py
  xen-max-free-mem.diff
* Tue Nov  6 2012 carnold@novell.com
- fate#311966: Fix XEN VNC implementation to correctly map keyboard
  layouts
  VNC-Support-for-ExtendedKeyEvent-client-message.patch
* Tue Oct 30 2012 ohering@suse.de
- fate#310510 - fix xenpaging
  restore changes to integrate paging into xm/xend
  xenpaging.autostart.patch
  xenpaging.doc.patch
* Mon Oct 29 2012 carnold@novell.com
- bnc#787163 - VUL-0: CVE-2012-4544: xen: Domain builder Out-of-
  memory due to malicious kernel/ramdisk (XSA 25)
  CVE-2012-4544-xsa25.patch
- bnc#779212 - VUL-0: CVE-2012-4411: XEN / qemu: guest
  administrator can access qemu monitor console (XSA-19)
  CVE-2012-4411-xsa19.patch
* Thu Oct 25 2012 carnold@novell.com
- bnc#786516 - VUL-0: CVE-2012-4535: xen: Timer overflow DoS
  vulnerability
  CVE-2012-4535-xsa20.patch
- bnc#786518 - VUL-0: CVE-2012-4536: xen: pirq range check DoS
  vulnerability
  CVE-2012-4536-xsa21.patch
- bnc#786517 - VUL-0: CVE-2012-4537: xen: Memory mapping failure
  DoS vulnerability
  CVE-2012-4537-xsa22.patch
- bnc#786519 - VUL-0: CVE-2012-4538: xen: Unhooking empty PAE
  entries DoS vulnerability
  CVE-2012-4538-xsa23.patch
- bnc#786520 - VUL-0: CVE-2012-4539: xen: Grant table hypercall
  infinite loop DoS vulnerability
  CVE-2012-4539-xsa24.patch
- bnc#784087 - L3: Xen BUG at io_apic.c:129
  26102-x86-IOAPIC-legacy-not-first.patch
* Wed Oct 24 2012 carnold@novell.com
- Upstream patches from Jan
  25920-x86-APICV-enable.patch
  25921-x86-APICV-delivery.patch
  25922-x86-APICV-x2APIC.patch
  25957-x86-TSC-adjust-HVM.patch
  25958-x86-TSC-adjust-sr.patch
  25959-x86-TSC-adjust-expose.patch
  25975-x86-IvyBridge.patch
  25984-SVM-nested-paging-mode.patch
  26054-x86-AMD-perf-ctr-init.patch
  26055-x86-oprof-hvm-mode.patch
  26056-page-alloc-flush-filter.patch
  26061-x86-oprof-counter-range.patch
  26062-ACPI-ERST-move-data.patch
  26063-x86-HPET-affinity-lock.patch
  26095-SVM-nested-leak.patch
  26096-SVM-nested-vmexit-emul.patch
  26098-perfc-build.patch
* Mon Oct 22 2012 ohering@suse.de
- handle possible asprintf failures in log-guest-console.patch
* Mon Oct 22 2012 ohering@suse.de
- bnc#694863 - kexec fails in xen
  26093-hvm_handle_PoD_and_grant_pages_in_HVMOP_get_mem_type.patch
* Thu Oct 18 2012 carnold@novell.com
- fate#312709: Pygrub needs to know which entry to select
  26114-pygrub-list-entries.patch
* Thu Oct 18 2012 ohering@suse.de
- merge changes fron xen-unstable, obsolete our changes
  26077-stubdom_fix_compile_errors_in_grub.patch
  26078-hotplug-Linux_remove_hotplug_support_rely_on_udev_instead.patch
  26079-hotplug-Linux_close_lockfd_after_lock_attempt.patch
  26081-stubdom_fix_rpmlint_warning_spurious-executable-perm.patch
  26082-blktap2-libvhd_fix_rpmlint_warning_spurious-executable-perm.patch
  26083-blktap_fix_rpmlint_warning_spurious-executable-perm.patch
  26084-hotplug_install_hotplugpath.sh_as_data_file.patch
  26085-stubdom_install_stubdompath.sh_as_data_file.patch
  26086-hotplug-Linux_correct_sysconfig_tag_in_xendomains.patch
  26087-hotplug-Linux_install_sysconfig_files_as_data_files.patch
  26088-tools_xend_fix_wrong_condition_check_for_xml_file.patch
* Tue Oct 16 2012 carnold@novell.com
- fate#311966: Fix XEN VNC implementation to correctly map keyboard
  layouts
  VNC-Support-for-ExtendedKeyEvent-client-message.patch
* Mon Oct 15 2012 ohering@suse.de
- workaround bash bug in locking.sh:claim_lock, close fd
* Sat Oct 13 2012 ohering@suse.de
- fix incorrect self-provides/obsoletes of xen-tools-ioemu
* Tue Oct  9 2012 carnold@novell.com
- bnc#783847 - Virtualization/xen: Bug Xen 4.2 'xendomins' init
  script incorrectly Requires 'xend' service when using 'xl'
  toolstack
  init.xendomains
* Mon Oct  8 2012 carnold@novell.com
- bnc#782835 - Xen HVM Guest fails (errors) to launch on Opensuse
  12.2 + Xen 4.2 + 'xl' toolstack
  xen-pygrub-grub-args.patch
* Mon Oct  8 2012 ohering@suse.de
- backport parallel build support for stubdom
- rename 5 patches which were merged upstream
* Fri Oct  5 2012 ohering@suse.de
- remove more obsolete changes:
  CFLAGS passing to qemu-traditional, PYTHON_PREFIX_ARG handling
  and pygrub installation
* Fri Oct  5 2012 ohering@suse.de
- update blktap-pv-cdrom.patch
  handle allocation errors in asprintf to fix compile errors
  handle value returned from xs_read properly
  remove casts from void pointers
* Fri Oct  5 2012 ohering@suse.de
- update xenalyze to revision 138
  Fix dump time calculation overflow
  move struct record_info into a header
  correctly display of count of HW events
  update trace.h to match xen-unstable
  Remove vestigal HW_IRQ trace records
  Remove decode of PV_UPDATE_VA_MAPPING
  automatically generate dependencies
  Get rid of redundant hvm dump_header
  Introduce more efficient read mechanism
  Eliminate unnecessary cycles_to_time calculation
  Rework math to remove two 64-bit divisions
  Enable -O2 optimization level
  Remove --dump-cooked
  Remove spurious dump_header construction
  Improve record-sorting algorithm
  Use long to cast into and out of pointers
  Make max_active_pcpu calculation smarter
  Optimize pcpu_string
  Enable more cr3 output
  Sort cr3 enumerated values by start time
  Add option to skip vga range in MMIO enumeration
  Handle MMIO records from different vmexits
  Relocate pio and mmio enumaration structs to their own sub-struct
  Handle new hvm_event traces
  Introduce generic summary functionality
  Function-ize setting of h->post_process
  Reorganize cr trace handling
  Allow several summary handlers to register on a single vmexit
  Get rid of all tabs in xenalyze.c
  Handle new IRQ tracing
  Decrease verbosity
  Print exit reason number if no string is available
  Fix minor summary issue
  Add string for TPR_BELOW_THRESHOLD
  Raise MAX_CPUS to 256 cpus.
  Add --report-pcpu option to report physical cpu utilization.
  increase MAX_CPUS
  Handle RUNSTATE_INIT in domain_runstate calculation
* Fri Oct  5 2012 ohering@suse.de
- update RPM_OPT_FLAGS handling in spec file
  pass EXTRA_CFLAGS via environment
* Fri Oct  5 2012 ohering@suse.de
- remove obsolete xencommons-proc-xen.patch
* Mon Oct  1 2012 carnold@novell.com
- Upstream patches from Jan
  25927-x86-domctl-ioport-mapping-range.patch
  25929-tmem-restore-pool-version.patch
  25931-x86-domctl-iomem-mapping-checks.patch
  25940-x86-S3-flush-cache.patch
  25952-x86-MMIO-remap-permissions.patch
  25961-x86-HPET-interrupts.patch
  25962-x86-assign-irq-vector-old.patch
  25965-x86-ucode-Intel-resume.patch
* Tue Sep 25 2012 ohering@suse.de
- pygrub: always append --args
  25941-pygrub_always_append_--args.patch
* Mon Sep 24 2012 ohering@suse.de
- use BuildRequires: gcc46 only in sles11sp2 or 12.1 to fix build
  in 11.4
* Wed Sep 19 2012 carnold@novell.com
- Upstream patches from Jan
  25833-32on64-bogus-pt_base-adjust.patch
  25835-adjust-rcu-lock-domain.patch
  25836-VT-d-S3-MSI-resume.patch
  25850-tmem-xsa-15-1.patch
  25851-tmem-xsa-15-2.patch
  25852-tmem-xsa-15-3.patch
  25853-tmem-xsa-15-4.patch
  25854-tmem-xsa-15-5.patch
  25855-tmem-xsa-15-6.patch
  25856-tmem-xsa-15-7.patch
  25857-tmem-xsa-15-8.patch
  25858-tmem-xsa-15-9.patch
  25859-tmem-missing-break.patch
  25860-tmem-cleanup.patch
  25861-x86-early-fixmap.patch
  25862-sercon-non-com.patch
  25863-sercon-ehci-dbgp.patch
  25864-sercon-unused.patch
  25866-sercon-ns16550-pci-irq.patch
  25867-sercon-ns16550-parse.patch
  25874-x86-EFI-chain-cfg.patch
  25909-xenpm-consistent.patch
* Tue Sep 18 2012 carnold@novell.com
- Fixed the 32bit build.
* Mon Sep 17 2012 carnold@novell.com
- Update to Xen 4.2.0 FCS c/s 25844
* Fri Sep  7 2012 ohering@suse.de
- unmodified_drivers: handle IRQF_SAMPLE_RANDOM, it was removed
  in 3.6-rc1
* Wed Sep  5 2012 jfehlig@suse.com
- bnc#778105 - first XEN-PV VM fails to spawn
  xend: Increase wait time for disk to appear in host bootloader
  Modified existing xen-domUloader.diff
* Thu Aug 30 2012 carnold@novell.com
- Disable the snapshot patches. Snapshot only supported the qcow2
  image format which was poorly implemented qemu 0.10.2. Snapshot
  support may be restored in the future when the newer upstream
  qemu is used by Xen.
* Tue Aug 28 2012 ohering@suse.de
- bnc#776995 - attaching scsi control luns with pvscsi
  - xend/pvscsi: fix passing of SCSI control LUNs
  xen-bug776995-pvscsi-no-devname.patch
  - xend/pvscsi: fix usage of persistant device names for SCSI devices
  xen-bug776995-pvscsi-persistent-names.patch
  - xend/pvscsi: update sysfs parser for Linux 3.0
  xen-bug776995-pvscsi-sysfs-parser.patch
* Thu Aug 23 2012 carnold@novell.com
- Update to Xen 4.2.0 RC3+ c/s 25779
* Tue Aug 21 2012 carnold@novell.com
- Update to Xen 4.2.0 RC2+ c/s 25765
* Mon Aug 20 2012 ohering@suse.de
-bnc#766284 - compiled-in ata_piix driver issues with PVonHVM guests
  Update xen_pvdrivers.conf to match not only libata but also ata_piix
  This avoids IO errors in the piix driver caused by unplugged hardware
* Fri Aug 10 2012 carnold@novell.com
- Update to Xen 4.1.3 c/s 23336
* Mon Jul 30 2012 carnold@novell.com
- Upstream or pending upstream patches from Jan
  25587-fix-off-by-one-parsing-error.patch
  25616-x86-MCi_CTL-default.patch
  25617-vtd-qinval-addr.patch
  25688-x86-nr_irqs_gsi.patch
* Sun Jul 29 2012 aj@suse.de
- Build all files with optimization (fortify source does not work
  with -O0).
* Fri Jul 27 2012 carnold@novell.com
- bnc#773393 - VUL-0: CVE-2012-3433: xen: HVM guest destroy p2m
  teardown host DoS vulnerability
  CVE-2012-3433-xsa11.patch
- bnc#773401 - VUL-1: CVE-2012-3432: xen: HVM guest user mode MMIO
  emulation DoS
  25682-x86-inconsistent-io-state.patch
* Wed Jul 18 2012 carnold@novell.com
- bnc#762484 - VUL-1: CVE-2012-2625: xen: pv bootloader doesn't
  check the size of the bzip2 or lzma compressed kernel, leading to
  denial of service
  25589-pygrub-size-limits.patch
* Tue Jul 10 2012 werner@suse.de
- Make it build with latest TeXLive 2012 with new package layout
* Fri Jun 15 2012 carnold@novell.com
- bnc#767273 - unsupported /var/lock/subsys is still used by xendomains
  init.xendomains
* Tue Jun 12 2012 carnold@novell.com
- bnc#766283 - opensuse 12.2 pv guests can not start after
  installation due to lack of grub2 support in the host
  24000-pygrub-grub2.patch
  24001-pygrub-grub2.patch
  24002-pygrub-grub2.patch
* Mon Jun 11 2012 carnold@novell.com
- Upstream pygrub patches for grub2 support and fixes
  23686-pygrub-solaris.patch
  23697-pygrub-grub2.patch
  23944-pygrub-debug.patch
  23998-pygrub-GPT.patch
  23999-pygrub-grub2.patch
  24064-pygrub-HybridISO.patch
  24401-pygrub-scrolling.patch
  24402-pygrub-edit-fix.patch
  24460-pygrub-extlinux.patch
  24706-pygrub-extlinux.patch
* Wed Jun  6 2012 carnold@novell.com
- Revised version of security patch and an additional patch for
  bnc#764077
  x86_64-AMD-erratum-121.patch
  x86_64-allow-unsafe-adjust.patch
* Wed Jun  6 2012 ohering@suse.de
- remove dummy asm/smp-processor-id.h
* Tue May 29 2012 jsmeix@suse.de
- removed dummy xenapi.tex which was added because of bnc#750679
  (see the below entry dated "Mon Apr  2 13:07:20 CEST 2012")
  because "ps2pdf xenapi.ps xenapi.pdf" failed only for
  Ghostscript version 9.04 (now we have Ghostscript 9.05).
* Fri May 25 2012 carnold@novell.com
- bnc#764077 - VUL-0: EMBARGOED: xen: XSA-9: denial of service on
  older AMD systems
  x86_64-AMD-erratum-121.patch
- Revised version of security patch for bnc#757537
  x86_64-sysret-canonical.patch
* Tue May 15 2012 carnold@novell.com
- Upstream patches from Jan
  25242-x86_64-hotplug-compat-m2p.patch
  25247-SVM-no-rdtsc-intercept.patch
  25267-x86-text-unlikely.patch
  25269-x86-vMCE-addr-misc-write.patch
  25271-x86_64-IST-index.patch
  25327-pvdrv-no-asm-system-h.patch
* Mon May 14 2012 ohering@suse.de
- add dummy asm/smp-processor-id.h for kernel-source 3.4-rcX
* Sun May 13 2012 ohering@suse.de
- remove inclusion of asm/system.h from platform-pci.c
* Tue Apr 24 2012 carnold@novell.com
- Upstream patches from Jan
  25168-x86-memset-size.patch
  25191-x86-tdt-delta-calculation.patch
  25195-x86-cpuidle-C2-no-flush-or-bm-check.patch
  25196-x86-HAP-PAT-sr.patch
  25200-x86_64-trap-bounce-flags.patch
* Thu Apr 19 2012 carnold@novell.com
- bnc#757537 - VUL-0: xen: CVE-2012-0217 PV guest escalation
  x86_64-sysret-canonical.patch
- bnc#757970 - VUL-1: xen: guest denial of service on syscall GPF
  generation
  x86_64-trap-bounce-flags.patch
* Tue Apr  3 2012 carnold@novell.com
- Upstream patches from Jan
  25098-x86-emul-lock-UD.patch
  25101-x86-hpet-disable.patch
  ioemu-9877-MSI-X-device-cleanup.patch
* Mon Apr  2 2012 ohering@suse.de
- bnc#750679 - "ps2pdf xenapi.ps xenapi.pdf" fails for user abuild in Factory
  add dummy xenapi.tex until ghostscript is fixed
* Wed Mar 28 2012 ohering@suse.de
- remove vcd.o rule from PVonHVM Makefile, not needed anymore
* Tue Mar 20 2012 carnold@novell.com
- bnc#753165 - xen/scripts/network-bridge wont create bridge
  bridge-bonding.diff
* Mon Mar 19 2012 carnold@novell.com
- Upstream patches from Jan
  24950-gnttab-copy-mapped.patch
  24970-x86-cpuidle-deny-port-access.patch
  24996-x86-cpuidle-array-overrun.patch
  25041-tapdisk2-create-init-name.patch
* Wed Mar 14 2012 ohering@suse.de
- use BuildRequires: gcc46 only in sles11sp2 to avoid issues
  when gcc47 and newer is the distro default
* Mon Feb 27 2012 jfehlig@suse.com
- bnc#745880 - cpuid setting is not preserved across xend restarts
  xend-cpuid.patch
* Mon Feb 27 2012 jfehlig@suse.com
- Rename 2XXXX-vif-bridge.patch -> vif-bridge-tap-fix.patch
* Mon Feb 27 2012 carnold@novell.com
- bnc#747331 - XEN: standard "newburn" kernel QA stress test on guest
  (+ smartd on Dom0?) freezes the guest
  24883-x86-guest-walk-not-present.patch
- bnc#745367 - MCE bank handling during migration
  24781-x86-vmce-mcg_ctl.patch
  24886-x86-vmce-mcg_ctl-default.patch
  24887-x86-vmce-sr.patch
- bnc#744771 - L3: VM with passed through PCI card fails to reboot
  under dom0 load
  24888-pci-release-devices.patch
- Upstream patches from Jan
  24517-VT-d-fault-softirq.patch
  24527-AMD-Vi-fault-softirq.patch
  24535-x86-vMSI-misc.patch
  24615-VESA-lfb-flush.patch
  24690-x86-PCI-SERR-no-deadlock.patch
  24701-gnttab-map-grant-ref-recovery.patch
  24742-gnttab-misc.patch
  24780-x86-paging-use-clear_guest.patch
  24805-x86-MSI-X-dom0-ro.patch
  ioemu-9869-MSI-X-init.patch
  ioemu-9873-MSI-X-fix-unregister_iomem.patch
* Sat Feb 25 2012 ohering@suse.de
- add BuildRequires: libuuid-devel
* Tue Feb 14 2012 carnold@novell.com
- bnc#746702 - Xen HVM DomU crash during Windows Server 2008 R2
  install, when maxmem > memory
  README.SuSE
* Wed Feb  8 2012 jfehlig@suse.com
- bnc#745005 - Update vif configuration examples in xmexample*
  Updated xen-xmexample.diff
* Thu Feb  2 2012 jfehlig@suse.com
- bnc#743414 - using vifname is ignored when defining a xen virtual
  interface with xl/libxl
  24459-libxl-vifname.patch
* Thu Feb  2 2012 carnold@novell.com
- bnc#740165 - VUL-0: kvm: qemu heap overflow in e1000 device
  emulation (applicable to Xen qemu - CVE-2012-0029)
  cve-2012-0029-qemu-xen-unstable.patch
* Wed Feb  1 2012 carnold@novell.com
- bnc#744014 - blank screen in SLES11 SP2 guest with a VF statically
  assigned
  ioemu-MSI-X-fix-unregister_iomem.patch
- Upstream patches from Jan
  24453-x86-vIRQ-IRR-TMR-race.patch
  24456-x86-emul-lea.patch
* Thu Jan 26 2012 ohering@suse.de
- fate#310510 - fix xenpaging
  24586-x86-mm_Properly_account_for_paged_out_pages.patch
  24609-tools-libxc_handle_fallback_in_linux_privcmd_map_foreign_bulk_properly.patch
  24610-xenpaging_make_file_op_largefile_aware.patch
  xen-unstable.misc.linux_privcmd_map_foreign_bulk.retry_paged.patch
  xenpaging.speedup-page-out.resume_pages.find_next_bit_set.patch
  xenpaging.speedup-page-out.evict_pages.free_slot_stack.patch
  xenpaging.speedup-page-out.policy_choose_victim.patch
  update xenpaging.error-handling.patch, flush qemu cache not so often
* Thu Jan 26 2012 ohering@suse.de
- fate#310510 - fix xenpaging
  24566-tools-libxc_fix_error_handling_in_xc_mem_paging_load.patch
* Tue Jan 24 2012 ohering@suse.de
- fate#310510 - fix xenpaging
  24466-libxc_Only_retry_mapping_pages_when_ENOENT_is_returned.patch
* Mon Jan 23 2012 carnold@novell.com
- The xen kmp packages fail on the 09-check-packaged-twice script.
  Rename xen_pvdrivers.conf to xen_pvdrivers-<kernel flavor>.conf
* Fri Jan 20 2012 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.speedup-page-in.gfn_to_slot.patch
* Wed Jan 18 2012 carnold@novell.com
- bnc#739585 - L3: Xen block-attach fails after repeated attach/detach
  blktap-close-fifos.patch
  blktap-disable-debug-printf.patch
* Fri Jan 13 2012 jfehlig@suse.com
- bnc#741159 - Fix default setting of XENSTORED_ROOTDIR in
  xencommons init script
  xencommons-xenstored-root.patch
* Thu Jan 12 2012 carnold@novell.com
- bnc#740625 - xen: cannot interact with xend after upgrade (SLES)
- bnc#738694 - xen: cannot interact with xend after upgrade (os12.1)
- Other README changes included.
  README.SuSE
* Tue Jan 10 2012 ohering@suse.de
- bnc#694863 - kexec fails in xen
  24478-libxl_add_feature_flag_to_xenstore_for_XS_RESET_WATCHES.patch
* Mon Jan  9 2012 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.speedup-page-out.patch
* Tue Jan  3 2012 carnold@novell.com
- bnc#735806 - VF doesn't work after hot-plug for many times
  24448-x86-pt-irq-leak.patch
- Upstream patches from Jan
  24261-x86-cpuidle-Westmere-EX.patch
  24417-amd-erratum-573.patch
  24429-mceinj-tool.patch
  24447-x86-TXT-INIT-SIPI-delay.patch
  ioemu-9868-MSI-X.patch
* Mon Jan  2 2012 ohering@suse.de
- bnc#732884 - remove private runlevel 4 from init scripts
  xen.no-default-runlevel-4.patch
* Mon Dec 19 2011 carnold@novell.com
- bnc#727515 - Fragmented packets hang network boot of HVM guest
  ipxe-gcc45-warnings.patch
  ipxe-ipv4-fragment.patch
  ipxe-enable-nics.patch
* Mon Dec 19 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  update xenpaging.autostart.patch, make changes with mem-swap-target
  permanent
  update xenpaging.doc.patch, mention issues with live migration
* Thu Dec 15 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  add xenpaging.evict_mmap_readonly.patch
  update xenpaging.error-handling.patch, reduce debug output
* Thu Dec 15 2011 carnold@novell.com
- bnc#736824 - Microcode patches for AMD's 15h processors panic the
  system
  24189-x86-p2m-pod-locking.patch
  24412-x86-AMD-errata-model-shift.patch
  24411-x86-ucode-AMD-Fam15.patch
* Wed Dec 14 2011 carnold@novell.com
- bnc#711219 - SR-IOV VF doesn't work in SLES11 sp2 guest
  24357-firmware-no-_PS0-_PS3.patch
- Upstream patches from Jan
  24153-x86-emul-feature-checks.patch
  24275-x86-emul-lzcnt.patch
  24277-x86-dom0-features.patch
  24278-x86-dom0-no-PCID.patch
  24282-x86-log-dirty-bitmap-leak.patch
  24359-x86-domU-features.patch
  24360-x86-pv-domU-no-PCID.patch
  24389-amd-fam10-gart-tlb-walk-err.patch
  24391-x86-pcpu-version.patch
* Thu Dec  8 2011 ohering@suse.de
- bnc#729208 - xenpaging=-1 doesn't work
  xenpaging.doc.patch
* Thu Dec  8 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  readd xenpaging.qemu.flush-cache.patch
* Wed Dec  7 2011 jfehlig@suse.com
- bnc#732782 - L3: xm create hangs when maxmen value is enclosed
  in "quotes"
  xm-create-maxmem.patch
* Wed Dec  7 2011 carnold@novell.com
- Upstream patches / changes from Jan
  Added 24358-kexec-compat-overflow.patch
  Removed 24341-x86-64-mmcfg_remove___initdata_annotation_overlooked_in_23749e8d1c8f074ba.patch
  Removed 24345-tools-libxc_Fix_x86_32_build_breakage_in_previous_changeset..patch
* Wed Dec  7 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  24178-debug_Add_domain-vcpu_pause_count_info_to_d_key..patch
  Use wait queues for paging, improve foreign mappings.
  xenpaging.versioned-interface.patch
  xenpaging.mmap-before-nominate.patch
  xenpaging.p2m_is_paged.patch
  xenpaging.evict_fail_fast_forward.patch
  xenpaging.error-handling.patch
  xenpaging.mem_event-use-wait_queue.patch
  xenpaging.waitqueue-paging.patch
  Remove obsolete patch, not needed with wait queue usage
  xenpaging.HVMCOPY_gfn_paged_out.patch
* Wed Dec  7 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  Fix incorrect backport, remove double memset, use xzalloc
  24171-x86waitqueue_Allocate_whole_page_for_shadow_stack..patch
* Wed Dec  7 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  fix typo in nominate, use lock instead of double unlock
  23905-xenpaging_fix_locking_in_p2m_mem_paging_functions.patch
* Wed Dec  7 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  24327-After_preparing_a_page_for_page-in_allow_immediate_fill-in_of_the_page_contents.patch
  24328-Tools_Libxc_wrappers_to_automatically_fill_in_page_oud_page_contents_on_prepare.patch
  24329-Teach_xenpaging_to_use_the_new_and_non-racy_xc_mem_paging_load_interface.patch
* Tue Dec  6 2011 jfehlig@suse.com
- bnc#734826 - xm rename doesn't work anymore
  Updated xend-migration-domname-fix.patch
* Fri Dec  2 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  24269-mem_event_move_mem_event_domain_out_of_struct_domain.patch
  24270-Free_d-mem_event_on_domain_destruction..patch
* Fri Dec  2 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  24318-x86-mm_Fix_checks_during_foreign_mapping_of_paged_pages.patch
* Fri Dec  2 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  23949-constify_vcpu_set_affinitys_second_parameter.patch
* Fri Dec  2 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  24105-xenpaging_compare_domain_pointer_in_p2m_mem_paging_populate.patch
  24106-mem_event_check_capabilities_only_once.patch
* Fri Dec  2 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  24272-xenpaging_Fix_c-s_235070a29c8c3ddf7_update_machine_to_phys_mapping_during_page_deallocation.patch
* Fri Dec  2 2011 ohering@suse.de
- bnc#727081 - xend domains don't work anymore since update from 12.1 beta to 12.1 RC 1
  24344-tools-x86_64_Fix_cpuid_inline_asm_to_not_clobber_stacks_red_zone.patch
  24345-tools-libxc_Fix_x86_32_build_breakage_in_previous_changeset..patch
* Fri Dec  2 2011 ohering@suse.de
- bnc#733449 - Panic in mcfg_ioremap when booting xen-dbg.gz on Xeon E3-1230
  24341-x86-64-mmcfg_remove___initdata_annotation_overlooked_in_23749e8d1c8f074ba.patch
* Fri Dec  2 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  backport waitqueue changes from xen-unstable
  24104-waitqueue_Double_size_of_x86_shadow_stack..patch
  24171-x86waitqueue_Allocate_whole_page_for_shadow_stack..patch
  24195-waitqueue_Detect_saved-stack_overflow_and_crash_the_guest..patch
  24196-waitqueue_Reorder_prepare_to_wait_so_that_vcpu_is_definitely_on_the.patch
  24197-x86-waitqueue_Because_we_have_per-cpu_stacks_we_must_wake_up_on_teh.patch
  24231-waitqueue_Implement_wake_up_nroneall..patch
  24232-waitqueue_Hold_a_reference_to_a_domain_on_a_waitqueue..patch
* Fri Dec  2 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  24227-xenpaging_restrict_pagefile_permissions.patch
* Fri Dec  2 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  merge upstream version of our existing patches:
  24218-libxc_add_bitmap_clear_function.patch
  remove old versions:
  xenpaging.bitmap_clear.patch
* Fri Dec  2 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  merge upstream version of our existing patches:
  24138-xenpaging_munmap_all_pages_after_page-in.patch
  24208-xenpaging_remove_filename_from_comment.patch
  24209-xenpaging_remove_obsolete_comment_in_resume_path.patch
  24210-xenpaging_use_PERROR_to_print_errno.patch
  24211-xenpaging_simplify_file_op.patch
  24212-xenpaging_print_gfn_in_failure_case.patch
  24213-xenpaging_update_xenpaging_init.patch
  24214-xenpaging_remove_xc_dominfo_t_from_paging_t.patch
  24215-xenpaging_track_the_number_of_paged-out_pages.patch
  24216-xenpaging_move_page_add-resume_loops_into_its_own_function..patch
  24217-xenpaging_improve_mainloop_exit_handling.patch
  24219-xenpaging_retry_unpageable_gfns.patch
  24220-xenpaging_install_into_LIBEXEC_dir.patch
  24221-xenpaging_add_XEN_PAGING_DIR_-_libxl_xenpaging_dir_path.patch
  24222-xenpaging_use_guests_tot_pages_as_working_target.patch
  24223-xenpaging_watch_the_guests_memory-target-tot_pages_xenstore_value.patch
  24224-xenpaging_add_cmdline_interface_for_pager.patch
  24225-xenpaging_improve_policy_mru_list_handling.patch
  24226-xenpaging_add_debug_to_show_received_watch_event..patch
  remove old versions:
  xenpaging.XEN_PAGING_DIR.patch
  xenpaging.add_evict_pages.patch
  xenpaging.cmdline-interface.patch
  xenpaging.encapsulate_domain_info.patch
  xenpaging.file_op-return-code.patch
  xenpaging.install-to-libexec.patch
  xenpaging.low_target_policy_nomru.patch
  xenpaging.main-loop-exit-handling.patch
  xenpaging.misleading-comment.patch
  xenpaging.page_in-munmap-size.patch
  xenpaging.print-gfn.patch
  xenpaging.record-numer-paged-out-pages.patch
  xenpaging.reset-uncomsumed.patch
  xenpaging.stale-comments.patch
  xenpaging.target-tot_pages.patch
  xenpaging.use-PERROR.patch
  xenpaging.watch-target-tot_pages.patch
  xenpaging.watch_event-DPRINTF.patch
  xenpaging.xc_interface_open-comment.patch
* Wed Nov 30 2011 jfehlig@suse.com
- bnc#733348 - Use 'xm' in various scripts if xend is running.
  Modified xmclone.sh and xen-updown.sh
- Only emit xl warning when xend is running and -f (force) flag
  is not specified.
  Modified disable-xl-when-using-xend.patch
* Wed Nov 30 2011 carnold@novell.com
- Upstream patches from Jan
  24190-hap-log-dirty-disable-rc.patch
  24193-hap-track-dirty-vram-rc.patch
  24201-x86-pcpu-platform-op.patch
* Tue Nov 22 2011 carnold@novell.com
- Upstream patches from Jan
  23900-xzalloc.patch
  24144-cpufreq-turbo-crash.patch
  24148-shadow-pgt-dying-op-performance.patch
  24155-x86-ioapic-EOI-after-migration.patch
  24156-x86-ioapic-shared-vectors.patch
  24157-x86-xstate-init.patch
  24168-x86-vioapic-clear-remote_irr.patch
* Tue Nov 22 2011 cyliu@suse.com
- submit fixes for bnc#649209 and bnc#711892
  xl-create-pv-with-qcow2-img.patch
  update suspend_evtchn_lock.patch
* Sun Nov 20 2011 ohering@suse.de
- Update trace.c, merge patches from upstream
  23050-xentrace_dynamic_tracebuffer_allocation.patch
  23091-xentrace_fix_t_info_pages_calculation..patch
  23092-xentrace_print_calculated_numbers_in_calculate_tbuf_size.patch
  23093-xentrace_remove_gdprintk_usage_since_they_are_not_in_guest_context.patch
  23094-xentrace_update_comments.patch
  23095-xentrace_use_consistent_printk_prefix.patch
  23128-xentrace_correct_formula_to_calculate_t_info_pages.patch
  23129-xentrace_remove_unneeded_debug_printk.patch
  23173-xentrace_Move_register_cpu_notifier_call_into_boot-time_init..patch
  23239-xentrace_correct_overflow_check_for_number_of_per-cpu_trace_pages.patch
  23308-xentrace_Move_the_global_variable_t_info_first_offset_into_calculate_tbuf_size.patch
  23309-xentrace_Mark_data_size___read_mostly_because_its_only_written_once.patch
  23310-xentrace_Remove_unneeded_cast_when_assigning_pointer_value_to_dst.patch
  23404-xentrace_reduce_trace_buffer_size_to_something_mfn_offset_can_reach.patch
  23405-xentrace_fix_type_of_offset_to_avoid_ouf-of-bounds_access.patch
  23406-xentrace_update___insert_record_to_copy_the_trace_record_to_individual_mfns.patch
  23407-xentrace_allocate_non-contiguous_per-cpu_trace_buffers.patch
  23643-xentrace_Allow_tracing_to_be_enabled_at_boot.patch
  23719-xentrace_update___trace_var_comment.patch
  Remove old patches:
  xen-unstable.xentrace.dynamic_tbuf.patch
  xen-unstable.xentrace.empty_t_info_pages.patch
  xen-unstable.xentrace.verbose.patch
  xen-unstable.xentrace.no_gdprintk.patch
  xen-unstable.xentrace.comments.patch
  xen-unstable.xentrace.printk_prefix.patch
  xen-unstable.xentrace.remove_debug_printk.patch
  xen-unstable.xentrace.t_info_pages-formula.patch
  xen-unstable.xentrace.register_cpu_notifier-boot_time.patch
  xen-unstable.xentrace.t_info_page-overflow.patch
  xen-unstable.xentrace.t_info_first_offset.patch
  xen-unstable.xentrace.data_size__read_mostly.patch
  xen-unstable.xentrace.__insert_record-dst-type.patch
* Mon Nov 14 2011 carnold@novell.com
- Upstream patches from Jan
  24116-x86-continuation-cancel.patch
  24123-x86-cpuidle-quiesce.patch
  24124-x86-microcode-amd-quiesce.patch
  24137-revert-23666.patch
  24xxx-shadow-pgt-dying-op-performance.patch
* Thu Nov 10 2011 carnold@novell.com
- bnc#722738 - xm cpupool-create errors out
  xen-cpupool-xl-config-format.patch
* Fri Nov  4 2011 carnold@novell.com
- Fix broken build when building docs
  23819-make-docs.patch
* Fri Nov  4 2011 jfehlig@suse.com
- bnc#720054 - Prevent vif-bridge from adding user-created tap
  interfaces to a bridge
  2XXXX-vif-bridge.patch
* Fri Nov  4 2011 carnold@novell.com
- bnc#713503 - DOM0 filesystem commit
  23752-x86-shared-IRQ-vector-maps.patch
  23754-AMD-perdev-vector-map.patch
* Thu Nov  3 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  This change reverses the task of xenpaging. Before this change a
  fixed number of pages was paged out. With this change the guest
  will not have access to more than the given number of pages at
  the same time.
  The xenpaging= config option is replaced by actmem=
  A new xm mem-swap-target is added.
  The xenpaging binary is moved to /usr/lib/xen/bin/
  xenpaging.HVMCOPY_gfn_paged_out.patch
  xenpaging.XEN_PAGING_DIR.patch
  xenpaging.add_evict_pages.patch
  xenpaging.bitmap_clear.patch
  xenpaging.cmdline-interface.patch
  xenpaging.encapsulate_domain_info.patch
  xenpaging.file_op-return-code.patch
  xenpaging.guest-memusage.patch
  xenpaging.install-to-libexec.patch
  xenpaging.low_target_policy_nomru.patch
  xenpaging.main-loop-exit-handling.patch
  xenpaging.misleading-comment.patch
  xenpaging.page_in-munmap-size.patch
  xenpaging.print-gfn.patch
  xenpaging.record-numer-paged-out-pages.patch
  xenpaging.reset-uncomsumed.patch
  xenpaging.stale-comments.patch
  xenpaging.target-tot_pages.patch
  xenpaging.use-PERROR.patch
  xenpaging.watch-target-tot_pages.patch
  xenpaging.watch_event-DPRINTF.patch
  xenpaging.xc_interface_open-comment.patch
* Thu Nov  3 2011 ohering@suse.de
- xen.spec: update filelist
  package /usr/lib*/xen with wildcard to pickup new files
  remove duplicate /usr/sbin/xen-list from filelist
* Wed Oct 26 2011 carnold@novell.com
- bnc#725169 - xen-4.0.2_21511_03-0.5.3: bootup hangs
  23993-x86-microcode-amd-fix-23871.patch
* Wed Oct 26 2011 carnold@novell.com
- Update to Xen 4.1.2 FCS c/s 23174
* Mon Oct 24 2011 jfehlig@suse.com
- bnc#720054 - Fix syntax error introduced during recent adjustment
  of Xen's tap udev rule.
  Updated udev-rules.patch
* Thu Oct 20 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  Merge paging related fixes from xen-unstable:
  23506-x86_Disable_set_gpfn_from_mfn_until_m2p_table_is_allocated..patch
  23507-xenpaging_update_machine_to_phys_mapping_during_page_deallocation.patch
  23509-x86_32_Fix_build_Define_machine_to_phys_mapping_valid.patch
  23562-xenpaging_remove_unused_spinlock_in_pager.patch
  23576-x86_show_page_walk_also_for_early_page_faults.patch
  23577-tools_merge_several_bitop_functions_into_xc_bitops.h.patch
  23578-xenpaging_add_xs_handle_to_struct_xenpaging.patch
  23579-xenpaging_drop_xc.c_remove_ASSERT.patch
  23580-xenpaging_drop_xc.c_remove_xc_platform_info_t.patch
  23581-xenpaging_drop_xc.c_remove_xc_wait_for_event.patch
  23582-xenpaging_drop_xc.c_move_xc_mem_paging_flush_ioemu_cache.patch
  23583-xenpaging_drop_xc.c_move_xc_wait_for_event_or_timeout.patch
  23584-xenpaging_drop_xc.c_remove_xc_files.patch
  23585-xenpaging_correct_dropping_of_pages_to_avoid_full_ring_buffer.patch
  23586-xenpaging_do_not_bounce_p2mt_back_to_the_hypervisor.patch
  23587-xenpaging_remove_srand_call.patch
  23588-xenpaging_remove_return_values_from_functions_that_can_not_fail.patch
  23589-xenpaging_catch_xc_mem_paging_resume_errors.patch
  23590-xenpaging_remove_local_domain_id_variable.patch
  23591-xenpaging_move_num_pages_into_xenpaging_struct.patch
  23592-xenpaging_start_paging_in_the_middle_of_gfn_range.patch
  23593-xenpaging_pass_integer_to_xenpaging_populate_page.patch
  23594-xenpaging_add_helper_function_for_unlinking_pagefile.patch
  23595-xenpaging_add_watch_thread_to_catch_guest_shutdown.patch
  23596-xenpaging_implement_stopping_of_pager_by_sending_SIGTERM-SIGINT.patch
  23597-xenpaging_remove_private_mem_event.h.patch
  23599-tools_fix_build_after_recent_xenpaging_changes.patch
  23817-mem_event_add_ref_counting_for_free_requestslots.patch
  23818-mem_event_use_mem_event_mark_and_pause_in_mem_event_check_ring.patch
  23827-xenpaging_use_batch_of_pages_during_final_page-in.patch
  23841-mem_event_pass_mem_event_domain_pointer_to_mem_event_functions.patch
  23842-mem_event_use_different_ringbuffers_for_share_paging_and_access.patch
  23874-xenpaging_track_number_of_paged_pages_in_struct_domain.patch
  23904-xenpaging_use_p2m-get_entry_in_p2m_mem_paging_functions.patch
  23905-xenpaging_fix_locking_in_p2m_mem_paging_functions.patch
  23906-xenpaging_remove_confusing_comment_from_p2m_mem_paging_populate.patch
  23908-p2m_query-modify_p2mt_with_p2m_lock_held.patch
  23943-xenpaging_clear_page_content_after_evict.patch
  23953-xenpaging_handle_evict_failures.patch
  23978-xenpaging_check_p2mt_in_p2m_mem_paging_functions.patch
  23979-xenpaging_document_p2m_mem_paging_functions.patch
  23980-xenpaging_disallow_paging_in_a_PoD_guest.patch
  Remove obsolete patches:
  x86-show-page-walk-early.patch
  xenpaging.23817-mem_event_check_ring.patch
  xenpaging.catch-xc_mem_paging_resume-error.patch
  xenpaging.guest_remove_page.slow_path.patch
  xenpaging.mem_event-no-p2mt.patch
  xenpaging.no-srand.patch
  xenpaging.return-void.patch
  xenpaging.xenpaging_populate_page-gfn.patch
* Thu Oct 20 2011 ohering@suse.de
- xen.spec: use changeset number as patch number for upstream patches
* Wed Oct 19 2011 adrian@suse.de
- do not use runlevel 4 in init scripts, it makes it impossible
  to "insserv xend" on 12.1
* Mon Oct 17 2011 carnold@novell.com
- Upstream patches from Jan
  23955-x86-pv-cpuid-xsave.patch
  23957-cpufreq-error-paths.patch
* Tue Oct 11 2011 carnold@novell.com
- Upstream patches from Jan
  23933-pt-bus2bridge-update.patch
  23726-x86-intel-flexmigration-v2.patch
  23925-x86-AMD-ARAT-Fam12.patch
  23246-x86-xsave-enable.patch
  23897-x86-mce-offline-again.patch
* Mon Oct 10 2011 carnold@novell.com
- Update to Xen 4.1.2_rc3 c/s 23171
* Thu Oct  6 2011 jfehlig@suse.com
- bnc#720054 - Changed /etc/udev/rules.d/40-xen.rules to not run
  Xen's vif-bridge script when not running Xen.  This is not a
  solution to the bug but an improvement in the rules regardless.
  Updated udev-rules.patch
* Tue Oct  4 2011 carnold@novell.com
- Upstream patches from Jan
  23868-vtd-RMRR-validation.patch
  23871-x86-microcode-amd-silent.patch
  23898-cc-option-grep.patch
* Fri Sep 30 2011 jfehlig@suse.com
- Add pciback init script and sysconf file, giving users a simple
  mechanism to configure pciback.
  init.pciback sysconfig.pciback
* Fri Sep 23 2011 ohering@suse.de
- update scripts to use xl -f, or xm if xend is running:
  xen-updown.sh, init.xendomains, xmclone.sh
* Fri Sep 23 2011 ohering@suse.de
- bnc#694863 - kexec fails in xen
  xenstored: allow guest to shutdown all its watches/transactions
  xenstored.XS_RESET_WATCHES.patch
* Thu Sep 22 2011 carnold@novell.com
- Upstream patches from Jan
  23843-scheduler-switch.patch
  23846-x86-TSC-check.patch
  23848-vmx-conditional-off.patch
  23853-x86-pv-cpuid-xsave.patch
* Fri Sep 16 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  mem_event: add ref counting for free requestslots
  xenpaging.23817-mem_event_check_ring.patch
* Wed Sep 14 2011 carnold@novell.com
- bnc#717650 - Unable to start VM
- Update to Xen 4.1.2_rc2 c/s 23152
* Fri Sep  9 2011 jfehlig@suse.com
- bnc#716695 - domUs using tap devices will not start
  updated multi-xvdp.patch
* Tue Sep  6 2011 carnold@novell.com
- Upstream patches from Jan
  23803-intel-pmu-models.patch
  23800-x86_64-guest-addr-range.patch
  23795-intel-ich10-quirk.patch
  23804-x86-IPI-counts.patch
* Wed Aug 31 2011 jfehlig@suse.com
- bnc#706106 - Inconsistent reporting of VM names during migration
  xend-migration-domname-fix.patch
* Tue Aug 30 2011 carnold@novell.com
- bnc#712823 - L3:Xen guest does not start reliable when rebooted
  xend-vcpu-affinity-fix.patch
* Tue Aug 23 2011 carnold@novell.com
- Upstream patches from Jan
  23725-pci-add-device.patch
  23762-iommu-fault-bm-off.patch
  23763-pci-multi-seg-x2apic-vtd-no-crash.patch
  23765-x86-irq-vector-leak.patch
  23766-x86-msi-vf-bars.patch
  23771-x86-ioapic-clear-pin.patch
  23772-x86-trampoline.patch
  23774-x86_64-EFI-EDD.patch
  23776-x86-kexec-hpet-legacy-bcast-disable.patch
  23781-pm-wide-ACPI-ids.patch
  23782-x86-ioapic-clear-irr.patch
  23783-ACPI-set-_PDC-bits.patch
* Mon Aug 15 2011 ohering@suse.de
- Include gcc46 only when its available (>11.4 && >sles11sp1)
* Fri Aug 12 2011 carnold@novell.com
- bnc#711943 - [xl] Fail to create multi-guests with NIC assigned
  23685-libxl-segfault-fix.patch
* Thu Aug 11 2011 jfehlig@suse.com
- libxenlight and legacy xend toolstack should not be used
  together.  If xend is running, print a warning and exit
  xl.  Add a '-f' (force) option to xl to override this
  behavior.
  disable-xl-when-using-xend.patch
  bnc#707664
* Wed Aug 10 2011 carnold@novell.com
- Upstream patches from Jan
  23732-sedf.patch
  23735-guest-dom0-cap.patch
  23746-vtd-cleanup-timers.patch
  23747-mmcfg-base-address.patch
  23749-mmcfg-reservation.patch
* Tue Aug  9 2011 cyliu@novell.com
- bnc#704160 - crm resource migrate fails with xen machines
  update snapshot-xend.patch
- bnc#706574 - xm console DomUName hang after "xm save/restore" of
  PVM on the latest Xen
  xend-console-port-restore.patch
* Tue Aug  9 2011 ohering@suse.de
- update xencommons script to run only when needed
  xencommons-proc-xen.patch
* Fri Jul 22 2011 carnold@novell.com
- Upstream patches from Jan
  23726-x86-intel-flexmigration.patch
  23706-fix-20892.patch
  23723-x86-CMOS-lock.patch
  23676-x86_64-image-map-bounds.patch
  23724-x86-smpboot-x2apic.patch
* Mon Jul 11 2011 ohering@suse.de
- hotplug.losetup.patch
  correct dev:inode detection, stat returns major:minor without
  leading zeros, while losetup -a includes trailing zeros
* Fri Jul  8 2011 cyliu@novell.com
- fate#310635: xen npiv multipath support
  update block-npiv* scripts for testing
* Thu Jul  7 2011 carnold@novell.com
- Fixes for EFI support
  x86-EFI-discard-comment.patch
* Wed Jun 29 2011 carnold@novell.com
- fate#309894: Xen needs to correctly understand family 15h CPU
  topology
- fate#311376: EFI support in SP2
- fate#311529: Native UEFI booting under Xen (installation)
  23074-pfn.h.patch
  23571-vtd-fault-verbosity.patch
  23574-x86-dom0-compressed-ELF.patch
  23575-x86-DMI.patch
  23610-x86-topology-info.patch
  23611-amd-fam15-topology.patch
  23613-EFI-headers.patch
  23614-x86_64-EFI-boot.patch
  23615-x86_64-EFI-runtime.patch
  23616-x86_64-EFI-MPS.patch
* Wed Jun 29 2011 jbeulich@novell.com
- Mark xen-scsi.ko supported (bnc#582265, fate#309459).
* Tue Jun 28 2011 carnold@novell.com
- fate#310308: Hypervisor assisted watchdog driver
  ioemu-watchdog-support.patch
  ioemu-watchdog-linkage.patch
  ioemu-watchdog-ib700-timer.patch
  tools-watchdog-support.patch
* Mon Jun 27 2011 carnold@novell.com
- bnc#702025 - VUL-0: xen: VT-d (PCI passthrough) MSI trap
  injection  (CVE-2011-1898)
  Fixed in Xen version 4.1.1
* Wed Jun 22 2011 cyliu@novell.com
- fate#310956: Support Direct Kernel Boot for FV guests
  kernel-boot-hvm.patch
* Wed Jun 22 2011 cyliu@novell.com
- fate#310316: Support change vnc password while vm is running
  change-vnc-passwd.patch
- fate#310325: Support get domU console log from Dom0
  log-guest-console.patch
* Wed Jun 22 2011 ohering@suse.de
- fate#311487: remove modprobe.conf files for autoloading of Xen
  and Hyper-V drivers
  xen.sles11sp1.fate311487.xen_platform_pci.dmistring.patch
  add dmi modalias to xen-platform-pci.ko
* Tue Jun 21 2011 carnold@novell.com
- fate#308532: [NONCODE] Remove XEN 32-bit Hypervisor
  Modify ExclusiveArch in xen.spec to build only x86_64
* Tue Jun 21 2011 carnold@novell.com
- fate#309900 - Add Xen support for SVM Decode Assist in AMD family
  15h
- fate#309902 - Add Xen support for AMD family 12h processors
- fate#309903 - Add Xen support for AMD family 14h processors
- fate#309906 - Add Xen support for performance event counters in
  AMD family 15h
* Fri Jun 17 2011 carnold@novell.com
- fate#309893: Add Xen support for AMD family 15h processors
- fate#309901: Add Xen support for SVM TSC scaling in AMD family
  15h
- fate#311951: Ivy Bridge: XEN support for Supervisor Mode
  Execution Protection (SMEP)
  23437-amd-fam15-TSC-scaling.patch
  23462-libxc-cpu-feature.patch
  23481-x86-SMEP.patch
  23504-x86-SMEP-hvm.patch
  23505-x86-cpu-add-arg-check.patch
  23508-vmx-proc-based-ctls-probe.patch
  23510-hvm-cpuid-DRNG.patch
  23511-amd-fam15-no-flush-for-C3.patch
  23516-cpuid-ERMS.patch
  23538-hvm-pio-emul-no-host-crash.patch
  23539-hvm-cpuid-FSGSBASE.patch
  23543-x86_64-maddr_to_virt-assertion.patch
  23546-fucomip.patch
* Wed Jun 15 2011 jfehlig@novell.com
- Fix libxc reentrancy issues
  23383-libxc-rm-static-vars.patch
* Wed Jun 15 2011 carnold@novell.com
- fate#310957 - Update to Xen 4.1.1 FCS c/s 23079
* Tue Jun 14 2011 lidongyang@novell.com
- fate#311000 - Extend Xen domain lock framework to support
  more alternative
  xend-domain-lock-sfex.patch
* Mon Jun 13 2011 lidongyang@novell.com
- fate#311371 - Enhance yast to configure live migration for
  Xen and KVM
  add firewall service file for xen-tools
* Fri Jun 10 2011 jfehlig@novell.com
- Add man page for xen-list utility
  updated xen-utils-0.1.tar.bz2
* Thu May 26 2011 carnold@novell.com
- Upstream patches from Jan
  23233-hvm-cr-access.patch
  23234-svm-decode-assist-base.patch
  23235-svm-decode-assist-crs.patch
  23236-svm-decode-assist-invlpg.patch
  23238-svm-decode-assist-insn-fetch.patch
  23303-cpufreq-misc.patch
  23304-amd-oprofile-strings.patch
  23305-amd-fam15-xenoprof.patch
  23306-amd-fam15-vpmu.patch
  23334-amd-fam12+14-vpmu.patch
  23338-vtd-force-intremap.patch
* Thu May 26 2011 carnold@novell.com
- fate#310957 - Update to Xen 4.1.1-rc1 c/s 23064
* Tue May 24 2011 ohering@suse.de
- xentrace: dynamic tracebuffer allocation
  xen-unstable.xentrace.dynamic_tbuf.patch
  xen-unstable.xentrace.empty_t_info_pages.patch
  xen-unstable.xentrace.verbose.patch
  xen-unstable.xentrace.no_gdprintk.patch
  xen-unstable.xentrace.comments.patch
  xen-unstable.xentrace.printk_prefix.patch
  xen-unstable.xentrace.remove_debug_printk.patch
  xen-unstable.xentrace.t_info_pages-formula.patch
  xen-unstable.xentrace.register_cpu_notifier-boot_time.patch
  xen-unstable.xentrace.t_info_page-overflow.patch
  xen-unstable.xentrace.t_info_first_offset.patch
  xen-unstable.xentrace.data_size__read_mostly.patch
  xen-unstable.xentrace.__insert_record-dst-type.patch
* Tue May 24 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  update xenpaging patches for xen 4.1
  xenpaging.guest_remove_page.slow_path.patch
  xenpaging.mem_event-no-p2mt.patch
  xenpaging.no-srand.patch
  xenpaging.return-void.patch
  xenpaging.catch-xc_mem_paging_resume-error.patch
  xenpaging.xenpaging_populate_page-gfn.patch
  xenpaging.autostart.patch
* Fri May 20 2011 carnold@novell.com
- bnc#670465 - When connecting to Xen guest through vncviewer mouse
  tracking is off.
- Upstream patch 23298-hvmop-get-mem-type.patch replaces
  xen.sles11sp1.bug684297.HVMOP_get_mem_type.patch
- Upstream patches from Jan
  23333-hvm-32bit-compat-hypercalls.patch
  23337-vtd-malicious-msi-filter.patch
  23338-vtd-force-intremap.patch (CVE-2011-1898)
  23341-x86-ioapic-write-entry.patch
  23343-vtd-error-path-leaks.patch
* Thu May 19 2011 ohering@suse.de
- bnc#684305 - on_crash is being ignored with kdump now working in HVM
  xend-config-enable-dump-comment.patch
* Thu May 19 2011 ohering@suse.de
- disable xend's logrotation for xend.log, use included logrotate.conf
* Wed May 18 2011 ohering@suse.de
- bnc#684297 - HVM taking too long to dump vmcore
  xen.sles11sp1.bug684297.HVMOP_get_mem_type.patch
  new hvm_op hyper call option
  xen.sles11sp1.bug684297.xen_oldmem_pfn_is_ram.patch
  Use new Xen HVMOP_get_mem_type hvmop hypercall option and new Linux
  kernel register_oldmem_pfn_is_ram interface.
  (depends on two kernel-source changes)
* Tue May 17 2011 carnold@novell.com
- Update to Xen 4.1.1-rc1-pre c/s 23051
* Thu May 12 2011 carnold@novell.com
- Numerous cleanups when compiling with the unused-but-set-variable
  flag enabled and warnings equal to errors.
  xen-warnings-unused.diff
* Thu May 12 2011 jfehlig@novell.com
- Add a 'long' option to xen-list utility
  Updated xen-utils-0.1.tar.bz2
* Tue May 10 2011 jfehlig@novell.com
- bnc#691256 - move modprobe of xen backend modules from xend to
  xencommons initscript
  tmp-initscript-modprobe.patch
* Mon May  9 2011 jfehlig@novell.com
- bnc#691738 - Xen does not find device create with npiv block
  xen-qemu-iscsi-fix.patch
* Tue May  3 2011 carnold@novell.com
- Upstream patches from Jan
  22998-x86-get_page_from_l1e-retcode.patch
  22999-x86-mod_l1_entry-retcode.patch
  23000-x86-mod_l2_entry-retcode.patch
  23096-x86-hpet-no-cpumask_lock.patch
  23099-x86-rwlock-scalability.patch
  23103-x86-pirq-guest-eoi-check.patch
  23127-vtd-bios-settings.patch
  23153-x86-amd-clear-DramModEn.patch
  23154-x86-amd-iorr-no-rdwr.patch
  23199-amd-iommu-unmapped-intr-fault.patch
  23200-amd-iommu-intremap-sync.patch
  23228-x86-conditional-write_tsc.patch
* Tue May  3 2011 carnold@novell.com
- bnc#691238 - L3: question on behaviour change xm list
  snapshot-xend.patch
* Mon May  2 2011 ohering@suse.de
- update xenalyze to revision 98
  * Unify setting of vcpu data type
  * Unify record size checks
  * Fix cr3_switch not to access hvm struct before it's initialized
- add xenalyze.gcc46.patch to fix unused-but-set-variable errors
* Thu Apr 28 2011 jfehlig@novell.com
- bnc#688473 - VUL-0: potential buffer overflow in tools
  cve-2011-1583-4.0.patch
* Thu Apr 28 2011 ohering@suse.de
- hotplug.losetup.patch
  correct dev:inode detection and use variable expansion
* Tue Apr 26 2011 carnold@novell.com
- bnc#623680 - xen kernel freezes during boot when processor module
  is loaded
  23228-x86-conditional-write_tsc.patch
- bnc#680824 - dom0 can't recognize boot disk when IOMMU is enabled
  23200-amd-iommu-intremap-sync.patch
- Upstream patches from Jan
  23127-vtd-bios-settings.patch
  23153-x86-amd-clear-DramModEn.patch
  23154-x86-amd-iorr-no-rdwr.patch
  23199-amd-iommu-unmapped-intr-fault.patch
* Thu Apr 21 2011 ohering@suse.de
- bnc#685189: update vif-route-ifup.patch to use correct variable
  after upstream commit 22910:d4bc41a8cecb
* Wed Apr 20 2011 ohering@suse.de
- bnc#688519: correct indention in xend-domain-lock.patch
* Tue Apr 19 2011 jfehlig@novell.com
- bnc#687981 - L3: mistyping model type when defining VIF crashes
  VM
  xend-validate-nic-model.patch
* Mon Apr 11 2011 jfehlig@suse.de
- bnc#685338: Fix porting of xend-domain-lock.patch
* Mon Apr 11 2011 ohering@suse.de
- update scripts to use xl instead of xm:
  xen-updown.sh, init.xendomains, xmclone.sh
* Mon Apr 11 2011 ohering@suse.de
- disable xend in openSuSE > 11.4
  the xl command is the replacement for the xm command
* Thu Apr  7 2011 ohering@suse.de
- mark runlevel scripts as config to preserve local changes by
  admin or dev during package update
* Thu Apr  7 2011 ohering@suse.de
- enable xencommons runlevel script during upgrade if xend was
  already enabled
* Thu Apr  7 2011 ohering@suse.de
- call /sbin/ldconfig directly in xen-libs post install scripts
* Tue Apr  5 2011 carnold@novell.com
- Upstream patches from Jan
  23103-x86-pirq-guest-eoi-check.patch
  23030-x86-hpet-init.patch
  23061-amd-iommu-resume.patch
  23127-vtd-bios-settings.patch
* Thu Mar 31 2011 coolo@novell.com
- add baselibs.conf as libvirt uses 32bit libraries
* Tue Mar 29 2011 carnold@novell.com
- Remus support is enabled for now.
* Mon Mar 28 2011 carnold@novell.com
- Enable support for kernel decompression for gzip, bzip2, and LZMA
  so that kernels compressed with any of these methods can be
  launched
* Fri Mar 25 2011 carnold@novell.com
- Update to Xen 4.1 FCS
* Thu Mar 24 2011 ohering@suse.de
- fix xentrace.dynamic_sized_tbuf.patch
  the default case did not work, correct size calculation
* Tue Mar 22 2011 carnold@novell.com
- Update to c/s 23010 Xen 4.1 rc8
* Tue Mar 22 2011 ohering@suse.de
- use _smp_mflags instead of jobs, jobs is not expanded everywhere
* Mon Mar 21 2011 carnold@novell.com
- bnc#681302 - xm create -x <guest> returns "ImportError: No module
  named ext"
  xm-create-xflag.patch
* Thu Mar 17 2011 carnold@novell.com
- bnc#675817 - Kernel panic when creating HVM guests on AMD
  platforms with XSAVE
  22462-x86-xsave-init-common.patch
* Tue Mar 15 2011 carnold@novell.com
- bnc#679344 - Xen: multi-vCPU pv guest may crash host
  23034-x86-arch_set_info_guest-DoS.patch
- bnc#678871 - dom0 hangs long time when starting hvm guests with
  memory >= 64GB
  22780-pod-preempt.patch
- bnc#675363 - Random lockups with kernel-xen. Possibly graphics
  related
  22997-x86-map_pages_to_xen-check.patch
- Upstream patches from Jan
  22949-x86-nmi-pci-serr.patch
  22992-x86-fiop-m32i.patch
  22996-x86-alloc_xen_pagetable-no-BUG.patch
  23020-x86-cpuidle-ordering.patch
  23039-csched-constrain-cpu.patch
* Mon Mar 14 2011 jfehlig@novell.com
- Fix xen-utils to cope with xen-unstable c/s 21483
* Mon Mar 14 2011 carnold@novell.com
- bnc#678229 - restore of sles HVM fails
  22873-svm-sr-32bit-sysenter-msrs.patch
* Fri Mar 11 2011 ohering@suse.de
- xz-devel is available since 11.2, make it optional for SLES11SP1
* Mon Feb 28 2011 cyliu@novell.com
- Fix /vm/uuid xenstore leak on tapdisk2 device cleanup
  22499-xen-hotplug-cleanup.patch
* Fri Feb 25 2011 carnold@novell.com
- Upstream patches from Jan
  22872-amd-iommu-pci-reattach.patch
  22879-hvm-no-self-set-mem-type.patch
  22899-x86-tighten-msr-permissions.patch
  22915-x86-hpet-msi-s3.patch
  22947-amd-k8-mce-init-all-msrs.patch
* Thu Feb 17 2011 jfehlig@novell.com
- bnc#672833 - xen-tools bug causing problems with Ubuntu 10.10
  under Xen 4.
  22238-pygrub-grub2-fix.patch
* Thu Feb 17 2011 lidongyang@novell.com
- bnc#665610 - xm console > 1 to same VM messes up both consoles
  Upstream rejected due to portability concern, see
  http://lists.xensource.com/archives/html/xen-devel/2011-02/msg00942.html
  xenconsole-no-multiple-connections.patch
* Fri Feb 11 2011 carnold@novell.com
- Enable support for kernel decompression for gzip, bzip2, and LZMA
  so that kernels compressed with any of these methods can be
  launched.
* Thu Feb 10 2011 lidongyang@novell.com
- bnc#651822 - xm snapshot-xxx scripts lead to an XP SP3 HVM domU
  to chkdsk
  Make sure we only apply the snapshot once, and the changes made
  after snapshot-apply hit the disk.
* Wed Feb  9 2011 carnold@novell.com
- Update to Xen 4.1.0 c/s 22861
* Tue Feb  8 2011 jfehlig@novell.com
- bnc#658569 - SLES 11 SP1 dom0 iptables gives lots of physdev
  messages
  22385-vif-common.patch
* Mon Feb  7 2011 ohering@suse.de
- update xenalyze, more 64bit fixes
* Mon Feb  7 2011 ohering@suse.de
- allocate xentrace buffer metadata based on requested tbuf_size
  xentrace.dynamic_sized_tbuf.patch
* Mon Feb  7 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.runtime_mru_size.patch
  - specify policy mru size at runtime
  xenpaging.no_domain_id.patch
  - reduce memory usage in pager
* Mon Feb  7 2011 ohering@suse.de
- bnc#625394 - set vif mtu from bridge mtu if kernel supports it
  vif-bridge.mtu.patch
* Sun Feb  6 2011 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.autostart_delay.patch
  - decouple create/destroycreateXenPaging from _create/_removeDevices
  - change xenpaging variable from int to str
  - init xenpaging variable to 0 if xenpaging is not in config file
    to avoid string None coming from sxp file
* Tue Feb  1 2011 carnold@novell.com
- Update to Xen 4.0.2 rc2-pre, changeset 21443
* Mon Jan 31 2011 carnold@novell.com
- bnc#633573 - System fail to boot after running several warm
  reboot tests
  22749-vtd-workarounds.patch
- Upstream patches from Jan
  22744-ept-pod-locking.patch
  22777-vtd-ats-fixes.patch
  22781-pod-hap-logdirty.patch
  22782-x86-emul-smsw.patch
  22789-i386-no-x2apic.patch
  22790-svm-resume-migrate-pirqs.patch
  22816-x86-pirq-drop-priv-check.patch
* Thu Jan 27 2011 carnold@novell.com
- Don't pass the deprecataed extid parameter to xc.hvm_build
* Fri Jan 14 2011 carnold@novell.com
- bnc#658704 - SLES11 SP1 Xen boot panic in x2apic mode
  22707-x2apic-preenabled-check.patch
- bnc#641419 - L3: Xen: qemu-dm reports "xc_map_foreign_batch: mmap failed:
  Cannot allocate memory"
  7434-qemu-rlimit-as.patch
- Additional or upstream patches from Jan
  22693-fam10-mmio-conf-base-protect.patch
  22694-x86_64-no-weak.patch
  22708-xenctx-misc.patch
  21432-4.0-cpu-boot-failure.patch
  22645-amd-flush-filter.patch
  qemu-fix-7433.patch
* Wed Jan 12 2011 carnold@novell.com
- Maintain compatibility with the extid flag even though it is
  deprecated for both legacy and sxp config files.
  hv_extid_compatibility.patch
* Wed Jan 12 2011 cyliu@novell.com
- bnc#649209-improve suspend eventchn lock
  suspend_evtchn_lock.patch
* Tue Jan 11 2011 carnold@novell.com
- Removed the hyper-v shim patches in favor of using the upstream
  version.
* Mon Jan 10 2011 carnold@novell.com
- bnc#641419 - L3: Xen: qemu-dm reports "xc_map_foreign_batch: mmap
  failed: Cannot allocate memory"
  qemu-rlimit-as.patch
* Mon Jan 10 2011 cyliu@novell.com
- Upstream c/s 7433 to replace qemu_altgr_more.patch
  7433-qemu-altgr.patch
* Fri Jan  7 2011 jfehlig@novell.com
- bnc#661931 - Fix fd leak in xenstore library
  21344-4.0-testing-xenstore-fd-leak.patch
* Tue Jan  4 2011 carnold@novell.com
- bnc#656369 - g5plus: sles11sp1 xen crash with 8 socket x2apic
  preenabled
  21989-x2apic-resume.patch
  22475-x2apic-cleanup.patch
  22535-x2apic-preenabled.patch
- bnc#658163 - maintenance release - Nehalem system cannot boot
  into xen with maintenance release installed
  22504-iommu-dom0-holes.patch
  22506-x86-iommu-dom0-estimate.patch
- bnc#658704 - SLES11 SP1 Xen boot panic in x2apic mode
  21810-x2apic-acpi.patch
- Upstream patches from Jan
  22470-vlapic-tick-loss.patch
  22484-vlapic-tmcct-periodic.patch
  22526-ept-access-once.patch
  22533-x86-32bit-apicid.patch
  22534-x86-max-local-apic.patch
  22538-keyhandler-relax.patch
  22540-32on64-hypercall-debug.patch
  22549-vtd-map-page-leak.patch
  22574-ept-skip-validation.patch
  22632-vtd-print-entries.patch
* Tue Jan  4 2011 carnold@novell.com
- bnc#661298 - maintenance release candidate - Windows VMs reboot
  too fast, triggering failsafe
  xen-minimum-restart-time.patch
* Tue Jan  4 2011 cyliu@novell.com
- bnc#659070 - Fail to input '|' in en-us keyboard
  qemu_altgr_more.patch
* Tue Dec 28 2010 jfehlig@novell.com
- bnc#659466 - XEN drbd block device type not working on SLES 11 SP1
  20158-revert.patch
* Mon Dec 27 2010 jfehlig@novell.com
- Revert changes made to snapshot-xend.patch and
  snapshot-ioemu-restore.patch made on 2010-11-19.  The changes
  were intended to fix bnc#651822, but testing revealed additional
  changes were needed to completely resolve the bug.  bnc#651822
  will be fixed in a subsequent maintenance release.
* Mon Dec 27 2010 lidongyang@novell.com
- bnc#654543 - PV guest won't unplug the IDE disk created by
  qemu-dm
  a dirty hack, only add the device to drives_table[] if we are FV
  domU, that will be unplugged anyway if a PV driver is loaded
  later.
  ioemu-disable-emulated-ide-if-pv.patch
* Wed Dec 22 2010 cyliu@novell.com 
- Upstream patch to replace xenfb_32bpp.patch
  7426-xenfb-depth.patch
* Tue Dec 21 2010 lidongyang@novell.com
- bnc#651822 make sure we only apply the snapshot once, and the
  changes made after snapshot-apply hit the disk.
  snapshot-xend.patch
  snapshot-without-pv-fix.patch
* Fri Dec 17 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.HVMCOPY_gfn_paged_out.patch
  - remove incorrect and unneeded cleanup from do_memory_op
    subfunctions
  add mainline tag to merged patches
* Thu Dec 16 2010 jfehlig@novell.com
- bnc#613584 - If available, use kpartx '-f' option in domUloader
* Thu Dec 16 2010 jfehlig@novell.com
- bnc#659872 - xend: Do no release domain lock on checkpoint
  operation.
* Tue Dec 14 2010 carnold@novell.com
- Upstream patches from Jan
  22431-p2m-remove-bug-check.patch
  22448-x86_64-gdt-ldt-fault-filter.patch
  22466-x86-sis-apic-bug.patch
  22451-hvm-cap-clobber.patch
  22388-x2apic-panic.patch
  22452-x86-irq-migrate-directed-eoi.patch
* Tue Dec 14 2010 carnold@novell.com
- bnc#658163 - maintenance release - Nehalem system cannot boot
  into xen with maintenance release installed
  iommu-dom0-holes.patch
  x86-iommu-dom0-estimate.patch
* Tue Dec 14 2010 carnold@novell.com
- bnc#659085 - physical host is rebooted with unknown reason
  Regression: Remove the patch 22071-ept-get-entry-lock.patch
* Mon Dec 13 2010 carnold@novell.com
- Removed 7410-qemu-alt-gr.patch and altgr_2.patch.  It causes a
  regression (see bnc#659070)
* Tue Dec  7 2010 ohering@suse.de
- make stubdom build optional
* Tue Dec  7 2010 ohering@suse.de
- pass -j N to stubdom build
* Tue Dec  7 2010 ohering@suse.de
- add xenalzye from http://xenbits.xensource.com/ext/xenalyze.hg
* Tue Dec  7 2010 ohering@suse.de
- hotplug-block-losetup-a.patch
  allow hardlinked blockdevices
- fate#310510 - fix xenpaging
  xenpaging.paging_prep_enomem.patch
  - retry page-in if guest is temporary out-of-memory
  xenpaging.print-arguments.patch
  - print arguments passed to xenpaging
  xenpaging.machine_to_phys_mapping.patch
  - invalidate array during page deallocation
  xenpaging.autostart_delay.patch
  - fold xenpaging.enabled.patch into this patch
  - set xenpaging_delay to 0.0 to start xenpaging right away
* Fri Dec  3 2010 carnold@novell.com
- bnc#654591 - SLES11 SP0->Sp1 regression? (Xen, HVMs, NPIV)
  Fixed xen-qemu-iscsi-fix.patch
* Fri Dec  3 2010 cyliu@novell.com
- blktap2 patch - fix problem that blktap2 device info not cleared
  when block-attach fail.
  blktap2.patch
* Tue Nov 30 2010 carnold@novell.com
- bnc#655438 - Using performance counter in domU on Nehalem cpus
  22417-vpmu-nehalem.patch
- Upstream patches from Jan
  22389-amd-iommu-decls.patch
  22416-acpi-check-mwait.patch
  22431-p2m-remove-bug-check.patch
* Tue Nov 30 2010 carnold@novell.com
- bnc#656245 - VUL-1: hypervisor: application or kernel in any pv
  Xen domain can crash Xen
  x86_64-gdt-ldt-fault-filter.patch
* Mon Nov 29 2010 carnold@novell.com
- bnc#654050 - Python: a crasher bug in pyexpat - upstream patch
  needs backporting
  22235-lxml-validator.patch
* Tue Nov 23 2010 jfehlig@novell.com
- bnc#628729 - Add a small, fast alternative to 'xm list' for
  enumerating active domains.  xen-list is a C program that uses
  libxenstore and libxenctl directly, bypassing the python
  toolstack.
  xen-utils-0.1.tar.bz2
* Mon Nov 22 2010 jfehlig@novell.com
- bnc#628729 - Add a small, fast alternative to 'xm list' for
  enumerating active domains.  xen-list is a C program that uses
  libxenstore and libxenctl directly, bypassing the python
  toolstack.
  xen-utils-0.1.tar.bz2
* Fri Nov 19 2010 lidongyang@novell.com
- bnc#651822 - xm snapshot-xxx scripts lead to an XP SP3 HVM domU
  to chkdsk
  snapshot-xend.patch
  snapshot-ioemu-restore.patch
* Wed Nov 17 2010 carnold@novell.com
- bnc#651957 - Xen: vm-install failed to start
  xenpaging.enabled.patch
* Wed Nov 17 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.signal_handling.patch
  - unlink pagefile in signal handler
* Fri Nov 12 2010 carnold@novell.com
- Upstream patch for python 2.7 compatibility
  22045-python27-compat.patch
* Thu Nov 11 2010 cyliu@novell.com
- bnc#641144 - FV Xen VM running windows or linux cannot write to
  virtual floppy drive
  bdrv_default_rwflag.patch
* Thu Nov 11 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.optimize_p2m_mem_paging_populate.patch
  xenpaging.HVMCOPY_gfn_paged_out.patch
* Thu Nov 11 2010 carnold@novell.com
- bnc#649864 - automatic numa cpu placement of xen conflicts with
  cpupools
  22326-cpu-pools-numa-placement.patch
* Wed Nov 10 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.populate_only_if_paged.patch
  - revert logic, populate needs to happen unconditionally
  xenpaging.p2m_mem_paging_populate_if_p2m_ram_paged.patch
  - invalidate current mfn only if gfn is not in flight or done
  xenpaging.mem_event_check_ring-free_requests.patch
  - print info only if 1 instead of 2 slots are free
  xenpaging.guest_remove_page.patch
  - check mfn before usage in resume function
  xenpaging.machine_to_phys_mapping.patch
  - check mfn before usage in resume function
* Tue Nov  9 2010 jfehlig@novell.com
- bnc#552115 - Remove target discovery in block-iscsi
  modified block-iscsi script
* Mon Nov  8 2010 jfehlig@novell.com
- bnc#649277 - Fix pci passthru in xend interface used by libvirt
  22369-xend-pci-passthru-fix.patch
* Sun Nov  7 2010 lidongyang@novell.com
- bnc#642078 - xm snapshot-create causes qemu-dm to SEGV
  snapshot-without-pv-fix.patch
* Fri Nov  5 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.num_pages_equal_max_pages.patch
* Fri Nov  5 2010 carnold@novell.com
- bnc#647681 - L3: Passthrough of certain PCI device broken after
  SLES 11 to SP1 upgrade
- bnc#650871 - Regression in Xen PCI Passthrough
  22348-vtd-check-secbus-devfn.patch
- Upstream patches from Jan
  22223-vtd-workarounds.patch (bnc#652935)
  22231-x86-pv-ucode-msr-intel.patch
  22232-x86-64-lahf-lm-bios-workaround.patch
  22280-kexec.patch
  22337-vtd-scan-single-func.patch
* Wed Nov  3 2010 carnold@novell.com
- bnc#497149 - SLES11 64bit Xen - SLES11 64bit HVM guest has
  corrupt text console
  stdvga-cache.patch
* Wed Nov  3 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.page_already_populated.patch
  xenpaging.notify_policy_only_once.patch
  xenpaging.guest_remove_page.patch
  xenpaging.machine_to_phys_mapping.patch
  remove xenpaging.memory_op.patch, retry loops are not needed
* Tue Nov  2 2010 carnold@novell.com
- bnc#474789 - xen-tools 3.3 rpm misses pv-grub
- PV-GRUB replaces PyGrub to boot domU images safely: it runs the
  regular grub inside the created domain itself and uses regular
  domU facilities to read the disk / fetch files from network etc.;
  it eventually loads the PV kernel and chain-boots it.
* Wed Oct 27 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.doc.patch
- add /var/lib/xen/xenpaging directory
* Wed Oct 27 2010 ksrinivasan@novell.com
- Some cleanup in the APIC handling code in the HyperV shim.
  hv_apic.patch
* Wed Oct 27 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.memory_op.patch, correct delay handling in retry loop
* Wed Oct 27 2010 cyliu@novell.com
- bnc#640370 - VM graphic console in VNC is corrupted
  xenfb_32bpp.patch
* Fri Oct 22 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.autostart_delay.patch
  delay start of xenpaging 7 seconds for smooth BIOS startup
* Wed Oct 20 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.tools_xenpaging_cleanup.patch
* Wed Oct 20 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.mem_event_check_ring-free_requests.patch
* Wed Oct 20 2010 ohering@suse.de
- install /etc/xen/examples/xentrace_formats.txt to get human readable
  tracedata if xenalyze is not used
* Sun Oct 17 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.autostart_delay.patch
  xenpaging.blacklist.patch
  xenpaging.MRU_SIZE.patch
  remove xenpaging.hacks.patch, realmode works
* Mon Oct 11 2010 carnold@novell.com
- Upstream patches from Jan including fixes for the following bugs
  bnc#583568 - Xen kernel is not booting
  bnc#615206 - Xen kernel fails to boot with IO-APIC problem
  bnc#640773 - Xen kernel crashing right after grub
  bnc#643477 - issues with PCI hotplug/hotunplug to Xen driver domain
  22222-x86-timer-extint.patch
  22214-x86-msr-misc-enable.patch
  22213-x86-xsave-cpuid-check.patch
  22194-tmem-check-pv-mfn.patch
  22177-i386-irq-safe-map_domain_page.patch
  22175-x86-irq-enter-exit.patch
  22174-x86-pmtimer-accuracy.patch
  22160-Intel-C6-EOI.patch
  22159-notify-evtchn-dying.patch
  22157-x86-debug-key-i.patch
* Mon Oct 11 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.signal_handling.patch
  xenpaging.autostart.patch
  xenpaging.hacks.patch
* Mon Oct 11 2010 ohering@suse.de
- rename xenpaging.XENMEM_decrease_reservation.patch
  to xenpaging.memory_op.patch
* Fri Oct  8 2010 cyliu@novell.com
- bnc#632956 - fix VNC altgr-insert behavior
  7410-qemu-alt-gr.patch
  altgr_2.patch
* Thu Oct  7 2010 jfehlig@novell.com
- bnc#618087 - VNC view won't stay connected to fully virtualized
  Linux Xen VMs
  modified ioemu-vnc-resize.patch
* Tue Oct  5 2010 carnold@novell.com
- bnc#639546 - Dom-U deleted after introduction of the parameter
  "change_home_server False" in the VM configuration
  change_home_server.patch
* Mon Oct  4 2010 jfehlig@novell.com
- bnc#641859 - block-dmmd script does not handle the configuration
  when only MD is used
  modified block-dmmd script
* Thu Sep 30 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.populate_only_if_paged.patch
* Mon Sep 27 2010 carnold@novell.com
- bnc#640773 - Xen kernel crashing right after grub
  21894-intel-unmask-cpuid.patch
- Upstream patch from Jan
  22148-serial-irq-dest.patch
* Thu Sep 23 2010 cyliu@novell.com
- bnc#628719 - improve check_device_status to handle HA cases
  check_device_status.patch
* Thu Sep 23 2010 cyliu@novell.com
- bnc#628719 - multi-xvdp
  mutli-xvdp.patch
* Wed Sep 22 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.XENMEM_decrease_reservation.patch
  xenpaging.xenpaging_init.patch
  xenpaging.policy_linear.patch
* Mon Sep 20 2010 cyliu@novell.com
- bnc#632956 - fix VNC altgr-insert behavior
  7410-qemu-alt-gr.patch
  altgr_2.patch
* Fri Sep 17 2010 ohering@suse.de
- fate#310510 - fix xenpaging
  xenpaging.pageout_policy.patch
  xenpaging.xs_daemon_close.patch
  xenpaging.pagefile.patch
  xenpaging.mem_paging_tool_qemu_flush_cache.patch
  xenpaging.get_paged_frame.patch
  xenpaging.notify_via_xen_event_channel.patch
* Mon Sep 13 2010 carnold@novell.com
- bnc#636231 - XEN: Unable to disconnect/remove CDROM drive from VM
  xend-devid-or-name.patch
* Mon Sep 13 2010 carnold@novell.com
- Upstream patches from Jan
  22019-x86-cpuidle-online-check.patch
  22051-x86-forced-EOI.patch
  22067-x86-irq-domain.patch
  22068-vtd-irte-RH-bit.patch
  22071-ept-get-entry-lock.patch
  22084-x86-xsave-off.patch
* Mon Sep 13 2010 carnold@novell.com
- bnc#638465 - hypervisor panic in memory handling
  22135-heap-lock.patch
* Fri Sep 10 2010 carnold@novell.com
- Update to Xen 4.0.1.  This is a bug fix release.
* Thu Sep  9 2010 jfehlig@novell.com
- bnc#635380 - Fix pygrub Grub2 support
  See update to Xen 4.0.1 for fixes
* Fri Aug 27 2010 cyliu@novell.com
- bnc#628701 - Improve performance when activate/deactivate dmmd
  devices
  modified block-dmmd script
* Wed Aug 25 2010 jfehlig@novell.com
- bnc#628701 - Fix qemu-dm handling of dmmd devices
  modified xen-qemu-iscsi-fix.patch
* Mon Aug 16 2010 carnold@novell.com
- bnc#626262 - Populate-on-demand memory problem on xen with hvm
  guest
  21971-pod-accounting.patch
* Mon Aug 16 2010 cyliu@novell.com
- bnc#584204 - xm usb-list broken
  usb-list.patch
* Thu Aug 12 2010 carnold@novell.com
- bnc#625520 - TP-L3: NMI cannot be triggered for xen kernel
  21926-x86-pv-NMI-inject.patch
* Mon Aug  9 2010 carnold@novell.com
- bnc#613529 - TP-L3: kdump kernel hangs when crash was initiated
  from xen kernel
  21886-kexec-shutdown.patch
* Mon Aug  2 2010 carnold@novell.com
- Upstream Intel patches to improve X2APIC handling.
  21716-iommu-alloc.patch
  21717-ir-qi.patch
  21718-x2apic-logic.patch
* Tue Jul 27 2010 jfehlig@novell.com
- bnc#623833 - Error in Xend-API method VM_set_actions_after_crash
  21866-xenapi.patch
* Tue Jul 27 2010 jfehlig@novell.com
- bnc#625003 - Fix vm config options coredump-{restart,destroy}
  Added hunk to xm-create-xflag.patch
* Mon Jul 26 2010 jfehlig@novell.com
- bnc#605186 - Squelch harmless error messages in block-iscsi
* Mon Jul 26 2010 jfehlig@novell.com
- bnc#623438 - Add ability to control SCSI device path scanning
  in xend
  21847-pscsi.patch
* Mon Jul 26 2010 carnold@novell.com
- Enable the packaging of create.dtd.  This is needed for when xm
  is configured to use xenapi.
* Wed Jul 21 2010 carnold@novell.com
- bnc#624285 - TP-L3: xen rdtsc emulation reports wrong frequency
  21445-x86-tsc-handling-cleanups-v2.patch
* Tue Jul 20 2010 carnold@novell.com
- bnc#623201 - drbd xvd will fail in new xen4 packages due to wrong
  popen2 arguments in blkif.py
  popen2-argument-fix.patch
* Thu Jul  8 2010 carnold@novell.com
- bnc#620694 - Xen yast vm-install for existing paravirtualized
  disk fails with UnboundLocalError: local variable 'dev_type'
  referenced before assignment
  21678-xend-mac-fix.patch
* Wed Jul  7 2010 carnold@novell.com
- bnc#586221 - cannot add DomU with USB host controller defined
  domu-usb-controller.patch (Chun Yan Liu)
* Tue Jul  6 2010 carnold@novell.com
- Upstream patches from Jan
  21151-trace-bounds-check.patch
  21627-cpuidle-wrap.patch
  21643-vmx-vpmu-pmc-offset.patch
  21682-trace-buffer-range.patch
  21683-vtd-kill-timer-conditional.patch
  21693-memevent-64bit-only.patch
  21695-trace-t_info-readonly.patch
  21698-x86-pirq-range-check.patch
  21699-p2m-query-for-type-change.patch
  21700-32on64-vm86-gpf.patch
  21705-trace-printk.patch
  21706-trace-security.patch
  21712-amd-osvw.patch
  21744-x86-cpufreq-range-check.patch
  21933-vtd-ioapic-write.patch
  21953-msi-enable.patch
* Fri Jun 25 2010 jsong@novell.com
- bnc#599550 - Xen cannot distinguish the status of 'pause'
  21723-get-domu-state.patch
* Tue Jun 22 2010 jfehlig@novell.com
- bnc#604611 - Do not store vif device details when vif config
  contains invalid mac address.
  21653-xend-mac-addr.patch
* Wed Jun 16 2010 carnold@novell.com
- linux pvdrv: generalize location of autoconf.h
  Fixes error because of missing autoconf.h when building os11.2
  Factory.
* Mon Jun 14 2010 carnold@novell.com
- bnc#609153 - xm migrate <domain_name> localhost -l fails on
  Windows VMs
  21615-dont-save-xen-heap-pages.patch
- Upstream fixes from Jan
  21446-iommu-graceful-generic-fail.patch
  21453-shadow-avoid-remove-all-after-teardown.patch
  21456-compat-hvm-addr-check.patch
  21492-x86-pirq-unbind.patch
  21526-x86-nehalem-cpuid-mask.patch
  21620-x86-signed-domain-irq.patch
* Mon Jun  7 2010 carnold@novell.com
- bnc#612189 - Clear APIC Timer Initial Count Register when masking
  timer interrupt
  21542-amd-erratum-411.patch
* Fri Jun  4 2010 carnold@novell.com
- bnc#610658 - XEN: PXE boot fails for fully virtualized guests -
  e1000 virtual nic. (see also bnc#484778)
  enable_more_nic_pxe.patch
* Tue May 25 2010 carnold@novell.com
- bnc#608191 - /var/adm/fillup-templates/sysconfig.xend from
  package xen-tools is no valid sysconfig file
  xend-sysconfig.patch
* Tue May 25 2010 carnold@novell.com
- bnc#608194 - /etc/xen/* config files are not packaged with
  noreplace
* Tue May 25 2010 carnold@novell.com
- bnc#569744 - SLE HVM guest clock/timezone is incorrect after
  reboot
  21460-xend-timeoffset.patch
* Tue May 25 2010 jfehlig@novell.com
- bnc#606882 - Allow spaces in vbd path names
  21459-block-script.patch
* Mon May 24 2010 jsong@novell.com
- bnc#591799 - The status of Caps Lock is incorrect in domU
  capslock_enable.patch
* Thu May 20 2010 carnold@novell.com
-  Upstream fixes from Jan including a fix for Intel's ATS issue
  21435-vmx-retain-global-controls.patch
  21406-x86-microcode-quiet.patch
  21421-vts-ats-enabling.patch
* Wed May 19 2010 carnold@novell.com
- bnc#607219 - AMD Erratum 383 workaround for Xen
  21408-amd-erratum-383.patch
* Wed May 19 2010 carnold@novell.com
- Added modprobe of evtchn to init.xend.  The kernel will also need
  to build evtchn as a module for this to be meaningful.
* Mon May 17 2010 carnold@novell.com
- bnc#603008 - On an 8 Socket Nehalem-EX system, the fix for 593536
  causes a hang during network setup.
- Upstream patches from Jan.
  21360-x86-mce-polling-disabled-init.patch
  21372-x86-cross-cpu-wait.patch
  21331-svm-vintr-during-nmi.patch
  21333-xentrace-t_info-size.patch
  21340-vtd-dom0-mapping-latency.patch
  21346-x86-platform-timer-wrap.patch
  21373-dummy-domain-io-caps.patch
* Wed May 12 2010 carnold@novell.com
- bnc#605182 - /etc/xen/scripts/xen-hotplug-cleanup: line 24: [:
  !=: unary operator expected
  21129-xen-hotplug-cleanup.patch
* Mon May 10 2010 carnold@novell.com
- bnc#599929 - Hot add/remove Kawela NIC device over 500 times will
  cause guest domain crash
  passthrough-hotplug-segfault.patch
* Fri May  7 2010 jfehlig@novell.com
- bnc#603583 - Fix migration of domUs using tapdisk devices
  21317-xend-blkif-util-tap2.patch
  suse-disable-tap2-default.patch
* Thu May  6 2010 carnold@novell.com
- Match upstreams cpu pools switch from domctl to sysctl
- Upstream replacements for two of our custom patches (to ease
  applying further backports)
- Fixed dump-exec-state.patch (could previously hang the system, as
  could - with lower probability - the un-patched implementation)
* Wed May  5 2010 carnold@novell.com
- bnc#593536 - xen hypervisor takes very long to initialize Dom0 on
  128 CPUs and 256Gb
  21272-x86-dom0-alloc-performance.patch
  21266-vmx-disabled-check.patch
  21271-x86-cache-flush-global.patch
* Tue May  4 2010 carnold@novell.com
- bnc#558815 - using multiple npiv luns with same wwpn/wwnn broken
- bnc#601104 - Xen /etc/xen/scripts/block-npiv script fails when
  accessing multiple disks using NPIV
  block-npiv
* Fri Apr 30 2010 carnold@novell.com
- bnc#595124 - VT-d can not be enabled on 32PAE Xen on Nehalem-EX
  platform
  21234-x86-bad-srat-clear-pxm2node.patch
  bnc#585371 - kdump fails to load with xen: locate_hole failed
  21235-crashkernel-advanced.patch
* Thu Apr 29 2010 carnold@novell.com
- bnc#588918 - Attaching a U-disk to domain's failed by
  "xm usb-attach"
  init.xend
* Wed Apr 21 2010 jfehlig@novell.com
- bnc#596442 - Preserve device config on domain start failure
  xend-preserve-devs.patch
* Tue Apr 20 2010 jfehlig@novell.com
- bnc#597770 - insserv reports a loop between xendomains and
  openais.  Remove openais from Should-Start in xendomains script.
* Fri Apr 16 2010 jfehlig@novell.com
- bnc#569194 - Tools-side fixes for tapdisk protocol specification
  blktap-script.patch
  ioemu-subtype.patch
  Modified xen-domUloader.diff
* Wed Apr 14 2010 carnold@novell.com
- Upstream bug fixes from Jan
  21089-x86-startup-irq-from-setup-gsi.patch
  21109-x86-cpu-hotplug.patch
  21150-shadow-race.patch
  21160-sysctl-debug-keys.patch
* Fri Apr  9 2010 jfehlig@novell.com
- Updated to Xen 4.0.0 FCS, changeset 21091
* Tue Apr  6 2010 jfehlig@novell.com
- Change default lock dir (when domain locking is enabled) to
  /var/lib/xen/images/vm_locks
- Support SXP config files in xendomains script
* Wed Mar 31 2010 carnold@novell.com
- Update to changeset 21087 Xen 4.0.0 RC9.
* Fri Mar 26 2010 carnold@novell.com
- Update to changeset 21075 Xen 4.0.0 RC8.
* Thu Mar 25 2010 jsong@novell.com
- bnc#584210 - xm usb-hc-destroy does not remove entry from xend
  del_usb_xend_entry.patch
* Tue Mar 23 2010 carnold@novell.com
- Update to changeset 21057 Xen 4.0.0 RC7.
* Wed Mar 17 2010 jsong@novell.com
-Fix bnc#466899 - numa enabled xen fails to start/create vms
  adjust_vcpuaffinity_more_cpu.patch
* Tue Mar  9 2010 carnold@novell.com
- Update to changeset 21022 Xen 4.0.0 RC6.
* Tue Mar  9 2010 carnold@novell.com
- bnc#586510 - cpupool fixes
  cpu-pools-update.patch
* Fri Mar  5 2010 carnold@novell.com
- bnc#582645 - Xen stuck, mptbase driver attempting to reset config
  request
* Mon Mar  1 2010 carnold@novell.com
- Update to changeset 20990 Xen 4.0.0 RC5.
* Mon Feb 22 2010 jfehlig@novell.com
- bnc#556939 - Improve device map cleanup code in domUloader
* Sun Feb 21 2010 jfehlig@novell.com
- bnc# 578910 - xm block-detach does not cleanup xenstore
  hotplug-cleanup-fix.patch
* Fri Feb 19 2010 carnold@novell.com
- bnc#579361 - Windows Server 2003 cannot wake up from stand by in
  sp1
  hibernate.patch
* Fri Feb 19 2010 carnold@novell.com
- fate#308852: XEN CPU Pools
  cpupools-core.patch
  cpupools-core-fixup.patch
  keyhandler-alternative.patch
  cpu-pools-libxc.patch
  cpu-pools-python.patch
  cpu-pools-libxen.patch
  cpu-pools-xmtest.patch
  cpu-pools-docs.patch
* Thu Feb 18 2010 ksrinivasan@novell.com
- bnc#558760: Disable scsi devices when PV drivers are loaded.
* Tue Feb 16 2010 carnold@novell.com
- Update to changeset 20951 Xen 4.0.0 RC4 for sle11-sp1 beta5.
* Mon Feb  8 2010 carnold@novell.com
- bnc#572146 - SLES11 SP1 beta 2 Xen - BUG: soft lockup - CPU#31
  stuck for 61s! [kstop/31:4512]
  cpuidle-hint-v3.patch
* Fri Feb  5 2010 carnold@novell.com
- Update to changeset 20900 RC2+ for sle11-sp1 beta4.
* Fri Jan 29 2010 carnold@novell.com
- bnc#573376 - OS reboot while create DomU with Windows CD
* Wed Jan 27 2010 carnold@novell.com
- bnc#573881 - /usr/lib64/xen/bin/qemu-dm is a broken link
* Thu Jan 21 2010 carnold@novell.com
- Update to changeset 20840 RC1+ for sle11-sp1 beta3.
* Thu Jan 21 2010 jfehlig@novell.com
- bnc#569581 - SuSEfirewall2 should handle rules.  Disable
  handle_iptable in vif-bridge script
  vif-bridge-no-iptables.patch
* Wed Jan 20 2010 carnold@novell.com
- bnc#569577 - /etc/modprove.d/xen_pvdrivers, installed by
  xen-kmp-default, to ../xen_pvdrivers.conf
* Wed Jan  6 2010 ksrinivasan@novell.com
- bnc#564406 - Make the new PV drivers work with older hosts that
  do not understand the new PV driver protocol.
* Fri Dec 11 2009 carnold@novell.com
- Upstream Xen version renamed to 4.0.0 in changeset 20624 & 20625.
* Wed Dec  9 2009 carnold@novell.com
- fate#307594: HP-MCBS: XEN: support NR_CPUS=256
  This is a spec file change (xen.spec)
* Thu Dec  3 2009 carnold@novell.com
- bnc#555152 - "NAME" column in xentop (SLES11) output limited to
  10 characters unlike SLES10
  The update to c/s 20572 includes this fix (at c/s 20567).
* Tue Dec  1 2009 wkong@novell.com
- Modify xen-paths.diff
* Tue Dec  1 2009 wkong@novell.com
- Merge xend-tap-fix.patch to xen-domUloader.diff
  remove part of it which accepted by upstream
* Tue Dec  1 2009 jfehlig@novell.com
- Load gntdev module in xend init script similar to blkbk,
  netbk, etc.
* Thu Nov 26 2009 wkong@novell.com
- Backport dmmd from sles11/xen
  block-dmmd
  xen-qemu-iscsi-fix.patch
  xen.spec
* Thu Nov 26 2009 wkong@novell.com
- Fix regression when create_vbd for tap
  xend-tap-fix.patch
* Tue Nov 24 2009 carnold@novell.com
- Temporarily disable libxl because of libconfig dependency.
* Thu Nov 19 2009 wkong@novell.com
- fate#302864 domUloader support lvm in disk
  domUloader.py
  Note: for test in Beta1, if not good, remove it
* Thu Nov 19 2009 wkong@novell.com
- fate#302864 domUloader support fs on whole disk
  domUloader.py
* Fri Nov  6 2009 carnold@suse.de
- Turn KMPs back on now that kernel side fix is checked in.
* Tue Oct 20 2009 jfehlig@novell.com
- fate#304415 VMM: ability to switch networking mode
  Add vif-route-ifup to handle routed configurations using
  sysconfig scripts.
  vif-route-ifup.patch
* Mon Oct 19 2009 jsong@novell.com
- fate#307540 USB for Xen VMs
  usb-add.patch
* Mon Oct 19 2009 jsong@novell.com
- fate#305545 XEN extra descriptive field within xenstore
  add_des.patch
* Mon Oct 12 2009 carnold@novell.com
- Update to Xen version 3.5.0 for the following features.
  fate#304226 XEN: FlexMigration feature of VT-x2 support
  fate#305004 Add SR-IOV PF and VF drivers to Vt-d enabled Xen
  fate#306830 T states in Xen controlling by MSR
  fate#306832 Fix for xen panic on new processors
  fate#306833 Westmere and Nehalem-EX: Add support for Pause Loop exiting feature for Xen
  fate#306835 Xen: server virtual power management enhacement
  fate#306837 VT-d2 - PCI SIG ATS support
  fate#306872 Xen: Node manager support P/T-states change when Vt-d enable
  fate#306873 Xen: SMP guest live migration may fail with hap=1 on NHM
  fate#306875 Westmere: LT-SX (Xen)
  fate#306891 RAS features for Xen: Add support for Machine Check and CPU/Memory online/offline features
  fate#307322 1GB page support in Xen
  fate#307324 Xen IOMMU support
* Fri Oct  9 2009 carnold@novell.com
- bnc#541945 - xm create -x command does not work in SLES 10 SP2 or
  SLES 11
  xm-create-xflag.patch
* Thu Oct  8 2009 jfehlig@novell.com
- Minor enhancement to xen-updown.sh sysconfig hook
* Mon Sep 28 2009 wkong@novell.com
- Add patch ioemu-bdrv-open-CACHE_WB.patch
  for install guest on tapdisk very very slow.
* Fri Sep 25 2009 jfehlig@novell.com
- Add temporary workaround for race between xend writing and
  qemu-dm reading from xenstore.  The issue is preventing PV
  domUs from booting as they have no backend console.
  qemu-retry-be-status.patch
- bnc#520234 - npiv does not work with XEN
  Update block-npiv
- bnc#496033 - Support for creating NPIV ports without starting vm
  block-npiv-common.sh
  block-npiv-vport
  Update block-npiv
- bnc#500043 - Fix access to NPIV disk from HVM vm
  Update xen-qemu-iscsi-fix.patch
* Tue Sep 15 2009 jfehlig@novell.com
- bnc#513921 - Xen doesn't work get an eror when starting the
  install processes or starting a pervious installed DomU
  20125-xc-parse-tuple-fix.patch
* Wed Sep  2 2009 carnold@novell.com
- bnc#536176 - Xen panic when using iommu after updating hypervisor
  19380-vtd-feature-check.patch
* Fri Aug 28 2009 jfehlig@novell.com
- bnc#530959 - virsh autostart doesn't work
  Fixing this libvirt bug also required fixing xend's op_pincpu
  method with upstream c/s 19580
  19580-xend-pincpu.patch
* Fri Aug 28 2009 jbeulich@novell.com
- bnc#534146 - Xen: Fix SRAT check for discontig memory
  20120-x86-srat-check-discontig.patch
* Mon Aug 24 2009 carnold@novell.com
- bnc#491081 - Xen time goes backwards x3950M2
  20112-x86-dom0-boot-run-timers.patch
* Mon Aug 10 2009 ro@suse.de
- disable module build for ec2 correctly to fix build
  (at the suse_kernel_module_package macro)
* Mon Aug 10 2009 ksrinivasan@novell.com
- bnc#524071 - implemented workaround for a windows7 bug.
  hv_win7_eoi_bug.patch
* Mon Aug  3 2009 jfehlig@novell.com
- bnc#524180 - xend memory leak resulting in long garbage collector
    runs
  20013-xend-memleak.patch
* Fri Jul 31 2009 carnold@novell.com
- Upstream bugfixes from Jan.
  19896-32on64-arg-xlat.patch
  19960-show-page-walk.patch
  19945-pae-xen-l2-entries.patch
  19953-x86-fsgs-base.patch
  19931-gnttblop-preempt.patch
  19885-kexec-gdt-switch.patch
  19894-shadow-resync-fastpath-race.patch
- hvperv shim patches no longer require being applied conditionally
* Wed Jul 29 2009 jfehlig@novell.com
- bnc#520234 - npiv does not work with XEN in SLE11
  Update block-npiv
- bnc#496033 - Support for creating NPIV ports without starting vm
  block-npiv-common.sh
  block-npiv-vport
  Update block-npiv
- bnc#500043 - Fix access to NPIV disk from HVM vm
  Update xen-qemu-iscsi-fix.patch
* Wed Jul 15 2009 carnold@novell.com
- Don't build the KMPs for the ec2 kernel.
* Thu Jul  2 2009 jfehlig@novell.com
- Upstream fixes from Jan Beulich
  19606-hvm-x2apic-cpuid.patch
  19734-vtd-gcmd-submit.patch
  19752-vtd-srtp-sirtp-flush.patch
  19753-vtd-reg-write-lock.patch
  19764-hvm-domain-lock-leak.patch
  19765-hvm-post-restore-vcpu-state.patch
  19767-hvm-port80-inhibit.patch
  19768-x86-dom0-stack-dump.patch
  19770-x86-amd-s3-resume.patch
  19801-x86-p2m-2mb-hap-only.patch
  19815-vtd-kill-correct-timer.patch
- Patch from Jan Beulich to aid in debugging bnc#509911
  gnttblop-preempt.patch
* Tue Jun 23 2009 wkong@novell.com
- bnc#515220 - qemu-img-xen snapshot Segmentation fault
  qemu-img-snapshot.patch update
* Tue Jun  9 2009 wkong@novell.com
- bnc#504491 - drop write data when set read only disk in xen config
  bdrv_open2_fix_flags.patch
  bdrv_open2_flags_2.patch
* Fri Jun  5 2009 carnold@novell.com
- Upstream fixes from Jan Beulich.
  19474-32on64-S3.patch
  19490-log-dirty.patch
  19492-sched-timer-non-idle.patch
  19493-hvm-io-intercept-count.patch
  19505-x86_64-clear-cr1.patch
  19519-domctl-deadlock.patch
  19523-32on64-restore-p2m.patch
  19555-ept-live-migration.patch
  19557-amd-iommu-ioapic-remap.patch
  19560-x86-flush-tlb-empty-mask.patch
  19571-x86-numa-shift.patch
  19578-hvm-load-ldt-first.patch
  19592-vmx-exit-reason-perfc-size.patch
  19595-hvm-set-callback-irq-level.patch
  19597-x86-ioport-quirks-BL2xx.patch
  19602-vtd-multi-ioapic-remap.patch
  19631-x86-frametable-map.patch
  19653-hvm-vcpuid-range-checks.patch
* Fri Jun  5 2009 jsong@novell.com
- bnc#382112 - Caps lock not being passed to vm correctly.
  capslock_enable.patch
* Wed May 27 2009 jfehlig@novell.com
- bnc#506833 - Use pidof in xend and xendomains init scripts
* Wed May 27 2009 jsong@novell.com
- bnc#484778 - XEN: PXE boot of FV domU using non-Realtek NIC fails
  enable_more_nic_pxe.patch
* Wed May 27 2009 jsong@novell.com
  cross-migrate.patch
- bnc#390961 - cross-migration of a VM causes it to become
  unresponsive (remains paused after migration)
* Tue May 19 2009 carnold@novell.com
- Patches taken to fix the xenctx tool. The fixed version of this
  tool is needed to debug bnc#502735.
  18962-xc_translate_foreign_address.patch
  18963-xenctx.patch
  19168-hvm-domctl.patch
  19169-remove-declare-bitmap.patch
  19170-libxc.patch
  19171-xenctx.patch
  19450-xc_translate_foreign_address.patch
* Mon May 18 2009 wkong@novell.com
-bnc#485770 - check exsit file for save and snapshot-create
  xm-save-check-file.patch
  snapshot-xend.patch
* Mon May 18 2009 wkong@novell.com
-bnc#503782 - Using converted vmdk image does not work
  ioemu-tapdisk-compat-QEMU_IMG.patch
* Thu May 14 2009 jfehlig@novell.com
- bnc#503332 - Remove useless qcow tools
  /usr/sbin/{qcow-create,img2qcow,qcow2raw} from xen-tools package.
* Wed May 13 2009 jsong@novell.com
- bnc#474738 - adding CD drive to VM guest makes it unbootable.
  parse_boot_disk.patch
* Mon May 11 2009 wkong@novell.com
- bnc#477892 - snapshot windows can't accomplish.
  snapshot-xend.patch
* Tue Apr 28 2009 carnold@novell.com
- bnc#495300 - L3: Xen unable to PXE boot Windows based DomU's
  18545-hvm-gpxe-rom.patch, 18548-hvm-gpxe-rom.patch
* Mon Apr 27 2009 jfehlig@novell.com
- bnc#459836 - Fix rtc_timeoffset when localtime=0
  xend-timeoffset.patch
* Wed Apr 22 2009 carnold@novell.com
- bnc#497440 - xmclone.sh script incorrectly handles networking for
  SLE11.
* Fri Apr 17 2009 wkong@novell.com
- bnc#477890 - VM becomes unresponsive after applying snapshot
* Wed Apr 15 2009 jfehlig@novell.com
- bnc#494892 - Update xend-domain-lock.patch to flock the lock
    file.
* Wed Apr  8 2009 ksrinivasan@novell.com
- bnc#439639 - SVVP Test 273 System - Sleep Stress With IO" fails
  Turned off s3/s4 sleep states for HVM guests.
* Tue Apr  7 2009 jsong@novell.com
- bnc#468169 - fix domUloader to umount the mounted device mapper target in dom0
    when install a sles10 guest with disk = /dev/disk/by_path
* Thu Apr  2 2009 jfehlig@novell.com
- bnc#488490 - domUloader can't handle block device names with ':'
- bnc#486244 - vms fail to start after reboot when using qcow2
* Tue Mar 31 2009 carnold@novell.com
- bnc#490835 - VTd errata on Cantiga chipset
  19230-vtd-mobile-series4-chipset.patch
* Mon Mar 30 2009 carnold@novell.com
- bnc#482515 - Missing dependency in xen.spec
* Thu Mar 26 2009 carnold@novell.com
- Additional upstream bug fix patches from Jan Beulich.
  19132-page-list-mfn-links.patch
  19134-fold-shadow-page-info.patch
  19135-next-shadow-mfn.patch
  19136-page-info-rearrange.patch
  19156-page-list-simplify.patch
  19161-pv-ldt-handling.patch
  19162-page-info-no-cpumask.patch
  19216-msix-fixmap.patch
  19268-page-get-owner.patch
  19293-vcpu-migration-delay.patch
  19391-vpmu-double-free.patch
  19415-vtd-dom0-s3.patch
* Wed Mar 25 2009 carnold@novell.com
- Imported numerous upstream bug fix patches.
  19083-memory-is-conventional-fix.patch
  19097-M2P-table-1G-page-mappings.patch
  19137-lock-domain-page-list.patch
  19140-init-heap-pages-max-order.patch
  19167-recover-pat-value-s3-resume.patch
  19172-irq-to-vector.patch
  19173-pci-passthrough-fix.patch
  19176-free-irq-shutdown-fix.patch
  19190-pciif-typo-fix.patch
  19204-allow-old-images-restore.patch
  19232-xend-exception-fix.patch
  19239-ioapic-s3-suspend-fix.patch
  19240-ioapic-s3-suspend-fix.patch
  19242-xenstored-use-after-free-fix.patch
  19259-ignore-shutdown-deferrals.patch
  19266-19365-event-channel-access-fix.patch
  19275-19296-schedular-deadlock-fixes.patch
  19276-cpu-selection-allocation-fix.patch
  19302-passthrough-pt-irq-time-out.patch
  19313-hvmemul-read-msr-fix.patch
  19317-vram-tracking-fix.patch
  19335-apic-s3-resume-error-fix.patch
  19353-amd-migration-fix.patch
  19354-amd-migration-fix.patch
  19371-in-sync-L1s-writable.patch
  19372-2-on-3-shadow-mode-fix.patch
  19377-xend-vnclisten.patch
  19400-ensure-ltr-execute.patch
  19410-virt-to-maddr-fix.patch
* Mon Mar  9 2009 jfehlig@novell.com
- bnc#483565 - Fix block-iscsi script.
  Updated block-iscsi and xen-domUloader.diff
* Mon Mar  9 2009 carnold@novell.com
- bnc#465814 - Mouse stops responding when wheel is used in Windows
  VM.
  mouse-wheel-roll.patch (James Song)
- bnc#470704 - save/restore of windows VM throws off the mouse
  tracking.
  usb-save-restore.patch (James Song)
* Thu Mar  5 2009 jfehlig@novell.com
- bnc#436629 - Use global vnc-listen setting specified in xend
  configuration file.
  xend-vnclisten.patch
- bnc#482623 - Fix pygrub to append user-supplied 'extra' args
  to kernel args.
  19234_pygrub.patch
* Thu Mar  5 2009 carnold@novell.com
- bnc#481161 upgrade - sles10sp2 to sles11 upgrade keeps
  xen-tools-ioemu
* Tue Mar  3 2009 kukuk@suse.de
- Don't load 8139* driver if xen-vnif works [bnc#480164]
* Fri Feb 27 2009 carnold@novell.com
- bnc#480164 - Default network proposal in fully virtualized
  SLES 11 VM is invalid.
  xen_pvdrivers
* Thu Feb 26 2009 carnold@novell.com
- bnc#474822 - L3: Win2003 i386 XEN VM can see only 2 TB with a
  4TB LUN.
  int13_hardisk-64bit-lba.patch
* Wed Feb 25 2009 jfehlig@novell.com
- bnc#477890 - Destroy domain if snapshot restore fails.
  Updated snapshot-xend.patch
* Tue Feb 24 2009 ksrinivasan@novell.com
- bnc#470238 - SLE11 32FV guest is hanging during certification
  tests.
  bnc#468265 - Xen guest shows duplicate drives
  bnc#469598 - SLES11 RC2 64bit Xen - SLES11 full virt guests
  hanging under load.
  disable_emulated_device.diff
* Tue Feb 24 2009 kwolf@suse.de
- bnc#477892 - Disable xend timeout for snapshots
  Updated snapshot-xend.patch
* Tue Feb 24 2009 kwolf@suse.de
- bnc#477895 - Fix detaching blktap disks from domains without
  device model
  Updated blktap-ioemu-close-fix.patch
* Fri Feb 20 2009 kwolf@suse.de
- bnc#472390 - Enable debuginfo for ioemu
  ioemu-debuginfo.patch
* Thu Feb 19 2009 carnold@novell.com
- bnc#473883 - Xen: 64 bit guest crashes with qemu-dm segfault
  qemu-dm-segfault.patch
* Wed Feb 18 2009 jfehlig@novell.com
- bnc#437776 - Remove tracing (bash -x) from network-nat script
  network-nat.patch
* Wed Feb 18 2009 jfehlig@novell.com
- bnc#473815 - Handle NULL return when reading a xenstore path.
  Updated blktap-error-handling.patch
* Wed Feb 18 2009 kwolf@suse.de
- Fix VHD image support for > 4 GB (offsets truncated to 32 bits)
  ioemu-vpc-4gb-fix.patch
* Thu Feb 12 2009 ksrinivasan@novell.com
- bnc#468660 - Fix migration from sles10 to sles11 on Intel.
  old-arbytes.patch
* Thu Feb 12 2009 carnold@novell.com
- bnc#473800 - If VT-d is enabled, Dom0 fails to boot up on
  Nehalem-HEDT platform.
  19198-fix-snoop.patch
  19154-snoop-control.patch
* Thu Feb  5 2009 jfehlig@novell.com
- bnc#470133 - Better error handling in xm when not booted Xen
  19153-xm-noxen-error.patch
* Wed Feb  4 2009 kwolf@suse.de
- bnc#472075 - Fix ioemu to initialize its blktap backend also for
  fully virtualized guests
  ioemu-blktap-fv-init.patch
* Tue Feb  3 2009 jfehlig@novell.com
- bnc#470855 - Add note to xm man page on how to detach domain
  console
  19152-xm-man-page.patch
* Mon Feb  2 2009 jfehlig@novell.com
- bnc#471090 - XendAPIStore: Do not remove non-existent item
  class list
  19151-xend-class-dereg.patch
* Mon Feb  2 2009 carnold@novell.com
- bnc#470949 - user mode application may crash kernel
  19088-x86-page-non-atomic-owner.patch (Jan Beulich)
  19089-x86_64-widen-page-refcounts.patch
  19103-x86_64-fold-page-lock.patch
  x86_64-page-info-pack.patch
  x86_64-sh-next-shadow.patch
* Fri Jan 23 2009 carnold@novell.com
- Intel - Remove improper operating condition that results in a
  machine check.
  19072-vmx-pat.patch
  19079-snp_ctl-1.patch
* Fri Jan 23 2009 kwolf@suse.de
- bnc#465379 - Fix blktap error handling
  blktap-error-handling.patch
* Thu Jan 22 2009 carnold@novell.com
- bnc#435219 - XEN pv-driver doesn't work
* Thu Jan 22 2009 jbeulich@novell.com
- Fix unmaskable MSI handling.
  18778-msi-irq-fix.patch
* Wed Jan 21 2009 jfehlig@novell.com
- bnc#467883 - Squelch output of xen-updown.sh sysconfig hook
  script and don't save state of tap devices not belonging to Xen.
* Wed Jan 21 2009 carnold@novell.com
- bnc#467807 - Xen: IRQs stop working
  xen-ioapic-ack-default.diff
* Fri Jan 16 2009 carnold@novell.com
- bnc#447178 - xm dump-core does not work for cross-bitness guest.
  19046-cross-bit-coredumping.patch
  19048-cross-bit-coredumping.patch
  19051-cross-bit-coredumping.patch
* Thu Jan 15 2009 brieske@novell.com
- bnc#429637 - SSVP SMBIOS HCT Test failing
  19027-hvmloader-SMBIOS-dev-mem-boundary.patch
* Wed Jan 14 2009 carnold@novell.com
- bnc#460805 - Unable to boot with Xen kernel with IBM T42p / T41p
  19039-x86-propagate-nolapic.patch
  19038-x86-no-apic.patch
* Mon Jan  5 2009 carnold@novell.com
- bnc#435596 - dom0 S3 resume fails if disk drive is set as AHCI
  mode.
  18937-S3-MSI.patch
- Final Xen 3.3.1 FCS changeset 18546
* Mon Dec 29 2008 carnold@novell.com
- bnc#436021 - On PAE host with EPT enabled, booting a HVM guest
  with 4G memory will cause Xen hang.
  18943-amd-32bit-paging-limit.patch
* Mon Dec 22 2008 carnold@novell.com
- bnc#461596 - Failue to load 64-bit HVM Solaris 10U6 DomU with 2
  vcpus.  Update to RC4 contains fix in c/s 18538.
* Mon Dec 22 2008 jfehlig@novell.com
- bnc#379032 and bnc#404014 - Fix loop device leak in domUloader
* Wed Dec 17 2008 kwolf@suse.de
- bnc#456758 - Allow all block device types for which a script
  exists in /etc/xen/scripts besides file, tap and phy.
  reenable-block-protocols.patch
* Mon Dec 15 2008 carnold@novell.com
- Patch cleanup. Updated tarball with several of our stand-alone
  but now upstream patches (c/s 18536).
* Fri Dec  5 2008 kwolf@suse.de
- bnc#404014 - Fix memory leak in libxenguest during domain
  creation
  libxc-zlib-memleak.patch
* Thu Dec  4 2008 jfehlig@novell.com
- bnc#456511 - Fix domain name change after checkpoint/shutdown
  events.
* Tue Dec  2 2008 carnold@novell.com
- Fixed xmclone.sh. It calls lomount which no longer exists in the
  distro.
* Tue Nov 25 2008 kwolf@suse.de
- Fix the build. Build system seems to be unhappy about having two
  copies of the xenstore binary (this is not a proper fix in fact
  as the build error says the two files are not identical - they
  are hardlinks, so this seems unlikely to be the real cause).
  tmp_build.patch
* Mon Nov 24 2008 jfehlig@novell.com
- bnc#448364 - Fix cpu affinity on save/restore/migrate
* Thu Nov 20 2008 kwolf@suse.de
- bnc#444731 - Fix data corruption bug (caused by broken x86
  emulation for movnti instruction)
  xen-x86-emulate-movnti.patch
* Wed Nov 19 2008 kwolf@suse.de
- Report device model errors during the creation of snapshots
  to xend instead of failing silently
* Wed Nov 19 2008 kwolf@suse.de
- bnc#445659 - ioemu: Workaround for VNC client initialization
  race with xenfb changing the resolution (caused VNC connection
  to be closed, vm-install recognized this as failed installation)
  ioemu-vnc-resize.patch
* Tue Nov 18 2008 carnold@novell.com
- bnc#444203 - With EPT mode4, HVM S3 causes Xen HV crash.
  18783-hvm-vcpu-reset-state-fix.patch
* Mon Nov 17 2008 carnold@novell.com
- bnc#444731 - Blackscreen instead of second stage during
  installation
  18766-realmode-stack-size-fix.patch
* Thu Nov 13 2008 carnold@novell.com
- bnc#429739 - Network failure with bnx2 when booted to XEN
  18778-msi-irq-fix.patch
* Wed Nov 12 2008 kwolf@suse.de
- bnc#444197 - Add udev rule to fix domUloader race with
  automounter (udev-rules.patch)
* Sun Nov  9 2008 ro@suse.de
- disable kmp to fix build again
* Fri Nov  7 2008 kwolf@suse.de
- Fix merge damage which prevented disks to be snapshotted when
  not in disk-only snapshot mode
* Wed Nov  5 2008 kwolf@suse.de
- bnc#435195 - Fix error handling for blktap devices and ioemu;
  check for images smaller than a sector and abort (causes hangs
  of the complete blktap stack otherwise)
  ioemu-blktap-zero-size.patch
* Mon Nov  3 2008 plc@novell.com
- bnc#436572 - L3: vm serial port configuration and access is not
  persistent across dom0 reboot
* Wed Oct 29 2008 carnold@novell.com
- bnc#436926 - Xen hypervisor crash
* Tue Oct 28 2008 jfehlig@novell.com
- bnc#438927 - Fix migration bug in xend
* Tue Oct 28 2008 carnold@suse.de
- disable KMP, does not build with current kernel
* Fri Oct 24 2008 jfehlig@novell.com
- bnc#437756 - Fix default netdev device in network-route
* Wed Oct 22 2008 jfehlig@novell.com
- bnc#434560 - Remove local patch that prevents creating PV vif
  when "type=ioemu" is specified in guest vif config.  This patch
  is causing several problems with recent changes to xenstore
  layout.
* Wed Oct 22 2008 jfehlig@novell.com
- bnc#431758 - Added upstream changeset 18654 to prevent setting
  vcpus > VCPUs_max on running domain.
* Tue Oct 21 2008 carnold@novell.com
- Update to changeset 18455.
* Fri Oct 17 2008 olh@suse.de
- add ExclusiveArch x86 x86_64
* Wed Oct 15 2008 jfehlig@novell.com
- bnc#433722 - Fix handling of default bridge in qemu-ifup.
* Mon Oct 13 2008 carnold@novell.com
- bnc#431324 - Cannot boot from XEN kernel
* Mon Oct 13 2008 kwolf@suse.de
- blktapctrl: Close connection to tapdisk-ioemu only if there are
  no more attached disks
  blktap-ioemu-close-fix.patch
- blktapctrl: If tapdisk-ioemu has been shut down and a new
  instance is needed, fix saving the PID of the new instance
* Thu Oct  2 2008 jfehlig@novell.com
- bnc#431737 - Fix use of deprecated python constructs in xend
* Mon Sep 29 2008 carnold@novell.com
- Update to c/s 18430, remove our versions of upstream patches.
- fate#303867 - minimum HVM domain limits.  Pulled upstream
  patches for supporting up to 255 cpus.
* Fri Sep 26 2008 kwolf@suse.de
- bnc#430222 - Fixed block-attach for tap:aio images
* Thu Sep 25 2008 kwolf@suse.de
- bnc#429801 - Fixed xm start -c / --vncviewer
  xm-start-fix.patch
* Wed Sep 24 2008 carnold@novell.com
- bnc#382401 - xm man page missing information for commands.
* Wed Sep 17 2008 carnold@novell.com
- Pulled some upstream patches for Intel and AMD microcode fixes.
* Tue Sep 16 2008 carnold@novell.com
- Update to changeset 18412.  Contains several bug fixes including
  a crash fix in qemu-dm and also various memory leaks fixes.
* Mon Sep 15 2008 carnold@novell.com
- Fix parameters in call to kill_proc_info (pv drivers).
- Add conditional for use of smp_call_function so the pv drivers
  can be built on older kernel versions.
* Thu Sep 11 2008 brogers@novell.com
- Added gdbserver-xen to the set of tools we build.
  fate#302942
* Thu Sep 11 2008 jfehlig@novell.com
- Added ocfs2 to Should-Start in xendomains init script
* Wed Sep 10 2008 plc@novell.com
- Added pv cdrom support to blktap
  fate#300964
* Wed Sep 10 2008 jfehlig@novell.com
- Removed invocation of network-bridge script from xend-config.sxp.
  Networks are now created through yast2-network package.
- Added sysconfig hook script for Xen to cope with ifup/ifdown
  events on network devices (e.g. bridges) in use by virtual
  machines.
  fate#303386
* Mon Sep  8 2008 carnold@novell.com
- Updated to xen version 3.3.1 RC changeset 18390.
* Wed Sep  3 2008 kwolf@suse.de
- Snapshots: Fix xend API functions for libvirt usage
* Mon Sep  1 2008 carnold@novell.com
- Fix problems building KMPs against the 2.6.27 kernel.
* Fri Aug 29 2008 plc@novell.com
- Added 'tap' to the type of devices for HalDaemon.py to
  scan for change of xenstore attribute media-present.
* Wed Aug 27 2008 jfehlig@novell.com
- Don't create pv vif device if emulated network device is
  explicitly specified in guest config.
* Fri Aug 22 2008 carnold@novell.com
- Updated to xen-unstable changeset 18358 Xen 3.3.0 FCS.
* Wed Aug 20 2008 carnold@novell.com
- Updated to xen-unstable changeset 18353 RC7.
* Wed Aug 20 2008 kwolf@suse.de
- Implementation of xm snapshot-delete
  snapshot-ioemu-delete.patch, snapshot-xend.patch
- Add snapshot options to qemu-img-xen
  qemu-img-snapshot.patch
* Tue Aug 19 2008 carnold@novell.com
- Enable kboot and kexec patches.
* Mon Aug 18 2008 carnold@novell.com
- Updated to xen-unstable changeset 18335 RC5.
* Mon Aug 18 2008 carnold@suse.de
- Removed git dependency.  Instead use a static version of
  ioemu-remote.
* Thu Aug 14 2008 jfehlig@novell.com
- Added patch to prevent starting same domU from multiple hosts.
  Feature is disabled by default - see /etc/xen/xend-config.sxp.
  fate#305062
* Mon Aug 11 2008 jfehlig@novell.com
- Added python-openssl to Requires list for xen-tools.  This
  package is required if SSL relocation is enabled by user.
* Mon Aug 11 2008 carnold@novell.com
- Updated to xen-unstable changeset 18309. Pre 3.3.0-rc4.
* Sat Aug  9 2008 jfehlig@novell.com
- Disabled xend-relocation-ssl-server for now.  Certificates must
  be created and feature needs testing.
* Fri Aug  8 2008 carnold@novell.com
- Update to xen-unstable changeset 18269 post RC3.  Reverse
  version back to 3.3.0 from 4.0.0.
* Wed Aug  6 2008 carnold@novell.com
- Updated to xen-unstable changeset 18242.  Version changes from
  3.3.0 to 4.0.0
* Mon Aug  4 2008 carnold@novell.com
- Updated to xen-unstable changeset 18210. Post 3.3.0-rc2.
* Tue Jul  8 2008 carnold@novell.com
- Updated to xen-unstable changeset 17990.
* Tue Jul  8 2008 kwolf@suse.de
- ioemu: Write barriers for blktap devices
  ioemu-blktap-barriers.patch
* Thu Jul  3 2008 kwolf@suse.de
- blktapctrl defaults to using ioemu instead of tapdisk now
  blktapctrl-default-to-ioemu.patch
- Now that ioemu is default, it can be called with image paths
  starting e.g. with tap:qcow2. If the image format is specified,
  it has to be respected and no guessing on the image file must
  happen.
  ioemu-blktap-image-format.patch
- qcow2: Read/Write multiple sectors at once if possible to
  improve performance.
  ioemu-qcow2-multiblock-aio.patch
* Thu Jun 12 2008 kwolf@novell.com
- Add snapshot support to ioemu and blktapctrl
  snapshot-ioemu-save.patch
  snapshot-ioemu-restore.patch
* Fri Jun  6 2008 jfehlig@novell.com
- bnc#397890 - Create and own /var/lib/xen/dump
* Thu Jun  5 2008 kwolf@novell.com
- Fix tapdisk for qcow2 images > 2 GB
  1xxxx-qcow2-2gb-bug.patch
* Thu Jun  5 2008 jfehlig@novell.com
- Updated to xen-unstable changeset 17772.
* Tue May 27 2008 plc@novell.com
- bnc#381368 - boot qcow image fix.
* Fri May 23 2008 jfehlig@novell.com
- bnc#378595 - Revert patch that disables use of ifup/ifdown.
  ifup-bridge in sysconfig has been fixed so patch is no longer
  needed.  Calling ifdown on bridge now removes ports and deletes
  bridge, so network-bridge no longer needs to do these tasks.
* Fri May 16 2008 carnold@novell.com
- bnc#390985 - xm man page needs FIXME sections to be fixed
  xen-fixme-doc.diff
* Wed May 14 2008 carnold@novell.com
- bnc#375322 - L3:timer went backwards
  x86-domain-shutdown-latency.patch
* Sat May 10 2008 plc@novell.com
- bnc#388969 - Shift tab traversal does not work
  xen-shift-key.patch
- bnc#384277 - PVFB security hole
  xen-pvfb-security.patch
- bnc#385586 - VNC windows size too small
  xen-vnc-resize.patch
* Fri Apr 25 2008 carnold@novell.com
- bnc#383513 - Unknown unit 'K' in Xen's logrotate config file.
* Fri Apr 25 2008 carnold@novell.com
- Update to Xen 3.2.1 FCS changeset 16881.
* Fri Apr 11 2008 carnold@novell.com
- Update to Xen 3.2.1 RC5 changeset 16864.
* Thu Apr 10 2008 jfehlig@novell.com
- bnc#378595 - Do not use ifup/ifdown in network-bridge for now.
* Mon Mar 24 2008 carnold@novell.com
- bnc#373194 - The xen module and the kernel for Dom0 don't match.
- Add ncurses-devel build dependency
* Mon Mar 24 2008 carnold@novell.com
- Update to Xen 3.2.1 RC1 changeset 16820.
* Thu Mar 20 2008 coolo@suse.de
- 3.1.0 is unfortunately not enough to obsolete 3.1.0_<something>
  in rpm terms
* Fri Mar 14 2008 carnold@novell.com
- Update to Xen 3.2.1 changeset 16805.
* Fri Mar 14 2008 coolo@suse.de
- ipcalc does not exist - and breaks pattern
* Wed Mar 12 2008 jfehlig@novell.com
- Increased dom0-min-mem value to 512Mb in xend-config.sxp
  bnc#370007
* Mon Mar 10 2008 jfehlig@novell.com
- Fixed initialization of default VM config values when creating
  VMs through Xen API.  bnc#368273
* Mon Mar 10 2008 jfehlig@novell.com
- Removed unused/untested xend-relocation script.
* Fri Mar  7 2008 jfehlig@novell.com
- Set device model when creating pvfb consoles via XenAPI.
  bnc#367851
* Fri Mar  7 2008 jfehlig@novell.com
- Ensure dhcpcd is activated, if appropriate, on bridges created
  by network-multinet.  bnc#364633
* Fri Feb 29 2008 carnold@novell.com
- bnc#357966 - VT-D dosen't work for HVM guest.
* Fri Feb 29 2008 plc@novell.com
- Send UNIT_ATTENTION when CD drive has newly inserted media and
  becomes ready.  bnc#365386
* Thu Feb 28 2008 jfehlig@novell.com
- Updated block-iscsi script and xen-domUloader patch, bnc #365385
* Thu Feb 28 2008 carnold@novell.com
- Add support for Intel EPT / VPID.
* Tue Feb 26 2008 carnold@novell.com
- bnc#362415 - SLE-based installs 32-bit fully-virtualized have
  network problems during installs.
- bnc#358244 - Time remaining does not change properly for FV SLES10
  SP2 guest.
- bnc#363053 - Install remaining time always shows 2:00:00
* Tue Feb 26 2008 carnold@novell.com
- bnc#359457 - Xen full virt has data integrity issue.
* Tue Feb 26 2008 plc@novell.com
- Tranlate colors from 32 bit to 16 bit when viewing a 32 bit PV
  VM from a 16 bit client.  bnc#351470
  Also includes upstream mouse queue patch.
* Fri Feb 22 2008 jfehlig@novell.com
- Added PAM configuration files for remote authentication via
  Xen API.  bnc #353464
* Tue Feb 19 2008 carnold@novell.com
- Fix PV drivers for HVM guests.
* Fri Feb 15 2008 carnold@novell.com
- Support for pxe booting fully virtualized guests in vm-install is
  complete.
* Thu Feb 14 2008 carnold@novell.com
- Added upstream changesets that fix various bugs.
  16859 16929 16930 16945 16947 16962 16976 16980 16995 16998 17036
* Wed Feb 13 2008 jfehlig@novell.com
- Updated network-multinet
  - Simplify bridge creation
  - Create traditional bridge and hostonly networks by default
* Fri Feb  8 2008 jfehlig@novell.com
- Added upstream changesets 16932, 16965, 16977, and 16988 to fix
  various bugs in tool stack
- Also added upstream changeset 16989 to complete fate #302941.
* Mon Feb  4 2008 plc@novell.com
- Replaced xen-blktab-subtype-strip.patch with official upstream
  changeset for bnc#353065.
* Fri Feb  1 2008 carnold@novell.com
- Update to xen 3.2 FCS.  Changeset 16718
- Merge xen-tools and xen-tools-ioemu into xen-tools.
* Wed Dec 19 2007 carnold@novell.com
- Update to xen 3.2 RC2.  Changeset 16646
* Thu Dec 13 2007 carnold@novell.com
- Added agent support for HP Proliant hardware.
* Wed Dec  5 2007 carnold@novell.com
- #338108 - VUL-0: Xen security issues in SLE10
- #279062 - Timer ISR/1: Time went backwards
* Thu Nov 29 2007 carnold@novell.com
- Added part of upstream c/s 15211.  Fixed open call with O_CREAT
  because it had no mode flags (15211-fix-open-mode.patch).
* Mon Nov  5 2007 jfehlig@novell.com
- Added upstream c/s 15434 to allow access to serial devices.
  Bug #338486.
* Thu Nov  1 2007 carnold@novell.com
- #334445: xenbaked: Fix security vulnerability CVE-2007-3919.
* Thu Nov  1 2007 carnold@novell.com
- #310279: Kernel Panic while booting Xen
* Tue Oct  2 2007 ccoffing@novell.com
- #286859: Fix booting from SAN
* Thu Sep 13 2007 ccoffing@novell.com
- #310338: Fix "No such file or directory" in network-multinet
* Wed Sep 12 2007 jfehlig@novell.com
- #309940: Fix 'xm reboot'
- Moved hvm_vnc.diff and xend_mem_leak.diff to 'Upstream patches'
  section of spec file since both have been accepted upstream now.
* Mon Sep 10 2007 jfehlig@novell.com
- #289283: Fix memory leak in xend
* Fri Sep  7 2007 jfehlig@novell.com
- #297125: Expose 'type vnc' in vfb device sexp for HVM guests.
* Thu Sep  6 2007 ccoffing@novell.com
- #302106: Update network-multinet
* Wed Sep  5 2007 carnold@novell.com
- #307458: AMD-V CR8 intercept reduction for HVM windows 64b guests
* Wed Aug 29 2007 ccoffing@novell.com
- Update block-iscsi to match changes to open-iscsi.
* Mon Aug 27 2007 carnold@novell.com
- #289275 - domu will not reboot if pci= is passed in at boot time.
* Fri Aug 24 2007 carnold@novell.com
- #297345: Added several upstream patches for hvm migration.
* Fri Aug 17 2007 jfehlig@novell.com
- Added upstream c/s 15128, 15153, 15477, and 15716.  These patches
  provide foundation for bug #238986
- Renamed xend_dev_destroy_cleanup.patch to reflect the upstream
  c/s number and moved it to "upstream patches" section of spec
  file.
* Mon Aug 13 2007 carnold@novell.com
- hvm svm: Log into 'xm dmesg' that SVM NPT is enabled.
* Fri Aug 10 2007 ccoffing@novell.com
- Honor RPM_OPT_FLAGS better
* Thu Aug  9 2007 ccoffing@novell.com
- #298176: Do not enable NX if CPU/BIOS does not support it
- #289569: Modify network-bridge to handle vlan
- #297295: Fix bridge setup: stop using getcfg
* Tue Aug  7 2007 olh@suse.de
- remove inclusion of linux/compiler.h and linux/string.h
  remove ExclusiveArch and fix prep section for quilt setup *.spec
* Thu Aug  2 2007 jfehlig@novell.com
- Added patch to fix/cleanup destoryDevice code path in xend.
  Patch was submitted upstream.  Aids in fixing several bugs, e.g.
  [#217211] and #242953.
* Tue Jul 31 2007 ccoffing@novell.com
- Update Ron Terry's network-multi script
- Fix insserv
* Tue Jul 31 2007 jfehlig@novell.com
- Added following upstream patches:
  + 15642 - Fixes bug 289421 found in SLES10 SP1 but applies to
    Xen 3.1.0 as well.
  + 15649, 15650, 15651 - Fixes/enhancements to Xen API required
    by Xen CIM providers
* Fri Jul 27 2007 ccoffing@novell.com
- #242953: Allow HVM to use blktap
- #239173: block-attach as RW for domUloader to avoid failures with
  reiserfs (since blktap does not yet correctly communicate RO to
  the kernel)
* Mon Jul 23 2007 ccoffing@novell.com
- Drop xen-bootloader-dryrun.diff; not needed for xen 3.1
- rpmlint: Actually apply patch for #280637
- rpmlint: Rename logrotate config from xend to xen
- Don't package xenperf twice
- xen-detect is a domU tool
* Mon Jul 23 2007 jfehlig@novell.com
- Added upstream patches that fix various bugs
  + 15168 fixes check for duplicate domains
  + 15587 resets domain ID and fixes problems with domain state
    via Xen API
  + 15609 stores memory values changed via Xen API
* Thu Jul 19 2007 ccoffing@novell.com
- BuildRequires LibVNCServer-devel
- Rotate all logs.
- Fix network data corruption on Win2003 with rtl8139. (#254646)
- Xen fails to create VM due to "out of memory" errors. (#280637)
* Tue Jul 17 2007 plc@novell.com
- Added CDROM removable media patch from 3.0.4
* Fri Jul  6 2007 ccoffing@novell.com
- xensource bug #858: Disable strict aliasing for xenstore, to
  avoid domU hangs.
* Tue Jul  3 2007 ccoffing@novell.com
- #285929: Bad "xendomains status" output w/ empty XENDOMAINS_SAVE
* Tue Jul  3 2007 carnold@novell.com
- Changes necessary to support EDD and EDID from Jan.
* Wed Jun 20 2007 jfehlig@novell.com
- Added upstream changesets 15273, 15274, and 15275.
- Removed the modified 15157 patch.  This patch was actually a
  consolidation of changesets 15157 and 15250.  These changesets
  are now discrete patches to ease subsequent updates of Xen.
* Wed Jun 20 2007 ccoffing@novell.com
- Split vm-install off as a separate package.
- Update man page.
- Update Ron Terry's network-multi script.
* Mon Jun 18 2007 ccoffing@novell.com
- Fix compiler warnings.
- Update block-npiv.
* Mon Jun 11 2007 ccoffing@novell.com
- Fix more warn_unused_value compiler warnings.
* Fri Jun  8 2007 ccoffing@novell.com
- Update to official rc10 (changeset 15042).
- Updated vm-install:
  + easier to exit with Ctrl-C
  + drop "TERM=xterm" for Linux (breaks PVFB text install)
  + use "TERM=vt100" when calling "xm" to suppress terminal codes
  + command-line support for VNC password
  + fixed disk groups (e.g., 2 disks on command line w/o PDEV)
  + fixed regression:  Don't let user close progress window
  + failure to open a device should not completely fail search for
  bootsector (consider: no media in /dev/cdrom)
  + always remove PV kernel and initrd from /tmp
  + #279153: Support disks on iscsi/qcow/vmdk/nbd/file/phy/...
* Fri Jun  8 2007 jfehlig@novell.com
- Added a modified version of upstream c/s 15157.  Original version
  of c/s 15157 fixed bug #262805 but also broke
  'xm block-detach dom dev_name'.  Modified version fixes bug 262805
  without introducing regression.  Patch fixing c/s 15157 has been
  submitted upstream.
* Wed May 23 2007 ccoffing@novell.com
- Drop xen-messages.diff; Xen now supports HVM save/restore.
* Tue May 22 2007 ccoffing@novell.com
- Update Ron Terry's network-multi script.
- Drop xen-doc-ps.  (#267948)
- Update init scripts.
- Tidy spec file to fix rpmlint errors.
- Updated patches from Jan.
* Mon May 21 2007 ccoffing@novell.com
- vm-install bug fixes:
  + #211342: better progress bar
  + #259994: disk size would reset when editing path
  + #247073: handle autoyast URLs
  + #254311: physical disks were showing as 0.0 GB
* Wed May 16 2007 ccoffing@novell.com
- Properly quote pathnames in domUloader to fix EVMS.  (#274484)
- Allow user to specify a default 'keymap' in xend's configuration
  file. (#258818 and 241149)
* Mon May 14 2007 plc@novell.com
- Added upstream python patches for keymap specification in
  PV config file. Added upstream ALTGR fix, sign extension fix
  and modified patch 323 so that upstream patches applied cleanly.
  (#258818)
* Fri May 11 2007 ccoffing@novell.com
- Update to xen-3.1-testing rc10 (changeset 15040).
- Update .desktop with proper group.  (#258600)
- Include Kurt's updated block-iscsi.  (#251368)
- Jim's updated patch to honor localtime setting.  (#273430)
- Fix vm-install to work correctly when doing multiple simultaneous
  installs via virt-manager.  (#259917)
- Network connectivity fails in FV SLES 10 SP1; MAC address was
  being read incorrectly from xenstore by PV driver.  (#272351)
- For FV SLES 9, default apic=1 to allow x86_64 SLES 9 to boot.
  (#264183)
* Fri May  4 2007 carnold@novell.com
- Added security fixes for problems found Travis Orandy (#270621)
  CVE-2007-1320, CVE-2007-1321, CVE-2007-1322, CVE-2007-1323,
  CVE-2007-1366
* Thu May  3 2007 ccoffing@novell.com
- Update to xen-3.1-testing rc7 (changeset 15020).
- Fix identification of virt-manager windows.  (#264162)
* Tue May  1 2007 jfehlig@novell.com
- Integrated domUloader with 3.0.5.  Updated xen-domUloader.diff.
* Mon Apr 30 2007 ccoffing@novell.com
- Update to xen-3.0.5-testing rc4 (changeset 14993).
* Thu Apr 26 2007 jfehlig@novell.com
- Fixed autobuild error in function that returns random data.
  File tools/ioemu/hw/piix4acpi.c line 72.  Fix added to
  xen-warnings.diff.
* Thu Apr 26 2007 ccoffing@novell.com
- Fix build on SLES 10 SP1.
* Wed Apr 25 2007 ccoffing@novell.com
- Update to xen-3.0.5-testing rc3 (changeset 14934).
- Switch BuildRequires to texlive.
* Fri Apr 20 2007 ccoffing@novell.com
- Updated README. (#250705)
- Fix vm-install's detection of PV RHEL4/5 kernels. (#260983)
* Thu Apr 19 2007 ccoffing@novell.com
- Place xenstore-* tools in new xen-tools-domU package, to be used
  by suse_register.  (#249157)
* Tue Apr 17 2007 ccoffing@novell.com
- Update translations.
* Thu Apr 12 2007 ccoffing@novell.com
- Combine two xenstore reads into one transaction, which causes
  xenstored to not thrash so badly, and makes virt-manager more
  responsive and less likely to time out or lock up.  Partial fix
  for #237406.
- If disk is read-only, pass -r to losetup.  (#264158)
* Thu Apr  5 2007 ccoffing@novell.com
- Update vm-install:
  + #260510: do not delete xml settings file
  + #260579: write correct vif line for PV NIC in FV VM
  + #261288: re-enable add disk buttons after deleting a disk
  + #192272, #222765, #250618:  Update OS list and their defaults
* Tue Apr  3 2007 ccoffing@novell.com
- Could not do simultaneous installs via virt-manager. (#259917)
* Mon Apr  2 2007 jfehlig@novell.com
- Fix improper handling of guest kernel arguments in domUloader.
  Bug #259810
* Mon Apr  2 2007 ccoffing@novell.com
- Update vm-install:
  + #259420: refresh available memory more often
  + #259972: cannot enter autoyast url
* Mon Apr  2 2007 ccoffing@novell.com
- Update translations for RC2.
* Fri Mar 30 2007 ccoffing@novell.com
- Fix "cannot allocate memory" when starting VMs. (#229849, 258743)
* Thu Mar 29 2007 ccoffing@novell.com
- Fix quoting of args for child processes during VM install.
  (#258376)
- Fix retry logic in block hotplug script. (#257925)
* Wed Mar 28 2007 ccoffing@novell.com
- Updated vm-install's icon name.
- Updated translations.
* Fri Mar 23 2007 ccoffing@novell.com
- Disable aspects of qemu's console that can affect domain 0.
  (#256135)
- Fix xmclone.sh to work with managed domains. (#253988)
- Update to xen-unstable changeset 14535.
* Mon Mar 19 2007 ccoffing@novell.com
- Update to xen-unstable changeset 14444.
- Include Ron Terry's network-multi_bridge
* Fri Mar  9 2007 jfehlig@novell.com
- Added lame patch to handle showing suspended state via Xen API.
  The patch only affects Xen API and is thus low risk.
  Bug #237859
* Fri Mar  9 2007 carnold@novell.com
- Added AMD support for Vista 64 installation and boot.
* Fri Mar  9 2007 ccoffing@novell.com
- Make vm-install support NFS for SUSE (#241251).
* Fri Mar  9 2007 jfehlig@novell.com
- Fixed bug #250522
  + Upstream c/s 13557 stores model attribute of vif in xenstore.
* Thu Mar  8 2007 ccoffing@novell.com
- Update vm-install:
  + Better description on "Virtual Disk" drop-down (not "xvda")
  + Proper separation of recording options versus calculating
  defaults; fixes corner cases
  + #247849, #253013, 253009: Multiple fixes related to how disks
  are defined, centered around bug #247849 (handle partitioned
  PV installation disk)
  + #252437: Allow virtual CDROM to be added (via ISO) even if
  physical CDROM doesn't exist
* Wed Mar  7 2007 jfehlig@novell.com
- Fixed bug #252396
  + Added upstream c/s 14021.  Applies to Xen API c-bindings -
    low risk.
  + Added local patch to correctly set Xen API Console.protocol
    property
* Wed Mar  7 2007 jfehlig@novell.com
- Added upstream patch that fixes save/restore on 32pae guests.
  Upstream c/s 14150.  Bug #237859
* Tue Mar  6 2007 carnold@novell.com
- Remove a debug message which is spamming the logs during live
  migration.
* Mon Mar  5 2007 jfehlig@novell.com
- Fixed handling of vbd type in Xen API <-> sexpr integration.
  Bug #250351
  + Updated an existing patch (xend_disk_decorate_rm.patch) and
    then renamed patch to xend_vbd_type.patch to better reflect
    purpose of patch.
* Mon Mar  5 2007 ccoffing@novell.com
- Default apic=0 for SLES 8 and 9, for performance.  (#228133)
* Fri Mar  2 2007 carnold@novell.com
- Xen kernel crashes at domain creation time. Bug #248183.
  Fix mouse for win2k hvm guest.
* Fri Mar  2 2007 jfehlig@novell.com
- Incorrect values returned for actions_after_* in Xen API.  Added
  patch xend-actions-after.patch for fix.  Patch submitted upstream
  as well.  Bug #250870.
* Fri Mar  2 2007 ccoffing@novell.com
- Update vm-install:
  + Fixed possible "tree path exception" when editing disk
  + Fixed failure to properly refresh fields when editing disk
  + #248356: allow specifying bridge
* Fri Mar  2 2007 jfehlig@novell.com
- Add check for HVM domain in domain_save.  The check is
  performed in domain_suspend and should be included here as well.
* Thu Mar  1 2007 ccoffing@novell.com
- Update vm-install:
  + #250201: for linux PVFB, pass xencons=tty if graphics=none
  + #250016: honor non-sparse flag
* Thu Mar  1 2007 jfehlig@novell.com
- Fix exception caused by incorrect method name in xen-messages.diff.
  This is one of perhaps several problems with save/restore,
  bug #237859
* Thu Mar  1 2007 dpmerrill@novell.com
- Add xen-ioemu-hvm-pv-support.diff
  This patch allows for shutting down the IDE drive.
* Thu Mar  1 2007 jfehlig@novell.com
- Fix bug #243667
  + Updated domUloader to accept '--args' parameter.  The args
    provided as an option to --args are simply added to the sexpr
    returned by domUloader.  pygrub has similar behavior.
* Wed Feb 28 2007 ccoffing@novell.com
- Update vm-install:
  + #249013, #228113: default to realtek instead of pcnet
  + #249124: write os-type to config files
  + Updated translations
  + Setting os_type should implicitly set full_virt; fixes NIC
    model exceptions
  + Add "Add" button to Operating System Installation page, based
    on usability feedback
* Wed Feb 28 2007 jfehlig@novell.com
- Added changeset 13786 and 14022 from xen-unstable.  These
  changesets affect the Xen API C bindings only and are low risk.
  This is a continuation of support for FATE feature 110320.  ECO
  has been approved for late arrival of this feature.
* Mon Feb 26 2007 ccoffing@novell.com
- Update vm-install:
  + #244772: display error message in GUI if xen isn't running
  + #246049: better error message when OS==SUSE but ISO looks wrong
  + Fix printing of jobid when run with --background
* Wed Feb 21 2007 ccoffing@novell.com
- Don't allow "xm create" of running VM.  (#245253)
- Update vm-install:
  + Fix inability to use already-extracted SUSE kernel/initrds
  + Fix accumulation of 0-byte tmp files
  + #237063: close fds before running vncviewer
  + default apic=0 for Windows, due to performance
* Tue Feb 20 2007 carnold@novell.com
- Domain0 reboots after 2-6 hours of running guests. (#246160)
* Tue Feb 20 2007 ccoffing@novell.com
- Fix typo in xendomains.  (#246107)
- Fix order in which vm-install processes command-line arguments.
* Fri Feb 16 2007 jfehlig@novell.com
- Added changeset 13775 from xen-unstable.  This patch fixes
  the last known issue with the Xen API patchset backported
  from xen-unstable.
* Fri Feb 16 2007 jfehlig@novell.com
- Added c/s 13226 from xen-unstable.  It affects Xen API only.
- Added patch to remove ':disk' and 'tap:qcow' from stored domain
  config.  Fixes bug #237414 and helps with bug #242953.
* Thu Feb 15 2007 jfehlig@novell.com
- Backported Xen API functionality from xen-unstable to support
  hosting CIM providers.  This functionality is required for
  FATE feature 110320.  ECO has been approved.
  + Includes 19 changesets from xen-unstable.  Most are
    specific to Xen API.
  + Includes 1 patch that relaxes parsing of xml response
    in Xen API c-bindings.
* Thu Feb 15 2007 carnold@novell.com
- Added x86-nmi-inject.patch for NW debuging. (#245942)
* Thu Feb 15 2007 carnold@novell.com
- kernel panic in DomU while installing 32bit DomU on 64bit
  Dom0. (#244055) Patches 13630-domctl.patch,
  13903-domctl.patch and 13908-domctl.patch
- Updated patch pae-guest-linear-pgtable.patch
* Mon Feb 12 2007 ccoffing@novell.com
- Load xenblk at dom0 start to support bootstrapping from
  non-loopback devices.  (#242963, #186696)
- Update vm-install:
  + Update translations
  + Clean up exception error codes and sync man pages
  + Honor ordering of arguments (as claimed in man page)
  + #240984: properly detach vncviewer
  + #240387: default to absolute coordinate mouse for Windows
- Drop logging patch.  (#245150)
* Sun Feb 11 2007 ro@suse.de
- remove -fstack-protector from RPM_OPT_FLAGS for now
* Thu Feb  8 2007 ccoffing@novell.com
- Update vm-install:
  + Allow specifing disk (and disk size) vs. cdrom from CLI
  + Add missing -M/--max-memory parameter to CLI to match GUI
  + #241528: Display error if user selects FV OS but hw lacks VT
  + Move all consistency checks out of Options class, since CLI
    options may be processed in a "bad" order
  + Fix infinite loops when info is missing from background jobs
  + --background implies --no-auto-console
  + Don't let user close progress window
  + Fix bug in qemu slowness work-around, reported by Jan Albrecht
  + Do disk.validate() when clicking "OK" on disks page
  + #238959: Probe for removable media via /sys/block
  + Output VNC info for backgrounded job
  + Fix method of waiting for VM to exit when --no-autoconsole
  + #239582: Use extracted kernel-xen/initrd-xen if present
* Tue Feb  6 2007 ro@suse.de
- disable commented out buildreq for kernel for the moment
  to workaround endless rebuild
* Tue Feb  6 2007 ccoffing@novell.com
- xm-test should clean up xenstore better (#180138)
* Thu Feb  1 2007 ccoffing@novell.com
- Implement better job support for CIM (#241197)
- Temporary fix to allow PV VMs to reboot (#237414)
- Delete PYTHONOPTIMIZE for good; callers don't set it.
* Wed Jan 31 2007 ccoffing@novell.com
- Update xen-3.0.4 (changeset 13138); includes migration bugfix.
* Tue Jan 30 2007 ccoffing@novell.com
- Enable building KMP.
- Fix xendomains to work with managed domains. (#238781)
* Thu Jan 25 2007 ccoffing@novell.com
- Various bug fixes of 32on64, from Jan and Keir.
- Gerd's fix for domain builder with > 4 GB RAM (#233761)
- Update xen-vm-install:
  [#234331], #239007: CD/DVDs should always be marked read-only
  [#238458]: Work-around qemu slowness bug
  [#239196]: Support SLED
  [#239275]: Fix .desktop file
  [#240064]: Clean up VMs better after failed install
* Tue Jan 23 2007 ccoffing@novell.com
- Update xen-vm-install:
  [#237370]: Can now install 32pae SLES 10 on x86_64 hypervisor
  [#237396]: Be able to use an existing disk, bypass OS installation
  Fix handling of user's extra_args
- Patch from Jan to enable building PV drivers KMP for FV SUSE.
  Currently conditionalized.
- Drop unused patches xen-io-register-context.diff and
  xen-console.diff
* Sat Jan 20 2007 brogers@novell.com
- Fix handling of localtime config file parameter for PV guests
  (#234376)
* Fri Jan 19 2007 ccoffing@novell.com
- Update xen-vm-install (NIC UI work; do not require tcp port bz
  [#236517]; integrate with virt-manager)
* Wed Jan 17 2007 ccoffing@novell.com
- Update xen-vm-install (more disk UI work; support NetWare
  response files and licenses)
* Tue Jan 16 2007 ccoffing@novell.com
- Major fixes to xen-vm-install (adding disks in the UI now works,
  and fixed several CLI exceptions)
- Microcode does not need to be exactly 2048 bytes (changeset
  13079; Kurt)
* Fri Jan 12 2007 ccoffing@novell.com
- Include script to clone SLES 10 domU, from coolsolutions (fate
  [#301742])
- Updated patches from Gerd and Jan, including PAE > 4 gig fix,
  updated VGA console patch.
- Updated xen-vm-install with finalized strings and desktop file.
* Thu Jan 11 2007 ccoffing@novell.com
- Include xen-unstable patches for HVM save/restore and 32-on-64
  HVM.
- Update to xen-3.0.4-1 (changeset 13132).
* Wed Jan 10 2007 ccoffing@novell.com
- Update xen-vm-install and domUloader to support NetWare.
- Include AMD's nested page table patches.
* Mon Jan  8 2007 ccoffing@novell.com
- Update to xen-3.0.4 (changeset 13129).
- Fix from upstream for mis-emulation of x86-64 pop.
* Fri Jan  5 2007 carnold@novell.com
- Many patches from Jan Beulich and Gerd Hoffmann in support of
  32 on 64 pv guests.  These patches apply to both the hypervisor
  and the tools.
* Fri Dec 22 2006 ccoffing@novell.com
- Do not require authentication on XenAPI socket, since CIMOM does
  not support authentication.  Socket is only accessible to root.
* Wed Dec 20 2006 ccoffing@novell.com
- Update to xen-3.0.4 (changeset 13100).
- Update xen-vm-install tools.
- Include Jim's 2 xen-tools patches for CIM provider issues.
* Mon Dec 18 2006 ccoffing@novell.com
- Update to xen-3.0.4-rc3 (changeset 13087).
- Fix line terminators in block-iscsi (#228864)
- Make domUloader work with blktap support in xend.
* Fri Dec 15 2006 ccoffing@novell.com
- Update to xen-3.0.4-rc2 (changeset 13067).
* Thu Dec 14 2006 ccoffing@novell.com
- Update to xen-3.0.4-rc1 (changeset 12901).
* Wed Dec 13 2006 brogers@novell.com
- Patch for loading bimodal PAE kernel to suuport NetWare
* Thu Dec  7 2006 ccoffing@novell.com
- Update to xen-unstable (changeset 12757).
- Enable LIBXENAPI_BINDINGS and XENFB_TOOLS.
- Enable unix domain socket for xend; needed by tools.
* Tue Dec  5 2006 ccoffing@novell.com
- Update to xen-unstable (changeset 12734; feature freeze for
  3.0.4)
- Make /etc/xen mode 0700 to protect vnc passwords.
* Mon Nov 27 2006 ccoffing@novell.com
- Fix how bootloader is called by the xend during restarts.
  (#223850)
* Wed Nov 22 2006 ccoffing@novell.com
- Series of patches from Jan to address selectors with non-zero-
  bases and other related issues in HVM. (#214568)
- Default pae=1, otherwise 64 bit HVM does not work at all.
  (#217160)
* Fri Nov 17 2006 ccoffing@novell.com
- Backport several HVM fixes. (#176171?)
* Thu Nov 16 2006 ccoffing@novell.com
- Fix some problems in the xen-hvm-default-bridge patch. (#219092)
- xmlrpc isn't 64-bit clean, causing xend to get exceptions when
  PFN is > 2 GB. (#220418)
* Mon Nov 13 2006 kallan@novell.com
- Backport changesets 11847, 11888, 1189[6-9], 119[00-18], 11974,
  1203[0-2], and 12205 from xen-unstable so that the PV drivers
  can compile on older kernels such as sles9 and rhel4
- Fix netfront.c to fail the probe if it is called for an ioemu
  type device.  This allows both PV and FV drivers to exist at
  same time in the FV guest.
* Thu Nov  9 2006 ccoffing@novell.com
- Add xen-vm-install.
- Default bridge correctly for HVM guests. (#219092)
* Wed Nov  8 2006 aj@suse.de
- Set correct permissions on man files.
* Tue Nov  7 2006 ccoffing@novell.com
- Update name of blktap.ko in xend init script. (#215384)
- Remove some extraneous bad chars in xm manpage. (#218440)
- Update logrotate.conf.
- Update spec file.
* Wed Nov  1 2006 kallan@novell.com
- Backport xen-unstable changesets 12040 to address spurious
  interrupts with PV drivers in HVM guests.
* Tue Oct 31 2006 ccoffing@novell.com
- Backport xen-unstable changesets 1184[1-3] to address SVM
  interrupt injection issues.  Replaces earlier (broken) patches.
* Mon Oct 30 2006 ccoffing@novell.com
- /var/lib/xen/images should not be world readable. (#214638)
- Update to xen-3.0.3-0 (changeset 11774; no code changes).
* Mon Oct 16 2006 ccoffing@novell.com
- Update to xen-3.0.3-testing changeset 11772 (rc5).
- Fix several possible type errors when running domUloader.
- Remove pygrub.  Was broken on reiserfs and never had ext2
  support, so it is useless. (#173384)
- First attempt at moving domUloader to blktap.  Still disabled
  due to block-detach failing.
* Fri Oct 13 2006 ccoffing@novell.com
- Update to xen-3.0.3-testing changeset 11760 (rc4).
* Tue Oct 10 2006 ccoffing@novell.com
- Update to xen-3.0.3-testing changeset 11740 (rc3).
- Fix crash on PAE when specifying dom0_mem=4096M. (#211399)
- Make xend.balloon aware of kernel's memory floor, to fix
  "Privileged domain did not balloon" errors. (#184727)
* Mon Oct  9 2006 ccoffing@novell.com
- Include AMD's interrupt injection fix.
* Wed Oct  4 2006 ccoffing@novell.com
- Imported keymap patch. (#203758)
- Account for minimum memory required by dom0 kernel. (#184727)
- Package /usr/include/xen/hvm/*.h
* Tue Oct  3 2006 ccoffing@novell.com
- Update to xen-3.0.3-testing changeset 11686.
* Tue Oct  3 2006 kallan@novell.com
- Updated README.SuSE to reflect the current method of handling
  Xen network-bridging when using SuSEfirewall2.  (#205092)
* Sat Sep 30 2006 aj@suse.de
- Cleanup BuildRequires.
* Thu Sep 28 2006 ccoffing@novell.com
- Only "eval" disks once in domUloader, to match current Xen.
* Wed Sep 27 2006 ccoffing@novell.com
- Switch to xen-3.0.3-testing tree; changeset 11633.
- Update (but disable) paravirtualized framebuffer patches.
* Tue Sep 26 2006 ccoffing@novell.com
- Update to xen-unstable changeset 11623.
- Fix domUloader typo introduced in last update.
- Build debug version of xen-pae.
* Mon Sep 25 2006 ccoffing@novell.com
- Update to xen-unstable changeset 11616.
* Tue Sep 12 2006 ccoffing@novell.com
- Update check_python script to identify Python 2.5 RCs as valid.
* Mon Sep 11 2006 ccoffing@novell.com
- Update to xen-unstable changeset 11440.
- xen-tools conflicts with qemu.  Do not package qemu.1 manpage.
  (#204758)
- Include Jan's updated patch for #192150 (to preserve register
  context when doing IO).
* Tue Sep  5 2006 ccoffing@novell.com
- Update block-nbd and xmexample.nbd, and add block-iscsi and
  xmexample.iscsi (from Kurt).
* Thu Aug 31 2006 ccoffing@novell.com
- Automatically create/destroy virtual frame buffer viewer.  Add
  "sdl=1" to config file of a paravirtualized VM to get the viewer.
- Log files have moved to /var/log/xen.
* Tue Aug 29 2006 ccoffing@novell.com
- xendomains does not actually save domains.  (#201349)
- Update to xen-unstable changeset 11299.
* Mon Aug 28 2006 ccoffing@novell.com
- Fix incorrect path on x86_64 for vncfb and sdlfb.
* Thu Aug 17 2006 ccoffing@novell.com
- Improve xendomains init script, to handle unset sysconfig vars.
- Import virtual framebuffer patches.
- Drop reboot patch; resync patches.
* Wed Aug 16 2006 ccoffing@novell.com
- Update to xen-unstable changeset 11134.
- Drop xen-reverse-10064.diff now that kernel is updated.
* Tue Aug  8 2006 ccoffing@novell.com
- Re-enabled patch for #184175.
- Update to xen-unstable changeset 10986.
- Include Jan's patch to preserve register context when doing
  IO.  (#192150)
* Fri Jul 28 2006 ccoffing@novell.com
- Add support to domUloader for "xm create --dry-run".  Based on
  patch from HP.
* Thu Jul 27 2006 ccoffing@novell.com
- Add link for qemu-dm that is invariant across architectures, so
  that VM config files can be simple key/value pairs parsable by
  yast, and still be movable to another arch.  (#193854)
- Add loop.ko to rescue image created by mk-xen-rescue-img, and
  remove usbfs from image's /etc/fstab since USB isn't yet
  supported, to avoid errors during boot.  (#191627)
* Mon Jul 17 2006 ccoffing@novell.com
- Update to xen-unstable changeset 10712.
- Update domUloader and rcxend to work with blktap.
* Fri Jul 14 2006 ccoffing@novell.com
- When waiting for domains to shut down, must also wait for
  loopback devices to be torn down, otherwise higher-level tools
  may migrate a VM before the disk image is flushed.  (#185557)
- More updates to the README.
* Thu Jul 13 2006 kallan@novell.com
- Added for loop to retry the losetup -d in /etc/xen/scripts/block.
  It is possible for the losetup -d to fail if another process is
  examining the loopback devices e.g. losetup -a.  (#151105)
* Wed Jul 12 2006 ccoffing@novell.com
- Corrected and updated README.
* Mon Jul 10 2006 ccoffing@novell.com
- Add Jeff Mahoney's block-sync.diff, to give control of
  "losetup -y" to the user (and potentially yast).  Defaults to
  old async behavior.  (#190869)
* Thu Jul  6 2006 ccoffing@novell.com
- Update to xen-unstable tree.  Revert changeset 10064, to maintain
  backwards compatibility with SLES 10.
* Wed Jul  5 2006 ccoffing@novell.com
- Do not open migration port by default.  (#190170)
- Update patch for migration oops, to latest version in bug
  [#162865].
* Mon Jul  3 2006 okir@suse.de
- xen-losetup-sync.diff: use the new "losetup -y" option to force
  the loop device to use synchronous I/O (#189051)
* Fri Jun 30 2006 ccoffing@novell.com
- Increase balloon timeout value.  (#189815)
- Update to xen-3.0-testing tree, changeset 9762.
* Thu Jun 29 2006 ccoffing@novell.com
- Fix some loopback races in domUloader.  (#151105)
* Tue Jun 27 2006 ccoffing@novell.com
- Add "max_para_memory" and "max_hvm_memory" to output of "xm info"
  for bug #184727.
- Include Jan's patches for bug #184175.  Improves PAE guest
  support on HVM.
* Mon Jun 26 2006 ccoffing@novell.com
- Include patch from HP to fix a domU migration failure ("Kernel
  BUG at mm/mmap.c:1961").  Force L1/L2 page tables to be updated
  at the end, to avoid them from being dirtied and not transferred.
  (#162865)
* Fri Jun 23 2006 kallan@novell.com
- Updated xen-bonding.diff to enable bonding again after the latest
  patches to network-bridge etc. (#161888)
* Wed Jun 21 2006 ccoffing@novell.com
- Clean up the useless "Nothing to flush" messages, from 'ip addr
  flush', in /var/log/xen-hotplug.log
- Fix race condition in domUloader.py, when another process did
  losetup -d while domUloader was running.  This would result in
  the mount failing, and so the VM would fail to start.
* Tue Jun 20 2006 ccoffing@novell.com
- Revamp balloon.py to account for pages currently being
  scrubbed.  (#185135)
* Mon Jun 19 2006 ccoffing@novell.com
- Update to xen-3.0-testing tree, changeset 9749.
- DomUs are getting starved for CPU (up to 40 seconds was seen)
  when dom0 has a load.  This can cause pathological behavior, and
  can cause OCFS2 to fence (panic) the domain.  (#179368, #178884)
- Import Gerd's fix to network-bridge script for bug #161888.
* Wed Jun 14 2006 ccoffing@novell.com
- Pull out accidentally-included debugging code.
- Drop xenvers patch; this was for backwards compatibility for
  some early internal builds.
- Update from Jan on the console patch.  Not all graphics cards /
  drivers properly reflect the state in the register being tested.
  Improved the check, to prevent screen corruption.  (#161541)
* Tue Jun 13 2006 ccoffing@novell.com
- Resync with new tarball from xen-3.0-testing; changeset 9738.
* Mon Jun 12 2006 ccoffing@novell.com
- Drop BUILD_BUG_ON and pirq-shared patches.  Last week's pirq
  sharing patch from upstream (for bug #152892) makes these patches
  redundant.  Dropping these makes our shared_info structure match
  upstream again, which is needed for compatibility with other
  paravirtualized guests.
- Import changeset 9734 from xen-3.0-testing.  This fixes a hyper-
  call (used by the pcifront driver) to work on MP guests.  Without
  this, the pciback driver can hang on MP.  (#181467)
- Import changeset 9733 from xen-3.0-testing.  This patch is
  required to match the Linux kernel, since Linux always calls
  this operation from VCPU0 during secondary VCPU bringup.
  Without this, process run-time accounting on secondary CPUs is
  completely wrong.
- Updated README:  Documented work-around for bug #180058.
* Fri Jun  9 2006 ccoffing@novell.com
- Include Jan's patch: "IOPL is ignored for VM86 mode port
  accesses.  Fix Xen emulation to match native behaivour."  Fixes
  some X lockup issues.  (#179045)
- Include Keir's patch to allow reading from port 0x61, to avoid
  an X server lockup.  (#171087)
- Include xen-3.0-testing changeset 9726, which is needed to
  support the latest kernel-xen.  With this support, Linux will
  only trigger unhandled IRQ path if IRQ is not shared across
  multiple guests (another guest may have handled the interrupt).
  This is more upstream work that goes with bug #152892.
- Add versioning to the Requires lines, to guard against mixing
  binary incompatible versions.  (#183292)
- I accidentially dropped part of Clyde's fix for bug #162244.
  SMP support in HVM is working in xen-unstable, so upstream
  dropped the HT CPUID masking code, which we then inheirited.
  Re-add HT CPUID masking.  (#162244)
- Updated README:  VNC installations, known issues.
* Thu Jun  8 2006 ccoffing@novell.com
- Drop our XCHG patch for the equivalent upstream patch, to fix
  patch application order.  No code change.
* Wed Jun  7 2006 ccoffing@novell.com
- Updated README:  HVM issues/tips, CDROM tips, known issues.
- Add patch from Intel to decode LODS/STOS instructions to fix
  Windows installation.  Only affects HVM.  Xen changeset #9725
  consolidates this patch and xen-hvm-decode.diff; drop our 2 in
  favor of the consolidated upstream patch.  (#176717)
* Tue Jun  6 2006 ccoffing@novell.com
- Drop xen-8-way-bios patch, because it breaks Windows HVM
  installation.  The patch was only necessary when running SMP HVM
  with "acpi=0" on the kernel command line.  (#181974)
- Include two patches from xen-3.0-testing that change the
  interface between Xen and guests.  Including these now to help
  forward-compatibility:
  + 9709: Changes interface for accessing %%cr3 so that extra bits
    (>4GB) for PAE pgdirs are placed in low-order bits of %%cr3.
    Kernels without support for this will still run fine.
  + 9721: Use explicitly-sized types in the dom0_ops and privcmd
    structures.
- Fix ability to change ISOs images for HVM guest.  (#181895)
- Removed pointless whitespace changes from xen-removable.diff, for
  better maintainability.  Cut the patch size in half; no code
  changes.
* Mon Jun  5 2006 ccoffing@novell.com
- Include select patches from xen-3.0-testing:
  + 9698: Official fix for bug #159001.  Dropped our patch.
  + 9702: Fix MMU_NORMAL_PT_UPDATE when passed a page that is no
    longer of type page-table.
  + 9703: Modification to fix for bug #159001; ignore empty PTEs.
  + 9704: Fix for obvious typo in map_pages_to_xen: When replacing
    a pte, free the page table pointed to by the old entry, not the
    new entry.
  + 9705: Jan's previous signed-ness patch (c/s 9695) was changed
    when accepted upstream, which broke it; this changeset
    attempts to fix the breakage.
  + 9708: HVM: Fix a hang when doing an "xm destroy" of Windows VM.
  + 9717: HVM: Interrupts must be kept disabled when entering Xen
    for external interrupt processing.
* Fri Jun  2 2006 ccoffing@novell.com
- Include xen-3.0-testing changeset 9693.  This scales the
  ballooning timeout with the amount of memory being requested
  (necessary for large memory machines).  This is a more proper fix
  for Novell bug #175805, and addresses XenSource bug #650.
* Thu Jun  1 2006 ccoffing@novell.com
- Update the README, regarding how to make the mouse work properly
  with VNC in HVM.
- Update help text in mk-xen-rescue-img.
* Wed May 31 2006 ccoffing@novell.com
- Jan's backport of xen-unstable changesets 9517, 9518, and 9529.
  This allows Xen to boot on 4-node configurations without
  crashing.  (#150114)
- Include patch from Jun Nakajima at Intel to fix inability to
  start XWindows after creating HVM guest.  (#159001)
- Include select patches from xen-3.0-testing:
  + 9697: Fix infinite recursion loop in get_page_type() error path
- Include xen-unstable changeset 9967, to improve Summagraphics
  tablet emulation, to help mouse tracking in HVM.  (#167187)
- Include 3 patches from AMD to fix SMP support in HVM.  (#176171)
- Add CPUID masking patches from AMD and Intel for HVM.  This
  prevents the OS from seeing (and trying to use) various hardware
  features that are not supported within the VM.  (#180879)
* Fri May 26 2006 ccoffing@novell.com
- Fix deadlock between xm and qemu.  Qemu should not call xm;
  issue xc commands directly.  This deadlock was exposed when
  making qemu exit nicely and clean up.  (#176400)
- Include Gerd's update to his previous REP MOVS fix.  Calculating
  high_addr and low_addr is more complicated than previously
  thought, and the count was wrong.  (#165448).
- Drop previous patch that forcefully turns off Xen's console
  logging to avoid video corruption; instead use Jan's patch which
  only turns logging off when in graphical mode.  (#161541)
- Include Jan's patch to call machine_halt rather than inline
  assembly "hlt" when Xen crashes to sync display, disable watchdog
  timers, etc.
- Tweak the auto-ballooning patch to limit the VM itself to the
  requested amount of memory, don't include the overhead, as
  suggested by Intel.  Separate calls exist elsewhere to increase
  the max as needed.  (#149179)
- Include select patches from xen-3.0-testing:
  + 9688, 9696:  These remove some broken assembly string
    functions.  This is prep work from Jan for bug #160066.
  + 9695: Updates in the hypervisor to EDI and ESI could be
    incorrect, due to sign not being handled correctly.
* Fri May 19 2006 ccoffing@novell.com
- Update from Intel to previous patch to fix installation of HVM
  W2k.  Adds decoding for two more instructions.  (#176717)
- Updated the README.
- Included updated version of KY's patch to reserve some lowmem
  for PAE, to avoid kernel BUG() during boot.  The amounts of
  memory reserved at various physical memory sizes have been
  adjusted.  (#175124)
- Include Intel's patch for unchecked allocations in shadow*.c.
  (#149179)
* Thu May 18 2006 ccoffing@novell.com
- Include Intel's patch to fix installation of HVM W2k.  This patch
  adds decoding for 'xor' and 'and' instructions.  Without this,
  the VM crashes when W2k attempts to install network components.
  (#176717)
- While tidying xen-hvm-memory-check.diff for submission upstream,
  I noticed an error in the patch (such that low-memory while
  starting the HVM domain could still crash the physical machine.)
  Now all uses of iopm are protected by the check.  (#149179)
- Xen must always relinquish control of the VGA console once dom0
  has started.  Otherwise, it could be over-writing dom0's memory,
  causing screen or other memory corruption.  Admin can use
  "xm dmesg" to view Xen's log instead.  (#161541)
- First send a SIGTERM, rather than SIGKILL, to qemu to give it a
  chance to clean up.  This fixes both mouse and CD-ROM issues
  for fully virtualized VMs.  This is a work-around; Ross is
  still working on the proper fix.  (#176400, #171258, #176157)
- Include select patches from xen-3.0-testing:
  + 9682,9683: These patches only affect full virtualization on
    AMD.  Fixes register corruption, cleans up event injection,
    cleans up IO handling.
  + 9685,9686: This patch only affects full virtualization on
    Intel.  Fixes VM's segment base address, to avoid vmentry
    failure.  Also remove 32/64 differences in vmx reg store/load.
* Wed May 17 2006 ccoffing@novell.com
- When auto-ballooning domain 0's memory for a new HVM domain,
  all memory (including memory intended for overhead) was given
  to the VM itself.  So increasing the memory size calculations
  did not actually free up any more memory.  Now, treat the amount
  to balloon and the amount to give to the VM as separate values.
  (#149179)
* Tue May 16 2006 ccoffing@novell.com
- Include Gerd's fix for HVM emulation of REP MOVS when the copy
  spans a page.  If the direction flag was set, the emulation code
  broke.  This caused the VM to freeze when configuring firewall
  (#165448).
- Include KY's fix to default to reserving 16M of lowmem for PAE,
  to avoid hitting kernel BUG() during boot (#175124).
- Don Dugger's (Intel) fix for HVM screen corruption (#164573).
- Increase maximum time auto-ballooning will wait for domain 0 to
  respond, otherwise large VMs will fail to start from yast
  (#175805).
* Mon May 15 2006 ccoffing@novell.com
- Update memory size calculations when auto-ballooning for HVM
  to make more stable (#149179).
* Fri May 12 2006 ccoffing@novell.com
- Include select patches from xen-3.0-testing:
  + 9674: xc_ptrace: Fix reversed conditional, which broke single-
    stepping.
  + 9675: xc_ptrace: Fix out-of-bounds memory-access for FPU state.
  + 9678: Fix the performance issues of 2-level paging HVM guests
    on the PAE Xen.
- Update man pages.
* Wed May 10 2006 brogers@novell.com
- Fix loading of binary images which either require PAE or
  dynamically support running on both PAE hypervisor and non-PAE
  hypervisors. (#174080)
* Wed May 10 2006 carnold@novell.com
- Handle memory failure when staring fully virtualized
  guests to prevent reboot of the box (AMD) or
  hanging the box (VT) (#149179).
* Tue May  9 2006 ccoffing@novell.com
- Include select patches from xen-3.0-testing:
  + 9665: Fix pciif parsing for compatibility variable.
  + 9666: Fix HVM hang; was broken due to previous "hda lost
    interrupt" patch. (#169146)
  + 9667: Do not set GP fault in VMCS for VMX (no bug#; from Intel)
* Thu May  4 2006 cgriffin@novell.com
- Update xen-3.0-testing tree, changeset 9664:
  + Changesets 9663 and 9664 fix AMD fully virtualized
    guests causing the system to reboot when
    first starting up.  (#169855)
* Thu May  4 2006 cgriffin@novell.com
- With a Xen domain set up with a loop-mountable file as rootfs,
  the "xm start " invocation fails. The cause is a bug
  domUloader.py (#172586)
* Thu May  4 2006 rmaxfiel@novell.com
- Added the ability to 'attach' and 'detach' removable media
  devices to hvm guests.  Also made cdrom eject when the eject
  request comes from the hvm guest. (#159907)
- Fixed the loss of mouse when a SDL session ends with 'grab'
  in effect.  (#159001)
* Thu May  4 2006 cgriffin@novell.com
- Update xen-3.0-testing tree, changeset 9661:
  + Drop patches merged upstream
  + Took Kier's official patches for dropped patches most
    notably spurious interrupts (#152892)
- Took Intel's patch to fix screen corruption when
    resizing the screen of windows hvm guests (#164573)
* Wed May  3 2006 kallan@novell.com
- Added configuring network interfaces when using Xen bridging instructions
  to the README.SuSE file as requested by bug #171533.
* Mon May  1 2006 tthomas@novell.com
- Added message to xm save to indicate that save is not currently
  supported for fully virtualized guests. (#161661)
* Fri Apr 28 2006 ccoffing@novell.com
- Close fds before exec-ing vncviewer, so yast2-vm doesn't hang
  when viewing fully-virtualized console (#168392).
* Thu Apr 27 2006 ccoffing@novell.com
- Update xen-3.0-testing tree, changeset 9656:
  + Drop patches merged upstream.
  + Fix reboot on large SMP machines (IBM, no bug #).
- Integrate Jan's patches:
  + Spurious interrupt roundup (#152892).
* Mon Apr 24 2006 ccoffing@novell.com
- Integrate Jan's patches:
  + FXSR patch (#135677).
  + APIC option patch (work-around #150114).
  + Protect against hypervisor crash (#169143).
- Update xen-3.0-testing tree, changeset 9649:
  + Avoid spurious timer activations in hypervisor.
  + Fix xen command line parsing (lapic / nolapic parsing).
  + Fix inverted BUG_ON w.r.t. SiS APIC bug.
* Fri Apr 21 2006 ccoffing@novell.com
- Update to 3.0.2-2 (xen-3.0-testing tree, changeset 9640):
  + Fix for "hda lost interrupt" for PAE VMX.
  + Increase L2 PDE to 1 GB; allows x86_64 to boot larger dom0.
  + Fix for SVM booting 32pae-on-32pae.
- Drop upstream patches (SiS APIC bug, HTT, HVM interrupt race)
- Add Jan's port of spurious interrupt patch (#152892).
- Add /etc/xen/images link for convenience (#168070).
- Updated README.
* Thu Apr 20 2006 ccoffing@novell.com
- SiS APIC bug patch (Jan Beulich, #116485).
* Wed Apr 19 2006 ccoffing@novell.com
- Don't kill xenstored and xenconsoled when stopping xend.
  (#158562, #156261)
* Wed Apr 19 2006 ccoffing@novell.com
- Update to 3.0.2-2 (xen-3.0-testing tree, changeset 9629):
  + Fix for SMP IA32 VMX guest booting.
  + KY's SETMAXMEM fix.
* Wed Apr 19 2006 cgriffin@novell.com
- Removed HTT bit from cpuid and set logical processor count to 1.
  Also fixed logic problem in svm code where apic=0 was not
  handled (#162244).
* Wed Apr 19 2006 agruen@suse.de
- Create /boot symlinks in the %%install section instead of in
  %%post so that they will end up in the package file list.
* Tue Apr 18 2006 ccoffing@novell.com
- Add /etc/xen/vm to vm config file search path (#167208).
* Fri Apr 14 2006 kallan@novell.com
- Add support for bonding in network-bridge. (#161678).
* Fri Apr 14 2006 ccoffing@novell.com
- Update to 3.0.2-2 (xen-3.0-testing tree, changeset 9620):
  + Fixes stack corruption in libxs (XenSource #411).
* Thu Apr 13 2006 rmaxfiel@novell.com
- Fixed a problem in ioemu which exited when the cdrom line was
  found in the guest def file but the cd device contained no media.
  (#161210)
* Wed Apr 12 2006 ccoffing@novell.com
- Auto-balloon domain 0 for HVM domains (#149179).
- Update to 3.0.2-1 (xen-3.0-testing tree, changeset 9612):
  + Fixes xmlrpc issues.
  + Fixes several emulated instructions for HVM.
  + Fixes for x86_64 inline assembly.
* Tue Apr 11 2006 ccoffing@novell.com
- Fix "jitter" and race in dom0's memory target calculation, which
  could cause auto-ballooning to fail (#164714).
* Tue Apr 11 2006 brogers@novell.com
- Fix problem where localtime=1 results in zombie domains after
  they shutdown (#164960)
* Mon Apr 10 2006 ccoffing@novell.com
- Update to hg 9598 (xen-3.0-testing tree; 3.0.2-rc).  Discounting
  Linux changes and patches we already carry, this update contains:
  + Saner error handling in iret hypercall (x86/64).
  + Make root page table sanity check on restore more generic.
  + Additional sanity / compatability checks during guest build.
  + IO-APIC update hypercall fixes.
* Fri Apr  7 2006 ccoffing@novell.com
- Don't throw an exception if 'xm top' is run by non-root; print
  error message instead (#164224).
- Change localtime patch to account for daylight savings time
  (Bruce Rogers).
- Re-add patch to make tightvnc work.  It was accidentally dropped
  recently (#149556).
* Thu Apr  6 2006 ccoffing@novell.com
- Update to hg 9590 (xen-3.0-testing tree; 3.0.2-rc).
- Fix type error in localtime patch for para (Bruce Rogers).
- Fix default localtime for full (Bruce Rogers).
- Fix path in mk-xen-resue-img.sh (#163622).
- Update README (pathnames, yast2-vm descriptions, terminology).
* Mon Apr  3 2006 garloff@suse.de
- init script: Test for control_d in capabilities to determine dom0
  rather than privcmd.
- init script: Try loading netloop and backend modules.
- mk-xen-rescue-img.sh: Copy frontend drivers, remove stale files.
- example config files: provide commented out domUloader exmaples.
* Mon Apr  3 2006 ccoffing@novell.com
- Update to hg 9514 (xen-unstable tree; 3.0.2-rc).
- Fix for rebooting (Jan Beulich; #160064).
* Fri Mar 31 2006 ccoffing@novell.com
- Update to hg 9502 (xen-unstable tree; 3.0.2-rc).
- Update man page (#162402).
- xen-tools requires python-xml (#161712).
- Include localtime patch to support NetWare (Bruce Rogers).
* Thu Mar 30 2006 ccoffing@novell.com
- Update to hg 9481 (xen-unstable tree; 3.0.2-rc).
- Correctly default XAUTHORITY if it is not set.  This allows the
  GUI to come up for fully virtualized guests (was especially
  problematic when VM was started from YaST).  (#142472)
* Wed Mar 29 2006 ccoffing@novell.com
- Fixed reversed "Do I have enough memory?" test when creating
  new VMs (#156448).
* Tue Mar 28 2006 ccoffing@novell.com
- Pick up two critical fixes for AMD to fix full virtualization:
  c/s 9453 & c/s 9456.
* Thu Mar 23 2006 ccoffing@novell.com
- Update to hg 9434 (xen-unstable tree; 3.0.2-rc).
- Fix /etc/xen/scripts/block to properly check if devices can be
  shared.
- Default XENDOMAINS_AUTO_ONLY to true; previous setting
  contradicts yast2-vm's claim that only VM's marked auto will be
  auto-started.
* Mon Mar 20 2006 ccoffing@novell.com
- Update to hg 9329 (xen-unstable tree).
* Wed Mar 15 2006 ccoffing@novell.com
- Update to hg 9251 (xen-unstable tree).
- Update to latest versions of Intel's VNC patches:
  patch-vga-sse2-0314.l, patch-vnc_loop-0314.l,
  patch-vncmouse-0315.l
- Gather example files in /etc/xen/examples.
* Tue Mar 14 2006 rmaxfiel@novell.com
- Removed the intermediate sym-link between xen.gz and
  xen-<version>-<release>.gz.  Grub 0.97 XFS can not handle a
  double indirect to a file.  (#151792)
* Mon Mar 13 2006 garloff@suse.de
- Update README.SuSE: Document limits (mem, cpu hotplug, max_loop),
  more network troubleshooting, update security info.
- Be more tolerant against errors in ifdown/ifup to better coexist
  with non-std network setups (e.g. ifplugd/NetworkManager).
* Tue Mar  7 2006 ccoffing@novell.com
- Update to hg 9172 (xen-unstable tree).
- Create new xen-libs package, split from xen-tools (#154473).
- Update mk-xen-rescume-img and xmexample.rescue to work with
  current rescue image on CD (#152971).
- Include Kurt's patch to domUloader, to pass command line args.
- xendomains shouldn't try to migrate or save HVM domains, as this
  isn't supported and will stall the shutdown (#155265).
- Create empty /etc/xen/vm directory for YaST to place config files
  in, to avoid name collisions (#156322).
- Update and re-enable vga patch from Intel (Don Dugger).  VGA
  emul is faster and not corrupted.
- ifup is run to ensure IPs are assigned before rearranging for
  xen, but this can fail with ifplugd; this should not kill the
  whole script (Kirk Allan) (#154115).
- Make network-bridge script more robust, by checking /sys instead
  of grep-ing.
* Mon Mar  6 2006 ccoffing@novell.com
- Update to hg 9148 (xen-unstable tree).  Drop patches merged
  upstream.
- More README improvements (#154134).
- Fix "vncviewer=1" to bring up vncviewer (#149556).
* Mon Mar  6 2006 ccoffing@novell.com
- Fix build of hvmloader and vmxassist by removing external
  CFLAGS (XS changeset #9110).
- Fix build by forcing --prefix during installation of *.py.
* Wed Mar  1 2006 ccoffing@novell.com
- Update to hg 9029 (xen-unstable tree).  Adds support for HVM on
  64 bit hardware.
- Update vncmouse diff to 20060301 from Intel; compensates for lack
  of eager events in our LibVNCServer.
- Fix many bugs in lomount.
- Cap maximum value of "xm mem-set" for domain 0, based on size of
  dom0's page tables (#152667).
* Mon Feb 27 2006 ccoffing@novell.com
- Update to hg 9015 (xen-unstable tree).  More bug fixes.
- Update patch to better honor RPM_OPT_FLAGS.
- Updated README (#154134).
- Disable xen-vga-0213 patch; it speeds VGA updates but was
  corrupting the display.
- Change max mouse polling time from 1ms to 10ms to reduce CPU
  load (from Intel).
* Thu Feb 23 2006 ccoffing@novell.com
- Update to hg 8954 (xen-unstable tree).  More bug fixes.
- Don't use a dummy IP of 1.2.3.4 for NFS server when booting domU
  with DHCP.  Seems to hang x86_64 Linux.
- Remove unnecessary x86_64 patch.
- Fix auto-ballooning of dom0 memory for HVM domUs (XenSource bug
  521).
* Tue Feb 21 2006 ccoffing@novell.com
- Update to hg 8920 (xen-unstable tree).  Fixes instruction decode
  for fully virtualized guests, fixing booting from CDs.
- Integrate 3 patches from Intel, to improve VNC performance.
* Tue Feb 21 2006 ccoffing@novell.com
- Update to hg 8910 (xen-unstable tree).
  fixes 32 on 32, 32 pae on 32pae, 64 on 64, 32 on 64.
  critical HVM fixes, for fully virtualized guests.
* Fri Feb 17 2006 ccoffing@novell.com
- Update to hg 8870 (xen-unstable tree).  More HVM fixes.
- Remove duplicate balloon.free call.
- Add patch from Intel to fix dom0 crash on 64 bit SMP HVM.
* Thu Feb 16 2006 carnold@novell.com
- Update to hg 8858 (xen-unstable tree).
* Wed Feb 15 2006 ccoffing@novell.com
- Update to hg 8857 (xen-unstable tree).  Syncs hypervisor core
  with Linux 2.6.16, which may fix some ACPI issues.  Fixes HVM.
- Fix uninitialized variable in xc_load_bin (from Bruce Rogers).
- Auto-balloon dom0 for fully virtualized domains (#149179).
- xen-doc-html was missing image files.
* Mon Feb 13 2006 ccoffing@novell.com
- Update to hg 8830 (xen-unstable tree).
- Restore cs 8783/8792 to match kernel.
* Wed Feb  8 2006 ccoffing@novell.com
- Update to hg 8800 (xen-unstable tree).
- Update BuildRequires.
- Add "max-free-memory" to "xm info", to support yast2-vm (#147612)
- Insserv xendomains, to support yast2-vm.
- Fix exit code of "xend stop".
- Revert cs 8783/8792 to allow xenstore to start (until kernel
  catches up).
- Ensure eth0 aka veth0 really comes up in network-bridge.
* Sat Feb  4 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 27 2006 ccoffing@novell.com
- Update to hg 8728 (xen-unstable tree).
- Improve network-bridge:
  + Ensure netdev really is up, to fix STARTMODE="manual".
  + Stop ifplugd when doing ifdown, to fix STARTMODE="ifplugd".
  + Improve check for whether bridge already exists.
  + Improve defaults for netdev.
- Fix log rotate so xend moves to new log.
- xen-tools "Requires" python, et.al.; xen proper doesn't.
- Revamp mk-xen-rescue-img.sh (#118566).
- Revamp rcxendomains:  improved output, error checking, return
  values (#143754, #105677).
* Tue Jan 24 2006 ccoffing@novell.com
- Update to hg 8659 (xen-unstable tree).
* Mon Jan 23 2006 ccoffing@novell.com
- Correct return values and improve messages of init scripts.
* Fri Jan 20 2006 ccoffing@novell.com
- Use domUloader instead of pygrub.
* Thu Jan 19 2006 carnold@novell.com
- Build based on the xen-unstable.hg 8628
* Wed Jan 18 2006 carnold@novell.com
- Update to hg 8646 xen-unstable-hvm.hg tree.
* Fri Jan 13 2006 ccoffing@novell.com
- Allow version string "XEN_VER=3.0" instead of just
  "XEN_VER=xen-3.0" for backwards compatibility.
- Correctly set changeset in compile.h.
* Thu Jan 12 2006 carnold@novell.com
- Added two patches from AMD that apply to the 8513 changeset.
* Thu Jan 12 2006 kukuk@suse.de
- Add libreiserfs-devel to nfb.
* Wed Jan 11 2006 carnold@novell.com
- Update to hg 8513 xen-unstable-hvm.hg tree.
* Tue Jan 10 2006 ccoffing@novell.com
- Update to hg 8269 (xen-3.0-testing).
- Support try-restart in init scripts.
- Clean up installation of udev rules.
* Wed Dec 14 2005 ccoffing@novell.com
- Update to hg 8257 (xen-3.0-testing).
- Update documentation.
- Fix gcc 4.1 warnings.
* Wed Dec  7 2005 ccoffing@novell.com
- Update to hg 8241 (xen-3.0-testing).
* Mon Nov 28 2005 ccoffing@novell.com
- Update to hg 8073.
- Rationalize command names (eg, setsize -> xentrace-setsize).
- Fix gcc 4.1 warnings.
* Wed Nov 16 2005 ccoffing@novell.com
- Update to hg 7782.
- Honor RPM_OPT_FLAGS better.
- Include a few simple, obvious fixes from upstream.
- Build xm-test package.
- Update udev scripts.
* Mon Nov 14 2005 ccoffing@novell.com
- Includes upstream fixes to fix i586 save/restore.
* Thu Nov 10 2005 ccoffing@novell.com
- Include a few simple, obvious fixes: 7609, 7618, 7636, 7689,
  7690, 7692, 7696
* Thu Nov  3 2005 ccoffing@novell.com
- Update to hg 7608.
- Fix warn_unused_result warnings.
- Drop some patches (merged upstream)
- Tidy README.SuSE.
* Tue Nov  1 2005 ccoffing@novell.com
- Update to hg 7583.
* Thu Oct 20 2005 ccoffing@novell.com
- Don't mention unwritten man pages.
- Update xmexample* to match SUSE paths.
- Update xs-include patch.
* Wed Oct 19 2005 garloff@suse.de
- Avoid race in watchdog functionality.
- Improve network-bridge script.
* Tue Oct 18 2005 garloff@suse.de
- Ignore zombies in the xendomains shutdown procedure and have a
  configurable timeout for the commands. Make xendomains status
  report something useful.
- Make xendomains script comaptible to non-SUSE distros.
* Mon Oct 17 2005 garloff@suse.de
- Update to hg 7398.
* Mon Oct 17 2005 garloff@suse.de
- Create useful xendomains init script and sysconfig file.
* Mon Oct 17 2005 garloff@suse.de
- Create symlinks also for -pae and -dbg hypervisor.
- Build doxygen documentation.
- Include block-nbd script and xen-nbd example config.
- Include patchset info.
* Wed Oct 12 2005 garloff@suse.de
- Update docu.
- Enable xen-dbg hypervisor for gdbserver domU debugging.
* Tue Oct 11 2005 garloff@suse.de
- Update docu.
- Update to hg 7313.
- Move libxenstore.so to xen-tools.
* Tue Oct 11 2005 garloff@suse.de
- Fix buglet in /sbin/xen-vbd.
* Mon Oct 10 2005 garloff@suse.de
- Downgrade to hg 7267.
- Add troubleshooting section to README.SUSE.
* Mon Oct 10 2005 garloff@suse.de
- Fix typo in SrvDomain for mem-set operation.
- Workaround: write directly to balloon in dom0 setMemoryTarget.
- Kill xenconsoled and xenstored in rcxend stop.
* Sun Oct  9 2005 garloff@suse.de
- Update to hg 7278.
- Provide udev rules to setup vifs and vbds in dom0 when domUs
  boot (kraxel).
- Change default FS size for rescue images to 80MB.
* Sat Sep 10 2005 garloff@suse.de
- Update to hg 6715.
- Fix network-bridge down.
* Wed Sep  7 2005 garloff@suse.de
- Build PAE version along non-PAE version of Hypervisor.
* Tue Sep  6 2005 garloff@suse.de
- Try to fix network bridge down issue.
- Document netowrking and firewalling caveats in README.SUSE.
- Enable PAE.
* Tue Sep  6 2005 garloff@suse.de
- Update to hg 6644.
* Sun Sep  4 2005 garloff@suse.de
- Update to hg 6610.
- Rename default name of xen-br0 to xenbr0.
- Fix pygrub installation.
- Use libreiserfs to support pygrub on reiser.
* Mon Aug 29 2005 ccoffing@novell.com
- xen-bridge-net.diff: do not destroy domain 0's network setup
  when starting xend.
* Mon Aug 29 2005 garloff@suse.de
- Update to hg 6458.
- Drop privileged port check -- we use Unix dom sockets anyway
  (#105178).
- init.xend: Fix linebreaks in PID list.
- Correctly assign insserv to xen-tools subpackage.
* Thu Aug 25 2005 garloff@suse.de
- Add dirs /var/run/xenstored and /var/lib/xenstored.
* Thu Aug 25 2005 garloff@suse.de
- Update to hg 6393.
* Mon Aug 22 2005 garloff@suse.de
- Update to hg 6315.
- Include linux-public headers in xen-devel package.
* Sun Aug 21 2005 garloff@suse.de
- Update to hg 6305.
* Sat Aug 20 2005 garloff@suse.de
- Update to hg 6299.
- Enable VNC support (depending on LibVNCServer).
* Sat Aug 20 2005 garloff@suse.de
- Split off xen-tools-ioemu for supporting unmodified guests.
* Fri Aug 19 2005 garloff@suse.de
- Enable pygrub (at the cost of depending on e2fsprogs-devel)
- Enable VMX ioemu SDL support (at the cost of many dependencies)
* Fri Aug 19 2005 garloff@suse.de
- Update to mercurial changeset 6223.
- Move /usr/libexec/xen/ to /usr/lib[64]/xen/bin/.
- Split off -tools package.
* Mon Aug 15 2005 garloff@suse.de
- Create symlinks in %%post.
- Update README.SUSE.
- Mark /etc/xen/ as %%config(noreplace).
- Fix x86-64 build (movl -> mov, lib vs. lib64 inst dirs).
- Remove PYTHONOPTIMIZE.
* Tue Aug  2 2005 ccoffing@novell.com
- Fix warn_unused_result warnings
* Thu Jul 28 2005 ccoffing@novell.com
- Update to latest 3.0-unstable snapshot.
* Wed Jul 13 2005 ccoffing@novell.com
- Fixed bug in glibc24 patch that caused erroneous "out of memory"
  errors
* Fri Jun 24 2005 ccoffing@novell.com
- Fix gcc4 patch that caused a panic in Xen at boot.
* Fri Jun 24 2005 ccoffing@novell.com
- Fix xen-syms link.
* Fri Jun 17 2005 ccoffing@novell.com
- Fix version-check in NetWare loader (0x336ec577 -> 0x326ec578).
* Fri Jun 17 2005 ccoffing@novell.com
- Backport NetWare-friendly loader from Xen 3.0.
* Thu Jun 16 2005 ccoffing@novell.com
- Destroy domains that failed to be fully created.
* Fri Jun 10 2005 garloff@suse.de
- Update to latest 2.0-testing snapshot.
- Use RPM version and release no as xen version.
* Tue Jun  7 2005 garloff@suse.de
- Update mk-xen-rescue-img.sh script: Handle SLES9 better.
- Export PYTHONOPTIMIZE in xend start script.
* Mon Jun  6 2005 garloff@suse.de
- Merge _perform_err fixes.
* Mon May 23 2005 ccoffing@novell.com
- update to 2.0.6
* Wed Apr 13 2005 garloff@suse.de
- More gcc4 and binutils related fixes.
* Wed Apr 13 2005 garloff@suse.de
- Build fixes for gcc4.
* Sun Apr  3 2005 garloff@suse.de
- Update xen: Various fixes (scheduling, memset, domain crash
  handling) and enhancements (bg page scrubbing).
* Thu Mar 24 2005 garloff@suse.de
- xen-bridge-net.diff: Make sure bridge netdev is up after adding
  addresses to it.
* Wed Mar 23 2005 garloff@suse.de
- xen-secure.diff: Check for privileged port before allowing
  certain control operations.
- README.SUSE: Document this change.
* Wed Mar 23 2005 garloff@suse.de
- Require ports < 1024 to allow controlling VMs.
* Mon Mar 21 2005 garloff@suse.de
- Update xen.
* Wed Mar 16 2005 garloff@suse.de
- Update xen.
- Add /var/lib/xen/xen-db/ subdirs.
* Sun Mar 13 2005 garloff@suse.de
- Update to post-2.0.5
- Make /usr/sbin/xm root:trusted 0750
- Drop some patches (merged upstream)
* Tue Mar  8 2005 garloff@suse.de
- Update README with security notes.
- Update mk-xen-rescue-image.sh script allowing to specify the
  kernel version to be used.
- Rather than busy-looping, exit console on a domain that has
  shutdown.
* Mon Mar  7 2005 garloff@suse.de
- Update xen to latest snapshot.
- tgif not needed any more.
* Tue Mar  1 2005 garloff@suse.de
- Include serial-split from Charles Coffing.
* Tue Mar  1 2005 garloff@suse.de
- Update xen to latest snapshot.
* Mon Feb 21 2005 garloff@suse.de
- Update README.SuSE.
- Update xen to latest snapshot.
* Sun Feb 13 2005 garloff@suse.de
- Add init header to xendomains init script.
- Add bridge-utils dependency.
- Update config file and README.
- Activate xend init script on installation.
* Wed Feb  9 2005 ro@suse.de
- remove te_etex and te_pdf from neededforbuild.
* Wed Feb  9 2005 garloff@suse.de
- Update README about IDE dma.
- Default to dhcp.
* Wed Feb  9 2005 garloff@suse.de
- Update to xen post-2.0.4.
- Little bugfix for xen rescue install script.
- Update README.SUSE: Better explanation of root FS creation.
* Sun Jan 23 2005 garloff@suse.de
- Change some defaults to be more secure (xend only binds to
  localhost, ip spoof protection on).
- Avoid ipv6 issue with xend network script.
- Extensive docu in README.SUSE now.
- mk-xen-rescue-img.sh creates a xen root fs image from the std
  SUSE rescue image.
- Put boot.local script in root img to parse ip boot par.
* Thu Jan 20 2005 garloff@suse.de
- Update to newer snapshot.
* Wed Jan 19 2005 garloff@suse.de
- Update to xen-2.0-unstable (post 2.0.3).
* Thu Dec  9 2004 garloff@suse.de
- Initial creation of package xen, xen-doc-*.
- i686 only for now.
