Examples
============

minimal db mapper utils for mysql

python orm utils for mysql

-----------
Install
-----------
pip install miniorm

-----------
model define
-----------
    dbargkws = {'user': 'test','password': 'test','host': 'localhost','port': "3306",'database': 'test','autocommit': False,'charset': 'utf8'}
    from miniorm import Model
    user_model = Model.make("User", dbargkws, "users")  #users is db tablename

-----------
select
-----------
    s = user_model.get_by_map({"pid": 123}, select_cols=["id", 'name'])

-----------
select one
-----------
    s = user_model.get_one_by_map({"id": u.id}, select_cols=["id", 'name'])

-----------
select like
-----------
    s = user_model.get_by_map({"id": u.id, "name$like":"john"}, select_cols=["id", 'name'])

-----------
select in
-----------
    s = user_model.get_by_map({"name$in":["john", "abc", "addd"]}, select_cols=["id", 'name'])

-----------
select search
-----------
    search all name with john* and nathen*
    s = user_model.get_by_map({"id": u.id, "name$match":"john nathen"}, select_cols=["id", 'name'])

-----------
select gt/gte/lt/lte
-----------
    s = user_model.get_by_map({"id$gt": 1, "name$like":"john"}, select_cols=["id", 'name'])

-----------
select order by
-----------
    s = user_model.get_by_map({"name$like":"john"}, order_by=["id desc", "name"])

-----------
pagination/
-----------
    s = user_model.get_by_map({"name$like":"john"}, start=0,limit=20, and_or="and")

-----------
count distinct
-----------
    usercont = user_model.count_by_map({"id$gt": 1, "name$like":"john"}, distinct="pid")

-----------
group by
-----------
    usercont = user_model.count_by_map({"id$gt": 1, "name$like":"john"}, group_by="name")

-----------
insert
-----------
    #by namedtuple
    User = namedtuple("User", ['id', 'name', 'pwd', 'email'])
    user = User(None, '1', '2', "10000003exeee@a.com")
    ins = user_model.insert(user)

    #by dict
    user = {'name':"ww", 'pwd':"pwd", 'email': "xxx"}
    ins = user_model.insert(user)

-----------
update
-----------
    #by namedtuple
    User = namedtuple("User", ['id', 'name', 'pwd', 'email'])
    user = User(1, '1', '2', "10000003exeee@a.com")
    updates, nops = user_model.update(user)
    updates, nops = user_model.update(user, where={"id":1})

    #by dict
    user = {'id':1, 'name':"ww", 'pwd':"pwd", 'email': "xxx"}
    updates, nops = user_model.update(user)
    updates, nops = user_model.update(user, where={"id":1})

-----------
delete
-----------
    uid = 1
    user_model.delete_by_id(uid)
    user_model.delete_by_map({"id":uid})
    user_model.delete_all()
    user_model.truncate()

-----------
columns
-----------
    user_model.columns()
