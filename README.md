# kcc-oasis

`kcc-oasis` is a small standalone command-line wrapper around the official
Kindle Comic Converter source tree. It does not use the macOS
`Kindle Comic Converter.app` bundle or download a KCC installer package.

The default target is the KCC README profile `KO`, listed there as
`Kindle Oasis 2/3`.

## Quick Start

```sh
scripts/bootstrap.sh
bin/kcc-oasis "/path/to/comic.cbz"
```

By default this runs KCC with:

```sh
-p KO -m -f EPUB --nokepub
```

That means Kindle Oasis 2/3 sizing, manga right-to-left mode, and plain EPUB
output.

## Output Format

EPUB is the default:

```sh
bin/kcc-oasis "/path/to/comic.cbz"
```

MOBI can be requested explicitly:

```sh
bin/kcc-oasis --format MOBI "/path/to/comic.cbz"
```

## Profiles

Friendly names are mapped to KCC README profile codes:

```text
oasis        -> KO
paperwhite   -> KPW
paperwhite34 -> KPW34
paperwhite5  -> KPW5
paperwhite6  -> KPW6
```

KCC profile codes are also accepted directly:

```sh
bin/kcc-oasis --profile KPW5 "/path/to/comic.cbz"
```

List supported wrapper profiles:

```sh
bin/kcc-oasis --list-profiles
```

## Common Options

```sh
bin/kcc-oasis --output "/path/to/out" "/path/to/comic.cbz"
bin/kcc-oasis --no-manga "/path/to/comic.cbz"
bin/kcc-oasis --hq "/path/to/comic.cbz"
bin/kcc-oasis --dry-run "/path/to/comic.cbz"
```

KCC-native options can be placed after `--`:

```sh
bin/kcc-oasis "/path/to/comic.cbz" -- --cropping 2
```

## Requirements

This project vendors KCC source code under `vendor/kcc` and creates its own
Python virtual environment under `.venv`.

KCC still expects system extraction tools for archives. On macOS, install them
with Homebrew:

```sh
brew install p7zip unar sevenzip
```
