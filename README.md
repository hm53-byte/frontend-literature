# frontend-literature

Strojno citljiv katalog frontend literature: **1659 zapisa**, od toga **1541
provjeren**, sa shemom, zatvorenim skupovima vrijednosti i testovima koji
katalog drze upotrebljivim.

Nije popis linkova. Svaki zapis nosi vrstu, kategoriju, razinu, nacin
pristupa, oznake i recenicu o tome zasto vrijedi, pa se moze filtrirati
strojno umjesto citati redom.

```
$ python alat/query.py --category webgl-threejs-shaders --level expert --access free
$ python alat/query.py --search "view transitions" --gold
$ python alat/query.py --list-categories
```

---

## Sto je unutra

| | |
|---|---|
| Zapisa | 1659 |
| Provjerenih (`gold`) | 1541 |
| Jedinstvenih URL-ova | 1659, bez ponavljanja |
| S oznakom DOI | 161 |
| Kategorija | 55 |

**Po vrsti:** dokumentacija 418, clanak 311, znanstveni rad 195, knjiga 179,
repozitorij 140, vodic 114, tecaj 93, specifikacija 87, interaktivno 57, video
44, bilten 21.

**Po razini:** napredno 577, srednje 576, ekspertno 294, pocetno 212.

**Po pristupu:** besplatno 1318, placeno 283, mjesovito 58.

Najveca kategorija nosi 2,7 posto zapisa, dakle katalog nije popis jedne teme
pod sirokim imenom. To drzi test.

Raspon ide od zivih specifikacija do temeljnih radova iz psihologije
percepcije: Hick 1952, Fitts 1954, Miller 1956, Stevens 1957 stoje uz WHATWG i
suvremene alate, jer se moderno oblikovanje sucelja na njih izravno oslanja.

## Shema

[`katalog/schema.json`](katalog/schema.json). Obavezno je `id`, `title`,
`type`, `category`, `level`, `access`, `url`. Tri polja imaju zatvoren skup
vrijednosti, jer sluze za filtriranje:

```json
"type":   ["book","docs","paper","course","tutorial","article",
           "video","spec","repo","newsletter","interactive"],
"level":  ["beginner","intermediate","advanced","expert"],
"access": ["free","paid","freemium"]
```

Vrijednost izvan skupa nije samo neuredna: filtar bi tiho prestao vracati taj
zapis umjesto da javi gresku. Zato to drzi test, a ne dogovor.

Polje `source` biljezi **kako je zapis pronadjen** (`scholar`, `web`,
`known`), a `verified` je li postojanje provjereno. Ta dva polja postoje da se
ne mijesa "znam za ovo" s "provjerio sam ovo".

## Provjereni skup

`frontend_literature_gold.jsonl` je podskup s provjerenim zapisima. Odnos
izmedju dvije datoteke nije stvar povjerenja nego testa: provjereni skup mora
biti **tocno** oni zapisi koji nose zastavicu `verified`. Ako se to razidje,
jedna od dvije tvrdnje o katalogu je neistinita, a ne zna se koja.

## Sto testovi cuvaju

16 testova, i nisu ukras. Katalog bez njih trune tiho:

- **jedinstven identifikator** i **jedinstven URL**, jer je isti zapis pod dva
  imena gori od zapisa koji nedostaje,
- **zatvoreni skupovi** za tri polja po kojima se filtrira,
- **opis nije prazan**, jer katalog postoji zato da se ne mora otvoriti svaki
  link da bi se znalo je li relevantan,
- **znanstveni radovi nose DOI ili mjesto objave**, inace se ne mogu
  provjeriti,
- **nijedna kategorija ne prelazi desetinu** zapisa.

Dva nalaza iz pisanja tih testova, oba zadrzana:

**Dvanaest ponovljenih identifikatora.** URL-ovi su bili jedinstveni, ali
dvanaest parova dijelilo je isti kljuc, pa je dohvat po kljucu ovisio o
redoslijedu citanja. Razrijeseno sufiksom, ne brisanjem: oba zapisa su stvarni
i razliciti izvori.

**Prva granica godine bila je kriva, ne podaci.** Postavio sam donju granicu
na 1960 i test je odbacio cetiri zapisa. Sva cetiri su temeljni radovi na koje
se struka i danas poziva. Granica je spustena na 1950, uz zapisan razlog.

## Jezik

Opisi su na hrvatskom, ostala polja i oznake na engleskom. To je posljedica
nastanka, ne odluke; za medjunarodnu upotrebu opisi bi trebali prijevod.
Filtriranje i strojna upotreba time nisu pogodjeni jer su sva polja s
zatvorenim skupom na engleskom.

## Pokretanje

```
python -m pytest testovi -q
python alat/query.py --help
```

Trazi Python 3.11 ili noviji i nista izvan standardne biblioteke.

## Licenca

Apache-2.0 za shemu, alat i testove, vidi [LICENSE](LICENSE).

Katalog sadrzi **metapodatke o tudjim radovima**: naslov, autora, godinu,
poveznicu i vlastiti opis. Ne sadrzi ni jedan redak tudjeg sadrzaja. Prava na
same radove pripadaju njihovim nositeljima i poveznica na rad nije dozvola za
njegovu upotrebu.
