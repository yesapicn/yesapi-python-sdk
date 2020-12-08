#!/usr/bin/python
#coding=utf-8
#
#
# @author puluter 20201206
import time
import requests
import hashlib
import json

API_URL     = 'http://hn216.api.yesapi.cn/'
APP_KEY     = ''
APP_SECRET  = ''

# 生成签名
def Signature(params, key=None, secret=None):
    key = key or APP_KEY
    secret = secret or APP_SECRET
    params.pop('app_secret', None)
    params['app_key'] = key
    md5_ctx = hashlib.md5()
    md5_ctx.update(str(''.join([params[value] for value in sorted([key for key in params])]) + secret).encode('utf-8'))
    return md5_ctx.hexdigest().upper()
    

# 请求小白接口
def yes(params):
    global API_URL
    print(1)
    print(time.asctime(time.localtime(time.time())))
    params['sign'] = Signature(params)
    print(time.asctime(time.localtime(time.time())))
    print('reqstuck')
    resp = requests.get(API_URL, params)
    print(time.asctime(time.localtime(time.time())))
    return resp.json()


class user:
    def login(self, username, password):
        """
        登录
        """
        params = {'s': "App.User.Login", 'username': username, 'password':hashlib.md5(password.encode(encoding='utf-8')).hexdigest()}
        return yes(params)
    def reg(self, username, password, extInfo=""):
        params = {'s': "App.User.Register", 'username': username, 'password':hashlib.md5(password.encode(encoding='utf-8')).hexdigest(), 'ext_info': extInfo}
        return yes(params)
    def log_out(self, uuid, token):
        params = {'s': "App.User.Logout", 'uuid': uuid, 'token': token}
        return yes(params)
    def get_self_info(self, uuid, token):
        params = {'s': "App.User.Profile", 'uuid': uuid, 'token': token}
        return yes(params)

class table:
    def readFree(self, model_name,
    uuid  =None, token=None, model_uuid=None, 
    select=None, logic=None, where=None,
    order =None, page =None, per_page=None
    ):
        """
        自由查询接口，需要注意where默认为[["id","=","1"]],需要修改一下才能让它查询一整页
        """
        params = {'s': "App.Table.FreeQuery", 'model_name': model_name}
        if uuid: params['uuid'] = uuid
        if token: params['token'] = token
        if model_uuid: params['model_uuid'] = model_uuid
        if select: params['select'] = select
        if logic: params['logic'] = logic
        if where: params['where'] = where
        if order: params['order'] = order
        if page: params['page'] = str(page)
        if per_page: params['per_page'] = str(per_page)
        return yes(params)

    def readFreeJoinQuery(self, model_name, join_model_name,
        join_select, on,
        uuid  =None, token=None, model_uuid=None,
        select=None, logic=None, where=None,
        order =None, page =None, per_page=None
    ):
        """
        联合查询接口。
        on: 	用于指定模型关联关系的ON部分，JSON格式，key-value对，key为主表字段名，value为关联表字段名，支持多组。例如：model_name.name = join_model_name.name AND model_name.age = join_model_name.other_age，则接口传递参数为：on={"name":"name","age":"other_age"}
        例子：{"com_id":"id"}
        """
        params = {'s': "App.Table.FreeLeftJoinQuery", 'model_name': model_name,
                  'join_model_name':join_model_name, 'join_select':join_select,
                  'on':json.dumps(on)}
        if uuid: params['uuid'] = uuid
        if token: params['token'] = token
        if model_uuid: params['model_uuid'] = model_uuid
        if select: params['select'] = select
        if logic: params['logic'] = logic
        if where: params['where'] = where
        if order: params['order'] = order
        if page: params['page'] = str(page)
        if per_page: params['per_page'] = str(per_page)
        print(params)
        return yes(params)

    def readFreeFindOne(self, model_name, 
    uuid  =None, token=None, model_uuid=None, 
    select=None, logic=None, where=None
    ):
        """
        通过where来精确获取一个值
        """
        params = {'s': "App.Table.FreeFindOne", 'model_name': model_name}
        if uuid: params['uuid'] = uuid
        if token: params['token'] = token
        if model_uuid: params['model_uuid'] = model_uuid
        if select: params['fields'] = select
        if logic: params['logic'] = logic
        if where: params['where'] = where
        return yes(params)

    def readViaID(self, model_name, id,
    uuid  =None, token=None, model_uuid=None
    ):
        """
        通过id来精确读取一个值
        """
        params = {'s': "App.Table.Get", 'model_name': model_name, 'id': str(id)}
        if uuid: params['uuid'] = uuid
        if token: params['token'] = token
        if model_uuid: params['model_uuid'] = model_uuid
        return yes(params)
    
    def updateViaID(self, model_name, id,
    data,
    uuid =None, token=None, model_uuid=None
    ):
        """
        通过id来精确更新一个值
        """
        params = {'s': "App.Table.Update", 'model_name': model_name, 'id': str(id),
        'data':json.dumps(data)}
        if uuid: params['uuid'] = uuid
        if token: params['token'] = token
        if model_uuid: params['model_uuid'] = model_uuid
        return yes(params)
    
    def updateFree(self, model_name,
    data,
    uuid =None, token=None, model_uuid=None, 
    logic=None, where=None,
    ):
        """
        通过where来精确更新数据
        """
        params = {'s': "App.Table.FreeUpdate", 'model_name': model_name,
        'data': json.dumps(data)
        }
        if uuid: params['uuid'] = uuid
        if token: params['token'] = token
        if model_uuid: params['model_uuid'] = model_uuid
        if logic: params['logic'] = logic
        if where: params['where'] = where
        return yes(params)
    
    def updateChangeNumber(self, model_name, id,
    change_field, change_value,
    uuid =None, token=None, model_uuid=None, 
    ):
        """
        通过id去修改对应field的数值
        """
        params = {'s': "App.Table.ChangeNumber", 'model_name': model_name,
        'id':str(id), 'change_field':change_field, 'change_value': change_value
        }
        if uuid: params['uuid'] = uuid
        if token: params['token'] = token
        if model_uuid: params['model_uuid'] = model_uuid
        return yes(params)
    
    
    def create(self, model_name, data,
    uuid =None, token=None, model_uuid=None
    ):
        """
        创建一个值
        """
        params = {'s': "App.Table.Create", 'model_name': model_name,
        'data':json.dumps(data)}
        if uuid: params['uuid'] = uuid
        if token: params['token'] = token
        if model_uuid: params['model_uuid'] = model_uuid
        return yes(params)
    
    def getMax(self, model_name, field, where='[["id","<>","-1"]]',
    uuid =None, token=None, model_uuid=None
    ):
        """
        获得最大值
        """
        params = {'s': "App.Table.FreeMax", 'model_name': model_name,
        'field': field}
        if uuid: params['uuid'] = uuid
        if token: params['token'] = token
        if model_uuid: params['model_uuid'] = model_uuid
        if where: params['where'] = where
        return yes(params)



class other:
    def getUniqueId(self):
        """
        获取一个uniqueId
        """
        params = {'s': "App.Common_UniqueId.GetUniqueId"}
        return yes(params)


class yesapi_class:
    user = user()
    table = table()
    other = other()

yesapi = yesapi_class()

# print(y1.table.updateViaID("bgmList", 53, {'music_name': 'glassware '}))
