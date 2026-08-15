"""Testovi cjelovitosti kataloga.

Katalog bez provjere je popis linkova. Ovo su uvjeti pod kojima se na njega
smije osloniti stroj: jedinstven kljuc, zatvoreni skupovi vrijednosti,
obavezna polja i podudarnost izmedju punog i provjerenog skupa.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pytest

KORIJEN = Path(__file__).resolve().parents[1]
SHEMA = json.loads((KORIJEN / "katalog" / "schema.json").read_text(encoding="utf-8"))
PUNI = KORIJEN / "katalog" / "frontend_literature.jsonl"
ZLATNI = KORIJEN / "katalog" / "frontend_literature_gold.jsonl"


def ucitaj(p: Path) -> list[dict]:
    return [json.loads(r) for r in p.read_text(encoding="utf-8").splitlines() if r.strip()]


@pytest.fixture(scope="module")
def puni() -> list[dict]:
    return ucitaj(PUNI)


@pytest.fixture(scope="module")
def zlatni() -> list[dict]:
    return ucitaj(ZLATNI)


# --- kljuc ------------------------------------------------------------------


def test_identifikator_je_jedinstven(puni):
    """Identifikator je jedini stabilan kljuc zapisa. Dva zapisa s istim
    kljucem znace da dohvat po kljucu ovisi o redoslijedu citanja."""
    ponovljeni = [k for k, v in Counter(r["id"] for r in puni).items() if v > 1]
    assert ponovljeni == []


def test_identifikator_je_kebab_case(puni):
    uzorak = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
    lose = [r["id"] for r in puni if not uzorak.match(r["id"])]
    assert lose == []


def test_url_je_jedinstven(puni):
    """Dva zapisa s istim URL-om su isti izvor pod dva imena."""
    ponovljeni = [k for k, v in Counter(r["url"] for r in puni).items() if v > 1]
    assert ponovljeni == []


# --- shema ------------------------------------------------------------------


def test_obavezna_polja_postoje(puni):
    trazeno = set(SHEMA["required"])
    for r in puni:
        assert trazeno <= set(r), f"{r.get('id')} nema {trazeno - set(r)}"


@pytest.mark.parametrize("polje", ["type", "level", "access"])
def test_zatvoreni_skupovi(puni, polje):
    """Ova tri polja sluze za filtriranje. Vrijednost izvan skupa znaci da
    filtar tiho ne vraca zapis, umjesto da javi gresku."""
    dopusteno = set(SHEMA["properties"][polje]["enum"])
    stvarno = {r[polje] for r in puni}
    assert stvarno <= dopusteno, f"{polje}: {stvarno - dopusteno}"


def test_url_je_http(puni):
    lose = [r["id"] for r in puni if not r["url"].startswith(("http://", "https://"))]
    assert lose == []


def test_godina_je_smislena(puni):
    """Donja granica je 1950, ne 1990: katalog namjerno drzi temeljne radove
    iz psihologije percepcije i odlucivanja (Hick 1952, Fitts 1954, Miller
    1956, Stevens 1957) jer se na njih oslanja moderno oblikovanje sucelja.
    Prva postavljena granica od 1960 ih je odbacila, i granica je bila kriva,
    ne podaci."""
    lose = [r["id"] for r in puni if r.get("year") is not None and not (1950 <= r["year"] <= 2030)]
    assert lose == []


def test_opis_nije_prazan(puni):
    """Zapis bez opisa je link, a katalog postoji zato da se ne mora otvoriti
    svaki link da bi se znalo je li relevantan."""
    lose = [r["id"] for r in puni if not (r.get("description") or "").strip()]
    assert lose == []


# --- odnos punog i provjerenog skupa ----------------------------------------


def test_zlatni_je_podskup_punog(puni, zlatni):
    puni_ids = {r["id"] for r in puni}
    visak = [r["id"] for r in zlatni if r["id"] not in puni_ids]
    assert visak == []


def test_zlatni_su_tocno_provjereni(puni, zlatni):
    """Provjereni skup mora biti tocno oni zapisi koji nose zastavicu.
    Ako se to razidje, jedna od dvije tvrdnje o katalogu je neistinita."""
    oznaceni = {r["id"] for r in puni if r.get("verified")}
    assert {r["id"] for r in zlatni} == oznaceni


def test_svaki_zapis_ima_izvor_pronalaska(puni):
    dopusteno = set(SHEMA["properties"]["source"]["enum"])
    for r in puni:
        assert r.get("source") in dopusteno, r["id"]


# --- sadrzajna ravnoteza ----------------------------------------------------


def test_katalog_nije_jednolican(puni):
    """Katalog u kojem jedna kategorija nosi vecinu nije katalog nego popis
    jedne teme. Prag je grub namjerno; sluzi da se pomak primijeti."""
    najveca = Counter(r["category"] for r in puni).most_common(1)[0][1]
    assert najveca / len(puni) < 0.10


def test_ima_i_besplatnog_i_placenog(puni):
    pristup = Counter(r["access"] for r in puni)
    assert pristup["free"] > 0 and pristup["paid"] > 0


def test_akademski_zapisi_nose_doi_ili_mjesto(puni):
    """Rad bez oznake ili mjesta objave ne da se provjeriti."""
    bez = [r["id"] for r in puni if r["type"] == "paper" and not (r.get("doi") or r.get("venue"))]
    assert len(bez) / max(1, sum(1 for r in puni if r["type"] == "paper")) < 0.35
