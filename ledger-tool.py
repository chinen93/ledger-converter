from src.main import mainConverter, mainReports

import click

@click.command(no_args_is_help=True)
@click.option(
    "--convert",
    is_flag=True,
    help="Convert bank files",
)
@click.option(
    "--report",
    is_flag=True,
    help="Create reports",
)
def main(convert: bool, report: bool) -> None:
    if convert:
        mainConverter()
        return
    if report:
        mainReports()
        return

if __name__ == "__main__":
    main()
