# -*- coding: utf-8 -*-
#
# Copyright (C) 2003-2014 Sébastien Helleu <flashcode@flashtux.org>
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
# along with WeeChat.org.  If not, see <http://www.gnu.org/licenses/>.
#

from datetime import date

from django.db import models

from weechat.common.tracker \
    import commits_links, tracker_links
from weechat.common.templatetags.localdate import localdate
from weechat.download.models import Release


class Task(models.Model):
    visible = models.BooleanField(default=True)
    version = models.CharField(max_length=32)
    tracker = models.CharField(max_length=64, blank=True)
    status = models.IntegerField(default=0)
    commits = models.CharField(max_length=1024, blank=True)
    component = models.CharField(max_length=64, default='core')
    description = models.CharField(max_length=512)
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        desc = self.description if len(self.description) < 100 \
            else '%s...' % self.description[0:100]
        return '%s%s%s, %s, %d%%, %s: %s (%d)' % (
            '' if self.visible else '(',
            self.version,
            '' if self.visible else ')',
            self.tracker if self.tracker else '-',
            self.status,
            self.component,
            desc,
            self.priority)

    def version_date(self):
        """
        Return date of version (prefixed with "≈ " if the date is
        in the future).
        """
        try:
            release_date = Release.objects.get(version=self.version).date
            if release_date > date.today():
                return '&asymp; %s' % localdate(release_date)
            return localdate(release_date)
        except:
            return ''

    def url_tracker(self):
        return tracker_links(self.tracker) or '-'

    def status_remaining(self):
        return 100 - self.status

    def url_commits(self):
        return commits_links(self.commits)

    class Meta:
        ordering = ['-version', 'priority']