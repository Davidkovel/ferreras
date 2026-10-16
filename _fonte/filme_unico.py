"""Hero de um só filme 16:9, nítido, a partir dos reels verticais 1080x1920.

    python -I _fonte/filme_unico.py folha hero     # folha de contacto com a faixa 16:9 escolhida em cada plano
    python -I _fonte/filme_unico.py faz hero       # super-resolução (Real-ESRGAN compacto, CPU) + codificação

Uma faixa 16:9 de um vertical tem 1080x608; ampliada 1,78x para 1920x1080 fica mole. Cada fotograma passa pelo
realesr-general-x4v3 (x4, ~5,5 s por fotograma neste PC) e desce para 1920x1080 com Lanczos: arestas limpas, sem os
blocos da compressão do Instagram. Saídas: video/<nome>-1080.mp4 e -720.mp4 (+ cartazes). O telemóvel usa os
verticais nativos (<nome>-v1080/-v720), que não precisam de nada.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, r"C:\Users\David\ferreras-extra\sr")
FF = r"C:\Users\David\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
IG = Path(r"C:\Users\David\ferreras-extra\ig")
OUT = Path(__file__).resolve().parents[1] / "video"
TMP = Path(r"C:\Users\David\ferreras-extra\sr\tmp")
L, G = "DWJdRoJiDJI.mp4", "DSDaaJDDa5a.mp4"
# (fonte, início, fim, topo da faixa 16:9 em px do vertical 1080x1920)
FILMES = {
    "hero": [(L, 0.0, 2.6, 560), (G, 0.3, 2.5, 640), (L, 2.4, 4.2, 760), (G, 29.4, 31.4, 360),
             (L, 12.0, 13.8, 660), (G, 34.0, 36.0, 700), (L, 22.4, 24.6, 560), (L, 15.6, 17.6, 560)],
    "mkt": [(G, 4.0, 6.2, 640), (L, 8.0, 10.0, 700), (G, 8.0, 9.8, 640), (L, 18.0, 19.8, 660),
            (G, 14.0, 15.8, 560), (L, 24.6, 26.4, 520), (G, 24.0, 26.0, 700), (L, 27.6, 29.4, 660)],
}


def corre(args, **kw):
    return subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y"] + args, check=True, **kw)


def folha(nome):
    ims = []
    for f, a, b, y in FILMES[nome]:
        p = TMP / "f.png"
        corre(["-ss", str(a + (b - a) / 2), "-i", str(IG / f), "-frames:v", "1", str(p)])
        im = Image.open(p).convert("RGB")
        d = ImageDraw.Draw(im)
        d.rectangle((2, y, 1077, y + 608), outline=(255, 210, 0), width=8)
        im.thumbnail((270, 480))
        ims.append(im)
    c = Image.new("RGB", (270 * len(ims), 480))
    for i, im in enumerate(ims):
        c.paste(im, (i * 270, 0))
    c.save(TMP / f"folha-{nome}.jpg", quality=85)
    print(TMP / f"folha-{nome}.jpg")


def faz(nome):
    import sr
    m = sr.carrega()
    W, H = 1920, 1080
    enc = subprocess.Popen([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30",
                            "-i", "-", "-an", "-vf", "eq=contrast=1.03:saturation=0.95,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                            "-profile:v", "high", "-movflags", "+faststart", str(OUT / f"{nome}-1080.mp4")], stdin=subprocess.PIPE)
    total = 0
    for k, (f, a, b, y) in enumerate(FILMES[nome]):
        dec = subprocess.Popen([FF, "-hide_banner", "-loglevel", "error", "-ss", str(a), "-t", str(b - a), "-i", str(IG / f),
                                "-vf", f"fps=30,crop=1080:608:0:{y}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        n = 0
        while True:
            buf = dec.stdout.read(1080 * 608 * 3)
            if len(buf) < 1080 * 608 * 3:
                break
            fr = np.frombuffer(buf, np.uint8).reshape(608, 1080, 3)
            big = Image.fromarray(sr.sobe(m, fr)).resize((W, H), Image.LANCZOS)
            enc.stdin.write(big.tobytes())
            n += 1
        dec.wait()
        total += n
        print(f"{nome} plano {k + 1}/{len(FILMES[nome])}: {n} fotogramas", flush=True)
    enc.stdin.close()
    enc.wait()
    corre(["-i", str(OUT / f"{nome}-1080.mp4"), "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "22",
           "-movflags", "+faststart", "-an", str(OUT / f"{nome}-720.mp4")])
    for k in ("1080", "720"):
        j = TMP / "c.jpg"
        corre(["-ss", "0.4", "-i", str(OUT / f"{nome}-{k}.mp4"), "-frames:v", "1", "-q:v", "2", str(j)])
        Image.open(j).save(OUT / f"{nome}-{k}-poster.webp", "WEBP", quality=86, method=6)
    print(nome, total, "fotogramas;", round((OUT / f"{nome}-1080.mp4").stat().st_size / 1e6, 1), "MB")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    TMP.mkdir(exist_ok=True)
    {"folha": folha, "faz": faz}[sys.argv[1]](sys.argv[2])
