%global pypi_name semantic_version
%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           python-%{pypi_name}
Version:        2.6.0
Release:        5%{?dist}
Summary:        Library implementing the 'SemVer' scheme

License:        BSD
URL:            https://github.com/rbarrois/python-semanticversion
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

Patch1:         0001-Fix-django-tests.patch

%global _description \
This small python library provides a few tools to handle semantic versioning\
in Python.

%description %{_description}

%if %{with python2}
%package -n     python2-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python2-devel
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  python-setuptools
%else
BuildRequires:  python2-setuptools
%endif
#BuildRequires:  python2-django
%{?python_provide:%python_provide python2-%{pypi_name}}
Provides:       python-semantic-version

%description -n python2-%{pypi_name} %{_description}

Python 2 version.
%endif # with python2

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
#BuildRequires:  python3-django
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %{_description}

Python 3 version
%endif

%package doc
Summary:        Documentation for python-%{pypi_name}
BuildRequires:  python3-sphinx

%description doc
%{summary}.

%prep
%autosetup -p1 -n python-semanticversion-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# documentation builds due to broken symlink
# https://github.com/rbarrois/python-semanticversion/issues/20
rm docs/credits.rst

%build
%if %{with python2}
%py2_build
%endif # with python2
%if %{with python3}
%py3_build
%endif
# generate html docs
sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%if %{with python2}
%py2_install
%endif # with python2
%if %{with python3}
%py3_install
%endif

%check
%if %{with python2}
%{__python2} setup.py test
%endif # with python2
%if %{with python3}
%{__python3} setup.py test
%endif

%if %{with python2}
%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst ChangeLog
%{python2_sitelib}/%{pypi_name}/
%{python2_sitelib}/%{pypi_name}-*.egg-info/
%endif # with python2

%if %{with python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst ChangeLog
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.egg-info/
%endif

%files doc
%license LICENSE
%doc html

%changelog
* Wed Jul 18 2018 Brian C. Lane <bcl@redhat.com> - 2.6.0-5
- Enable tests
- Fix django test, it should be skipped when django is not installed

* Wed Jul 18 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.6.0-4
- Conditionalize the python2 subpackage
- Use python3-sphinx for docs
- Remove django dependency

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.6.0-1
- Update to 2.6.0
- Make package to comply guidelines

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 24 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 2.5.0-1
- Upstream 2.5.0
- Add python3 subpackage

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 03 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2.4.2-1
- Upstream 2.4.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 01 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2.4.1-1
- Upstream 2.4.1

* Mon Mar 30 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2.3.1-1
- Initial package.
