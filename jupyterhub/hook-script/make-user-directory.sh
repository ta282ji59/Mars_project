#!/bin/bash

# adding user and making the user directory
adduser -q --gecos '""' --disabled-password $1
mkdir -p -m 777 /data/users/$1/
chown $1: /data/users/$1/