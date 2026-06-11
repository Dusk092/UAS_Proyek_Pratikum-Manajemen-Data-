#!/bin/bash

sisa=$(df -h / | awk 'NR==2 {print $5}')

echo "Notifikasi : Space HDD anda tinggal $sisa"
