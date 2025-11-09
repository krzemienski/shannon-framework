"""Shannon CLI entry point"""

def main():
    """Entry point for python -m shannon"""
    from shannon.cli.commands import cli
    cli()

if __name__ == '__main__':
    main()
