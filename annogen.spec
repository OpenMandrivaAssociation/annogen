# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section         free
%define gcj_support     1

# To make the tarball:
# svn export svn://svn.annogen.codehaus.org/annogen/scm/annogen/tags/release-0_1_0/ annogen

Name:           annogen
Version:        0.1.1
Release:        %mkrel 5.1.6
Epoch:          0
Summary:        Framework to help work with JSR175 Annotations
License:        Public Domain
Group:          Development/Java
URL:            https://www.mathcs.emory.edu/dcl/util/backport-util-concurrent/
Source0:        %{name}-%{version}.tar.gz
Patch0:         annogen-no1.5.patch
Patch1:         annogen-stax-jarnamefix.patch
BuildRequires:  java-rpmbuild, ant, junit
BuildRequires:  antlr >= 0:2.7.4
BuildRequires:  findbugs >= 0:0.9.1
BuildRequires:  bcel >= 0:5.1
BuildRequires:  bea-stax-api >= 0:1.2.0
BuildRequires:  bea-stax >= 0:1.2.0
BuildRequires:  dom4j >= 0:1.6.1
BuildRequires:  qdox >= 0:1.4
BuildRequires:  xerces-j2 >= 0:2.7.1
Requires:       java >= 1.6
Requires:       antlr >= 0:2.7.4
Requires:       bcel >= 0:5.1
Requires:       bea-stax-api >= 0:1.2.0
Requires:       bea-stax >= 0:1.2.0
Requires:       dom4j >= 0:1.6.1
Requires:       findbugs >= 0:0.9.1
Requires:       qdox >= 0:1.4
Requires:       xerces-j2 >= 0:2.7.1

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif

%description
Annogen is a framework which helps you work with JSR175 Annotations. 
In a nutshell, Annogen generates a proxy layer in front of your Annotations.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}
find . -name '*.?ar' | xargs rm -f
%{__perl} -pi -e 's/<javac/<javac nowarn="true"/g' `find . -name 'build*.xml'`

build-jar-repository -s -p external/lib \
        antlr \
        bcel \
        bea-stax-api \
        bea-stax-ri \
        dom4j \
        qdox \
        junit \
        xerces-j2

build-jar-repository -s -p external/findbugs \
        findbugs/findbugs \
        findbugs/findbugs-ant \
        findbugs/findbugs-gui \
        findbugs/findbugs-coreplugin

%patch0
%patch1

%build
export CLASSPATH=$(build-classpath antlr bcel bea-stax-api bea-stax-ri dom4j qdox junit xerces-j2 findbugs/findbugs findbugs/findbugs-ant findbugs/findbugs-gui findbugs/findbugs-coreplugin)
export OPT_JAR_LIST=:
%ant -Dbuild.sysclasspath=only distribution

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 build/distribution/%{name}-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%create_jar_links

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/distribution/docs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%doc %dir %{_javadocdir}/%{name}
