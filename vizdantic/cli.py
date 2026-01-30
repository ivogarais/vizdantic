#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import skill_install


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='vizdantic')
    subparsers = parser.add_subparsers(dest='command', required=True)

    install_parser = subparsers.add_parser(
        'install-codex-skill',
        help='Install the vizdantic-runner Codex skill globally.',
    )
    install_parser.add_argument(
        '--dest',
        help='Override skills directory (defaults to $CODEX_HOME/skills or ~/.codex/skills).',
    )
    install_parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing install if present.',
    )
    install_parser.add_argument(
        '--symlink',
        action='store_true',
        help='Symlink the skill instead of copying (handy for local dev).',
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == 'install-codex-skill':
        try:
            target = skill_install.install_codex_skill(
                dest=Path(args.dest) if args.dest else None,
                force=args.force,
                symlink=args.symlink,
            )
        except (FileExistsError, FileNotFoundError) as exc:
            print(f'Error: {exc}', file=sys.stderr)
            return 1

        action = 'Symlinked' if args.symlink else 'Copied'
        print(f'{action} vizdantic-runner -> {target}')
        print('Restart Codex to pick up the new skill.')
        return 0

    parser.print_help()
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
