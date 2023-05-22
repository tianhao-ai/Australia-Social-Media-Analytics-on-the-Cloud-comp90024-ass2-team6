#!/usr/bin/env bash
. ./group-06-openrc.sh; ansible-playbook --ask-become-pass deploy_backend.yaml -i inventory/application_hosts.ini