#!/bin/bash

LOG_FILE=$1

echo $(date +'%Y-%m-%d %H:%M') Starting S3 backup >> $LOG_FILE

s3cmd sync --delete-removed --exclude 'raw/*' --exclude '/.*' /mnt/backup/zotac/Foto/ s3://pirkojm-backup/Foto/
FOTO=$?

s3cmd sync --delete-removed --exclude="la quadrilla/*" /mnt/backup/zotac/Video/archiv/ s3://pirkojm-backup/VideoArchiv/
VIDEO=$?

echo $(date +'%Y-%m-%d %H:%M') Finished S3 backup. Foto result: $FOTO, Video result: $VIDEO >> LOG_FILE
