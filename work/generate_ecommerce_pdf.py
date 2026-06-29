from pathlib import Path
from urllib.parse import quote

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "pdfs_individuais" / "JLS_00_Ecommerce.pdf"
HERO_SRC = ROOT / "outputs" / "assets" / "conexao-mt.png"
LOGO_SRC = ROOT / "outputs" / "assets" / "logo" / "jls-logo-negative-transparent.png"
MARK_SRC = ROOT / "outputs" / "assets" / "logo" / "jls-logo-symbol-transparent.png"
WORK = ROOT / "work"
HERO_CROP = WORK / "ecommerce_hero_crop.jpg"

NAVY = colors.HexColor("#0F2238")
NAVY_2 = colors.HexColor("#183048")
ORANGE = colors.HexColor("#F07008")
MIST = colors.HexColor("#C9CFD6")
GRAPHITE = colors.HexColor("#3A4654")
FOG = colors.HexColor("#E8EBEE")
PAPER = colors.white


def crop_cover(src: Path, dest: Path, aspect: float) -> None:
    img = Image.open(src).convert("RGB")
    w, h = img.size
    current = w / h
    if current > aspect:
      new_w = int(h * aspect)
      left = (w - new_w) // 2
      img = img.crop((left, 0, left + new_w, h))
    else:
      new_h = int(w / aspect)
      top = (h - new_h) // 2
      img = img.crop((0, top, w, top + new_h))
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, quality=92)


