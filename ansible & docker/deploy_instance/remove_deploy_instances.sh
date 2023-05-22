#!/usr/bin/env bash

. ./group-06-openrc.sh; ansible-playbook --ask-become-pass remove_deploy_instances.yaml