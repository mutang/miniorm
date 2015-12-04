# coding: utf-8
# __author__ = 'inwn'

import logging
import unittest
from collections import namedtuple

from settings import dbargkws

logging.basicConfig(level=logging.DEBUG)


class DBTest(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)
        from miniorm.db import Model

        user_model = Model.make("User", dbargkws, "usertest")
        user_model.delete_all()

    def test_model_define(self):
        from miniorm.db import Model

        user_model = Model.make("User", dbargkws, "usertest")
        self.assertEqual(user_model.__name__, "usertest")
        self.assertEqual(user_model.tablename, "usertest")

        # get table name by default model name's lower case
        user_model = Model.make("UserTest", dbargkws)
        self.assertEqual(user_model.tablename, "usertest")

    def test_model_query_by_id(self):
        from miniorm.db import Model

        user_model = Model.make("User", dbargkws, "usertest")
        User = namedtuple("User", ['id', 'name', 'pwd', 'email'])
        ins = user_model.insert(User(None, '1', '2', "t"))

        u = ins[0]
        # make new model and do some query
        user_model = Model.make("User", dbargkws, "usertest")
        s = user_model.get_by_id(u['id'], select_cols=["id", 'name'])
        self.assertEqual(s["id"], u["id"])
        self.assertTrue(s["name"], u["name"])
        print s, u

        user_model.delete_by_id(u['id'])

    def test_model_query_by_map(self):
        from miniorm.db import Model

        # get table name by default model name's lower case
        user_model = Model.make("User", dbargkws, "usertest")
        User = namedtuple("User", ['id', 'name', 'pwd', 'email'])
        ins = user_model.insert(User(None, '1', '2', "t"))

        u = ins[0]
        # make new model and do some query
        user_model = Model.make("User", dbargkws, "usertest")
        s = user_model.get_by_map({"id": u['id']}, select_cols=["id", 'name'])

        self.assertEqual(s[0]["id"], u['id'])
        self.assertTrue("name" in s[0])
        self.assertEqual(s[0]["name"], '1')
        self.assertTrue("pwd" not in s[0])

        user_model.delete_by_id(u['id'])

    def test_model_update(self):
        from miniorm.db import Model

        # get table name by default model name's lower case
        user_model = Model.make("User", dbargkws, "usertest")
        User = namedtuple("User", ['id', 'name', 'pwd', 'email'])
        ins = user_model.insert(User(None, '1', '2', "t"))

        u = ins[0]
        # make new model and do some query
        user_model = Model.make("User", dbargkws, "usertest")
        u["pwd"] = "23444"
        ups, nos = user_model.update(u)
        print ups, nos
        u2 = ups[0]
        self.assertEqual(u2["id"], u['id'])
        self.assertEqual(u2["name"], u["name"])

        user_model.delete_by_id(u['id'])

    def test_model_update2(self):
        from miniorm.db import Model

        # get table name by default model name's lower case
        user_model = Model.make("User", dbargkws, "usertest")
        User = namedtuple("User", ['id', 'name', 'pwd', 'email'])
        ins = user_model.insert(User(None, '1', '2', "t"))

        u = ins[0]
        # make new model and do some query
        user_model = Model.make("User", dbargkws, "usertest")
        u["pwd"] = "23444"
        print ">>>>>>>>>>>>>>", ins[0]
        self.assertEqual(ins[0]['id'] is not None, True)
        ups, nos = user_model.update(u, where={"id": ins[0]["id"]})
        print ups, nos
        u2 = ups[0]
        self.assertEqual(u2["id"], u['id'])
        self.assertEqual(u2["name"], u["name"])
        user_model.delete_by_id(u['id'])

    def test_save(self):

        from miniorm.db import Model

        user_model = Model.make("User", dbargkws, "usertest")
        User = namedtuple("User", ['id', 'name', 'pwd', 'email'])
        us = [User(*[None, str(i), str(i), str(i)]) for i in range(510, 520)]
        try:
            ins = user_model.insert(us)
            print "inserted: ", ins
            print "updated: ", user_model.update({"name": "nnn"}, where={"id": ins[0]["id"]})
            print user_model.get_conn, id(user_model.get_conn)
            user_model = Model.make("User", dbargkws, "usertest")
            for u in us:
                user_model.get_by_map({"email": u.email})
                user_model.delete_by_id(user_model.get_by_map({"email": u.email})[0]['id'])
        finally:
            [user_model.delete_by_map({"email": str(i)}) for i in range(510, 520)]

    def test_save_in_threads(self):
        from miniorm.db import Model
        user_model = Model.make("User", dbargkws, "usertest")
        User = namedtuple("User", ['id', 'name', 'pwd', 'email'])

        def run(user_model):
            us = [User(*[None, str(i), str(i), str(i)]) for i in range(5710, 5720)]
            try:
                ins = user_model.insert(us)
                print "inserted: ", ins
                print "updated: ", user_model.update({"name": "nnn"}, where={"id": ins[0]["id"]})
                print user_model.get_conn, id(user_model.get_conn)
                user_model = Model.make("User", dbargkws, "usertest")
                for u in us:
                    user_model.get_by_map({"email": u.email})
                    user_model.delete_by_id(user_model.get_by_map({"email": u.email})[0]['id'])
            finally:
                [user_model.delete_by_map({"email": str(i)}) for i in range(510, 520)]
                user_model.close()

        for i in range(100):
            from threading import Thread
            t = Thread(target=run, args=[user_model])
            t.setDaemon(True)
            t.start()

        import time
        time.sleep(50)
        print user_model.destory()


if __name__ == '__main__':
    unittest.main()
