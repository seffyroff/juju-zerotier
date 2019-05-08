from charms.reactive import when, when_not, set_flag, when_all
from charmhelpers.core.hookenv import status_set, config
import subprocess

# zerotier_network_id = config('zerotier-network-id')

@when_not('zerotier.installed')
def install_zerotier():
    status_set('maintenance', 'Installing Zerotier Client')

    install_ctxt = {'install_url': ("https://install.zerotier.com/"),
                    'install_exec': ('sudo bash')}
    cmd_install = ('curl -s {install_url} | {install_exec}'.format(**install_ctxt))

#TODO Switch to secure installer
#TODO output network id to status when connected to network
    # cmd_install = ('curl -s 'https://raw.githubusercontent.com/zerotier/download.zerotier.com/master/htdocs/contact%40zerotier.com.gpg' '
    #                 '| gpg --import && if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi')

    subprocess.check_call(cmd_install, shell=True)

    set_flag('zerotier.installed')
    status_set('maintenance', 'Zerotier installed, ZT address ')
    
# @when_all('zerotier.installed', 'zerotier-network-id')
@when('zerotier.installed')
@when_not ('zerotier.network.joined')
def zt_join_network():

    status_set('maintenance', 'Joining Network {}'.format(config('zerotier-network-id')))

    zt_join_ctxt = {'zerotier_network_id': config('zerotier-network-id')}

    cmd_zt_join_network = ('zerotier-cli join {zerotier_network_id}'.format(**zt_join_ctxt))
    subprocess.check_call(cmd_zt_join_network, shell=True)
    set_flag('zerotier.network.joined')

@when_all('zerotier.installed', 'zerotier.network.joined')
def set_status_active():
    status_set('active', 'Connected to network {}'.format(config('zerotier-network-id')))