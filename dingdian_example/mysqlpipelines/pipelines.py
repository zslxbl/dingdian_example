from .sql import Sql
from dingdian_example.items import DingdianExampleItem

class DingdianPipelines(object):
    def process_item(self, item, spider):
        # defaultToThread(self, process_item, item, spider)
        if isinstance(item, DingdianExampleItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret[0] == 1:
                print (u'{}已经存在！'.format(str(name_id)))
                pass
            else:
                xs_name = item['name']
                xs_author = item['author']
                category = item['category']
                Sql.insert_dd_name(xs_name, xs_author, category, name_id)
                print(u'开始存小说标题！')


