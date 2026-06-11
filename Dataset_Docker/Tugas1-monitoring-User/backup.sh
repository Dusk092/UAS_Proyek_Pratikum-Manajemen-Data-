#!/bin/bash

tanggal=$(date +%Y%m%d_%H%M%S)

tar --exclude='lost+found' -czvf /backup/backup_$tanggal.tar.gz /mnt/dataku
