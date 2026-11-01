from dalang_dict import Vendored, build_index, fetch, package_dictionary

GITHUB_REPO = "dariyooo/kanji-networks-etymology-yomitan"
ASSET = "kanji-networks-etymology-yomitan"
TITLE = "kanji-networks-etymology-yomitan"

# `used_for` and the version are listed in the release notes
SOURCE = Vendored("<name>", path="vendored_sources/<name>/<file>", version="<date retrieved>", used_for="")

INDEX_FIELDS = {
    "author": "",
    "url": f"https://github.com/{GITHUB_REPO}",
    "description": "Kanji etymologies from Lawrence J. Howell's Kanji Networks",
    "attribution": "",
}


def build_banks(source: object) -> dict[str, list]:
    """Converts the source data to bank entries, e.g. {"kanji_bank": [...]}."""
    raise NotImplementedError


def main() -> None:
    banks = build_banks(fetch(SOURCE))
    index = build_index(TITLE, GITHUB_REPO, ASSET, **INDEX_FIELDS)
    package_dictionary(ASSET, index, banks)
