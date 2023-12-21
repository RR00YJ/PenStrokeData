import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import tkinter.filedialog
from PIL import Image, ImageDraw

filetypes = [("CSV (コンマ区切り)", "*.csv")]
data_path = tkinter.filedialog.askopenfilename(filetypes=filetypes, title="ファイルをひらく")

# CSVファイルを読み込む
data = pd.read_csv(data_path)

def process_actions_v4(data, seed=0):
    random.seed(seed)

    used_colors = [('#000000', 0)]  # 初期セッションは黒色 (#000000)

    def generate_new_color():
        """明るい色を含むが淡い色を避ける色を生成する関数"""
        while True:
            color_parts = [random.choice('0123456789ABCDEF') for _ in range(6)]
            # 少なくとも一つの部分を '5' 以下にする
            color_parts[random.randint(0, 5)] = random.choice('012345')
            color = "#" + ''.join(color_parts)
            if color not in [col for col, _ in used_colors]:
                return color

    img = Image.new('RGB', (800, 1000), 'white')
    draw = ImageDraw.Draw(img)

    images = []
    erasing = False
    current_color = '#000000'
    session_number = 0

    # 各アクションを順に処理
    for index, row in data.iterrows():
        action = row['Action']
        x = row['X']
        y = row['Y']

        # 描画開始
        if action == 'start-drawing':
            # 消去中であれば、その時点の画像を保存
            if erasing:
                images.append(img.copy())
                erasing = False
                current_color = generate_new_color()
                session_number += 1
                used_colors.append((current_color, session_number))
            last_x, last_y = x, y

        # 描画中
        elif action == 'move-drawing':
            draw.line([last_x, last_y, x, y], fill=current_color, width=2)
            last_x, last_y = x, y

        # 消去開始
        elif action == 'start-erasing':
            if not erasing:
                images.append(img.copy())
            erasing = True

        # 消去中
        elif action == 'move-erasing':
            # 消しゴムの範囲を設定
            eraser_size = 15
            draw.ellipse([x - eraser_size / 2, y - eraser_size / 2, x + eraser_size / 2, y + eraser_size / 2], fill='white')

        # 全消去
        elif action == 'allclear':
            if not erasing:
                images.append(img.copy())
            img = Image.new('RGB', (800, 1000), 'white')
            draw = ImageDraw.Draw(img)
            erasing = True
            current_color = generate_new_color()
            session_number += 1
            used_colors.append((current_color, session_number))

        # 保存アクションがあれば終了
        elif action == 'savenote':
            break

    # 凡例を追加
    for i, (color, num) in enumerate(sorted(used_colors, key=lambda x: x[1])):
        draw.text((10, 800 + 20 * i), f"Color {num + 1}: {color}", fill=color)

    images.append(img)

    return images

images_v4 = process_actions_v4(data)

image_paths_v4 = []
for i, img in enumerate(images_v4):
    image_path_v4 = rf"C:PATH\drawing_image_v4_{i+1}.png"
    img.save(image_path_v4)
    image_paths_v4.append(image_path_v4)
