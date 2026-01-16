from config import config_app

import typer
import yaml

app = typer.Typer()

app.add_typer(config_app, name="config")

@app.callback()
def main(context: typer.Context):
    with open(".yaml", "r") as stream:
        context.obj = yaml.safe_load(stream)


if __name__ == "__main__":
    app()
