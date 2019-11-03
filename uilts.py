#  coding = utf-8
import face_recognition
import dlib
import faiss
import cv2
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_128d_encodings(img_url):
    all_face_list = []
    image = face_recognition.load_image_file(img_url)
    encoding = face_recognition.face_encodings(image)
    if len(encoding) == 0:
        return 30002
    image_face_encoding = face_recognition.face_encodings(image)[0]
    # 将numpy array类型转化为列表
    encoding_array_list = image_face_encoding.tolist()
    # 把所有的特殊都放在一个列表里面
    all_face_list.append(encoding_array_list)
    # 转化成数据array类型
    all_face_list = np.array(all_face_list)
    # # 一个人的多张图片
    # all_face_list = all_face_list.T
    # save_image_data = np.mean(all_face_list, axis=1)

    # 将列表里的元素转化为字符串
    encoding_str_list = [str(i) for i in all_face_list[0]]
    # 拼接列表里的字符串
    encoding_str = ','.join(encoding_str_list)
    return encoding_str


def get_similarity(a1, a2):
    score = "{:.4f}".format(cosine_similarity([a1, a2])[0][1])
    return score


def array_to_image(filename):
    '''
    从二进制文件中读取数据并重新恢复为图片
    '''
    with open(data_base_path + filename, mode='rb') as f:
        arr = pickle.load(f)  # 加载并反序列化数据
    rows = arr.shape[0]  # rows=5
    # pdb.set_trace()
    # print("rows:",rows)
    arr = arr.reshape(rows, 3, 32, 32)
    print(arr)  # 打印数组
    for index in range(rows):
        a = arr[index]
        # 得到RGB通道
        r = PIL.Image.fromarray(a[0]).convert('L')
        g = PIL.Image.fromarray(a[1]).convert('L')
        b = PIL.Image.fromarray(a[2]).convert('L')
        image = PIL.Image.merge("RGB", (r, g, b))
        # 显示图片
        matplotlib.pyplot.imshow(image)
        matplotlib.pyplot.show()
        # image.save(self.image_base_path + "result" + str(index) + ".png",'png')
