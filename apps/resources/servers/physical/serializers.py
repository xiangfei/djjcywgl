from .models import Asset, TaskLog
from rest_framework import serializers
from utils.validators import validate_servername, validate_comment, validate_password, validate_serversn
from apps.account.account.models import User, DataDicName, DataDicContent

ENV_NODE = {'0': '总物理', '1': '未上线', '2': '物理', '3': '正式环境', '4': '预发环境', '5': '测试环境', '6': '开发环境', '7': '下线', '8': '报修', '9': '报废'}


def dic_search():
    ret_dict = {}
    dicnames = DataDicName.objects.all()
    for dicname in dicnames:
        values = []
        diccontents = DataDicContent.objects.filter(name_id=dicname.id).all()
        for diccontent in diccontents:
            values.append({"title": diccontent.content, "value": diccontent.id})
        ret_dict[dicname.aliasname] = values
    return ret_dict


def get_dictdata(valuename, valueid):
    json_str = dic_search()
    for i in json_str[valuename]:
        if i['value'] == valueid:
            return i['title']


def get_dictvalue(valuename):
    json_str = dic_search()
    for i in json_str['svrchangenid']:
        if i['title'] == valuename:
            return i['value']


class AssetAllSerializer(serializers.ModelSerializer):
    svrchange = serializers.SerializerMethodField('get_svrchangenid')
    idcname = serializers.SerializerMethodField('get_idcnamenid')
    iopname = serializers.SerializerMethodField('get_iopnamenid')
    sfwname = serializers.SerializerMethodField('get_sfwnamenid')
    tdtname = serializers.SerializerMethodField('get_tdtnamenid')
    user_name = serializers.SerializerMethodField('get_usersname')
    gettime = serializers.SerializerMethodField('get_time')
    gethandle = serializers.SerializerMethodField('get_handle')
    mkspassword = serializers.SerializerMethodField('get_mksspassword')

    class Meta:
        model = Asset
        fields = ("id", "manageip", "switchip", "hostuser", "svrname", "svrip", "svrsn",
                  "eqsname", "svrfirstusetime", "svrstoptime", "svrofftime",
                  "strdescription", "laststatus",  "errcontent", "hostpassword",
                  'svrchangenid', 'sfwnamenid', 'iopnamenid', 'idcnamenid', 'tdtnamenid',
                  "tdtname", "idcname", "iopname", "sfwname", "svrchange", 'svrabandon',
                  'mkspassword', "user_name", 'gettime', 'gethandle',
                  )

    def get_mksspassword(self, obj):
        mkspassword = obj.hostpassword
        return mkspassword

    def get_svrchangenid(self, obj):
        svrchange_id = obj.svrchangenid
        try:
            svrchange_id = int(svrchange_id)
        except:
            svrchange_id = ''
        if svrchange_id:
            svrchangename = get_dictdata('svrchangenid', int(svrchange_id))
            return svrchangename

    def get_idcnamenid(self, obj):
        idcnamenid = obj.idcnamenid
        try:
            idcnamenid = int(idcnamenid)
        except:
            idcnamenid = ''
        if idcnamenid:
            idcname = get_dictdata('idcnamenid', int(idcnamenid))
            return idcname

    def get_iopnamenid(self, obj):
        iopnamenid = obj.iopnamenid
        try:
            iopnamenid = int(iopnamenid)
        except:
            iopnamenid = ''
        if iopnamenid:
            iopname = get_dictdata('iopnamenid', int(iopnamenid))
            return iopname

    def get_sfwnamenid(self, obj):
        sfwnamenid = obj.sfwnamenid
        try:
            sfwnamenid = int(sfwnamenid)
        except:
            sfwnamenid = ''
        if sfwnamenid:
            sfwname = get_dictdata('sfwnamenid', int(sfwnamenid))
            return sfwname

    def get_tdtnamenid(self, obj):
        tdtnameid = obj.tdtnamenid
        try:
            tdtnameid = int(tdtnameid)
        except:
            tdtnameid = ''
        if tdtnameid:
            tdtname = get_dictdata('tdtnamenid', int(tdtnameid))
            return tdtname

    def get_usersname(self, obj):
        asset_id = obj.id
        user_name = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('user_name')
        if user_name:
            user_name = user_name[0]['user_name']
            return user_name
        return ''

    def get_time(self, obj):
        asset_id = obj.id
        gettime = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('starttime')
        if gettime:
            gettime = gettime[0]['starttime']
            return gettime.isoformat(' ')
        return ''

    def get_handle(self, obj):
        asset_id = obj.id
        origin_status = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('origin_status')
        if origin_status:
            origin_status = origin_status[0]['origin_status']
            if origin_status:
                svrchangename = get_dictdata('svrchangenid', int(origin_status))
                return svrchangename
        return ''


class AssetAddSerializer(serializers.ModelSerializer):
    svrsn = serializers.CharField(validators=[validate_serversn])

    def create(self, validated_data):
        return Asset.objects.create(**validated_data)

    class Meta:
        model = Asset
        fields = '__all__'


