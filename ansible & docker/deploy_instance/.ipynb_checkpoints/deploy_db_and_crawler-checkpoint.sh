#!/usr/bin/env bash
. ./group6.sh; ansible-playbook --ask-become-pass deploy_db_and_crawler.yaml -i inventory/application_hosts.ini