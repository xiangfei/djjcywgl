# coding=utf-8
import os
import sys
import shutil
import zipfile


# 创建路径
def make_dir(path):
    # 去除首位空格
    path = path.strip()

    # 去除尾部空格
    path = path.rstrip("\\")

    # 判断路径是否存在
    isExist = os.path.exists(path)

    # 判断结果
    if not isExist:
        # 如果不存在，则创建目录
        os.makedirs(path)

        print path + '创建成功';

        return True
    else:

        # 如果目录存在则不创建，并提示目录已民经存在
        print path + '目录已存在'

        return False


# 循环列出文件夹下所有文件
def list_files(path, files):
    for filename in os.listdir(path):
        if os.path.isdir(path + "/" + filename):
            list_files(path + "/" + filename, files)
        else:
            # print path + "/" + filename
            files.append(path + "/" + filename)
    return files


# 拷贝文件
def cp_file(source_file, target_file):
    # 判断文件是否存在
    fileName = target_file.split("/")[-1]
    target_file = target_file.replace(fileName, "")
    is_exist = os.path.exists(source_file)
    is_des_exist = os.path.exists(target_file)
    if not is_des_exist:
        print target_file + '目标路径不存在，准备创建'
        make_dir(target_file)
    if not is_exist:
        print source_file + '文件不存在'
        return False

    print '开始拷贝' + source_file + "到" + target_file
    shutil.copy(source_file, target_file)


# package转路径
def package_to_path(package):
    package_path = "";
    package_array = package.split(".")
    for k in range(len(package_array)):
        package_path = package_path + "/" + package_array[k]
    return package_path;


# 开始创建项目
def gen_project(source_path, package, des_path, des_project_name):
    package_path = package_to_path(package)
    file_list = list_files(source_path, global_source_file_list)
    for files in file_list:
        target_path = files.replace(default_package_path, package_path)
        target_path = target_path.replace(source_path, des_path + des_project_name)
        cp_file(files, target_path)


# 开始替换文件
def replace_project_files(project_name, des_path, default_artifact_id, default_project):
    file_list = list_files(des_path + project_name, global_target_file_list);
    for files in file_list:
        is_pom_file = pom_file in files
        is_java_file = java_file in files
        if is_pom_file:
            replacePomFile(files, default_group_id, default_artifact_id, global_des_group_id, global_des_artifact_id)
        elif is_java_file:
            replaceJavaFile(files, default_package, global_des_package)
        else:
            replace_normal_file(files, default_project, global_des_project_name, default_package, global_des_package)


# 替换pom文件内容
def replacePomFile(sourceFile, default_group_id, default_artifact_id, des_group_id, des_artifact_id):
    isExist = os.path.exists(sourceFile)

    if not isExist:
        print isExist + '文件不存在'
        return False

    is_correct_file = "pom.xml" in sourceFile
    if not is_correct_file:
        print sourceFile + '不是pom文件'
        return False
    # 替换group id
    replace_file(sourceFile, default_group_id, des_group_id)
    # 替换artifact id
    replace_file(sourceFile, default_artifact_id, des_artifact_id)


# 替换java文件内容
def replaceJavaFile(sourceFile, default_package, des_package):
    isExist = os.path.exists(sourceFile)

    if not isExist:
        print sourceFile + '文件不存在'
        return False

    isCorrectFile = ".java" in sourceFile
    if not isCorrectFile:
        print sourceFile + '不是java文件'
        return False
    # 替换package
    replace_file(sourceFile, default_package, des_package)


# 替换普通文件
def replace_normal_file(sourceFile, default_prject_name, des_project_name, default_package, des_package):
    isExist = os.path.exists(sourceFile)

    if not isExist:
        print isExist + '文件不存在'
        return False

    # 替换project name
    replace_file(sourceFile, default_prject_name, des_project_name)
    replace_file(sourceFile, default_package, des_package)


# 替换文件中的字符串
def replace_file(source_file, source_str, des_str):
    if not os.path.isfile(source_file):
        print source_file + '文件不存在'
        sys.exit();

    s_file = file(source_file, 'r+')
    d_file = file(source_file + '.tmp', 'w')

    print '开始替换' + source_file + '的所有' + source_file + "内容"

    for line in s_file.readlines():
        d_file.writelines(line.replace(source_str, des_str))

    print '替换完成!'

    s_file.close();
    d_file.close();
    os.rename(source_file + '.tmp', source_file)


def start_zip(file_path, zip_name):
    """压缩文件"""
    f = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for folder, subfolder, files in os.walk(file_path):
        for file in files:
            f.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), file_path))
    f.close()


# 全局
global_source_file_list = []

global_target_file_list = []

default_group_id = "com.jcgroup.demo"
default_package = "com.jcgroup.demo"
default_package_path = "com/jcgroup/demo"

provider_source = "./jc-provider/"
provider_default_artifact_id = "jc-provider"
provider_default_project = "jc-provider"

consumer_source = "./jc-consumer/"
consumer_default_artifact_id = "jc-consumer"
consumer_default_project = "jc-consumer"

java_file = ".java"
pom_file = "pom.xml"

# 入参
global_des_package = "com.jcgroup.jcy"
global_des_project_name = "jcy-base"
global_des_path = ""
global_des_group_id = "com.jcgroup"
global_des_artifact_id = "jcy-base"

if __name__ == '__main__':
    # 项目名
    project_name = sys.argv[1]
    # 服务名
    service_name = sys.argv[2]
    # 项目类型 1:dubbo, 2:网关项目
    projectType = sys.argv[3]

    global_des_artifact_id = global_des_project_name = project_name + '-' + service_name 
    global_des_package = global_des_group_id + '.' + project_name + '.' + service_name
    
    # 开始创建项目
    if projectType == "4":
        print "您的输入是1，dubbo服务项目"
        gen_project(provider_source, global_des_package, global_des_path, global_des_project_name)
        replace_project_files(global_des_project_name, global_des_path, provider_default_artifact_id, provider_default_project)
    elif projectType == "2":
        print "您的输入是2，准备创建网关项目"
        gen_project(consumer_source, global_des_package, global_des_path, global_des_project_name)
        replace_project_files(global_des_project_name, global_des_path, consumer_default_artifact_id,
                              consumer_default_project)

    import time
    date = time.strftime('%Y%m%d',time.localtime(time.time()))
    print "开始压缩项目文件目录"
    start_zip(global_des_project_name, global_des_project_name+'.zip')

    print "删除文件目录"
    shutil.rmtree(global_des_project_name)

    print "移动到下载目录"
    shutil.move(global_des_project_name+'.zip',"../../downloads")   

    print "创建项目成功"
