# coding=utf-8

broker_url = "redis://127.0.0.1"
# mysql
db_uri = "mysql+mysqlconnector://clambda:cccc@localhost/clambda"
result_backend = "db+" + db_uri
imports = "clambda.tasks"
database_table_names = {
    'task': 'taskmeta',
    'group': 'groupmeta',
}
