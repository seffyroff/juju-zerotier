#!/bin/bash
juju destroy-model zt9 -y
juju add-model zt9
juju deploy cs:~jameinel/ubuntu-lite-7 --series bionic
charm build
charm push ~/charms/builds/zerotier/
juju deploy cs:~seffyroff/zerotier-32
juju config zerotier zerotier-network-id=e5cd7a9e1c39e9d3
juju add-relation zerotier ubuntu-lite