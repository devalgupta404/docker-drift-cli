import click, json
from driftcli.fs_diff import get_fs_diff
from driftcli.env_diff import compare_env

@click.group()
def cli():
    """Docker Drift CLI - detect drift between containers and images."""
    pass

@cli.command()
@click.option("--container", required=True, help="Container ID or name")
@click.option("--image", required=True, help="Image name:tag")
@click.option("--format", default="text", type=click.Choice(["json", "text"]))
def scan(container, image, format):
    """Scan container for drift vs its image."""
    click.echo("🔍 Scanning container for drift...")

    fs_changes = get_fs_diff(container)
    env_changes = compare_env(container, image)

    result = {
        "filesystem": fs_changes,
        "env": env_changes
    }

    if format == "json":
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo("\nFilesystem changes:")
        if isinstance(fs_changes, list) and fs_changes:
            for change in fs_changes:
                click.echo(f"  {change}")
        else:
            click.echo("  No filesystem changes detected.")

        click.echo("\nEnv changes:")
        click.echo(f"  Added: {env_changes['added']}")
        click.echo(f"  Removed: {env_changes['removed']}")
        click.echo(f"  Modified: {env_changes['modified']}")

if __name__ == "__main__":
    cli()
