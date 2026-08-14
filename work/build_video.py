#!/usr/bin/env python3
import json, os, subprocess, itertools
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 25
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES = os.path.join(ROOT, 'work', 'frames')
CLIPS = os.path.join(ROOT, 'work', 'clips')
os.makedirs(FRAMES, exist_ok=True)
os.makedirs(CLIPS, exist_ok=True)

FONT_PATH = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'

with open(os.path.join(ROOT, 'work', 'photo_index.json')) as f:
    PHOTOS = {int(k): v for k, v in json.load(f).items()}

def photo_path(n):
    p = PHOTOS[n]
    return os.path.join(ROOT, p) if not os.path.isabs(p) else p

# ---------- frame composition ----------

def compose_photo_frame(n, out_png):
    src = photo_path(n)
    im = Image.open(src).convert('RGB')
    # background: cover-crop + blur
    bg = im.copy()
    bw, bh = bg.size
    scale = max(W / bw, H / bh)
    bg = bg.resize((int(bw * scale) + 2, int(bh * scale) + 2))
    bx = (bg.width - W) // 2
    by = (bg.height - H) // 2
    bg = bg.crop((bx, by, bx + W, by + H))
    bg = bg.filter(ImageFilter.GaussianBlur(30))
    bg = Image.eval(bg, lambda p: int(p * 0.55))  # darken

    # foreground: contain
    fw, fh = im.size
    fscale = min((W * 0.92) / fw, (H * 0.92) / fh)
    fg = im.resize((int(fw * fscale), int(fh * fscale)), Image.LANCZOS)
    fx = (W - fg.width) // 2
    fy = (H - fg.height) // 2

    canvas = bg.copy()
    # soft shadow
    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([fx - 6, fy - 6, fx + fg.width + 6, fy + fg.height + 6], fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas.convert('RGBA'), shadow).convert('RGB')
    canvas.paste(fg, (fx, fy))
    canvas.save(out_png, quality=95)

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if draw.textlength(test, font=font) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def compose_text_frame(out_png, lines, size=90, color=(255, 255, 255), bg=(12, 12, 12), align='center', y_center=None, accent=None):
    canvas = Image.new('RGB', (W, H), bg)
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT_PATH, size)
    all_lines = []
    for text in lines:
        all_lines.extend(wrap_text(draw, text, font, W * 0.82))
    line_h = int(size * 1.25)
    total_h = line_h * len(all_lines)
    y0 = y_center - total_h // 2 if y_center else (H - total_h) // 2
    for i, l in enumerate(all_lines):
        tw = draw.textlength(l, font=font)
        x = (W - tw) // 2
        y = y0 + i * line_h
        draw.text((x, y), l, font=font, fill=color)
    canvas.save(out_png, quality=95)

def compose_twocol_frame(out_png):
    canvas = Image.new('RGB', (W, H), (12, 12, 12))
    draw = ImageDraw.Draw(canvas)
    font_h = ImageFont.truetype(FONT_PATH, 64)
    font_b = ImageFont.truetype(FONT_PATH, 46)
    cols = [
        (W * 0.27, 'NOUS :', 'on avait des idées', (255, 255, 255)),
        (W * 0.73, 'LE MAÇON :', 'il les réalisait', (255, 210, 60)),
    ]
    for cx, head, body, col in cols:
        hw = draw.textlength(head, font=font_h)
        draw.text((cx - hw / 2, H * 0.42), head, font=font_h, fill=col)
        bw = draw.textlength(body, font=font_b)
        draw.text((cx - bw / 2, H * 0.42 + 90), body, font=font_b, fill=(230, 230, 230))
    canvas.save(out_png, quality=95)

def compose_number_frame(out_png, number):
    canvas = Image.new('RGB', (W, H), (12, 12, 12))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT_PATH, 340)
    tw = draw.textlength(number, font=font)
    draw.text(((W - tw) / 2, (H - 340) / 2 - 20), number, font=font, fill=(255, 255, 255))
    canvas.save(out_png, quality=95)

# ---------- clip rendering ----------

def render_clip(png_path, duration, out_mp4, zoom=True, fade=0.12):
    d = max(duration, 0.12)
    vf = []
    if zoom:
        frames = max(int(d * FPS), 1)
        vf.append(f"scale=2200:1238,zoompan=z='min(zoom+0.0009,1.08)':d={frames}:s={W}x{H}:fps={FPS}")
    else:
        vf.append(f"scale={W}:{H},fps={FPS}")
    if fade > 0 and d > 2 * fade:
        vf.append(f"fade=t=in:st=0:d={fade}:alpha=0")
        vf.append(f"fade=t=out:st={d - fade}:d={fade}:alpha=0")
    filt = ','.join(vf)
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', png_path, '-t', f'{d:.3f}',
        '-vf', filt, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    compose_photo_frame(60, '/tmp/test_photo.jpg')
    compose_text_frame('/tmp/test_text.jpg', ['SANS FENÊTRE.'])
    compose_twocol_frame('/tmp/test_twocol.jpg')
    compose_number_frame('/tmp/test_number.jpg', '40')
    print('ok')
