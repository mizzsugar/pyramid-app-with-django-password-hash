import argparse
import pathlib
import sqlite3
from typing import (
    Final,
    List,
)


def _list_migrations() -> List[pathlib.Path]:
    migration_directory: Final = (
        pathlib.Path(__file__).parent.parent.parent / 'migrations')
    return sorted(migration_directory.glob('*.sql'))


def _apply_migration(database: str, migration: pathlib.Path) -> None:
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.executescript(migration.read_text())
    connection.close()


def _migrate(database: str, quiet: bool) -> None:
    for migration in _list_migrations():
        _apply_migration(database, migration)
        if not quiet:
            print('success', migration.name)


def migrate(database: str, args: argparse.Namespace) -> None:
    _migrate(database=database, quiet=False)


def _recreate(
        database: str,
        quiet: bool,
        migrate: bool,
) -> None:
    db_path = pathlib.Path(database)
    if db_path.exists():
        db_path.unlink()
    if migrate:
        _migrate(database=database, quiet=quiet)


def recreate(args: argparse.Namespace) -> None:
    _recreate(database='db.sqlite3', quiet=False, migrate=migrate)


def main() -> None:
    parser: Final = argparse.ArgumentParser(__doc__)
    parser.set_defaults(func=lambda args: parser.print_help())
    parser.add_argument('--no-interactive', action='store_true')

    subpaersers: Final = parser.add_subparsers()

    recreate_parser: Final = subpaersers.add_parser(
        'recreate',
        help="""Recreate database after destroying database.
        All migrations will be applied.
        """)
    recreate_parser.set_defaults(func=recreate)

    migrate_parser: Final = subpaersers.add_parser(
        'migrate',
        help="""all migrations will be applied.
If some error occurs, next migration will be applied.
        """)
    migrate_parser.set_defaults(func=migrate)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
