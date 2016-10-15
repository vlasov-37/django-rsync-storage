#-*- coding: utf8 -*-
from django.utils.deconstruct import deconstructible
from django.core.files.storage import FileSystemStorage

from django.conf import settings

import os
from tasks import rsync_task
CURRENT_HOST = 'current'


@deconstructible
class RSyncStorage(FileSystemStorage):

    def _add_prefix(self, name):
        """
        name - примерно такого вида - orders_media/1_rGSQIX2.png
        """
        current_settings = next(iter([s for s in settings.RSYNC_HOSTS if s.get('host') == CURRENT_HOST]), None)
        if not current_settings or not current_settings.get('prefix'):
            return name
        upload_dir, file_name = os.path.split(name)
        prefix = current_settings.get('prefix')
        file_name = prefix + file_name
        new_name = os.path.join(*(upload_dir, file_name))
        return new_name

    """Backend that stores files both locally and remotely over HTTP."""
    def _save(self, name, content):
        """
        RSYNC_HOST_DATA = {
         'host': '172.17.0.2',
         'media_root': '/var/opt/project/media/'
        }
        name = orders_media/1_rGSQIX2.png    # Это <upload_to>/<file_name>

        upload_to на серверах должен быть одинаковым.
        """
        name = self._add_prefix(name)
        name = FileSystemStorage._save(self, name, content)
        abs_path_to_file_from = os.path.join(settings.MEDIA_ROOT, name)
        for RSYNC_HOST_CONF in settings.RSYNC_HOSTS:
            RSYNC_HOST_TO = RSYNC_HOST_CONF['host']
            if RSYNC_HOST_TO == CURRENT_HOST:
                continue
            RSYNC_MEDIA_ROOT_TO = RSYNC_HOST_CONF['media_root']
            abs_path_file_name_to = os.path.join(RSYNC_MEDIA_ROOT_TO, name)
            dir_to = os.path.dirname(abs_path_file_name_to) + '/'
            remote_dir_to = '%s:%s' % (RSYNC_HOST_TO, dir_to)
            dir_from = os.path.dirname(abs_path_to_file_from) + '/'
            rsync_task.delay(dir_from, remote_dir_to)
        return name



