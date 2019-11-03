import pymysql
import numpy as np


# 人脸特征信息保存
def save_encoding_mysql(user_name, encoding_str, user_id, sn, re_img_url):
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # SQL插入语句
    insert_sql = "insert into staff(user_name, encoding_str, user_id, sn, re_img_url) values(%s,%s,%s,%s,%s)"
    try:
        # 执行sql语句
        cursor.execute(insert_sql, (user_name, encoding_str, user_id, sn, re_img_url))
        # 提交到数据库执行
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return 0
    except Exception as e:
        # 如果发生错误则回滚并打印错误信息
        conn.rollback()
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e


# 从数据库获取保存的人脸特征信息
def get_info_mysql():
    # 从数据库获取保存的人脸特征信息
    # 人脸特征编码集合
    a_user_name = []
    a_encoding_str = []
    a_user_id = []
    a_sn = []
    a_re_img_url = []
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # SQL查询语句
    sql = "select user_name, encoding_str, user_id, sn, re_img_url from staff"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 返回的结果集为元组
        for row in results:
            user_name = row[0]
            encoding = row[1]
            user_id = row[2]
            sn = row[3]
            re_img_url = row[4]
            # print("name=%s,encoding=%s" % (name, encoding))
            # 将字符串转为numpy ndarray类型，即矩阵
            # 转换成一个list
            dlist = encoding.strip(' ').split(',')
            # 将list中str转换为float
            dfloat = list(map(float, dlist))
            arr = np.array(dfloat)
            # 将从数据库获取出来的信息追加到集合中
            a_user_name.append(user_name)
            a_encoding_str.append(arr)
            a_user_id.append(user_id)
            a_sn.append(sn)
            a_re_img_url.append(re_img_url)
    except Exception as e:
        print(e)
        conn.rollback()
        return a_user_name, a_encoding_str, a_user_id, a_sn, a_re_img_url
    # 关闭游标
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return a_user_name, a_encoding_str, a_user_id, a_sn, a_re_img_url


# 把设备信息存入到数据库里面
def save_device_mysql(device_name, sn):
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # SQL插入语句
    insert_sql = "insert into device(device_name, sn) values(%s,%s)"
    try:
        # 执行sql语句
        cursor.execute(insert_sql, (device_name, sn))
        # 提交到数据库执行
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return 0
    except Exception as e:
        # 如果发生错误则回滚并打印错误信息
        conn.rollback()
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e


# 从数据库删除人员信息信息
def delete_user_mysql(userid):
    # 从数据库删除保存的人脸特征信息
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # SQL查询语句
    sql = '''delete from device where user_id=%s'''
    try:
        # 执行SQL语句
        cursor.execute(sql, userid)
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return 0
    except Exception as e:
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e


# 从数据库删除人脸特征信息
def delete_face_mysql(userid):
    # 从数据库删除保存的人脸特征信息
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # SQL查询语句
    sql = '''delete from staff where user_id=%s'''
    try:
        # 执行SQL语句
        cursor.execute(sql, userid)
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return 0
    except Exception as e:
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e


# 从数据库删除人脸特征信息
def delete_device_mysql(sn):
    # 从数据库删除保存的人脸特征信息
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # SQL查询语句
    sql = '''delete from device where sn=%s'''
    try:
        # 执行SQL语句
        cursor.execute(sql, sn)
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return 0
    except Exception as e:
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e


# 查询数据库 sn 信息
def select_device_msyql():
    all_sn = []
    all_device_name = []
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # SQL插入语句
    insert_sql = '''select sn, device_name from device'''

    try:
        # 执行sql语句
        cursor.execute(insert_sql)
        results = cursor.fetchall()
        # 返回的结果集为元组
        for row in results:
            sn = row[0]
            device_name = row[1]
            all_sn.append(sn)
            all_device_name.append(device_name)
        # 提交到数据库执行
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return all_sn, all_device_name
    except Exception as e:
        # 如果发生错误则回滚并打印错误信息
        conn.rollback()
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e


# 存任务到数据库
def save_task_mysql(cam_url, sn):
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # SQL插入语句
    insert_sql = "insert into task (cam_url, sn) values(%s,%s)"
    try:
        # 执行sql语句
        cursor.execute(insert_sql, (cam_url, sn))
        # 提交到数据库执行
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return 0
    except Exception as e:
        # 如果发生错误则回滚并打印错误信息
        conn.rollback()
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e


# 查询数据库 sn， user_id 信息
def select_task_mysql(sn):
    all_sn = []
    all_cam_url = []
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # SQL插入语句
    insert_sql = '''select sn, cam_url from task where sn=%s'''

    try:
        # 执行sql语句
        cursor.execute(insert_sql, sn)
        results = cursor.fetchall()
        # 返回的结果集为元组
        for row in results:
            sn = row[0]
            cam_url = row[1]
            all_sn.append(sn)
            all_cam_url.append(cam_url)
        # 提交到数据库执行
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return all_sn, all_cam_url
    except Exception as e:
        # 如果发生错误则回滚并打印错误信息
        conn.rollback()
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e


# 从数据库获取 task 列表
def delete_task_mysql(cam_url):
    # 从数据库删除保存的人脸特征信息
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # SQL查询语句
    sql = '''delete from task where cam_url=%s'''
    try:
        # 执行SQL语句
        cursor.execute(sql, cam_url)
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return 0
    except Exception as e:
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e


# 初始化数据库
def init_databases():
    # 创建数据库连接对象
    conn = pymysql.connect(
        # 数据库的IP地址
        host="127.0.0.1",
        # 数据库用户名称
        user="root",
        # 数据库用户密码
        password="face123456",
        # 数据库名称
        db="facedb",
        # 数据库端口名称
        port=3306,
        # 数据库的编码方式 注意是utf8
        charset="utf8"
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # 删除语句
    delete_t1 = """DROP TABLE device """
    delete_t2 = """DROP TABLE staff """
    delete_t3 = """DROP TABLE task """
    # SQL插入语句
    insert_sql = """
        CREATE TABLE IF NOT EXISTS `device`(
        `device_name` VARCHAR(100) NOT NULL,
        `sn` VARCHAR(40) NOT NULL
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

    insert_sql1 = """
        CREATE TABLE IF NOT EXISTS `staff`(
        `user_name` VARCHAR(100) NOT NULL,
        `encoding_str` VARCHAR(20000) NOT NULL,
        `user_id` VARCHAR(40) NOT NULL,
        `sn` VARCHAR(40) NOT NULL,
        `re_img_url` VARCHAR(100) NOT NULL
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

    insert_sql2 = """
        CREATE TABLE IF NOT EXISTS `task`(
        `cam_url` VARCHAR(100) NOT NULL,
        `sn` VARCHAR(40) NOT NULL
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

    try:
        # 执行sql语句
        cursor.execute(delete_t1)
        cursor.execute(delete_t2)
        cursor.execute(delete_t3)
        cursor.execute(insert_sql)
        cursor.execute(insert_sql1)
        cursor.execute(insert_sql2)
        # 提交到数据库执行
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return 0
    except Exception as e:
        # 如果发生错误则回滚并打印错误信息
        conn.rollback()
        print(e)
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return e
