from glob import glob
from pathlib import Path
from PIL import Image, ImageDraw

files = sorted(glob('qa_final13_page-*.png'))
for start in range(0, len(files), 5):
    group = files[start:start + 5]
    pages = [Image.open(name).convert('RGB') for name in group]
    width = max(page.width for page in pages)
    height = max(page.height for page in pages)
    canvas = Image.new('RGB', (width * len(pages), height + 28), 'white')
    draw = ImageDraw.Draw(canvas)
    for index, page in enumerate(pages):
        canvas.paste(page, (index * width, 28))
        draw.text((index * width + 8, 6), f'Trang {start + index + 1}', fill='black')
    canvas.save(f'qa_final13_sheet_{start // 5 + 1}.png')
