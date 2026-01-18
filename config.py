from rich.console import Console
from rich.table import Table
from typing import Annotated, Any

import base64
import typer
import yaml

config_app = typer.Typer()

console = Console()


@config_app.command()
def delete_context(label: str, username: str):
    try:
        with open(".yaml", "r") as stream:
            data: dict[str, Any] = yaml.safe_load(stream) or {}
    except FileNotFoundError:
        data = {}

    if label not in data:
        return

    data[label].pop(username, None)

    if not data[label]:
        data.pop(label, None)

    with open(".yaml", "w") as stream:
        yaml.safe_dump(data, stream)


@config_app.command()
def get_context(context: typer.Context):
    data: dict[str, Any] = context.obj or {}

    table = Table("CURRENT", "LABEL", "USERNAME")

    for label, usernames in data.items():
        for username, data in usernames.items():
            current = "*" if data.get("current") == "*" else ""

            table.add_row(current, label, username)

    console.print(table)


@config_app.command()
def set_context(
    label: str,
    username: str,
    password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
):
    try:
        with open(".yaml", "r") as stream:
            data: dict[str, Any] = yaml.safe_load(stream) or {}
    except FileNotFoundError:
        data = {}

    is_first = len(data) == 0

    data.setdefault(label, {})

    data[label].setdefault(username, {})

    if is_first:
        data[label][username].setdefault("current", "*")

    data[label][username]["password"] = base64.b64encode(
        password.encode("utf-8")
    ).decode("utf-8")

    with open(".yaml", "w") as stream:
        yaml.safe_dump(data, stream)
