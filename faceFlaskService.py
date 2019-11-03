# coding=utf-8
import face_recognition
from flask import Flask, g
from flask_restful import reqparse, Api, Resource
from flask_httpauth import HTTPTokenAuth
import base64
import json
import os
import numpy as np
import cv2

from do_database import save_device_mysql, save_encoding_mysql, save_task_mysql, select_device_msyql, \
    delete_face_mysql, get_info_mysql, init_databases, delete_device_mysql, select_task_mysql, \
    delete_task_mysql
from uilts import get_128d_encodings, get_similarity

# Flask相关变量声明
app = Flask(__name__)
api = Api(app)

# RESTfulAPI的参数解析 -- put / post参数解析
parser_put = reqparse.RequestParser()
parser_put.add_argument("device_name", type=str, required=False, help="person name")
parser_put.add_argument("sn", type=str, required=False, help="device sn number")

parser_put.add_argument("binary_img_list", type=str, required=False, help="need binary")
parser_put.add_argument("user_id", type=str, required=False, help="need user id")
parser_put.add_argument("user_name", type=str, required=False, help="need user name")

parser_put.add_argument("img_register", type=str, required=False, help="img register")
parser_put.add_argument("cam_url", type=str, required=False, help="cam url")


# 功能方法部分案例
def to_do(arg1, args2):
    return str(arg1) + str(args2)


# 功能方法部分案例
def add(arg3, args4):
    return str(arg3 + args4)


class DatabasesInit(Resource):
    def post(self):
        resout_info = init_databases()
        if resout_info == 0:
            # 资源添加成功，返回0
            return {"code": "0", "msg": "Databases init success"}, 200
        else:
            return {"code": "400", "msg": resout_info}, 200


# 设备注册
class DeviceRegist(Resource):
    def post(self):
        args = parser_put.parse_args()
        # 构建新参数
        device_name = args['device_name']
        sn = args['sn']
        if device_name == None or sn == None:
            return {"code": "500", "msg": "Parameter error"}, 200
        # 调用方法to_do
        all_sn, all_device_name = select_device_msyql()
        if sn in all_sn and device_name in all_device_name:
            return {"code": "600", "msg": "The device is already registered"}, 200
        resout_info = save_device_mysql(device_name, sn)
        if resout_info == 0:
            # 资源添加成功，返回0
            return {"code": "0", "msg": "Device registration is successful"}, 200
        else:
            return {"code": "400", "msg": resout_info}, 200


# 人脸录入
class FaceRegister(Resource):
    def post(self):
        args = parser_put.parse_args()
        # 构建新参数
        binary_img_list = args['binary_img_list']
        sn = args['sn']
        user_id = args['user_id']
        user_name = args['user_name']
        if user_id == None or sn == None or binary_img_list == None or user_name == None:
            return {"code": "500", "msg": "Parameter error"}, 200

        # 对传入进来的数据进行先校验
        all_sn, all_user_id = select_device_msyql()
        if sn not in all_sn:
            return {"code": "10001", "msg": "Device not registered"}, 200
        if len(binary_img_list) == 0:
            return {"code": 30001, "msg": "img is empty"}, 200
        a_user_name, a_encoding_str, a_user_id, a_sn, a_re_img_url = get_info_mysql()
        # print(a_user_id)
        # print(type(a_user_id))
        if user_id in a_user_id:
            return {"code": 30005, "msg": "user id is registered"}, 200

        # 保存图片数据
        save_path = os.path.join(os.getcwd(), 'saveimg')
        if not os.path.exists(save_path):  # 如果路径不存在
            os.makedirs(save_path)
        img_id = len(os.listdir(save_path))
        re_img_url = os.path.join(save_path, f"{user_name}_{img_id}.jpg")
        print(re_img_url)

        # with open(img_name, "wb") as f:
        # print(binary_img_list[20])
        # f.write(binary_img_list.encode(encoding = "utf-8"))
        # img_data = base64.b64decode(binary_img_list[0])
        # file1 = open(img_name,'wb')
        # file1.write(img_data)
        # file1.close()
        bs_js = json.loads(binary_img_list)
        img = base64.b64decode(bs_js)
        image_data = np.fromstring(img, np.uint8)
        image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        cv2.imwrite(re_img_url, image_data)
        # # print(img)
        # print(type(img))
        # # 调用方法register
        encoding_str = get_128d_encodings(re_img_url)
        # print(encoding_str)

        if encoding_str == 30002:
            return {"code": "30002", "msg": "No people in img"}, 200
        resout_info = save_encoding_mysql(user_name, encoding_str, user_id, sn, re_img_url)
        if resout_info == 0:
            # 人脸添加成功，返回0
            return {"code": "0", "msg": "register success"}, 200
        else:
            # 资源添加失败，返回400
            return {"code": "400", "msg": resout_info}, 200


