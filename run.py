# -*- coding: utf-8 -*-
import os
import sys
import time


def aab_setup():  # 初始化文件
    def del_file(path):  # 删除apksPackage目录下所有文件
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                del_file(c_path)
            else:
                os.remove(c_path)
                print("删除{}文件成功".format(i))
    apks_path = "./apksPackage"
    del_file(apks_path)


def is_exist_apk():
    app_name = "\npackage:com.qiyee.recruit\n"
    app_list = os.popen('adb shell pm list packages').read()
    if app_name in app_list:
        return True


def abb_action():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append("{}/ADB".format(base_dir))
    pipeline = os.popen("adb devices")  # cmd获取设备名称
    adb_devices = pipeline.read()
    try:
        device_name = adb_devices.split()[4]
        print("安装设备编号：{}".format(device_name))
        flag = True
    except Exception as e:
        print("请检查移动安装设备是否连接正常，【异常信息:{}】".format(e))
        flag = False
    if flag:
        dir_lists = os.listdir("./aabPackage")
        aab_name = None
        max_time = 0
        for dir_list in dir_lists:
            if dir_list[-4:] == ".aab":
                creat_time = os.path.getctime("./aabPackage/{}".format(dir_list))  # 查找创建时间最近的.aab包
                # print("{},{}".format(dir_list, creat_time))
                if creat_time > max_time:
                    max_time = creat_time
                    aab_name = dir_list
        if aab_name:
            print("安装的aab包是：{}".format(aab_name))
            aab_path = "./aabPackage/{}".format(aab_name)
            exist_flag = is_exist_apk()
            if exist_flag:
                os.popen("adb uninstall com.qiyee.recruit")  # 卸载已有kupu安装包
                print("卸载已有的kupu安装包成功")
            aab_setup()  # 初始化文件数据
            time.sleep(1)
            #  生成手机配置json文件
            device_info = "java -jar ./tools/bundletool-all-1.8.0.jar get-device-spec " \
                          "--output=./apksPackage/device-spec.json"
            os.system(device_info)
            print("生成手机配置json文件成功")
            #  生成apks安装包
            apks_bag = "java -jar ./tools/bundletool-all-1.8.0.jar build-apks --bundle={} " \
                       "--output=./apksPackage/app-debug.apks --overwrite --ks=./tools/qiyee_recruit.jks " \
                       "--ks-pass=pass:qiyee_123456 --ks-key-alias=qiyeerecruit --key-pass=pass:qiyee_123456 " \
                       "--device-spec=./apksPackage/device-spec.json".format(aab_path)
            os.system(apks_bag)
            print("生成apks安装包成功")
            time.sleep(3)
            print("!!!准备apks包安装，设备需手动授权")
            apks_install = "java -jar ./tools/bundletool-all-1.8.0.jar install-apks --apks=./apksPackage/app-debug.apks"
            os.system(apks_install)
            exist_flag = is_exist_apk()
            if exist_flag:
                print("apks包已安装成功")
            else:
                print("apks包安装失败")
        else:
            print("aabPackage目录下未上传abb安装包")


if __name__ == '__main__':
    abb_action()
