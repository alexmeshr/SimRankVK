import vk_api
from user_data import number, password, group_name
import numpy as np
import requests
import time

def download_images(image_folder, image_links):
    for i in range(image_links.size):
        response = requests.get(image_links[i])
        with open(image_folder+"/image_{}.png".format(i), "wb") as f:
            f.write(response.content)
        if i % 100 == 0:
            print("downloaded {} akk photos".format(i))


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def request_for_subs(number, password, group_name, group_members_count):
    vk_session = vk_api.VkApi(login=number,
                              password=password,
                              auth_handler=auth_handler,
                              captcha_handler=captcha_handler,
                              api_version='5.154',
                              app_id=2685278
                              )

    vk_session.auth()
    if group_members_count > 1000:
        remain= group_members_count
        user_ids = np.array(1)
        shift = 0
        while remain > 0:
            print("requesting {} members from {} with offset {}".format(min(remain, 1000), group_name, shift))
            with vk_api.VkRequestsPool(vk_session) as pool:
                ret = pool.method('groups.getMembers',{'group_id':group_name, 'count':min(remain, 1000), 'offset':shift})
            local_user_ids = np.array(ret.result['items'])
            if user_ids.size == 1:
                user_ids = local_user_ids.copy()
            else:
                user_ids = np.concatenate((user_ids, local_user_ids))
            remain -= 1000
            shift += 1000
            time.sleep(0.34)

    else:
        print("requesting {} members from {}".format(group_members_count, group_name))
        with vk_api.VkRequestsPool(vk_session) as pool:
            ret = pool.method('groups.getMembers',
                              {'group_id': group_name, 'count': group_members_count})
        user_ids = np.array(ret.result['items'])

    user_matrix = np.zeros((user_ids.size, user_ids.size))
    friends = {}
    with vk_api.VkRequestsPool(vk_session) as pool:
        for user_id in user_ids:
            friends[user_id] = pool.method('friends.get', {
                'user_id': str(user_id)
            })

    counter = 0
    private_counter = 0
    for f in friends:
        try:
            i_idx = np.where(user_ids==f)[0]
            for person_id in friends[f].result['items']:
                pos = np.where(user_ids==person_id)
                if len(pos)>0:
                    j_idx = pos
                    user_matrix[i_idx, j_idx] = 1
                    user_matrix[j_idx, i_idx] = 1
            counter+=1
            if counter % 100 == 0:
                print("handled {} subscribers info".format(counter))
        except Exception as e:
            #print('{} has problem {}'.format(counter, e))
            private_counter+=1
    print("handled {} subscribers, can't handle {} people(private akk)".format(user_matrix.shape[0], private_counter))
    return user_matrix, user_ids, vk_session


def photos_request(user_ids, vk_session, number, password, photo_quality='photo_max'):
    photo_links = np.chararray(user_ids.size, itemsize=250)
    # names = [""]*user_ids.size
    if vk_session is None:
        vk_session = vk_api.VkApi(login=number,
                                  password=password,
                                  auth_handler=auth_handler,
                                  captcha_handler=captcha_handler,
                                  api_version='5.154',
                                  app_id=2685278
                                  )

        vk_session.auth()
    result = [0] * user_ids.size
    with vk_api.VkRequestsPool(vk_session) as pool:
        for i in range(user_ids.size):
            result[i] = pool.method('users.get', {
                'user_id': str(user_ids[i]),
                'fields': photo_quality
            })
    for i in range(user_ids.size):
        photo_links[i] = result[i].result[0][photo_quality]
        # names[i] = result[i].result[0]['first_name']
    # with open('files/sarov_names.txt', 'w') as f:
    #    for name in names:
    #        f.write("%s\n" % name.encode('utf8'))
    return photo_links
