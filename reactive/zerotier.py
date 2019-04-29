from charms.reactive import when, when_not, set_flag, when_all
from subprocess import call


@when_not('zerotier.installed')
def install_zerotier():
    status_set('maintenance', 'Installing Zerotier Client')
    
    cmd_install = \
        ('curl -s 'https://raw.githubusercontent.com/zerotier/download.zerotier.com/master/htdocs/contact%40zerotier.com.gpg'
            '| gpg --import && if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi)'.format()
    call(cmd_install.split())
    set_flag('zerotier.installed')

@when('zerotier.installed')
@when_not ('zerotier.network.joined')
def zt_join_network():
    status_set('maintenance', 'Joining Network {}'.format(config('zerotier-network-id')))

    zt_join_ctxt = {'zerotier_network_id': config('zerotier-network-id')}

    cmd_zt_join_network = ('zerotier-cli join {}'.format(**zt_join_ctxt))
    call(cmd_zt_join_network.split())
    set_flag('zerotier.network.joined')

@when_all('zerotier.installed', 'zerotier.network.joined')
    status_set('active', 'Connected to network {}'.format(config('zerotier-network-id')))