# coding=utf-8

import ldap3


class LdapService(object):
    """
    自定义Ldap驱动类
    """

    def __init__(self):
        self.ldap_uri = '10.0.28.10'
        self.ldap_port = 389
        self.ldap_base_dn = 'dc=gold-finance,dc=local'
        self.ldap_user = "ittest"
        self.ldap_passwd = "2345.com"

    def auth(self, username, password, is_unbind=True):
        """
        登录ldap
        """
        server = ldap3.Server(self.ldap_uri, self.ldap_port, get_info=ldap3.ALL)
        conn = None
        auto_bind = False
        try:
            if username:
                user = 'FINANCE\\%s' % username
                if password:
                    auto_bind = True
            conn = ldap3.Connection(server, user=user, password=password,
                                    auto_bind=auto_bind, authentication=ldap3.NTLM)

            if not auto_bind:
                succ = conn.bind()
            else:
                succ = True

            msg = conn.result
            if is_unbind:
                conn.unbind()
            return succ
        except Exception as e:
            if conn and is_unbind:
                conn.unbind()
            return False

    def ldap_search(self, groups, filter, attributes):
        """
        搜索ldap
        """
        server = ldap3.Server(self.ldap_uri, self.ldap_port, get_info=ldap3.ALL)
        conn = None
        auto_bind = False
        try:
            user = 'GOLD-FINANCE\\{0}'.format(self.ldap_user)
            if self.ldap_passwd:
                auto_bind = True
            conn = ldap3.Connection(server, user=user, password=self.ldap_passwd,
                                    auto_bind=auto_bind, authentication=ldap3.NTLM)
            if not auto_bind:
                conn.bind()

            conn.search(groups, filter, attributes=attributes)
            result = conn.entries
            conn.unbind()
            return True, result
        except Exception as e:
            if conn:
                conn.unbind()
            return False, e


myldap = LdapService()

