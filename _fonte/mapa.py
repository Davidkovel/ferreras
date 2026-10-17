# O mapa dos sectores: o nordeste peninsular desenhado a partir das províncias (geo/spain.geojson, click_that_hood,
# domínio público), com a casa em Barcelona e as rotas até onde já trabalhámos. Só lugares que constam no site antigo:
# Barcelona (a morada), a Costa Brava (náutica: regatas e alquiler de yates) e o Hotel Boltaña Ordesa (Pirineo de Huesca).
# A animação (rotas que se desenham, pontos que acendem) vive em js/99-mapa.js.
import json
import math
from pathlib import Path

_GEO = Path(__file__).parent / "geo" / "spain.geojson"
LON0, LON1, LAT0, LAT1 = -1.3, 3.5, 40.45, 43.0
K = math.cos(math.radians(41.7))
MP_W = 1000
MP_H = round(MP_W * (LAT1 - LAT0) / ((LON1 - LON0) * K))
DESTACA = {"Barcelona", "Girona", "Tarragona", "Lleida", "Lérida", "Gerona", "Huesca"}


def xy(lon, lat):
    return ((lon - LON0) * K / ((LON1 - LON0) * K) * MP_W, (LAT1 - lat) / (LAT1 - LAT0) * MP_H)


def _anel(coords):
    pts, ult = [], None
    for lon, lat in coords:
        x, y = xy(lon, lat)
        p = (round(x, 1), round(y, 1))
        if p != ult:
            pts.append(p); ult = p
    return "M" + "L".join(f"{x},{y}" for x, y in pts) + "Z"


def provincias():
    d = json.loads(_GEO.read_text(encoding="utf-8"))
    out = []
    for f in d["features"]:
        g, nome = f["geometry"], f["properties"].get("name", "")
        polis = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        dentro = any(LON0 - 1 < lon < LON1 + 1 and LAT0 - 1 < lat < LAT1 + 1 for p in polis for anel in p for lon, lat in anel[::20])
        if not dentro:
            continue
        caminho = "".join(_anel(anel) for p in polis for anel in p)
        cls = "mp-p mp-d" if any(n in nome for n in DESTACA) else "mp-p"
        out.append(f'<path class="{cls}" d="{caminho}"/>')
    return "".join(out)


LUGARES = [  # (id, lon, lat, rótulo, sub, lado do rótulo)
    ("bcn", 2.1686, 41.3874, "Barcelona", "La casa · Passeig de Gràcia 95", "dir"),
    ("cbrava", 3.05, 41.82, "Costa Brava", "Náutica: regatas y alquiler de yates", "esq"),
    ("boltana", 0.0689, 42.4456, "Hotel Boltaña Ordesa", "Hotelería · Pirineo de Huesca", "dir"),
]


def mapa_svg():
    bx, by = xy(2.1686, 41.3874)
    rotas, pontos = [], []
    for i, (k, lon, lat, rot, sub, lado) in enumerate(LUGARES):
        x, y = xy(lon, lat)
        if k != "bcn":
            mx, my = (bx + x) / 2, (by + y) / 2 - abs(x - bx) * 0.28 - 30
            rotas.append(f'<path class="mp-rota" pathLength="1" d="M{bx:.1f},{by:.1f} Q{mx:.1f},{my:.1f} {x:.1f},{y:.1f}" style="--i:{i}"/>')
        tx = x + 18 if lado == "dir" else x - 18
        ta = "" if lado == "dir" else ' text-anchor="end"'
        pontos.append(f'<g class="mp-ponto{" mp-casa" if k == "bcn" else ""}" style="--i:{i}"><circle class="mp-onda" cx="{x:.1f}" cy="{y:.1f}" r="10"/><circle class="mp-c" cx="{x:.1f}" cy="{y:.1f}" r="{7 if k == "bcn" else 5}"/>'
                      f'<text x="{tx:.1f}" y="{y - 4:.1f}" class="mp-t"{ta}>{rot}</text><text x="{tx:.1f}" y="{y + 16:.1f}" class="mp-s"{ta}>{sub}</text></g>')
    mar = xy(1.7, 40.75)
    fr = xy(1.0, 42.85)
    return (f'<svg class="mapa-svg" viewBox="0 0 {MP_W} {MP_H}" role="img" aria-label="Mapa: Barcelona, la Costa Brava y el Pirineo de Huesca">'
            f'<g class="mp-terra">{provincias()}</g>'
            f'<text class="mp-mar" x="{mar[0]:.0f}" y="{mar[1]:.0f}">Mar Mediterráneo</text><text class="mp-mar" x="{fr[0]:.0f}" y="{fr[1]:.0f}">Francia</text>'
            f'{"".join(rotas)}{"".join(pontos)}</svg>')
