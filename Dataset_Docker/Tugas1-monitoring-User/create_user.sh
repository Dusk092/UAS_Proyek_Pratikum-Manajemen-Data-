#!/bin/bash

while read username
do
    sudo useradd -m "$username"

    echo "$username:${username}@123" | sudo chpasswd

    echo "User $username berhasil dibuat dengan password ${username}@123"

done < users.txt
