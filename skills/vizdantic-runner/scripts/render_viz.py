#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable


def _add_repo_root_to_path() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    if (repo_root / 'vizdantic').is_dir():
        sys.path.insert(0, str(repo_root))

DEFAULT_THEME_PATH = Path('artifacts/vizdantic/theme.json')


def _parse_usecols(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    cols = [col.strip() for col in raw.split(',') if col.strip()]
    return cols or None


def _select_columns(df: 'object', usecols: list[str] | None) -> 'object':
    if not usecols:
        return df
    return df[usecols]


def _read_json(path: Path, nrows: int | None, usecols: list[str] | None) -> 'object':
    import pandas as pd

    try:
        df = pd.read_json(path)
        df = _select_columns(df, usecols)
        return df.head(nrows) if nrows else df
    except ValueError:
        if nrows:
            reader: Iterable['object'] = pd.read_json(path, lines=True, chunksize=nrows)
            df = next(reader)
        else:
            df = pd.read_json(path, lines=True)
        df = _select_columns(df, usecols)
        return df.head(nrows) if nrows else df


def _load_data(
    path: Path,
    sheet: str | None,
    usecols: list[str] | None,
    nrows: int | None,
) -> 'object':
    import pandas as pd

    suffix = path.suffix.lower()
    if suffix == '.csv':
        return pd.read_csv(path, usecols=usecols, nrows=nrows)
    if suffix == '.parquet':
        df = pd.read_parquet(path, columns=usecols)
        return df.head(nrows) if nrows else df
    if suffix == '.json':
        return _read_json(path, nrows, usecols)
    if suffix in {'.xlsx', '.xls'}:
        return pd.read_excel(path, sheet_name=sheet, usecols=usecols, nrows=nrows)

    raise ValueError(f'Unsupported data extension: {suffix}')


def _load_spec(spec_arg: str | None, spec_file: Path | None) -> dict:
    if spec_file is not None:
        with spec_file.open('r', encoding='utf-8') as handle:
            return json.load(handle)
    if spec_arg is not None:
        return json.loads(spec_arg)

    raise ValueError('Provide --spec or --spec-file')


def _load_theme(
    theme_arg: str | None,
    theme_file: Path | None,
    theme_template: str | None,
    theme_path: Path,
) -> tuple[dict | None, bool]:
    theme = None
    from_source = False

    if theme_arg:
        theme = json.loads(theme_arg)
        from_source = True
    elif theme_file is not None:
        with theme_file.open('r', encoding='utf-8') as handle:
            theme = json.load(handle)
        from_source = True
    elif theme_path.is_file():
        with theme_path.open('r', encoding='utf-8') as handle:
            theme = json.load(handle)

    if theme_template:
        parsed_template = theme_template
        if theme_template.strip().startswith('{'):
            parsed_template = json.loads(theme_template)
        theme = dict(theme or {})
        theme['template'] = parsed_template
        from_source = True

    return theme, from_source


def _apply_theme(fig: 'object', theme: dict | None) -> None:
    if not theme:
        return
    if isinstance(theme, dict) and 'data' in theme:
        fig.update_layout(template=theme)
        return
    if isinstance(theme, dict) and 'layout' in theme:
        theme = theme['layout']
    fig.update_layout(**theme)


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Validate a Vizdantic spec and render a Plotly figure.'
    )
    parser.add_argument('--data', required=True, help='Path to CSV, Parquet, JSON, or Excel file.')
    parser.add_argument('--sheet', help='Excel sheet name (only for .xlsx/.xls).')
    parser.add_argument('--usecols', help='Comma-separated list of columns to load.')
    parser.add_argument('--nrows', type=int, help='Limit rows when supported or after load.')
    parser.add_argument('--sample', type=int, help='Sample N rows after load.')
    parser.add_argument('--inspect', action='store_true', help='Print columns/dtypes/head and exit.')
    parser.add_argument(
        '--theme',
        help='Plotly layout JSON (string) applied via fig.update_layout.',
    )
    parser.add_argument('--theme-file', help='Path to a JSON file containing layout updates.')
    parser.add_argument(
        '--theme-template',
        help='Plotly template name or dict applied as layout.template.',
    )
    parser.add_argument(
        '--theme-path',
        help='Theme cache path (default: artifacts/vizdantic/theme.json).',
    )
    parser.add_argument(
        '--remember-theme',
        action='store_true',
        help='Persist the provided theme to --theme-path for future runs.',
    )

    spec_group = parser.add_mutually_exclusive_group()
    spec_group.add_argument('--spec', help='Vizdantic spec as a JSON string.')
    spec_group.add_argument('--spec-file', help='Path to a JSON file containing the spec.')

    parser.add_argument('--output-dir', default='artifacts/vizdantic', help='Output directory.')
    parser.add_argument('--name', help='Base filename for outputs (no extension).')
    parser.add_argument('--html', action='store_true', help='Write an HTML file (default).')
    parser.add_argument('--png', action='store_true', help='Write a PNG (requires kaleido).')
    parser.add_argument('--show', action='store_true', help='Display figure in a viewer.')

    args = parser.parse_args()

    _add_repo_root_to_path()

    try:
        data_path = Path(args.data).expanduser().resolve()
        spec_path = Path(args.spec_file).expanduser().resolve() if args.spec_file else None
        theme_path = (
            Path(args.theme_path).expanduser().resolve()
            if args.theme_path
            else DEFAULT_THEME_PATH
        )
        usecols = _parse_usecols(args.usecols)
        nrows = args.nrows
        sample = args.sample

        if not args.inspect and not (args.spec or args.spec_file):
            parser.error('Provide --spec or --spec-file (or use --inspect).')

        if args.inspect and nrows is None:
            nrows = 200

        df = _load_data(data_path, args.sheet, usecols, nrows)
        if sample and len(df) > sample:
            df = df.sample(n=sample, random_state=0)

        if args.inspect:
            print(f'Loaded rows: {len(df)}')
            print('Columns:')
            print(list(df.columns))
            print('Dtypes:')
            print(df.dtypes)
            print('Head:')
            print(df.head(5))
            return 0

        spec_dict = _load_spec(args.spec, spec_path)
        theme_file = Path(args.theme_file).expanduser().resolve() if args.theme_file else None
        theme, from_source = _load_theme(
            args.theme, theme_file, args.theme_template, theme_path
        )

        from vizdantic import validate
        from vizdantic.plugins.plotly import render

        spec = validate(spec_dict)
        fig = render(spec, df)
        _apply_theme(fig, theme)

        output_dir = Path(args.output_dir).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        base_name = args.name or f'{data_path.stem}-viz'
        wrote_any = False

        write_html = args.html or (not args.html and not args.png)
        if write_html:
            html_path = output_dir / f'{base_name}.html'
            fig.write_html(str(html_path))
            print(f'Wrote HTML: {html_path}')
            wrote_any = True

        if args.png:
            png_path = output_dir / f'{base_name}.png'
            fig.write_image(str(png_path))
            print(f'Wrote PNG: {png_path}')
            wrote_any = True

        if args.show:
            fig.show()

        if args.remember_theme:
            if not from_source:
                raise ValueError('Provide --theme, --theme-file, or --theme-template to remember.')
            theme_path.parent.mkdir(parents=True, exist_ok=True)
            with theme_path.open('w', encoding='utf-8') as handle:
                json.dump(theme or {}, handle, indent=2)
            print(f'Saved theme: {theme_path}')

        if not wrote_any:
            print('No outputs written. Use --html and/or --png.')

        return 0
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