# 删除设备
class DeviceDelete(Resource):
    def post(self):
        args = parser_put.parse_args()
        # 构建新参数
        device_name = args['device_name']
        sn = args['sn']
        if sn == None or device_name == None:
            return {"code": "500", "msg": "Parameter error"}, 200
        # 对传入进来的数据进行先校验
        all_sn, all_user_id = select_device_msyql()
        if sn not in all_sn:
            return {"code": "10001", "msg": "Device not registered"}, 200
        # if user_id not in all_user_id:
        #     return {"code": "20001", "msg": "User not registered"}, 200
        # 调用方法to_do
        resout_info = delete_device_mysql(sn)
        if resout_info == 0:
            # 资源添加成功，返回0
            return {"code": "0", "data": "delete device OK"}, 200
        else:
            # 资源添加失败，返回400
            return {"code": "400", "data": resout_info}, 200


# 删除人脸
class FaceDelete(Resource):
    def post(self):
        args = parser_put.parse_args()
        # 构建新参数
        user_id = args['user_id']
        sn = args['sn']
        if user_id == None or sn == None:
            return {"code": "500", "msg": "Parameter error"}, 200
        # 对传入进来的数据进行先校验
        a_user_name, a_encoding_str, a_user_id, a_sn, a_re_img_url = get_info_mysql()
        if sn not in a_sn:
            return {"code": "10001", "msg": "Device not registered"}, 200
        if user_id not in a_user_id:
            return {"code": "20001", "msg": "User not registered"}, 200
        # 调用方法to_do
        resout_info = delete_face_mysql(user_id)
        if resout_info == 0:
            # 资源添加成功，返回0
            return {"code": "0", "data": "delete user success"}, 200
        else:
            # 资源添加失败，返回400
            return {"code": "400", "data": resout_info}, 200


# 识别图片，返回图片是什么
class FaceDetection(Resource):
    def post(self):
        # 需要返回的结果
        result_sss = []
        result_user_id = []
        args = parser_put.parse_args()
        # 构建新参数
        binary_img_list = args['img_register']
        sn = args['sn']
        if binary_img_list == None or sn == None:
            return {"code": "500", "msg": "Parameter error"}, 200
        # 判断校验参数
        all_sn, all_device_name = select_device_msyql()
        if sn not in all_sn:
            return {"code": "10001", "msg": "Device not registered"}, 200
        # 调用获取数据库里面的信息
        a_user_name, a_encoding_str, a_user_id, a_sn, a_re_img_url = get_info_mysql()

        # 保存图片数据
        save_path = os.path.join(os.getcwd(), 'detection_img')
        if not os.path.exists(save_path):  # 如果路径不存在
            os.makedirs(save_path)
        img_id = len(os.listdir(save_path))
        de_img_url = os.path.join(save_path, f"detection_face_{img_id}.jpg")
        print(de_img_url)
        bs_js = json.loads(binary_img_list)
        img = base64.b64decode(bs_js)
        image_data = np.fromstring(img, np.uint8)
        image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        cv2.imwrite(de_img_url, image_data)
        # # print(img)
        # print(type(img))
        # 调用方法register
        encoding_str = get_128d_encodings(de_img_url)
        print(encoding_str)
        image = face_recognition.load_image_file(de_img_url)
        # 识别无人的时候
        if len(face_recognition.face_encodings(image)) == 0:
            return {"code": "30002", "msg": "No people in img"}, 200

        # 利用opencv的缩放函数改变摄像头图像的大小，图像越小，所做的计算就少， 如果需要增加速度，你们这里就可以减少fx和fy的数值
        small_frame = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
        rgb_small_frame = small_frame[:, :, ::-1]
        # 使用默认的HOG模型查找图像中的所有人脸
        face_locations = face_recognition.face_locations(rgb_small_frame)
        # 如果硬件允许，可以使用GPU进行加速，此时应改为CNN模型
        # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
        # 返回128维人脸编码，即人脸特征
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        # 将得到的人脸特征与数据库中的人脸特征集合进行比较，相同返回True，不同返回False
        for face_encoding in face_encodings:
            threshold_list = [0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28,
                              0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.40]
            for thres in threshold_list:
                try:
                    matches = face_recognition.compare_faces(a_encoding_str, face_encoding, tolerance=thres)
                except Exception as e:
                    print(e)
                if True in matches:
                    print(thres)
                    break
                else:
                    pass

            if True in matches:
                match_index = matches.index(True)
                userid = a_user_id[match_index]
                a1 = a_encoding_str[match_index]
                user_name = a_user_name[match_index]
                score = get_similarity(a1, face_encoding)
                result_sss.append({"score": score, "user_id": str(userid), "name": user_name})

        return {"code": "0", "data": {"find_records": result_sss}}


