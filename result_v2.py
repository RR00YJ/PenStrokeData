import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter.filedialog
from PIL import Image, ImageDraw

filetypes = [("CSV (コンマ区切り)", "*.csv")]
data_path = tkinter.filedialog.askopenfilename(filetypes=filetypes, title="ファイルをひらく")

# CSVファイルを読み込む
data = pd.read_csv(data_path)

def process_actions_v3(data):
    # 画像の初期化（白背景）
    img = Image.new('RGB', (800, 1000), 'white')
    draw = ImageDraw.Draw(img)

    # 画像を保存するためのリスト
    images = []
    erasing = False  # 現在消去中かどうかを追跡
    
    # 消しゴムの太さを設定（15ピクセル）
    eraser_size = 15

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
            last_x, last_y = x, y

        # 描画中
        elif action == 'move-drawing':
            draw.line([last_x, last_y, x, y], fill='black', width=2)
            last_x, last_y = x, y

        # 消去開始
        elif action == 'start-erasing':
            # 記述中に消去が始まった場合、画像を保存
            if not erasing:
                images.append(img.copy())
            erasing = True

        # 消去中
        elif action == 'move-erasing':
            # 消しゴムの範囲を設定
            draw.ellipse([x - eraser_size / 2, y - eraser_size / 2, x + eraser_size / 2, y + eraser_size / 2], fill='white')

        # 全消去
        elif action == 'allclear':
            # 記述中に全消去が始まった場合、画像を保存し、新しい画像でリセット
            if not erasing:
                images.append(img.copy())
            img = Image.new('RGB', (800, 1000), 'white')
            draw = ImageDraw.Draw(img)
            erasing = True

        # 保存アクションがあれば終了
        elif action == 'savenote':
            break

    # 最後の画像を保存
    images.append(img)

    return images

# 改訂版のアクション処理を実行（allclearを含む）
images_v3 = process_actions_v3(data)

# 生成された画像をファイルとして保存し、リンクを生成する
image_paths_v3 = []
for i, img in enumerate(images_v3):
    # 画像ファイルのパス
    # PATHの部分を変更し、適切なパスを指定
    image_path_v3 = rf"C:PATH\drawing_image_v3_{i+1}.png"
    # 画像を保存
    img.save(image_path_v3)
    image_paths_v3.append(image_path_v3)
