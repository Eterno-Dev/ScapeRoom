import os
from PIL import Image, ImageDraw
import numpy as np

TARGET_W = 340
TARGET_H = 480
BORDER_W = 5
RADIUS = 16

def process_card(img):
    img = img.convert('RGBA')
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    resized = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    
    # 1. Inset mask for content so content never bleeds outside the black border
    inner_mask = Image.new('L', (TARGET_W, TARGET_H), 0)
    draw_in = ImageDraw.Draw(inner_mask)
    draw_in.rounded_rectangle([2, 2, TARGET_W - 3, TARGET_H - 3], radius=RADIUS, fill=255)
    
    # 2. Outer mask for total erasure outside card
    outer_mask = Image.new('L', (TARGET_W, TARGET_H), 0)
    draw_out = ImageDraw.Draw(outer_mask)
    draw_out.rounded_rectangle([0, 0, TARGET_W - 1, TARGET_H - 1], radius=RADIUS, fill=255)
    
    # 3. Canvas and paste
    out = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    out.paste(resized, (0, 0), inner_mask)
    
    # 4. Draw pure black (#000000) border with width=BORDER_W
    draw = ImageDraw.Draw(out)
    draw.rounded_rectangle(
        [2, 2, TARGET_W - 3, TARGET_H - 3],
        radius=RADIUS,
        outline=(0, 0, 0, 255),
        width=BORDER_W
    )
    
    # 5. Invert selection of border and erase EVERYTHING outside
    arr = np.array(out)
    m_arr = np.array(outer_mask)
    arr[m_arr == 0] = [0, 0, 0, 0]
    
    return Image.fromarray(arr)

def get_intervals(sheet_path):
    im = Image.open(sheet_path)
    arr = np.array(im)
    alpha = arr[:, :, 3] > 30
    x_proj = alpha.sum(axis=0)
    y_proj = alpha.sum(axis=1)

    def extract_intervals(proj, min_val=20):
        intervals = []
        in_int = False
        start = 0
        for idx, v in enumerate(proj):
            if v > min_val and not in_int:
                in_int = True
                start = idx
            elif v <= min_val and in_int:
                in_int = False
                intervals.append((start, idx))
        if in_int:
            intervals.append((start, len(proj)))
        return intervals

    x_ints = extract_intervals(x_proj)
    y_ints = extract_intervals(y_proj)
    return im, x_ints, y_ints

def save_card(img, category, base_name, base_dirs):
    processed = process_card(img)
    for b in base_dirs:
        dest_dir = os.path.join(b, 'src', 'assets', 'images', category)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, base_name)
        processed.save(dest)
    print(f'Saved [{category}]: {base_name}')

def main():
    base_dirs = [
        'c:/Users/paucr/Documents/ScapeRoom',
        'c:/Users/paucr/Documents/CluedoWeb'
    ]

    # 1. CARTAS HOMBRE
    sheet_m = 'C:/Users/paucr/Downloads/cartas_hombre.png'
    im_m, x_m, y_m = get_intervals(sheet_m)
    m_names = [
        ['card-m-cazador.png', 'card-m-leonardo.png', 'card-m-alfonso.png'],
        ['card-m-santamaria.png', 'card-m-elias.png', 'card-m-raul.png'],
        ['card-m-hugo.png', 'card-m-victor.png', 'card-m-javier.png']
    ]
    for r in range(3):
        for c in range(3):
            crop = im_m.crop((x_m[c][0], y_m[r][0], x_m[c][1], y_m[r][1]))
            save_card(crop, 'personajes_masculinos', m_names[r][c], base_dirs)

    # 2. CARTAS MUJER
    sheet_f = 'C:/Users/paucr/Downloads/cartas_mujer.png'
    im_f, x_f, y_f = get_intervals(sheet_f)
    f_names = [
        ['card-f-cazadora.png', 'card-f-carmen.png', 'card-f-araujo.png'],
        ['card-f-isadora.png', 'card-f-isabel.png', 'card-f-lucia.png'],
        ['card-f-valentina.png', 'card-f-elena.png', 'card-f-sofia.png']
    ]
    for r in range(3):
        for c in range(3):
            crop = im_f.crop((x_f[c][0], y_f[r][0], x_f[c][1], y_f[r][1]))
            save_card(crop, 'personajes_femeninos', f_names[r][c], base_dirs)

    # 3. CARTAS ESPECIALES
    sheet_esp = 'C:/Users/paucr/Downloads/cartas_especiales.png'
    im_esp, x_esp, y_esp = get_intervals(sheet_esp)
    esp_names = [
        ['card-esp-title-1.png', 'card-esp-title-2.png', 'card-esp-title-3.png'],
        ['card-esp-frame-1.png', 'card-esp-frame-2.png', 'card-esp-frame-3.png'],
        ['card-back-base-1.png', 'card-back-base-2.png', 'card-back-base-3.png']
    ]
    for r in range(3):
        for c in range(3):
            crop = im_esp.crop((x_esp[c][0], y_esp[r][0], x_esp[c][1], y_esp[r][1]))
            save_card(crop, 'tarjetas', esp_names[r][c], base_dirs)

    # 4. CARTAS OBJETOS 1 (Camera + objects 2-9)
    sheet_obj1 = 'C:/Users/paucr/Downloads/cartas_objetos_1.png'
    im_obj1, x_o1, y_o1 = get_intervals(sheet_obj1)
    obj1_names = [
        ['card-scanner-camera.png', 'card-obj-2.png', 'card-obj-3.png'],
        ['card-obj-4.png', 'card-obj-5.png', 'card-obj-6.png'],
        ['card-obj-7.png', 'card-obj-8.png', 'card-obj-9.png']
    ]
    for r in range(3):
        for c in range(3):
            crop = im_obj1.crop((x_o1[c][0], y_o1[r][0], x_o1[c][1], y_o1[r][1]))
            save_card(crop, 'objetos', obj1_names[r][c], base_dirs)

    # 5. CARTAS OBJETOS 2 (Male/Female gender selection + objects 10-16)
    sheet_obj2 = 'C:/Users/paucr/Downloads/cartas_objetos_2.png'
    im_obj2, x_o2, y_o2 = get_intervals(sheet_obj2)
    obj2_configs = [
        [('tarjetas', 'card-gender-male.png'), ('tarjetas', 'card-gender-female.png'), ('objetos', 'card-obj-10.png')],
        [('objetos', 'card-obj-11.png'), ('objetos', 'card-obj-12.png'), ('objetos', 'card-obj-13.png')],
        [('objetos', 'card-obj-14.png'), ('objetos', 'card-obj-15.png'), ('objetos', 'card-obj-16.png')]
    ]
    for r in range(3):
        for c in range(3):
            crop = im_obj2.crop((x_o2[c][0], y_o2[r][0], x_o2[c][1], y_o2[r][1]))
            cat, name = obj2_configs[r][c]
            save_card(crop, cat, name, base_dirs)

    print('All cards rebuilt successfully in organized folders!')

if __name__ == '__main__':
    main()
