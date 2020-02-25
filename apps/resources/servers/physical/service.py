import functools
from .models import Asset
from .models import TaskLog
from datetime import datetime
import xlrd
import pandas as pd

from apps.account.account.models import User, DataDicName, DataDicContent
from utils.response_tools import ResponseCode

model_config = {'1': Asset}


def record_log(machine_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            machine_table = {"physical": Asset}.get(machine_type, Asset)

            data = args[1].data
            server_id = data['id']
            try:
                user_id = args[1].user_id
            except:
                user_id = 1
            user = User.objects.filter(id=user_id).first()
            user_name = user.chinese_name if user else ""
            # 操作前的状态
            before_machine = machine_table.objects.filter(id=server_id).first()
            before_status = before_machine.svrchangenid if before_machine else ''
            result = func(*args, **kw)
            # 操作后的状态
            after_machine = Asset.objects.filter(id=server_id).first()
            after_status = after_machine.svrchangenid if after_machine else ''
            # 记录存库
            loginfo = TaskLog(serverid=after_machine, starttime=datetime.now(), origin_status=before_status,
                              user_name=user_name, changed_status=after_status)
            loginfo.save()
            return result
        return wrapper
    return decorator


def excel_upload(file_type, Files, path_root):
    parser_config = ('svrsn', 'tdtnamenid', 'idcnamenid', 'svrfirstusetime', 'svrstoptime')
    servers_models = DataDicName.objects.filter(aliasname='tdtnamenid').first()
    servers_models_contents = [x.content for x in DataDicContent.objects.filter(name_id=servers_models.id)]
    servers_room_number = DataDicName.objects.filter(aliasname='idcnamenid').first()
    servers_room_number_contents = [x.content for x in DataDicContent.objects.filter(name_id=servers_room_number.id)]
    error_data = []
    right_data = []
    for File in Files:
        data_flag, error_line, error_column = True, 0, ''
        file_path = "{0}{1}".format(path_root, File.name)
        with open(file_path, 'wb+') as f:
            for chunk in File.chunks():
                f.write(chunk)
        try:
            ExcelFile = xlrd.open_workbook(file_path)
        except:
            return {'code': ResponseCode.params_error, 'msg': "请上传excel文件", 'data': ""}
        data_flag, error_column, error_line = parser_excel_data(ExcelFile, data_flag, error_column, error_line,
                                                                parser_config, right_data, servers_models_contents, servers_room_number_contents)
        if not data_flag:
            error_data.append({"error_file": File.name, "error_line": error_line, "error_column": error_column})
    if error_data:
        return {'code': ResponseCode.params_error, 'msg': "文件解析失败", 'data': error_data}
    for data in right_data:
        model_config.get(file_type, Asset)(**data).save()
    return {'code': ResponseCode.success, 'msg': "文件解析成功", 'data': ""}


def parser_excel_data(ExcelFile, data_flag, error_column, error_line, parser_config, right_data, servers_models_contents, servers_room_number_contents):
    sheet_name = ExcelFile.sheet_names()[0]
    sheet = ExcelFile.sheet_by_name(sheet_name)
    for i in range(1, sheet.nrows):
        servers_data = {}
        for j in range(0, sheet.ncols):
            value = sheet.cell_value(i, j)
            if (j == 1 and str(value).strip() not in servers_models_contents) or (j == 2 and str(value).strip() not in servers_room_number_contents):
                data_flag = False
                error_line = i + 1
                error_column = sheet.cell_value(0, j)
                break
            servers_data[parser_config[j]] = parser_method(value, j)
        right_data.append(servers_data)
        if not data_flag:
            break
    return data_flag, error_column, error_line


def parser_method(value, index):
    if index == 2:
        return str(value)
    elif index in [3, 4]:
        return datetime.strptime(str(int(value)), '%Y%m%d')
    else:
        return str(value)


def data_download(data_type, path):
    ret_data = model_config.get(data_type, Asset).objects.all()
    ret_data = pd.DataFrame(list(ret_data.values()))
    ret_data.to_excel(path + 'temp.xlsx')
    file = open(path + 'temp.xlsx', 'rb')
    return file
    # return ret_data.to_csv()