class AssetUpdateSerializer(serializers.ModelSerializer):
    svrname = serializers.CharField(required=False, validators=[validate_servername])
    strdescription = serializers.CharField(required=False, validators=[validate_comment])
    hostpassword = serializers.CharField(required=False, validators=[validate_password])

    class Meta:
        model = Asset
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    svrchange = serializers.SerializerMethodField('get_svrchangenid')
    idcname = serializers.SerializerMethodField('get_idcnamenid')
    iopname = serializers.SerializerMethodField('get_iopnamenid')
    sfwname = serializers.SerializerMethodField('get_sfwnamenid')
    tdtname = serializers.SerializerMethodField('get_tdtnamenid')
    # user_name = serializers.SerializerMethodField('get_usersname')
    # gettime = serializers.SerializerMethodField('get_time')
    # gethandle = serializers.SerializerMethodField('get_handle')

    class Meta:
        model = Asset
        fields = ("id", "manageip", "switchip", "hostuser", "svrname", "svrip", "svrsn",
                  "eqsname", "svrfirstusetime", "svrstoptime", "svrofftime",
                  "strdescription", "laststatus",  "errcontent", "hostpassword",
                  'svrchangenid', 'sfwnamenid', 'iopnamenid', 'idcnamenid', 'tdtnamenid',
                  "tdtname", "idcname", "iopname", "sfwname", "svrchange",
                  # "user_name", 'gettime', 'gethandle',
                  )

    def get_svrchangenid(self, obj):
        svrchange_id = obj.svrchangenid
        try:
            svrchange_id = int(svrchange_id)
        except:
            svrchange_id = ''
        if svrchange_id:
            svrchangename = get_dictdata('svrchangenid', int(svrchange_id))
            return svrchangename

    def get_idcnamenid(self, obj):
        idcnamenid = obj.idcnamenid
        try:
            idcnamenid = int(idcnamenid)
        except:
            idcnamenid = ''
        if idcnamenid:
            idcname = get_dictdata('idcnamenid', int(idcnamenid))
            return idcname

    def get_iopnamenid(self, obj):
        iopnamenid = obj.iopnamenid
        try:
            iopnamenid = int(iopnamenid)
        except:
            iopnamenid = ''
        if iopnamenid:
            iopname = get_dictdata('iopnamenid', int(iopnamenid))
            return iopname

    def get_sfwnamenid(self, obj):
        sfwnamenid = obj.sfwnamenid
        try:
            sfwnamenid = int(sfwnamenid)
        except:
            sfwnamenid = ''
        if sfwnamenid:
            sfwname = get_dictdata('sfwnamenid', int(sfwnamenid))
            return sfwname

    def get_tdtnamenid(self, obj):
        tdtnameid = obj.tdtnamenid
        try:
            tdtnameid = int(tdtnameid)
        except:
            tdtnameid = ''
        if tdtnameid:
            tdtname = get_dictdata('tdtnamenid', int(tdtnameid))
            return tdtname

    # def get_usersname(self, obj):
    #     asset_id = obj.id
    #     user_name = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('user_name')[0]['user_name']
    #     return user_name
    #
    # def get_time(self, obj):
    #     asset_id = obj.id
    #     gettime = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('starttime')[0]['starttime']
    #     return gettime
    #
    # def get_handle(self, obj):
    #     asset_id = obj.id
    #     origin_status = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('origin_status')[0]['origin_status']
    #     if origin_status:
    #         svrchangename = get_dictdata('svrchangenid', origin_status)
    #         return svrchangename


