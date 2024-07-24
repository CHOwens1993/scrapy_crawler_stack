"""_summary_

Raises:
    DropItem: _description_

Returns:
    _type_: _description_
"""
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo

#from scrapy.utils.project import get_project_settings
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem



class MongoDBPipeline(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(

            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
    def process_item(self, item, spider):
        """_summary_

        Args:
            item (_type_): _description_
            spider (_type_): _description_

        Raises:
            DropItem: _description_

        Returns:
            _type_: _description_
        """
        for data in item:
            if not data:
                raise DropItem(f"Missing {data}!")
        self.collection.update_one({'url' : item['url']},{"$set": dict(item)}, upsert = True)
        logging.log(logging.DEBUG,"Question added to MongoDB database!")
        return item
