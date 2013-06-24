%if 0%{?fedora} > 12
%global with_python3 1
%global sphinx_docs 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%global sphinx_docs 0
# These Sphinx docs do not build with python-sphinx 0.6 (el6)
%endif

%global srcname amqp

Name:           python-%{srcname}
Version:        1.0.11
Release:        1%{?dist}
Summary:        Low-level AMQP client for Python (fork of amqplib)

Group:          Development/Languages
License:        LGPLv2+
URL:            http://pypi.python.org/pypi/amqp
Source0:        http://pypi.python.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose
%if 0%{?sphinx_docs}
BuildRequires:  python-sphinx >= 0.8
%endif


%description
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

%description -n python3-%{srcname}
Low-level AMQP client for Python

This is a fork of amqplib, maintained by the Celery project.

This library should be API compatible with librabbitmq.

%endif


%prep
%setup -q -n %{srcname}-%{version}
%if 0%{?with_python3}
cp -a . %{py3dir}
%endif


%build
%{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif



%install
%{__python} setup.py install --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

# Remove execute bit from example scripts (packaged as doc)
chmod -x demo/*.py

%if 0%{?sphinx_docs}
pushd docs

# Disable extensions to prevent intersphinx from accessing net during build.
# Other extensions listed are not used.
sed -i s/^extensions/disable_extensions/ conf.py

SPHINX_DEBUG=1 sphinx-build -b html . build/html
rm -rf build/html/.doctrees build/html/.buildinfo

popd
%endif

%files
%doc Changelog LICENSE README.rst
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}*.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc Changelog LICENSE README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}*.egg-info
%endif

%package doc
Summary:        Documentation for python-amqp
Group:          Documentation
License:        LGPLv2+

Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for python-amqp

%files doc
%doc LICENSE demo/
%if 0%{?sphinx_docs}
%doc docs/build/html docs/reference
%endif


%changelog
* Fri Jun 21 2013 Eric Harney <eharney@redhat.com> - 1.0.11-1
- Initial package