class AssetNotOnLineSerializer(serializers.ModelSerializer):
    svrchange = serializers.SerializerMethodField('get_svrchangenid')
    idcname = serializers.SerializerMethodField('get_idcnamenid')
    iopname = serializers.SerializerMethodField('get_iopnamenid')
    sfwname = serializers.SerializerMethodField('get_sfwnamenid')
    tdtname = serializers.SerializerMethodField('get_tdtnamenid')
    # user_name = serializers.SerializerMethodField('get_usersname')
    # gettime = serializers.SerializerMethodField('get_time')
    # gethandle = serializers.SerializerMethodField('get_handle')

    class Meta:
        model = Asset
        fields = ("id", "manageip", "switchip", "hostuser", "svrname", "svrip", "svrsn",
                  "eqsname", "svrfirstusetime", "svrstoptime", "svrofftime",
                  "strdescription", "laststatus",  "errcontent", "hostpassword",
                  'svrchangenid', 'sfwnamenid', 'iopnamenid', 'idcnamenid', 'tdtnamenid',
                  "tdtname", "idcname", "iopname", "sfwname", "svrchange",
                  # "user_name", 'gettime', 'gethandle',
                  )

    def get_svrchangenid(self, obj):
        svrchange_id = obj.svrchangenid
        try:
            svrchange_id = int(svrchange_id)
        except:
            svrchange_id = ''
        if svrchange_id:
            svrchangename = get_dictdata('svrchangenid', int(svrchange_id))
            return svrchangename

    def get_idcnamenid(self, obj):
        idcnamenid = obj.idcnamenid
        try:
            idcnamenid = int(idcnamenid)
        except:
            idcnamenid = ''
        if idcnamenid:
            idcname = get_dictdata('idcnamenid', int(idcnamenid))
            return idcname

    def get_iopnamenid(self, obj):
        iopnamenid = obj.iopnamenid
        try:
            iopnamenid = int(iopnamenid)
        except:
            iopnamenid = ''
        if iopnamenid:
            iopname = get_dictdata('iopnamenid', int(iopnamenid))
            return iopname

    def get_sfwnamenid(self, obj):
        sfwnamenid = obj.sfwnamenid
        try:
            sfwnamenid = int(sfwnamenid)
        except:
            sfwnamenid = ''
        if sfwnamenid:
            sfwname = get_dictdata('sfwnamenid', int(sfwnamenid))
            return sfwname

    def get_tdtnamenid(self, obj):
        tdtnameid = obj.tdtnamenid
        try:
            tdtnameid = int(tdtnameid)
        except:
            tdtnameid = ''
        if tdtnameid:
            tdtname = get_dictdata('tdtnamenid', int(tdtnameid))
            return tdtname

    # def get_usersname(self, obj):
    #     asset_id = obj.id
    #     user_name = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('user_name')[0]['user_name']
    #     return user_name
    #
    # def get_time(self, obj):
    #     asset_id = obj.id
    #     gettime = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('starttime')[0]['starttime']
    #     return gettime
    #
    # def get_handle(self, obj):
    #     asset_id = obj.id
    #     origin_status = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('origin_status')[0]['origin_status']
    #     if origin_status:
    #         svrchangename = get_dictdata('svrchangenid', origin_status)
    #         return svrchangename


class AssetPhysicalSerializer(serializers.ModelSerializer):
    svrchange = serializers.SerializerMethodField('get_svrchangenid')
    idcname = serializers.SerializerMethodField('get_idcnamenid')
    iopname = serializers.SerializerMethodField('get_iopnamenid')
    sfwname = serializers.SerializerMethodField('get_sfwnamenid')
    tdtname = serializers.SerializerMethodField('get_tdtnamenid')
    # user_name = serializers.SerializerMethodField('get_usersname')
    # gettime = serializers.SerializerMethodField('get_time')
    # gethandle = serializers.SerializerMethodField('get_handle')

    class Meta:
        model = Asset
        fields = ("id", "manageip", "switchip", "hostuser", "svrname", "svrip", "svrsn",
                  "eqsname", "svrfirstusetime", "svrstoptime", "svrofftime",
                  "strdescription", "laststatus",  "errcontent", "hostpassword",
                  'svrchangenid', 'sfwnamenid', 'iopnamenid', 'idcnamenid', 'tdtnamenid',
                  "tdtname", "idcname", "iopname", "sfwname", "svrchange",
                  # "user_name", 'gettime', 'gethandle',
                  )

    def get_svrchangenid(self, obj):
        svrchange_id = obj.svrchangenid
        try:
            svrchange_id = int(svrchange_id)
        except:
            svrchange_id = ''
        if svrchange_id:
            svrchangename = get_dictdata('svrchangenid', int(svrchange_id))
            return svrchangename

    def get_idcnamenid(self, obj):
        idcnamenid = obj.idcnamenid
        try:
            idcnamenid = int(idcnamenid)
        except:
            idcnamenid = ''
        if idcnamenid:
            idcname = get_dictdata('idcnamenid', int(idcnamenid))
            return idcname

    def get_iopnamenid(self, obj):
        iopnamenid = obj.iopnamenid
        try:
            iopnamenid = int(iopnamenid)
        except:
            iopnamenid = ''
        if iopnamenid:
            iopname = get_dictdata('iopnamenid', int(iopnamenid))
            return iopname

    def get_sfwnamenid(self, obj):
        sfwnamenid = obj.sfwnamenid
        try:
            sfwnamenid = int(sfwnamenid)
        except:
            sfwnamenid = ''
        if sfwnamenid:
            sfwname = get_dictdata('sfwnamenid', int(sfwnamenid))
            return sfwname

    def get_tdtnamenid(self, obj):
        tdtnameid = obj.tdtnamenid
        try:
            tdtnameid = int(tdtnameid)
        except:
            tdtnameid = ''
        if tdtnameid:
            tdtname = get_dictdata('tdtnamenid', int(tdtnameid))
            return tdtname

    # def get_usersname(self, obj):
    #     asset_id = obj.id
    #     user_name = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('user_name')
    #     if user_name:
    #         user_name = user_name[0]['user_name']
    #         return user_name
    #     return ''

    # def get_time(self, obj):
    #     asset_id = obj.id
    #     gettime = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('starttime')[0]['starttime']
    #     return gettime
    #
    # def get_handle(self, obj):
    #     asset_id = obj.id
    #     origin_status = TaskLog.objects.filter(serverid__id=asset_id).order_by("-starttime")[:1].values('origin_status')[0]['origin_status']
    #     if origin_status:
    #         svrchangename = get_dictdata('svrchangenid', origin_status)
    #         return svrchangename


