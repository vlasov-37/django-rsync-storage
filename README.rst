=====
RSYNC STORAGE
=====

django storage for distrubute files  via rsync

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::
   from rsync_storage import RSyncStorage


2. In settings file specify ::
    RSYNC_HOSTS = [
       {'host': '172.17.0.2', 'media_root': '/opt/media/'}
    ]
    * make sure thatn you have ssh connection to "host" for user run your django App
    * make sure you have celery worker started