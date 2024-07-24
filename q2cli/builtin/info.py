# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import click

from q2cli.click.command import ToolCommand


def _echo_version():
    import sys
    import qiime2
    import q2cli

    pyver = sys.version_info
    click.echo('Python version: %d.%d.%d' %
               (pyver.major, pyver.minor, pyver.micro))
    click.echo('QIIME 2 release: %s' % qiime2.__release__)
    click.echo('QIIME 2 version: %s' % qiime2.__version__)
    click.echo('q2cli version: %s' % q2cli.__version__)


def _echo_plugins():
    import q2cli.core.cache

    plugins = q2cli.core.cache.CACHE.plugins
    if plugins:
        for name, plugin in sorted(plugins.items()):
            click.echo('%s: %s' % (name, plugin['version']))
    else:
        click.secho('No plugins are currently installed.\nYou can browse '
                    'the official QIIME 2 plugins at https://qiime2.org')


@click.command(help='Display information about current deployment.',
               cls=ToolCommand)
def info():
    import q2cli.util
    # This import improves performance for repeated _echo_plugins
    import q2cli.core.cache
    from qiime2.sdk.parallel_config import \
        (PARALLEL_CONFIG, get_vendored_config, load_config_from_dict)
    from tomlkit import dumps
    from parsl import Config

    click.secho('System versions', fg='green')
    _echo_version()
    click.secho('\nInstalled plugins', fg='green')
    _echo_plugins()

    click.secho('\nApplication config directory', fg='green')
    click.secho(q2cli.util.get_app_dir())

    click.secho('\nParallel Config', fg='green')
    parallel_config = PARALLEL_CONFIG.parallel_config
    config_source = 'Memory'

    mapping = PARALLEL_CONFIG.action_executor_mapping
    mapping_source = 'Memory'

    if not parallel_config or not mapping:
        vendored_config, vendored_mapping, vendored_source = \
            get_vendored_config()

        if not parallel_config:
            config_source = vendored_source
            parallel_config = vendored_config

        if not mapping:
            mapping_source = vendored_source
            mapping = vendored_mapping

    click.secho(f'Config Source: {config_source}')
    # parallel_config, _ = load_config_from_dict(parallel_config)
    if isinstance(parallel_config, Config):
        click.secho(parallel_config.__dict__)
    elif parallel_config:
        click.secho(dumps(parallel_config))
    else:
        click.secho('{}')

    click.secho(f'\nMapping Source: {mapping_source}')
    if not mapping:
        click.secho('{}')
    else:
        click.secho(dumps(mapping))

    click.secho('\nGetting help', fg='green')
    click.secho('To get help with QIIME 2, visit https://qiime2.org')
