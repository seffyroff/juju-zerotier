from charms.reactive import when, when_not, set_flag, when_all
from charmhelpers.core.hookenv import status_set, config, application_version_set
from charmhelpers.fetch import get_upstream_version
import subprocess
import json

@when_not('zerotier.installed')
def install_zerotier():
    status_set('maintenance', 'Installing Zerotier Client')

    install_ctxt = {'install_url': ("https://raw.githubusercontent.com/zerotier/download.zerotier.com/master/htdocs/contact%40zerotier.com.gpg"),
                    'install_exec': ("gpg --import && if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo \"$z\" | sudo bash; fi")}
    cmd_install = ('curl -s {install_url} | {install_exec}'.format(**install_ctxt))


    subprocess.check_call(cmd_install, shell=True)

    set_flag('zerotier.installed')
    zt_address_output = subprocess.check_output('zerotier-cli -j info', shell=True)
    zt_address_json = json.loads(zt_address_output)
    zt_address_ref = zt_address_json['address']
    status_set('maintenance', 'Zerotier installed, ZT address {}'.format(zt_address_json['address']))
    application_version_set(get_upstream_version('zerotier-one'))

@when('zerotier.installed')
@when_not ('zerotier.network.joined')
def zt_join_network():

    status_set('maintenance', 'Joining Network {}'.format(config('zerotier-network-id')))

    zt_join_ctxt = {'zerotier_network_id': config('zerotier-network-id')}

    cmd_zt_join_network = ('zerotier-cli join {zerotier_network_id}'.format(**zt_join_ctxt))
    subprocess.check_call(cmd_zt_join_network, shell=True)
    set_flag('zerotier.network.joined')
    status_set('maintenance', 'Connected to network {}'.format(config('zerotier-network-id')))
@when_all('zerotier.installed', 'zerotier.network.joined')
def set_status_active():
    zt_address_output = subprocess.check_output('zerotier-cli -j info', shell=True)
    zt_address_json = json.loads(zt_address_output)
    zt_address_ref = zt_address_json['address']
    status_set('active', '{} connected to network'.format(zt_address_json['address']))