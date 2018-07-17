class DBRouter(object):

    def db_for_read(self, model, **hints):
        # print('slave')
        return 'slave'

    def db_for_write(self, model, **hints):
        # print('default')
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True
