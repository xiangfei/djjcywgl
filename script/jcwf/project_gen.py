# coding=utf-8
import os
import sys
import shutil


# 创建路径
def mkdir(path):
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


# 拷贝文件
def cpfile(sourceFile, targetFile):
    # 判断文件是否存在
    isExist = os.path.exists(sourceFile)

    isDesExist = os.path.exists(targetFile)

    if not isDesExist:
        print targetFile + '目标路径不存在，准备创建'
        mkdir(targetFile)

    if not isExist:
        print sourceFile + '文件不存在'
        return False

    else:
        print '开始拷贝' + sourceFile + "到" + targetFile

        fileName = sourceFile.split("/")[-1]
        shutil.copy(sourceFile, targetFile)
        isPomFile = "pom.xml" in sourceFile
        if isPomFile:
            replacePomFile(targetFile + fileName, default_group_id, default_artifact_id, des_group_id, des_artifact_id)
        else:
            replaceJavaFile(targetFile + fileName, default_package, des_package)
        return True

        # 拷贝目录


def replacePomFile(sourceFile, default_group_id, default_artifact_id, des_group_id, des_artifact_id):
    isExist = os.path.exists(sourceFile)

    if not isExist:
        print isExist + '文件不存在'
        return False

    isCorrectFile = "pom.xml" in sourceFile
    if not isCorrectFile:
        print sourceFile + '不是pom文件'
        return False
    # 替换group id
    replaceFile(sourceFile, default_group_id, des_group_id)
    # 替换artifact id
    replaceFile(sourceFile, default_artifact_id, des_artifact_id)


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
    replaceFile(sourceFile, default_package, des_package)


def cpfolder(sourceFolder, desFolder):
    # 判断文件是否存在
    isExist = os.path.exists(sourceFolder)

    if not isExist:
        print sourceFolder + '文件不存在'
        return False

    else:
        print '开始拷贝' + sourceFolder + "到" + desFolder
        shutil.copytree(sourceFolder, desFolder)
        return True


# 替换文件中的字符串
def replaceFile(sourceFile, sourceStr, desStr):
    if not os.path.isfile(sourceFile):
        print sourceFile + '文件不存在'
        sys.exit();

    s_file = file(sourceFile, 'r+')
    d_file = file(sourceFile + '.tmp', 'w')

    print '开始替换' + sourceFile + '的所有' + sourceFile + "内容"

    for line in s_file.readlines():
        d_file.writelines(line.replace(sourceStr, desStr))

    print '替换完成!'

    s_file.close();
    d_file.close();

    os.rename(sourceFile + '.tmp', sourceFile)


def genBasicProject(source_folder, projectName):
    # 创建biz
    mkdir(projectName + "/" + app + app_child_pro[0])
    # 创建common
    mkdir(projectName + "/" + app + app_child_pro[1])
    # 创建web
    mkdir(projectName + "/" + app + app_child_pro[2])

    cpfile(source_folder + "pom.xml", projectName + "/")
    replacePomFile(projectName + "/pom.xml", default_group_id, default_artifact_id, des_group_id,
                   des_artifact_id)


def genProjectBasic(source_folder, root_path, project_name, base_package, package):
    project_path = root_path + project_name
    mkdir(project_path)
    source_pom_file = source_folder + project_name + "pom.xml";
    des_pom_file = root_path + project_name
    # 拷贝pom文件
    cpfile(source_pom_file, des_pom_file)

    base_package_path = "";
    base_package_array = base_package.split(".")
    for i in range(len(base_package_array)):
        base_package_path = base_package_path + "/" + base_package_array[i]

    # 项目包
    package_path = "";
    package_array = package.split(".")
    for k in range(len(package_array)):
        package_path = package_path + "/" + package_array[k]

    target = project_path + "/src/main/java" + base_package_path + package_path;
    mkdir(target);
    return target;


def cp_project_files(source_folder, source_files, des_files, package_path):
    for i in range(len(source_files)):
        cpfile(source_folder + source_files[i], package_path + des_files[i])
        # todo 替换对应文件


def gen_dal_resource(source_folder, source_file, des_path):
    mkdir(des_path)
    cpfile(source_folder + source_file, des_path)
    replaceFile(des_path + "/UserDOMapper.xml", default_package, des_package)


# gen_dalgen
def gen_dalgen():
    cpfolder(source_folder + "/dalgen", des_path + project + "/dalgen")
    replacePomFile(des_path + project + "/dalgen/pom.xml", default_group_id, default_artifact_id, des_group_id,
                   des_artifact_id)
    replaceFile(des_path + project + "/dalgen/config/config.xml", default_package, des_package)


