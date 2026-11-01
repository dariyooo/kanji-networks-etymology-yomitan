"""Builds the Kanji Networks etymology dictionary from the Kanji Networks PDF.

The Yomitan dictionary contains the etymologies, its DaDb variant also the PDF's introduction as manual.
"""

from pathlib import Path

from dalang_dict import Vendored, build_index, fetch, package_dictionary
from kanjinetworks import KanjiNetworksParser, get_text
from pypdf import PdfReader, PdfWriter

GITHUB_REPO = "dariyooo/kanji-networks-etymology-yomitan"
ASSET = "kanji-networks-etymology-yomitan"
TITLE = "Kanji Networks Etymology"

# `used_for` and the version are listed in the release notes
KANJI_NETWORKS = Vendored(
    "kanjinetworks",
    path="vendored_sources/kanjinetworks/kanjinetworks/data/etymologicaldictionaryofhanchinesecharacters-160816005400.pdf",
    version="0.1.8",
    used_for="etymologies parsed from the Kanji Networks PDF, its first 7 pages as manual",
)
MANUAL_ICON = Path(__file__).parent / "manual_icon.svg"
MANUAL_PAGES = 7

TMP_DIR = Path("tmp")

INDEX_FIELDS = {
    "sourceLanguage": "ja",
    "targetLanguage": "en",
    "author": "Lawrence J. Howell",
    "url": "http://www.kanjinetworks.com",
    "description": "Etymological Dictionary of Han/Chinese Characters.",
    "attribution": "Lawrence J. Howell / Hikaru Morimoto",
}


def build_kanji_bank(kanjis) -> list[list]:
    """Formats parsed Kanji objects (or dicts) as entries: [kanji, onyomi, kunyomi, tags, meanings, stats]."""
    kanji_bank = []
    for obj in kanjis:
        if isinstance(obj, dict):
            char = obj.get("kanji") or obj.get("character", "")
            definition = obj.get("definition") or obj.get("etymology") or obj.get("meaning", str(obj))
        else:
            char = getattr(obj, "kanji", getattr(obj, "character", ""))
            definition = getattr(obj, "definition", None) or getattr(obj, "etymology", None) or str(obj)
        if not char:
            continue
        kanji_bank.append([char, "", "", "etymology", [definition.strip()], {}])
    return kanji_bank


def verify_kanji_bank(kanji_bank: list[list]) -> None:
    empty = sum(1 for entry in kanji_bank if not entry[4][0])
    print(f"Kanji bank: {len(kanji_bank)} entries, {empty} with an empty definition.")
    if not kanji_bank:
        raise ValueError("No kanji found in the parsed text")


def extract_manual(pdf_path: Path, manual_path: Path) -> Path:
    """Writes the introduction (first `MANUAL_PAGES` pages) of the PDF as the DaDb manual."""
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages[:MANUAL_PAGES]:
        writer.add_page(page)
    manual_path.parent.mkdir(parents=True, exist_ok=True)
    with manual_path.open("wb") as f:
        writer.write(f)
    return manual_path


def main() -> None:
    pdf_path = fetch(KANJI_NETWORKS)
    # The text extracted from the PDF is cached in tmp/, not in the vendored package
    text = get_text(text_cache_path=str(TMP_DIR / "kanjinetworks.txt"))
    kanji_bank = build_kanji_bank(KanjiNetworksParser().parse(text))
    verify_kanji_bank(kanji_bank)
    manual = extract_manual(pdf_path, TMP_DIR / "manual.pdf")

    for package_name, extra_files in (
        (ASSET, {}),
        (f"{ASSET}-dadb", {"manual.pdf": manual, "manual_icon.svg": MANUAL_ICON}),
    ):
        index = build_index(TITLE, GITHUB_REPO, package_name, **INDEX_FIELDS)
        package_dictionary(package_name, index, {"kanji_bank": kanji_bank}, extra_files=extra_files)
