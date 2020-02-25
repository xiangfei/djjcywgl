#coding=utf-8


def user_id_split(user_id=None):
    if user_id:
        if isinstance(user_id, str):
            if '-' in user_id:
                user_id = int(user_id.split('-')[-1])
        return user_id
    return ''


def dict_key_instead(item, origin_names):
    for k, v in origin_names.items():
        item[k] = item.pop(v)
    return item


def project_userid_split(userids=None):
    if userids:
        ids_str = []
        if isinstance(userids, list):
            for id in userids:
                id = str(id).split('-')[1]
                if id.strip() == "":
                    continue
                else:
                    ids_str.append(id)
        return ','.join(ids_str)
    return []
