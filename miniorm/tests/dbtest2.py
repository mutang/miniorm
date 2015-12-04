# coding: utf-8
# __author__ = 'inwn'

import logging

from settings import dbargkws

logging.basicConfig(level=logging.DEBUG)


def main():
    from miniorm.db import Model
    # pool = pool = MySQLConnectionPool(pool_name="miniorm_pooling", pool_size=5, pool_reset_session=True, **dbargkws)

    user_model = Model.make("User", dbargkws, "usertest")

    print "delete", user_model.delete_by_map({"name$lt": "111"})
    for i in range(200):
        try:
            user_model.insert({'name': str(i), 'pwd': str(i), 'email': str(i)})
        except:
            import traceback
            print traceback.format_exc()
    print user_model.exists({'name': '100', "pwd": "100"})
    print "in trans", user_model.get_conn().in_transaction


if __name__ == '__main__':
    main()
