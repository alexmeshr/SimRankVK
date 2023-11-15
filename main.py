from vk_group_request import request_for_subs, photos_request, download_images
from prepare_data import clear_data
from draw_graph import print_graph
import os
import numpy as np
import matplotlib.pyplot as plt

from user_data import number, password, group_name

start_matrix_file = "files/{}_matrix.npy".format(group_name)
start_ids_file = "files/{}_ids.npy".format(group_name)
prepared_matrix_file = "files/{}_matrix_prepared.npy".format(group_name)
prepared_ids_file = "files/{}_ids_prepared.npy".format(group_name)
photo_links_file = "files/{}_photo_links.npy".format(group_name)
images_folder = "images_{}".format(group_name)

DPI = 2000
image_scale_factor = 0.01
spring_k = 0.3
photo_quality = 'photo_max'# 'photo_50' or 'photo_100', 'photo_200', 'photo_max'
group_members_count = 2000

if not (os.path.isfile(start_matrix_file) and os.path.isfile(start_ids_file)):
    user_matrix, user_ids, vk_session = request_for_subs(number, password, group_name, group_members_count)
    np.save(start_matrix_file, user_matrix)
    np.save(start_ids_file, user_ids)
else:
    user_matrix = np.load(start_matrix_file)
    user_ids = np.load(start_ids_file)
    vk_session = None

if not (os.path.isfile(prepared_matrix_file) and os.path.isfile(prepared_ids_file)):
    user_matrix, user_ids = clear_data(user_matrix, user_ids)
    np.save(prepared_matrix_file, user_matrix)
    np.save(prepared_ids_file, user_ids)
else:
    user_matrix = np.load(prepared_matrix_file)
    user_ids = np.load(prepared_ids_file)


if not os.path.isfile(photo_links_file):
    photo_links = photos_request(user_ids, vk_session, number, password, photo_quality=photo_quality)
    np.save(photo_links_file, photo_links)
else:
    photo_links = np.load(photo_links_file)


if not os.path.exists(images_folder):
    os.makedirs(images_folder)
    download_images(images_folder, photo_links)
#elif len(next(os.walk(images_folder)[2])) != photo_links.size:
#    download_images(images_folder, photo_links)


print_graph(user_matrix, photo_links, images_folder, spring_k=spring_k, image_scale_factor=image_scale_factor)
plt.savefig('{}_{}dpi.png'.format(group_name, DPI), dpi=DPI, bbox_inches='tight', pad_inches=0)
plt.show()



