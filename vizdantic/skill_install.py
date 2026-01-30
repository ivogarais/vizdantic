#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
from importlib import metadata
from pathlib import Path

SKILL_NAME = 'vizdantic-runner'
SKILL_RELATIVE_PATH = Path('skills') / SKILL_NAME


def _default_codex_skills_dir() -> Path:
    codex_home = os.environ.get('CODEX_HOME')
    if codex_home:
        return Path(codex_home).expanduser() / 'skills'
    return Path('~/.codex/skills').expanduser()


def _remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _resolve_skill_source(repo_root: Path | None = None) -> Path:
    if repo_root:
        candidate = repo_root / SKILL_RELATIVE_PATH
        if candidate.is_dir():
            return candidate

    try:
        dist = metadata.distribution('vizdantic')
    except metadata.PackageNotFoundError as exc:
        raise FileNotFoundError('Vizdantic distribution not found.') from exc

    if not dist.files:
        raise FileNotFoundError('Vizdantic distribution files are unavailable.')

    target_suffix = str(SKILL_RELATIVE_PATH / 'SKILL.md')
    for file in dist.files:
        if str(file).endswith(target_suffix):
            return dist.locate_file(file).parent

    raise FileNotFoundError(
        f'Could not locate {SKILL_RELATIVE_PATH} inside the vizdantic distribution.'
    )


def install_codex_skill(
    *,
    dest: Path | None = None,
    force: bool = False,
    symlink: bool = False,
    repo_root: Path | None = None,
) -> Path:
    source = _resolve_skill_source(repo_root)
    skills_dir = Path(dest).expanduser() if dest else _default_codex_skills_dir()
    skills_dir.mkdir(parents=True, exist_ok=True)
    target = skills_dir / SKILL_NAME

    if target.exists() or target.is_symlink():
        if not force:
            raise FileExistsError(
                f'{target} already exists. Use --force to overwrite.'
            )
        _remove_existing(target)

    if symlink:
        target.symlink_to(source, target_is_directory=True)
    else:
        shutil.copytree(source, target)

    return target


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Install the vizdantic-runner skill into your Codex skills directory.'
    )
    parser.add_argument(
        '--dest',
        help='Override skills directory (defaults to $CODEX_HOME/skills or ~/.codex/skills).',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing install if present.',
    )
    parser.add_argument(
        '--symlink',
        action='store_true',
        help='Symlink the skill instead of copying (handy for local dev).',
    )
    return parser


def cli_main(argv: list[str] | None = None, *, repo_root: Path | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    try:
        target = install_codex_skill(
            dest=Path(args.dest) if args.dest else None,
            force=args.force,
            symlink=args.symlink,
            repo_root=repo_root,
        )
    except FileExistsError as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1

    action = 'Symlinked' if args.symlink else 'Copied'
    print(f'{action} {SKILL_NAME} -> {target}')
    print('Restart Codex to pick up the new skill.')
    return 0


if __name__ == '__main__':
    raise SystemExit(cli_main())
