import sys

try:
    import pillow
except:
    import os
    os.system('pip install pillow  -i https://pypi.mirrors.ustc.edu.cn/simple/')
    from PIL import Image, ImageDraw, ImageFont

CHILD_W = CHILD_H = 16
txt = '我的心是宝宝的'
font = ImageFont.truetype('AliPuHui-Bold.ttf', CHILD_W)

# 程序入口
if __name__ == '__main__':
    imgSrc = Image.open(sys.argv[1])
    w, h = imgSrc.size

    imgChild = Image.new("RGB", (CHILD_W, CHILD_H))
    imgDst = Image.new("RGB", (CHILD_W*w, CHILD_H*h))

    textW, textH = font.getsize("迷")
    offsetX = (CHILD_W - textW) >> 1
    offsetY = (CHILD_H - textH) >> 1

    charIndex = 0
    draw = ImageDraw.Draw(imgChild)
    print("开始处理图片...")
    for y in range(h):
        for x in range(w):
            draw.rectangle((0, 0, CHILD_W, CHILD_H), fill='lightgray')
            draw.text((offsetX, offsetY), txt[charIndex], font=font, fill=imgSrc.getpixel((x, y)))
            imgDst.paste(imgChild, (x*CHILD_W, y*CHILD_H))
            charIndex += 1

            if charIndex == len(txt):
                charIndex = 0

    imgDst.save(sys.argv[2])
