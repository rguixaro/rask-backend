#!/usr/bin/env bash

DOMAIN=$(/opt/elasticbeanstalk/bin/get-config environment -k DOMAIN)

if [ -e "/home/certs/privkey.pem" ]
then 
    echo "Certificate already stored. Copying to app folder..."
    sudo cp /home/certs/privkey.pem /var/app/current/privkey.pem
    sudo cp /home/certs/fullchain.pem /var/app/current/fullchain.pem

    echo "Changing owner of certificates..."
    sudo chown webapp -R /var/app/current/privkey.pem
    sudo chown webapp -R /var/app/current/fullchain.pem
else
    if [ -d "/home/certs" ]
    then
        echo "Directory /home/certs exists."
    else
        echo "Creating directory /home/certs..."
        sudo mkdir /home/certs
    fi
    echo "Copying certificates to /home/certs..."
    sudo cp /etc/letsencrypt/live/${DOMAIN}/privkey.pem /home/certs/privkey.pem
    sudo cp /etc/letsencrypt/live/${DOMAIN}/fullchain.pem /home/certs/fullchain.pem

    echo "Copying certificates to app folder..."
    sudo cp /home/certs/privkey.pem /var/app/current/privkey.pem
    sudo cp /home/certs/fullchain.pem /var/app/current/fullchain.pem

    echo "Changing owner of certificates..."
    sudo chown webapp -R /var/app/current/privkey.pem
    sudo chown webapp -R /var/app/current/fullchain.pem
fi