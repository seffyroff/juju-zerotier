# Overview

This is a subordinate charm to install the Zerotier-cli client in existing charm deployments to enable cross-model relations and other comms across clouds.


This charm provides Zerotier-Cli. Zerotier is a SDN service useful for connecting machines across the net securely, and with decent throughput performance.

# Usage

juju deploy zerotier-cli

Add your network id to the config zerotier-network-id to join your network, then grant access through the ZT network admin tools.

# Contact Information

PRs accepted at github.com/seffyroff/juju-zerotier

## Upstream Project Name

  - https://www.zerotier.com
  - Upstream bug tracker



[service]: http://example.com
[icon guidelines]: https://jujucharms.com/docs/stable/authors-charm-icon
