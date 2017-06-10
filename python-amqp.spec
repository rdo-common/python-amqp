%if 0%{?fedora} > 12
%global with_python3 1
%else
# These Sphinx docs do not build with python-sphinx 0.6 (el6)
%endif
%global sphinx_docs 0

%global srcname amqp

Name:           python-%{srcname}
Version:        2.1.4
Release:        2%{?dist}
Summary:        Low-level AMQP client for Python (fork of amqplib)

Group:          Development/Languages
License:        LGPLv2+
URL:            http://pypi.python.org/pypi/amqp
Source0:        https://files.pythonhosted.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz
Patch1:         0001-Don-t-send-AAAA-DNS-request-when-domain-resolved-to-.patch
BuildArch:      noarch

%if 0%{?sphinx_docs}
BuildRequires:  python-sphinx >= 0.8
%endif



%description
Low-level AMQP client for Python

This is a fork of amqplib, maintained by the Celery project.

This library should be API compatible with librabbitmq.


%package -n python2-%{srcname}
Summary:     Client library for AMQP
Requires:    python2-vine
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-nose
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Low-level AMQP client for Python

This is a fork of amqplib, maintained by the Celery project.

This library should be API compatible with librabbitmq.


%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Client library for AMQP
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
%if 0%{?sphinx_docs}
BuildRequires:  python3-sphinx >= 0.8
%endif
%{?python_provide:%python_provide python3-%{srcname}}
Requires:    python3-vine

%description -n python3-%{srcname}
Low-level AMQP client for Python

This is a fork of amqplib, maintained by the Celery project.

This library should be API compatible with librabbitmq.

%endif

%package doc
Summary:        Documentation for python-amqp
Group:          Documentation

Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for python-amqp


%prep
%autosetup -n %{srcname}-%{version} -p1


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif



%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"


%if 0%{?sphinx_docs}
pushd docs

# Disable extensions to prevent intersphinx from accessing net during build.
# Other extensions listed are not used.
sed -i s/^extensions/disable_extensions/ conf.py

SPHINX_DEBUG=1 sphinx-build -b html . build/html
rm -rf build/html/.doctrees build/html/.buildinfo

popd
%endif

%files -n python2-%{srcname}
%doc Changelog README.rst
%license LICENSE
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc Changelog README.rst
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%endif

%files doc
%license LICENSE
%if 0%{?sphinx_docs}
%doc docs/build/html docs/reference
%endif


%changelog
* Sat Jun 10 2017 Ihar Hrachyshka <ihrachys@redhat.com> - 2.1.4-2
- Don't send AAAA DNS request when domain resolved to IPv4

* Wed Feb 08 2017 Matthias Runge <mrunge@redhat.com> - 2.1.4-1
- upgrade to 2.1.4 (rhbz#1340298)
- modernize spec, add provides (rhbz#1399248)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.4.9-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Eric Harney <eharney@redhat.com> - 1.4.9-1
- Update to 1.4.9

* Thu Jan 07 2016 Eric Harney <eharney@redhat.com> - 1.4.8-1
- Update to 1.4.8

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Nov 11 2015 Eric Harney <eharney@redhat.com> - 1.4.7-1
- Update to 1.4.7

* Wed Nov 04 2015 Matej Stuchlik <mstuchli@redhat.com> - 1.4.6-3
- Rebuilt for Python 3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 06 2014 Eric Harney <eharney@redhat.com> - 1.4.6-1
- Update to 1.4.6

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 16 2014 Eric Harney <eharney@redhat.com> - 1.4.5-1
- Update to 1.4.5

* Fri Feb 07 2014 Eric Harney <eharney@redhat.com> - 1.4.2-1
- Update to 1.4.2

* Fri Jan 17 2014 Eric Harney <eharney@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Fri Nov 15 2013 Eric Harney <eharney@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Fri Oct 25 2013 Eric Harney <eharney@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Tue Oct 08 2013 Eric Harney <eharney@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Fri Sep 20 2013 Eric Harney <eharney@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Eric Harney <eharney@redhat.com> - 1.0.11-1
- Initial package
