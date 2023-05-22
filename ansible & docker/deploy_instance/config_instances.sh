#!/usr/bin/env bash
. ./group6.sh; ansible-playbook --ask-become-pass config_instances.yaml -i inventory/application_hosts.ini