import os
import random
import base64
import time

def create_keys():
    list_salt = []
    for i in range(128):
        salt = os.urandom(16).hex()
        list_salt.append(salt)
    
    for i in range(random.randint(50, 128)):
        random.shuffle(list_salt)
    
    salt_str = "".join(list_salt)
    
    list_salt = list(salt_str)
    
    for i in range(random.randint(50, 128)):
        random.shuffle(list_salt)
    
    
    for i in range(random.randint(50, 128)):
        salt_str = "".join(list_salt)
        salt_list = [salt_str[i:i+32] for i in range(0, len(salt_str), 32)]
        random.shuffle(salt_list)
    
    
    while len(salt_list) >= 2:
        lenin = len(salt_list)
        if lenin == 2:
            break
        else:
            salt_list = random.sample(salt_list, lenin - 2)
    
    result = []
    for lists in salt_list:
        lists = lists.encode()
        lists = base64.b64encode(lists)
        result.append(lists)
    
    result_2 = []
    
    for lest in result:
        lest = lest.decode()
        result_2.append(lest)

    return result_2

def generate_random_key(size: int) -> str:
    main_list = []
    for i in range(128):
        salt = os.urandom(16).hex()
        main_list.append(salt)
    
    main_list = "".join(main_list)
    main_list = list(main_list)
    
    for i in range(random.randint(50, 128)):
        random.shuffle(main_list)
    
    for i in range(2):
        main_list = "".join(main_list)
        main_list = [main_list[i:i+size] for i in range(0, len(main_list), size)]
        random.shuffle(main_list)
        
    main_list = random.sample(main_list, 1)
    return main_list[0]