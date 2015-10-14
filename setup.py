# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(
    name='gs.group.messages.topic.base',
    version=version,
    description="Topics in a GroupServer Group",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Natural Language :: French",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: JavaScript",
        "Programming Language :: PL/SQL",
        "Topic :: Communications :: Email",
        "Topic :: Communications :: Email :: Mailing List Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='groupserver, message, post, topic',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='https://github.com/groupserver/gs.group.messages.topic.base',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.group', 'gs.group.messages',
                        'gs.group.messages.topic'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'SQLAlchemy',
        'zope.browserpage',
        'zope.browserresource',
        'zope.cachedescriptors',
        'zope.component',
        'zope.contentprovider',
        'zope.formlib',
        'zope.i18n[compile]',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.location',
        'zope.publisher',
        'zope.schema',
        'zope.security',
        'zope.sqlalchemy',
        'zope.tal',
        'zope.tales',
        'zope.viewlet',
        'gs.content.js.multifile[zope]',
        'gs.content.js.sharebox[zope]',
        'gs.content.layout',
        'gs.core',
        'gs.database',
        'gs.group.base',
        'gs.group.member.canpost',
        'gs.group.member.viewlet',
        'gs.group.messages.add.base',
        'gs.group.messages.post.base',
        'gs.group.messages.post.page',
        'gs.group.messages.privacy',
        'gs.group.privacy',
        'gs.help',
        'gs.profile.email.base',
        'gs.viewlet',
        'Products.XWFCore',
        'Products.XWFFileLibrary2',
        'Products.XWFMailingListManager',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)
