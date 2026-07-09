"""
Henter navn, fødselsdato og kursdato fra fallsikringssertifikater (Vinde-mal).

Mønster i PDF-en (bekreftet mot eksempeldokument):
    Simen Fallang              <- navnet står RETT FØR "Født:"-linjen
    Født: 31.10.1993
    Har gjennomført og bestått:
    Bane NOR - Grunnkurs
    ...
    Dato: 17.09.2025           <- kursdato, egen linje

Bruker pdfplumber (ikke pypdf) fordi pdfplumber bevarer visuell
leserekkefølge. pypdf blander om på linjene i dette dokumentet, og
gjør det umulig å bruke posisjon som anker.
"""

import csv
import re
from pathlib import Path

import pdfplumber

FODT_MØNSTER = re.compile(r"Født:\s*(\d{2}\.\d{2}\.\d{4})")
DATO_MØNSTER = re.compile(r"^Dato:\s*(\d{2}\.\d{2}\.\d{4})")


def hent_metadata(pdf_path: Path) -> dict:
    """Henter navn, fødselsdato og kursdato fra én PDF-fil."""
    with pdfplumber.open(pdf_path) as pdf:
        text = pdf.pages[0].extract_text() or ""

    linjer = [linje.strip() for linje in text.split("\n") if linje.strip()]

    navn = None
    fodselsdato = None
    kursdato = None

    for i, linje in enumerate(linjer):
        fodt_treff = FODT_MØNSTER.match(linje)
        if fodt_treff:
            fodselsdato = fodt_treff.group(1)
            if i > 0:
                navn = linjer[i - 1]
            continue

        dato_treff = DATO_MØNSTER.match(linje)
        if dato_treff:
            kursdato = dato_treff.group(1)

    return {"navn": navn, "fodselsdato": fodselsdato, "kursdato": kursdato}


def prosesser_mappe(mappe: str, output_csv: str) -> None:
    """Kjører hent_metadata() på alle PDF-er i mappa og lagrer resultatet til CSV."""
    mappe_path = Path(mappe)
    resultater = []
    advarsler = []

    pdf_filer = sorted(mappe_path.glob("*.pdf"))
    if not pdf_filer:
        print(f"Fant ingen PDF-filer i {mappe}")
        return

    for pdf_fil in pdf_filer:
        data = hent_metadata(pdf_fil)
        data["filnavn"] = pdf_fil.name
        resultater.append(data)

        manglende = [felt for felt in ("navn", "fodselsdato", "kursdato") if not data[felt]]
        if manglende:
            advarsler.append(f"{pdf_fil.name}: mangler {', '.join(manglende)}")

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filnavn", "navn", "fodselsdato", "kursdato"])
        writer.writeheader()
        writer.writerows(resultater)

    print(f"Ferdig! {len(resultater)} filer prosessert -> {output_csv}")

    if advarsler:
        print(f"\n{len(advarsler)} fil(er) med manglende data:")
        for a in advarsler:
            print(f"  - {a}")


if __name__ == "__main__":
    prosesser_mappe("sertifikater/", "resultat.csv")