# 查找用户，返回图片base64。
class Facefind(Resource):
    def post(self):
        # 需要返回的结果
        args = parser_put.parse_args()
        # 构建新参数
        user_id = args['user_id']
        sn = args['sn']
        if user_id == None or sn == None:
            return {"code": "500", "msg": "Parameter error"}, 200
        # 调用获取数据库里面的信息
        a_user_name, a_encoding_str, a_user_id, a_sn, a_re_img_url = get_info_mysql()
        # 判断校验参数
        if sn not in a_sn:
            return {"code": "10001", "msg": "Device not registered"}, 200
        if user_id not in a_user_id:
            return {"code": "20001", "msg": "user not registered"}, 200
        result_index = a_user_id.index(user_id)
        result_img_url = a_re_img_url[result_index]
        with open(result_img_url, "rb") as f:  # 转为二进制格式
            base64_data = base64.b64encode(f.read()).decode()  # 使用base64进行加密
            print(type(base64_data))
            json_base64_data = json.dumps(base64_data)

            return {"code": "0", "msg": {"user_id": user_id, "base64": json_base64_data}}, 200


# 添加任务
class TaskAdd(Resource):
    def post(self):
        args = parser_put.parse_args()
        # 构建新参数
        cam_url = args['cam_url']
        sn = args['sn']
        all_sn, all_user_id = select_device_msyql()
        a_sn, a_cam_url = select_task_mysql(sn)
        if cam_url == None or sn == None:
            return {"code": "500", "msg": "Parameter error"}, 200
        # 判断sn 有没有注册
        if sn not in all_sn:
            return {"code": "10001", "msg": "Device not registered"}, 200
        # 判断是不是重复注册了
        if sn in a_sn and cam_url in a_cam_url:
            return {"code": "0000", "msg": "The task has been registered"}, 200
        resout_info = save_task_mysql(cam_url, sn)
        if resout_info == 0:
            # 资源添加成功，返回0
            return {"code": "0", "msg": "Task registration is successful"}, 200
        else:
            return {"code": "400", "msg": resout_info}, 200


# 删除任务
class TaskDelete(Resource):
    def post(self):
        args = parser_put.parse_args()
        # 构建新参数
        cam_url = args['cam_url']
        sn = args['sn']

        if cam_url == None or sn == None:
            return {"code": "500", "msg": "Parameter error"}, 200

        # 对传入进来的数据进行先校验
        all_sn, all_user_id = select_device_msyql()
        if sn not in all_sn:
            return {"code": "10001", "msg": "Device not registered"}, 200
        a_sn, a_cam_url = select_task_mysql(sn)
        if cam_url not in a_cam_url:
            return {"code": "10001", "msg": "Task does not exist"}, 200

        # 调用方法to_do
        resout_info = delete_task_mysql(cam_url)
        if resout_info == 0:
            # 资源添加成功，返回0
            return {"code": "0", "data": "delete task success"}, 200
        else:
            # 资源添加失败，返回400
            return {"code": "400", "data": resout_info}, 200


# 任务列表
class TaskList(Resource):
    def post(self):
        args = parser_put.parse_args()
        # 构建新参数
        sn = args['sn']
        all_sn, all_user_id = select_device_msyql()
        if sn not in all_sn:
            return {"code": "10001", "msg": "Device not registered"}, 200

        all_sn, all_cam_url = select_task_mysql(sn)
        if len(all_sn) == 0:
            return {"code": "4000", "msg": "No task"}, 200
        result_list = []
        for i in range(len(all_sn)):
            result_data = {}
            result_data["sn"] = all_sn[i]
            print(i)
            result_data["cam_url"] = all_cam_url[i]
            result_list.append(result_data)
            del result_data
        return {"code": "0", "data": result_list}, 200


# Indexpost
class IndexPostView(Resource):
    def post(self):
        result_status = init_databases()
        if result_status == 0:
            return {"code": "0", "data": "index web site"}, 200
        else:
            return {"code": "400", "data": "index web site no success"}, 200


# Indexget
class IndexGetView(Resource):
    def get(self):
        return {"code": "0", "data": "index web site"}, 200


# 设置路由，即路由地址为http://127.0.0.1:5000/users
api.add_resource(IndexPostView, "/indexpost")
api.add_resource(IndexGetView, "/indexget")

api.add_resource(DeviceRegist, "/device/register.do")
api.add_resource(DeviceDelete, "/device/delete.do")

api.add_resource(FaceRegister, "/face/register.do")
api.add_resource(FaceDelete, "/face/delete.do")
api.add_resource(FaceDetection, "/face/find_detection.do")
api.add_resource(Facefind, "/face/find_user.do")

api.add_resource(TaskAdd, "/task/add.do")
api.add_resource(TaskDelete, "/task/delete.do")
api.add_resource(TaskList, "/task/list.do")

api.add_resource(DatabasesInit, "/data/init.do")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
