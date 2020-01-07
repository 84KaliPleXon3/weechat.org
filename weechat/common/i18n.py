# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2020 Sébastien Helleu <flashcode@flashtux.org>
#
# This file is part of WeeChat.org.
#
# WeeChat.org is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# WeeChat.org is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WeeChat.org.  If not, see <https://www.gnu.org/licenses/>.
#

"""Some i18n useful functions."""

from io import open

from weechat.common.path import project_path_join


def i18n_autogen(app, name, strings):
    """Create a file '_i18n_xxx.py' with strings to translate."""
    # build content of file
    content = [
        '# -*- coding: utf-8 -*-',
        '# This file is auto-generated after changes in database, '
        'DO NOT EDIT!',
        '',
        '# flake8: noqa',
    ]
    if strings:
        content += [
            '',
            'from django.utils.translation import gettext_noop',
            '',
            '',
            'def __i18n_%s():' % name,
        ]
        done = set()
        for string in sorted(strings):
            if type(string) is tuple:
                # if type is tuple of 2 strings: use the second as note for
                # translators
                (message, translators) = (string[0], string[1])
            else:
                # single string (no note for translators)
                (message, translators) = (string, None)
            # add string if not already done
            if message not in done:
                if translators:
                    content.append('    # Translators: %s' % translators)
                content.append('    gettext_noop("%s")' %
                               (message
                                .replace('\\', '\\\\')
                                .replace('"', '\\"')
                                .replace('\r\n', '\\n')))
                done.add(message)
    content.append('')
    # write file
    filename = project_path_join(app, '_i18n_%s.py' % name)
    with open(filename, 'w', encoding='utf-8') as _file:
        data = '\n'.join(content)
        if hasattr(data, 'decode') and isinstance(data, str):
            data = data.decode('utf-8')
        _file.write(data)