def gen_build(source_path, project_name):
    cpfolder(source_path, project_name + "/build")
    replaceFile(project_name + "/build/dev/disconf.properties", default_project, project)
    replaceFile(project_name + "/build/pre/disconf.properties", default_project, project)
    replaceFile(project_name + "/build/prod/disconf.properties", default_project, project)
    replaceFile(project_name + "/build/test/disconf.properties", default_project, project)


def gen_web_resource(source_path, des_path):
    cpfolder(source_path, des_path)
    replaceFile(des_path + "/application.properties", default_project, project)
    replaceFile(des_path + "/disconf.properties", default_project, project)
    replaceFile(des_path + "/disconf.xml", default_package, des_package)
    replaceFile(des_path + "/dubbo.properties", default_package, des_package)
    replaceFile(des_path + "/dubbo.properties", default_project, project)
    replaceFile(des_path + "/log4j.xml", default_package, des_package)


def gen_provider():
    # biz/facade-impl 文件拷贝
    facade_impl_source_files = ["/biz/facade-impl/DubboConfiguration.java",
                                "/biz/facade-impl/ServiceFacadeAspect.java", "/biz/facade-impl/DemoFacadeImpl.java"]
    facade_impl_des_files = ["/config/", "/aspect/", "/impl/"]
    # biz/service
    service_source_files = ["/biz/service/BizException.java", "/biz/service/ErrorEnum.java",
                            "/biz/service/ServiceException.java", "/biz/service/DemoService.java",
                            "/biz/service/DemoServiceImpl.java"]
    service_des_files = ["/exception/", "/exception/", "/exception/", "/manager/", "/manager/"]
    # common/dal
    common_dal_source_files = ["/common/dal/DataSourceConfig.java", "/common/dal/BasePage.java",
                               "/common/dal/UserDAO.java", "/common/dal/UserDO.java", "/common/dal/UserDOMapper.java"]
    common_dal_des_files = ["/config/", "/paging", "/dao/", "/dataobject/", "/mapper/"]

    # common/facade
    common_facade_source_files = ["/common/service-facade/DemoFacade.java", "/common/service-facade/UserVO.java"]
    common_facade_des_files = ["/facade/", "/vo/"]

    # web/service
    web_service_source_files = ["/web/service/ServletInitializer.java"]
    web_service_des_files = ["/init/"]

    # 创建基础项目
    genBasicProject(source_folder, des_path + project)

    # 创建facade-impl
    facade_impl_package_path = genProjectBasic(source_folder, des_path + project + "/app", "/biz/facade-impl/",
                                               des_package, "biz.service")
    cp_project_files(source_folder, facade_impl_source_files, facade_impl_des_files, facade_impl_package_path)

    # 创建service
    service_package_path = genProjectBasic(source_folder, des_path + project + "/app", "/biz/service/", des_package,
                                           "core.service")
    cp_project_files(source_folder, service_source_files, service_des_files, service_package_path)

    # 创建common/dal
    dal_package_path = genProjectBasic(source_folder, des_path + project + "/app", "/common/dal/", des_package,
                                       "common.dal")
    cp_project_files(source_folder, common_dal_source_files, common_dal_des_files, dal_package_path)
    gen_dal_resource(source_folder, "/common/dal/UserDOMapper.xml",
                     des_path + project + "/app/common/dal/src/main/resources/")

    # 创建service-integration
    service_integration_package_path = genProjectBasic(source_folder, des_path + project + "/app",
                                                       "/common/service-integration/",
                                                       des_package,
                                                       "integration.service")

    # 创建service-facade
    service_facade_package_path = genProjectBasic(source_folder, des_path + project + "/app", "/common/service-facade/",
                                                  des_package,
                                                  "facade.service")
    cp_project_files(source_folder, common_facade_source_files, common_facade_des_files, service_facade_package_path)

    # 创建web
    web_service_package_path = genProjectBasic(source_folder, des_path + project + "/app", "/web/service/", des_package,
                                               "web.service")
    cp_project_files(source_folder, web_service_source_files, web_service_des_files, web_service_package_path)
    # 创建web resource文件
    gen_web_resource(source_folder + "web/service/resources",
                     des_path + project + "/app/web/service/src/main/resources")

    # 创建dalgen
    gen_dalgen()
    # 创建build
    gen_build("./build", des_path + project)


