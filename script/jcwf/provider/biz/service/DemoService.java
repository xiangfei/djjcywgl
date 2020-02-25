package net.wan51.core.service.manager;

import net.wan51.common.dal.dataobject.UserDO;

import java.util.List;

/**
 * @author jim
 * @date 16/10/12
 */
public interface DemoService {

    List<UserDO> listUsers();

    UserDO getUser(Long id);

    void addUser(UserDO userDO);

    void updateUser(UserDO userDO);
}
