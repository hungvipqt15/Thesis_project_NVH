import shutil
from pathlib import Path
import os
import subprocess


FILE_NAME = Path() / 'transforms.json'

# UPLOAD_DIR = Path() / 'uploads/images'
# # shutil.rmtree(UPLOAD_DIR)
# # os.mkdir(UPLOAD_DIR)

# isExist = os.path.exists(UPLOAD_DIR)

# if isExist==True:
#     shutil.rmtree(UPLOAD_DIR)

# os.mkdir(UPLOAD_DIR)



# # python colmap2nerf.py --images uploads\images --run_colmap --aabb_scale 8 --out out
# # python C:\Users\Admin\Desktop\Project\scripts\colmap2nerf.py --images C:\Users\Admin\Desktop\Project\uploads\images --run_colmap --aabb_scale 8 


# import subprocess

# # Đường dẫn đến script Python
# script_path = r'C:\Users\Admin\Desktop\Project\scripts\colmap2nerf.py'

# # Các tham số truyền vào script
# images_dir = r'C:\Users\Admin\Desktop\Project\uploads\images'
# aabb_scale = '8'  # Đây là đoạn --aabb_scale 8 trong câu lệnh cmd

# # Xây dựng danh sách các đối số dòng lệnh
# command = [
#     'python',            # Lệnh để chạy script Python
#     script_path,         # Đường dẫn đến script colmap2nerf.py
#     '--images',          # Tham số --images
#     images_dir,          # Đường dẫn đến thư mục ảnh
#     '--run_colmap',      # Tham số --run_colmap
#     '--aabb_scale',      # Tham số --aabb_scale
#     aabb_scale           # Giá trị cho --aabb_scale (ở đây là '8')
# ]

# # Thực thi câu lệnh sử dụng subprocess
# try:
#     subprocess.run(command, check=True)
# except subprocess.CalledProcessError as e:
#     print(f"Error: {e}")
# else:
#     print("Command executed successfully!")


# import os
# import shutil
# from pathlib import Path
# colmap_sparse = Path() / 'colmap_sparse'
# colmap_sparse = Path() / 'colmap_sparse'
# colmap_text = Path() / 'colmap_text'
# if os.path.exists(colmap_sparse):
#     shutil.rmtree(colmap_sparse)

########################################################################################
COLMAP_TEXT = r'C:\Users\Admin\Desktop\Project\colmap_text'
command = 'colmap model_analyzer --path '+ COLMAP_TEXT



output =subprocess.run(command, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# if 'Python' in output:
#     print(True)
# else:
#     print(None)


# print(output.stderr)
# info = output.stderr
# if 'Cameras' in info:
#     print(True)

# import re
# cameras = re.search(r'Mean reprojection error:\s+([0-9.]+px)', info)

# if cameras:
#     print(f'Cameras number: {cameras.group(1)}')


