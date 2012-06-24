Summary:	Utils to manage the Linux SCSI device namespace
Summary(pl):	Narz�dzia do zarz�dzania przestrzeni� nazw urz�dze� SCSI pod Linuksem
Name:		scsiname
Version:	0.1.0
Release:	0.2
License:	GPL
Group:		Applications/System
Source0:	http://www-124.ibm.com/devreg/%{name}-%{version}.tar.gz
# Source0-md5:	4e8ef9f2dcc602643390189c849577b3
URL:		http://www-124.ibm.com/devreg/
Requires:	hotplug
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The purpose of this project is to manage the Linux device (/dev)
namespace so that names of devices remain the same across boots.

Today in Linux there exists the potential for device name slippage.
Currently device names are assigned based on discovery order or
topology. When hardware configuration changes or hardware failures
occur, different name assignments may result. In order to address this
slippage two utilities are offered that allow a device to be named
based on the characteristics of the device itself.

This utility
- utilizes SCSI sg kernel interface to collect device information,
- is targeted specifically to SCSI devices,
- is implemented completely in userspace,
- is hooked into hotplug framework to automatically assign names.

%description -l pl
Celem tego projektu jest zarz�dzanie przestrzeni� nazw urz�dze� pod
Linuksem (/dev) tak, �eby nazwy urz�dze� pozostawa�y takie same
pomi�dzy uruchomieniami.

Obecnie w Linuksie istnieje potencjalna mo�liwo�� przesuni�cia nazwy.
Aktualnie nazwy urz�dze� s� nadawane w zale�no�ci od kolejno�ci
wykrywania lub topologii. Kiedy zmienia si� konfiguracja sprz�tu lub
zachodzi awaria sprz�towa, mog� wyst�pi� r�ne przypisania nazw. Aby
zapobiec tym przesuni�ciom dost�pne s� dwa narz�dzia pozwalaj�ce na
nazwanie urz�dzenia w oparciu o charakterystyk� samego urz�dzenia.

To narz�dzie:
- wykorzystuje interfejs j�dra SCSI sg do zgromadzenia informacji o
  urz�dzeniu,
- jest przeznaczone specjalnie dla urz�dze� SCSI,
- jest zaimplementowane ca�kowicie w przestrzeni u�ytkownika,
- jest podpi�te do �rodowiska hotplug, aby automatycznie przypisywa�
  nazwy.

%prep
%setup -q

%build
%{__make} \
	CEXTRAS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir}}

%{__make} install \
	EXE_DIR=$RPM_BUILD_ROOT%{_sbindir}

cat > $RPM_BUILD_ROOT%{_sysconfdir}/scsiname.conf <<END
#name=UIBM-PCCODGHS6800BA25GKpart1
#host=1
#bus=0
#target=3
#lun=0
#part=1
#vendor=IBM-PCCO
#model=DGHS18Y*
#rev=04F0
#alias=/dev/z_scsi/partition1
#symlink=/dev/z_scsi/partition1
END

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README UsersGuide
%attr(750,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
