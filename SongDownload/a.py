import matplotlib.pyplot as plt
import base64
import cv2


def ToBase64(file, txt):
    with open(file, 'rb') as fileObj:
        audio_data = fileObj.read()
        base64_data = base64.b64encode(audio_data)
        fout = open(txt, 'w')
        fout.write(base64_data.decode())
        fout.close()


def ToFile(txt, file):
    with open(txt, 'r') as fileObj:
        base64_data = fileObj.read()
        ori_image_data = base64.b64decode(base64_data)
        fout = open(file, 'wb')
        fout.write(ori_image_data)
        fout.close()


ToBase64("./songs/毛不易-消愁.mp3", 'desk_base64.txt')  # 文件转换为base64
ToFile("desk_base64.txt", 'desk_cp_by_base64.mp3')  # base64编码转换为二进制文件
# img = cv2.imread('desk_cp_by_base64.jpg')
# plt.imshow(img)
# plt.show
