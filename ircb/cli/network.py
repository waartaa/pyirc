# -*- coding: utf-8 -*-
import click

from ircb.storeclient import NetworkStore
from ircb.lib.async import coroutinize

@click.group(name='networks')
def network_cli():
    """Manager networks"""
    pass


@click.command(name='create')
@click.argument('user')
@click.argument('network_name')
@click.argument('host')
@click.argument('port')
@click.argument('nick')
@click.option('--realname', default='')
@click.option('--username', default='')
@click.option('--password', default='')
@click.option('--usermode', default='0')
@click.option('--ssl', default=False)
@click.option('--ssl_verify', default="CERT_NONE")
@coroutinize
def network_create(user, network_name, host, port, nick, realname, 
                   username, password, usermode, ssl, ssl_verify):
    """Create a network for a user"""
    network = yield from NetworkStore.create(
        dict(
            user=user,
            name=network_name,
            nickname=nick,
            hostname=host,
            port=port,
            realname=realname,
            username=username,
            password=password,
            usermode=usermode,
            ssl=ssl,
            ssl_verify=ssl_verify
        )
    )
    print(network.access_token)


network_cli.add_command(network_create)
