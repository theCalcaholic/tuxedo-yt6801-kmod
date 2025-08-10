%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:           tuxedo-yt6801-kmod
Version:        1.0.30tux2
Release:        1%{?dist}
Summary:        Tuxedo driver for NIC yt6801 as kmod

License:        GPL-2.0-or-later
URL:            https://gitlab.com/tuxedocomputers/development/packages/tuxedo-yt6801
Source:         %{url}/-/archive/v%{version}/tuxedo-yt-6801-v%{version}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  kmodtool
BuildRequires:  kernel-devel
BuildRequires:  make
BuildRequires:  gcc

Provides: tuxedo-yt6801 = %{version}
Obsoletes: tuxedo-yt-6801 < 1.0.0

%description
Tuxedo driver for NIC yt6801 as kmod

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%prep
cd '%{_builddir}'
rm -rf 'tuxedo-yt6801-%{version}'
/usr/lib/rpm/rpmuncompress -x "${RPM_SOURCE_DIR}/tuxedo-yt-6801-v%{version}.tar.gz"
STATUS=$?
if [ $STATUS -ne 0 ]; then
  exit $STATUS
fi
mv "%{_builddir}/tuxedo-yt6801-v%{version}"* "%{_builddir}/tuxedo-yt6801-v%{version}"

cp "%{_builddir}/tuxedo-yt6801-v%{version}/debian/copyright" "%{_builddir}/copyright"

cd 'tuxedo-yt6801-v%{version}'
/usr/bin/chmod -Rf a+rX,u+w,g-w,o-w .

echo "kernel versions: %{?kernel_versions}"
echo "kernels: %{?kernels}"

for kernel_version in %{?kernel_versions}; do
  cp -a src %{_builddir}/_kmod_build_${kernel_version%%___*}
done

%build
echo "Build stage -----------------------------------------------------------------------------------------------"

set -ex
for kernel_version in %{?kernel_versions}; do
  make V=1 %{?_smp_mflags} -C /lib/modules/${kernel_version%%___*}/build M=%{_builddir}/_kmod_build_${kernel_version%%___*} modules
done

%install
echo "Install stage ---------------------------------------------------------------------------------------------"

set -x

for kernel_version in %{?kernel_versions}; do
  mkdir -p %{buildroot}/lib/modules/${kernel_version%%___*}/extra/tuxedo-yt6801/
  install -D -m 755 %{_builddir}/_kmod_build_${kernel_version%%___*}/*.ko %{buildroot}/lib/modules/${kernel_version%%___*}/extra/tuxedo-yt6801
  chmod a+x %{buildroot}/lib/modules/${kernel_version%%___*}/extra/tuxedo-yt6801/*.ko

done

%{?akmod_install}

%files


%license copyright
#%doc README.md


%changelog

