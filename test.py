# import shutil
# from pathlib import Path
# import os
# import subprocess


# FILE_NAME = Path() / 'transforms.json'

# # UPLOAD_DIR = Path() / 'uploads/images'
# # # shutil.rmtree(UPLOAD_DIR)
# # # os.mkdir(UPLOAD_DIR)

# # isExist = os.path.exists(UPLOAD_DIR)

# # if isExist==True:
# #     shutil.rmtree(UPLOAD_DIR)

# # os.mkdir(UPLOAD_DIR)



# # # python colmap2nerf.py --images uploads\images --run_colmap --aabb_scale 8 --out out
# # # python C:\Users\Admin\Desktop\Project\scripts\colmap2nerf.py --images C:\Users\Admin\Desktop\Project\uploads\images --run_colmap --aabb_scale 8 


# # import subprocess

# # # Đường dẫn đến script Python
# # script_path = r'C:\Users\Admin\Desktop\Project\scripts\colmap2nerf.py'

# # # Các tham số truyền vào script
# # images_dir = r'C:\Users\Admin\Desktop\Project\uploads\images'
# # aabb_scale = '8'  # Đây là đoạn --aabb_scale 8 trong câu lệnh cmd

# # # Xây dựng danh sách các đối số dòng lệnh
# # command = [
# #     'python',            # Lệnh để chạy script Python
# #     script_path,         # Đường dẫn đến script colmap2nerf.py
# #     '--images',          # Tham số --images
# #     images_dir,          # Đường dẫn đến thư mục ảnh
# #     '--run_colmap',      # Tham số --run_colmap
# #     '--aabb_scale',      # Tham số --aabb_scale
# #     aabb_scale           # Giá trị cho --aabb_scale (ở đây là '8')
# # ]

# # # Thực thi câu lệnh sử dụng subprocess
# # try:
# #     subprocess.run(command, check=True)
# # except subprocess.CalledProcessError as e:
# #     print(f"Error: {e}")
# # else:
# #     print("Command executed successfully!")


# # import os
# # import shutil
# # from pathlib import Path
# # colmap_sparse = Path() / 'colmap_sparse'
# # colmap_sparse = Path() / 'colmap_sparse'
# # colmap_text = Path() / 'colmap_text'
# # if os.path.exists(colmap_sparse):
# #     shutil.rmtree(colmap_sparse)

# ########################################################################################
# COLMAP_TEXT = r'C:\Users\Admin\Desktop\Project\colmap_text'
# command = 'colmap model_analyzer --path '+ COLMAP_TEXT



# output =subprocess.run(command, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# # if 'Python' in output:
# #     print(True)
# # else:
# #     print(None)


# # print(output.stderr)
# # info = output.stderr
# # if 'Cameras' in info:
# #     print(True)

# # import re
# # cameras = re.search(r'Mean reprojection error:\s+([0-9.]+px)', info)

# # if cameras:
# #     print(f'Cameras number: {cameras.group(1)}')

####################################################################################################
# import json
# import numpy as np
# import os

# with open("transforms.json","r") as json_file:
#     data = json.load(json_file)

# frames = data['frames']

# def change_path(frames):
#     for pose in frames:
#         path = pose['file_path']
#         file_name = os.path.basename(path)
#         change_name = './images/'+file_name
#         pose['file_path'] = change_name
#     return frames
# frames=change_path(frames)
# # Update again the frames of file json
# data['frames'] = frames

# with open("transforms.json","w") as json_file:
#     json.dump(data, json_file)
###################################################################################
from pathlib import Path
import sqlite3
import os

def matching_result(dataset_path):
    connection = sqlite3.connect(os.path.join(dataset_path))
    cursor = connection.cursor()

    cursor.execute("SELECT count(*) FROM images;")
    num_images = next(cursor)[0]

    cursor.execute("SELECT count(*) FROM two_view_geometries WHERE rows > 0;")
    num_inlier_pairs = next(cursor)[0]

    cursor.execute("SELECT sum(rows) FROM two_view_geometries WHERE rows > 0;")
    num_inlier_matches = next(cursor)[0]

    cursor.close()
    connection.close()

    return dict(num_images=num_images,
                num_inlier_pairs=num_inlier_pairs,
                num_inlier_matches=num_inlier_matches)

database = 'C:/Users/Admin/Desktop/instant-ngp/data/video/colmap_database_folder/1.db'

print(matching_result(database))


########################################################
# Importing Required Modules 
# import os
# import cv2
# from rembg import remove
# from PIL import Image
# from pathlib import Path

# def remove_background(input_folder, output_folder):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     for filename in os.listdir(input_folder):
#         if filename.endswith(".jpg") or filename.endswith(".png"):  # Add more extensions if needed

#             input_path = os.path.join(input_folder, filename)
#             output_path = os.path.join(output_folder, filename)
#             print(output_path)
#             # Read the image
#             img = Image.open(input_path)

#             # Remove background
#             img_no_bg = remove(img)

#             # Save the output image
#             img_no_bg.save(output_path)


# UPLOAD_DIR = Path() / 'uploads/images'
# RM_BACKGROUND_DIR = Path() / 'remove_background/images'
# input_folder = UPLOAD_DIR
# output_folder = RM_BACKGROUND_DIR

# remove_background(input_folder, output_folder)
