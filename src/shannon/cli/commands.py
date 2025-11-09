"""Shannon CLI commands"""

import click

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Shannon Framework - Standalone CLI Agent"""
    pass

if __name__ == '__main__':
    cli()