def wrap_text(text: str, font: str, size: float, max_width: float):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        trial = word if not line else f"{line} {word}"
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(c, text, x, y, width, font, size, leading, color, max_lines=None):
    c.setFillColor(color)
    c.setFont(font, size)
    lines = wrap_text(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_heading(c, text_parts, x, y, width, size=48, leading=49):
    c.setFont("Helvetica-Bold", size)
    line = []
    cursor_y = y
    current = ""

    flat_words = []
    for text, color in text_parts:
        for word in text.split():
            flat_words.append((word, color))

    for word, color in flat_words:
        trial = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(trial, "Helvetica-Bold", size) <= width:
            line.append((word, color))
            current = trial
        else:
            draw_colored_line(c, line, x, cursor_y, size)
            cursor_y -= leading
            line = [(word, color)]
            current = word
    if line:
        draw_colored_line(c, line, x, cursor_y, size)
        cursor_y -= leading
    return cursor_y


def draw_colored_line(c, line, x, y, size):
    cursor = x
    for word, color in line:
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", size)
        c.drawString(cursor, y, word)
        cursor += pdfmetrics.stringWidth(word + " ", "Helvetica-Bold", size)


def draw_bullet(c, text, x, y, width):
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, ">")
    return draw_wrapped(c, text, x + 14, y, width - 14, "Helvetica", 10.5, 15, GRAPHITE)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    w, h = A4
    hero_h = 348
    crop_cover(HERO_SRC, HERO_CROP, w / hero_h)

    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("JLS Log - E-commerce no Mato Grosso")
    c.setAuthor("JLS Log Soluções Logísticas")

    c.drawImage(ImageReader(str(HERO_CROP)), 0, h - hero_h, width=w, height=hero_h)
    c.saveState()
    c.setFillColor(NAVY)
    c.setFillAlpha(0.91)
    c.rect(0, h - hero_h, w * 0.73, hero_h, fill=1, stroke=0)
    c.setFillAlpha(0.55)
    c.rect(w * 0.56, h - hero_h, w * 0.44, hero_h, fill=1, stroke=0)
    c.restoreState()

    c.setStrokeColor(ORANGE)
    c.setLineWidth(2)
    c.line(28, h - 28, 54, h - 28)
    c.line(28, h - 28, 28, h - 54)
    c.line(w - 28, h - 28, w - 54, h - 28)
    c.line(w - 28, h - 28, w - 28, h - 54)

    logo = Image.open(LOGO_SRC)
    logo_w = 158
    logo_h = logo_w * logo.size[1] / logo.size[0]
    c.drawImage(ImageReader(str(LOGO_SRC)), 40, h - 92, width=logo_w, height=logo_h, mask="auto")

    c.setFillColor(colors.Color(1, 1, 1, alpha=0.12))
    c.rect(w - 190, h - 86, 150, 31, fill=1, stroke=0)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2)
    c.line(w - 190, h - 86, w - 190, h - 55)
    c.setFillColor(PAPER)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawRightString(w - 48, h - 74, "JLS E-COMMERCE")

    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(40, h - 146, "ESCALA REGIONAL PARA VENDAS ONLINE")
    c.setFillColor(ORANGE)
    c.rect(40, h - 166, 44, 3, fill=1, stroke=0)

    draw_heading(
        c,
        [
            ("Transferência, last mile e reversa sob", PAPER),
            ("controle.", ORANGE),
        ],
        40,
        h - 215,
        500,
        size=37,
        leading=39,
    )
    draw_wrapped(
        c,
        "Para marketplaces, lojas virtuais, operadores, transportadoras e distribuidores, a JLS apoia a entrada de carga no Mato Grosso, a distribuição regional, as entregas finais e o retorno de informação.",
        40,
        h - 306,
        505,
        "Helvetica",
        11.5,
        16,
        MIST,
    )

    body_top = h - hero_h
    c.setFillColor(PAPER)
    c.rect(0, 90, w, body_top - 90, fill=1, stroke=0)

    c.saveState()
    c.setFillAlpha(0.045)
    c.drawImage(ImageReader(str(MARK_SRC)), w - 138, body_top - 122, width=96, height=96, mask="auto")
    c.restoreState()

    left_x = 40
    right_x = 410
    y = body_top - 42
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(left_x, y, "A SOLUÇÃO JLS")
    y -= 24
    bullets = [
        "Recebimento ou transferência de volumes para a base local em Cuiabá.",
        "Triagem por cidade, prioridade, janela de entrega e criticidade da operação.",
        "Distribuição no Mato Grosso com last mile, comprovante e retorno operacional.",
        "Apoio em logística reversa para trocas, devoluções, coletas e reentregas.",
    ]
    for item in bullets:
        y = draw_bullet(c, item, left_x, y, 326) - 6

    c.setFillColor(FOG)
    c.roundRect(right_x, body_top - 213, 146, 170, 7, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(right_x + 17, body_top - 72, "Por que conecta")
    draw_wrapped(
        c,
        "No e-commerce, o cliente não enxerga a rota; ele sente prazo, informação e reversa. A JLS entra como apoio local para transformar volume em entrega acompanhada dentro do MT.",
        right_x + 17,
        body_top - 94,
        112,
        "Helvetica",
        9.8,
        13.2,
        GRAPHITE,
    )

    steps_y = 190
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(40, steps_y + 93, "COMO FUNCIONA")
    c.setFillColor(FOG)
    c.roundRect(40, steps_y, w - 80, 72, 7, fill=1, stroke=0)
    steps = [
        ("1", "Entrada", "A carga chega em Cuiabá ou é coletada conforme o fluxo combinado."),
        ("2", "Distribuição", "Separação por destino, rota, prioridade e janela de entrega."),
        ("3", "Reversa", "Comprovante, retorno de informação e tratamento de devoluções."),
    ]
    x = 62
    for num, title, text in steps:
        c.setFillColor(NAVY)
        c.circle(x + 10, steps_y + 48, 10, fill=1, stroke=0)
        c.setFillColor(PAPER)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(x + 10, steps_y + 45, num)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10.2)
        c.drawString(x + 31, steps_y + 52, title)
        draw_wrapped(c, text, x + 31, steps_y + 36, 126, "Helvetica", 8.7, 11.2, GRAPHITE)
        x += 174

    c.setFillColor(NAVY)
    c.rect(0, 0, w, 90, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(40, 59, "CONVERSAR SOBRE E-COMMERCE NO MT")
    c.setFillColor(PAPER)
    c.setFont("Helvetica", 21)
    c.drawString(40, 34, "(65) 98142-8733")
    c.setFillColor(MIST)
    c.setFont("Helvetica", 8)
    c.drawString(40, 18, "jlslog.com.br - Cuiabá/MT - CNPJ 20.162.078/0001-10")

    msg = "Olá, vim pelo material de E-commerce da JLS e quero entender apoio para transferência, last mile ou logística reversa no Mato Grosso."
    url = f"https://wa.me/5565981428733?text={quote(msg)}"
    btn_x, btn_y, btn_w, btn_h = 390, 31, 165, 34
    c.setFillColor(ORANGE)
    c.roundRect(btn_x, btn_y, btn_w, btn_h, 5, fill=1, stroke=0)
    c.setFillColor(PAPER)
    c.setFont("Helvetica-Bold", 9.2)
    c.drawCentredString(btn_x + btn_w / 2, btn_y + 13, "FALAR COM A OPERAÇÃO")
    c.linkURL(url, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), relative=0)

    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
