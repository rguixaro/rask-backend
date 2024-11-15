#!/usr/bin/env bash

DOMAIN_EMAIL=$(/opt/elasticbeanstalk/bin/get-config environment -k DOMAIN_EMAIL)
DOMAIN=$(/opt/elasticbeanstalk/bin/get-config environment -k DOMAIN)

sudo certbot -n -d $DOMAIN --nginx --agree-tos --email $DOMAIN_EMAIL