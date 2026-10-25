# -*- coding: utf-8 -*-
"""bestOS 字标素材生成器
与 build_bootanimation.py 第二屏同一套参数：SF Pro Rounded Heavy / 竖直灰渐变 /
Google 四色细条 / 落款。画布宽度可选，字标始终占画布 70%（与原动画一致）。
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
SYS_ROUNDED = "/System/Library/Fonts/SFNSRounded.ttf"
CJK = "/Users/fansullqingkongle/Desktop/deepseek 项目/bestOS项目/assets/fonts/ZCOOLKuaiLe-subset.ttf"

MARK_TOP, MARK_BOT = (146, 151, 156), (108, 113, 118)
G_BLUE, G_RED, G_YELLOW, G_GREEN = (66,133,244), (234,67,53), (251,188,5), (52,168,83)
CREDIT = (140, 146, 152)
BAR_W_R, BAR_H_R, GAP_R = 0.26/0.70, 7/756, 34/756     # 相对字标宽度的比例

def mark_font(width_target):
    size = max(8, int(width_target * 0.42))
    while size > 8:
        f = ImageFont.truetype(SYS_ROUNDED, size)
        f.set_variation_by_name("Heavy")
        if f.getlength("bestOS") <= width_target:
            return f
        size -= 2
    return ImageFont.truetype(SYS_ROUNDED, 8)

def vgrad(w, h, top, bottom):
    g = Image.new("RGB", (1, h)); px = g.load()
    for y in range(h):
        t = y / max(1, h-1)
        px[0, y] = tuple(round(top[k] + (bottom[k]-top[k])*t) for k in range(3))
    return g.resize((w, h), Image.BILINEAR)

def color_rule(w, h):
    im = Image.new("RGBA", (w, h), (0,0,0,0)); d = ImageDraw.Draw(im)
    seg = w // 4; gap = max(1, round(w * 3/280.8))
    for i, c in enumerate((G_BLUE, G_RED, G_YELLOW, G_GREEN)):
        x0 = i*seg; x1 = w if i == 3 else x0 + seg - gap
        d.rectangle([x0, 0, x1, h], fill=c+(255,))
    return im

def mark_asset(canvas_w, rule=True, mono=None):
    mw = canvas_w * 0.70
    f = mark_font(round(mw))
    bb = f.getbbox("bestOS"); gw, gh = bb[2]-bb[0], bb[3]-bb[1]
    bar_w, bar_h, gap = round(mw*BAR_W_R), max(2, round(mw*BAR_H_R)), round(mw*GAP_R)
    pad = round(mw * 0.06)
    ch = gh + (gap + bar_h if rule else 0) + pad*2
    cw = round(canvas_w)

    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).text(((cw-gw)//2-bb[0], pad-bb[1]), "bestOS", font=f, fill=255)

    out = Image.new("RGBA", (cw, ch), (0,0,0,0))
    if mono is None:
        lay = Image.new("RGBA", (cw, ch), (0,0,0,0))
        lay.paste(vgrad(gw, gh, MARK_TOP, MARK_BOT), ((cw-gw)//2, pad))
        out.paste(lay, (0,0), mask)
    else:
        out.paste(Image.new("RGBA", (cw, ch), tuple(mono)+(255,)), (0,0), mask)

    if rule:
        out.alpha_composite(color_rule(bar_w, bar_h).convert("RGBA"),
                            ((cw-bar_w)//2, ch-pad-bar_h))
    return out

def fullscreen(w=1080, h=1920):
    s = w / 1080.0
    img = Image.new("RGBA", (w, h), (0,0,0,255))
    f = mark_font(round(w*0.70))
    bb = f.getbbox("bestOS"); gw, gh = bb[2]-bb[0], bb[3]-bb[1]
    cy = int(h*0.455)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text(((w-gw)//2-bb[0], cy-gh//2-bb[1]), "bestOS", font=f, fill=255)
    lay = Image.new("RGBA", (w, h), (0,0,0,0)); lay.paste(vgrad(w, h, MARK_TOP, MARK_BOT), (0,0))
    img.paste(lay, (0,0), mask)
    bw, bh = round(w*0.26), max(4, round(7*s))
    img.alpha_composite(color_rule(bw, bh), ((w-bw)//2, cy-gh//2+bb[3]+round(34*s)))
    csize = round(56*s)
    cf = ImageFont.truetype(CJK, csize) if os.path.exists(CJK) else ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", csize, index=5)
    d = ImageDraw.Draw(img); tw = d.textlength("马特提供系统", font=cf)
    d.text(((w-tw)//2, int(h*0.918)-csize), "马特提供系统", font=cf, fill=CREDIT+(255,))
    return img

def save(im, name):
    p = os.path.join(OUT, name); im.save(p)
    print('  %-44s %6.0f KB  %s' % (name, os.path.getsize(p)/1024, im.size))

def scaled(im, target_w):
    k = target_w / im.width
    return im.resize((target_w, round(im.height*k)), Image.LANCZOS)

if __name__ == '__main__':
    print('== bestOS 字标 ==')
    base = mark_asset(3840)
    for w in (3840, 2560, 1920, 1080):
        save(base if w == 3840 else scaled(base, w), 'bestOS字标_透明底_%d.png' % w)
    plain = mark_asset(3840, rule=False)
    save(plain, 'bestOS字标_无四色条_透明底_3840.png')
    save(scaled(plain, 1920), 'bestOS字标_无四色条_透明底_1920.png')
    save(scaled(mark_asset(1920, rule=False, mono=(255,255,255)), 1920), 'bestOS字标_纯白_透明底_1920.png')
    save(scaled(mark_asset(1920, rule=False, mono=(0,0,0)), 1920), 'bestOS字标_纯黑_透明底_1920.png')
    save(fullscreen(1080, 1920), 'bestOS字标_整屏_1080x1920_黑底.png')
    save(fullscreen(2160, 3840), 'bestOS字标_整屏_2160x3840_黑底.png')
    print('完成')
