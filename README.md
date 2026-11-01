# kanji-networks-etymology-yomitan

Kanji etymologies from Lawrence J. Howell's Kanji Networks for Yomitan and DaKanji.

The dictionary contains one `kanji_bank` entry per kanji with its etymology as meaning, tagged `etymology`.
It is meant to be installed alongside a kanji dictionary like KANJIDIC.

| Asset | Contents |
|---|---|
| `kanji-networks-etymology-yomitan.zip` | Yomitan dictionary |
| `kanji-networks-etymology-yomitan-dadb.zip` | the same dictionary plus the PDF's introduction (first 7 pages) as DaKanji manual |

## Sources

[Kanji Networks](http://www.kanjinetworks.com) was a website offering etymologies of kanji by Lawrence J. Howell and Hikaru Morimoto.
It closed in August 2016 and its database was released as the PDF *Etymological Dictionary of Han/Chinese Characters*.

The PDF and Arnaud Coomans' parser [kanjinetworks](https://github.com/acoomans/kanjinetworks) (ported to Python 3)
are vendored in `vendored_sources/kanjinetworks/`. The build extracts the PDF's text, parses the etymology of every
kanji (6,631 entries) and strips the whitespace the PDF leaves around them.

## Installation

Make sure [uv](https://github.com/astral-sh/uv) is installed on your system and run

``` bash
uv sync
```

## Usage

``` bash
uv run build.py
```

This creates both dictionaries in `out/` (each as `.zip`, `.index.json` and `.manifest.json`).
The uncompressed dictionaries are kept in `tmp/` for inspection, together with the text extracted from the PDF
(`tmp/kanjinetworks.txt`) and the manual (`tmp/manual.pdf`).

## Development

``` bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pyright               # type check
uv run pytest                # tests
```

The repo follows the [DaLang dictionary repo standard](https://github.com/dariyooo/dalang-dict-utils/blob/main/docs/repo-standard.md),
update the shared setup with `uvx copier update --trust`.

## Release

Push a tag with today's date:

``` bash
git tag 2026-11-01 && git push origin 2026-11-01
```

The *Release* workflow runs the checks, builds the dictionaries with the tag as revision and publishes them as the GitHub release of the tag.
To redo a release, push the tag again with `git tag -f 2026-11-01 && git push -f origin 2026-11-01`.
Installed dictionaries pick up new releases through "Check for updates".

## License

Etymologies by Lawrence J. Howell and Hikaru Morimoto (Kanji Networks), parser by Arnaud Coomans (MIT).
