#!/usr/bin/env python3

import click
import logging
from pathlib import Path
from typing import Optional, Tuple

from .conflict_resolver import ConflictResolver
from .meta_file_handler import MetaFileHandler

logging.basicConfig(level=logging.DEBUG)

def validate_files(carcols_path: str, carvariations_path: str) -> Tuple[Path, Path]:
    """Validate input files exist and are proper meta files."""
    file_handler = MetaFileHandler()

    carcols = Path(carcols_path)
    carvariations = Path(carvariations_path)

    if not carcols.exists():
        raise click.BadParameter(f"Carcols meta file not found: {carcols}")
    if not carvariations.exists():
        raise click.BadParameter(f"Carvariations meta file not found: {carvariations}")

    if not file_handler.validate_meta_file(str(carcols)):
        raise click.BadParameter(f"Invalid carcols meta file: {carcols}")
    if not file_handler.validate_meta_file(str(carvariations)):
        raise click.BadParameter(f"Invalid carvariations meta file: {carvariations}")

    return carcols, carvariations

@click.group()
@click.version_option()
def cli():
    """GTA V FiveM Meta File Conflict Resolution Tool"""
    pass

@cli.command()
@click.argument('carcols_path', type=click.Path(exists=True))
@click.argument('carvariations_path', type=click.Path(exists=True))
@click.option('--vehicle', '-v', help='Process specific vehicle (optional)')
def resolve_carcols(carcols_path: str, carvariations_path: str, vehicle: Optional[str]):
    """Resolve carcols ID conflicts in meta files."""
    try:
        carcols, carvariations = validate_files(carcols_path, carvariations_path)

        # Create resolver and backup files
        resolver = ConflictResolver(str(carcols), str(carvariations))
        resolver.file_handler.backup_files([str(carcols), str(carvariations)])

        # Resolve conflicts
        changes = resolver.resolve_carcols_conflicts(vehicle)

        # Report changes
        click.echo("\nChanges made:")
        click.echo("\nCarcols.meta changes:")
        for old, new in changes['carcols']:
            click.echo(f"  {old} → {new}")

        click.echo("\nCarvariations.meta changes:")
        for old, new in changes['variations']:
            click.echo(f"  {old} → {new}")

        click.echo("\nBackups created in backups_* directory")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@cli.command()
@click.argument('carcols_path', type=click.Path(exists=True))
@click.argument('carvariations_path', type=click.Path(exists=True))
@click.option('--vehicle', '-v', help='Process specific vehicle (optional)')
def resolve_modkits(carcols_path: str, carvariations_path: str, vehicle: Optional[str]):
    """Resolve modkit ID conflicts in meta files."""
    try:
        carcols, carvariations = validate_files(carcols_path, carvariations_path)

        # Create resolver and backup files
        resolver = ConflictResolver(str(carcols), str(carvariations))
        resolver.file_handler.backup_files([str(carcols), str(carvariations)])

        # Resolve conflicts
        changes = resolver.resolve_modkit_conflicts(vehicle)

        # Report changes
        click.echo("\nChanges made:")
        click.echo("\nCarcols.meta changes:")
        for old, new in changes['carcols']:
            click.echo(f"  {old} → {new}")

        click.echo("\nCarvariations.meta changes:")
        for old, new in changes['variations']:
            click.echo(f"  {old} → {new}")

        click.echo("\nBackups created in backups_* directory")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()
