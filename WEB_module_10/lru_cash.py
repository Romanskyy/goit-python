import redis

red = redis.Redis(
    host='localhost',
    port=6379,
    db=2
)


def lru_cash(red_conn, max_depth=6):

    def wrapper(func):

        def inner(*args, **kwargs):

            print('LRU_CASH ' * 9)
            print('*' * 80)

            name, _ = args[0]

            if name.encode('utf-8') not in red_conn.lrange('hash_list', 0, max_depth - 1):
                print('-' * 26,  'DATA TAKEN NOT FROM REDIS ', '-' * 26)

                result = func(*args, **kwargs)

                red_conn.lpush('hash_list', name)

                red_list_len = len(red_conn.lrange('hash_list', 0, -1))

                if red_list_len > max_depth:
                    name_to_del = red_conn.rpop('hash_list')

                    red_conn.ltrim('hash_list', 0, max_depth - 1)
                    red_conn.hdel('hash_dict', name_to_del)

                red_conn.hset('hash_dict', name, result)

            else:
                print('-' * 28,  'DATA TAKEN FROM REDIS ', '-' * 28)
                red_conn.lrem('hash_list', name)
                red_conn.lpush('hash_list', name)
                result = red_conn.hget('hash_dict', name).decode('utf-8')

            return result

        return inner
    return wrapper
