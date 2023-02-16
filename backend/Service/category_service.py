'''
- receive the required information from the controller
- perform the required operation
- return the calculated result back to the controller
'''

from DAO.db_object import PostgresDB
from DAO.cache_object import RedisCache
from Service.db_queries import *


class CategoryService:
    def __init__(self):
        self.dboperator = PostgresDB()
        self.cacheoperator = RedisCache()

    # insert into redis cache
    def insert_redis_products(self, catlvl1, catlvl2, products):
        redis_query = f"{catlvl1.strip()}-{catlvl2.strip()}"
        for product in products:
            self.cacheoperator.redis.rpush(redis_query, *product)
        self.cacheoperator.redis.expire(redis_query, 60)
        return 1

    # get the value from redis cache, if present
    def get_redis_products(self, catlvl1, catlvl2):
        redis_query = f"{catlvl1.strip()}-{catlvl2.strip()}"
        final = []
        if self.cacheoperator.redis.exists(redis_query):
            products = self.cacheoperator.redis.lrange(redis_query, 0, -1)
            for length in range(len(products)//5):
                product = products[length*5: length*5+5]
                for index in range(len(product)):
                    product[index] = product[index].decode()
                final.append(product)
            print("Got products from redis...")
            return final
        else:
            return 1

    # get the products belonging to a level 2 category value
    def get_category_lvl2_prods(self, category_lvl1, category_lvl2, order=None):
        status = self.get_redis_products(category_lvl1, category_lvl2)
        if status == 1:
            response = self.dboperator.operation(
                get_id_cat, (category_lvl1, ), res=1)
            result = response[0]
            result = self.dboperator.operation(
                get_pid_cat, (result[0], category_lvl2, ), res=1)
            product_IDs = []
            print("In category service", order)
            final = []
            for product in result:
                product_IDs.append(product[0])
            for id in product_IDs:
                response = self.dboperator.operation(
                    get_fields_prdinfo, (id,), res=1)
                result = response[0]
                final.append(result)
            insert_status = self.insert_redis_products(
                category_lvl1, category_lvl2, final)
            if insert_status == 1:
                print("Inserted into redis...")
            result_list = []
            if order != 'None':
                for i in final:
                    result_list.append([float(i[2]), i[1], i[0], i[3], i[4]])
                if order == 'Ascending':
                    result_list.sort()
                else:
                    result_list.sort(reverse=True)
                for i in result_list:
                    temp = i[0]
                    i[0] = i[2]
                    i[2] = temp
                    i[2] = str(i[2])
                return result_list
            return final
        else:
            result_list = []
            if order != 'None':
                for i in status:
                    result_list.append([float(i[2]), i[1], i[0], i[3], i[4]])
                if order == 'Ascending':
                    result_list.sort()
                else:
                    result_list.sort(reverse=True)
                for i in result_list:
                    temp = i[0]
                    i[0] = i[2]
                    i[2] = temp
                    i[2] = str(i[2])
                return result_list
            return status