def gen_consumer():
    # 创建consumer基础结构
    genBasicProject(source_consumer_folder, des_path + project)
    # biz service
    biz_service_source_files = ["/biz/service/BizException.java", "/biz/service/ErrorEnum.java",
                                "/biz/service/ServiceException.java"]
    biz_service_des_files = ["/exception/", "/exception/", "/exception/"]

    # integration
    common_integration_source_files = ["/common/service-integration/DubboConfiguration.java"]
    common_integration_des_files = ["/"]

    # web/service
    web_service_source_files = ["/web/service/ServiceFacadeApplication.java", "/web/service/JsonResVo.java",
                                "/web/service/ServiceRequestAspect.java", "/web/service/WebConfiguration.java",
                                "/web/service/BaseReq.java", "/web/service/ParamsUtil.java",
                                "/web/service/ResultStatusCode.java", "/web/service/TestController.java"]
    web_service_des_files = ["/", "/model/res/", "/aspect/", "/interceptor/", "/model/req/", "/utils/", "/model/res/",
                             "/controller/"]

    # 创建基础项目
    biz_service_package_path = genProjectBasic(source_consumer_folder, des_path + project + "/app", "/biz/service/",
                                               des_package,
                                               "gateway.service")
    cp_project_files(source_consumer_folder, biz_service_source_files, biz_service_des_files, biz_service_package_path)

    common_integration_package_path = genProjectBasic(source_consumer_folder, des_path + project + "/app",
                                                      "/common/service-integration/",
                                                      des_package, "gateway.integration")
    cp_project_files(source_consumer_folder, common_integration_source_files, common_integration_des_files,
                     common_integration_package_path)

    web_service_package_path = genProjectBasic(source_consumer_folder, des_path + project + "/app", "/web/service/",
                                               des_package, "gateway.web")
    cp_project_files(source_consumer_folder, web_service_source_files, web_service_des_files,
                     web_service_package_path)
    gen_web_resource(source_consumer_folder + "web/service/resources",
                     des_path + project + "/app/web/service/src/main/resources")
    # 创建build
    gen_build("./build", des_path + project + "/build")


# 固定变量
app = "app/"
app_child_pro = ["biz/", "common/", "web/"]
default_group_id = "net.wan51"
default_artifact_id = "wan51"
default_project = "wan51"
default_package = "net.wan51"
source_folder = "./provider/"
source_consumer_folder = "./consumer/"

# 自定义常量
des_group_id = "com.jcgroup"
des_artifact_id = ""
des_package = ""
des_path = "./"
project = ""

# main入口
if __name__ == '__main__':

    print("################################################################")
    print("")
    print("")
    print("                 欢迎使用JWS项目开发脚手架 V0.1                   ")
    print("")
    print("")
    print("################################################################")
    print("")
    print("")
    print("")
    print("")

    # package
    print("请输入需要生成的项目存放路径以/结尾：(默认为脚本所在路径),使用默认路径请直接敲回车键")
    des_path = raw_input("")
    if not des_path:
        des_path = "./"
    print("项目生成路径：" + des_path)

    # project
    print("请输入project名称：(例如：jcy-base)")
    project = raw_input("")
    if not project:
        print "项目名不能为空"
        sys.exit()
    is_project_exist = os.path.exists(des_path + project)
    if is_project_exist:
        print project + "项目已经存在，请移除项目或换一个项目名"
        sys.exit()

    # 输入项目类型
    print("请输入你要创建的项目类型:")
    print("1: Dubbo服务层项目")
    print("2: 网关项目")
    projectType = raw_input("");
    if projectType == "1":
        print "您的输入是1，dubbo服务项目"
    elif projectType == "2":
        print "您的输入是2，准备创建网关项目"
    else:
        print "无法识别：" + projectType
        sys.exit()

    # group id
    print("请输入group id,(默认为com.jcgroup)使用默认group请直接敲回车键")
    des_group_id = raw_input("");
    if not des_group_id:
        des_group_id = "com.jcgroup"
    print("您输入的group id: " + des_group_id)

    # artifact id
    print("请输入artifact id: (例如：jcy-base)")
    des_artifact_id = raw_input("")
    if not des_artifact_id:
        print "artifact id不能为空"
        sys.exit()
    print("您输入的artifact id: " + des_artifact_id)
    print("")

    # package
    print("请输入包名:(例如：com.jcgroup.jcy.base)")
    des_package = raw_input("")
    if not des_package:
        print "包名不能为空"
        sys.exit()

    print("您输入的package包名：" + des_package)
    # 开始创建项目
    if projectType == "1":
        print "您的输入是1，dubbo服务项目"
        gen_provider()
    elif projectType == "2":
        print "您的输入是2，准备创建网关项目"
        gen_consumer()

    print "创建项目成功"
