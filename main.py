from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
import os
import shutil
import subprocess
import re
import sqlite3


templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path() / 'uploads/images'
FILE_JSON = Path() / 'transforms.json'
SPARSE_DIR = Path() / 'colmap_sparse'
TEXT_DIR = Path() / 'colmap_text'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/',response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/uploadfile')
async def create_upload_file(file_uploads: list[UploadFile] ):

    ## check if images folder is exist or not. If exist, delete folder. If no, create
    # isExist = os.path.exists(UPLOAD_DIR)
    # if isExist==True:
    #     shutil.rmtree(UPLOAD_DIR)
    # os.mkdir(UPLOAD_DIR)

    ## Save upload files to folder images
    for file_upload in file_uploads:
        data = await file_upload.read()
        save_to = UPLOAD_DIR / file_upload.filename
        with open(save_to, 'wb') as f:
            f.write(data)

    return {"filenames": [f.filename for f in file_uploads]}

@app.get('/colmap_execute/', response_class=HTMLResponse)
def colmap_execute(request: Request):
    # # colmap_sparse, colmap_text, colmap.db and transforms.json need to be removed if exist
    # colmap_sparse = Path() / 'colmap_sparse'
    # colmap_text = Path() / 'colmap_text'
    # if os.path.exists(colmap_sparse):
    #     shutil.rmtree(colmap_sparse)
    # if os.path.exists(colmap_text):
    #     shutil.rmtree(colmap_text)
    # if os.path.exists('transforms.json'):
    #     os.remove('transforms.json')
    # if os.path.exists('colmap.db'):
    #     os.remove('colmap.db')





    # Đường dẫn đến script Python
    script_path = r'C:\Users\Admin\Desktop\Project\scripts\colmap2nerf.py'

    # Các tham số truyền vào script
    images_dir = r'C:\Users\Admin\Desktop\Project\uploads\images'
    aabb_scale = '16'  # Đây là đoạn --aabb_scale 16 trong câu lệnh cmd

    # Xây dựng danh sách các đối số dòng lệnh
    command = [
        'python',            # Lệnh để chạy script Python
        script_path,         # Đường dẫn đến script colmap2nerf.py
        '--images',          # Tham số --images
        images_dir,          # Đường dẫn đến thư mục ảnh
        '--run_colmap',      # Tham số --run_colmap
        '--aabb_scale',      # Tham số --aabb_scale
        aabb_scale           # Giá trị cho --aabb_scale (ở đây là '16')
    ]

    # Thực thi câu lệnh sử dụng subprocess
    try:
        subprocess.run(command, check=True)
        
    except subprocess.CalledProcessError as e:
        output = f"Error: {e}"
    else:
        output = "Command executed successfully!"

    if 'Error' in output:
        return templates.TemplateResponse("error_announcement.html", {"request": request})


    COLMAP_TEXT = r'C:\Users\Admin\Desktop\Project\colmap_text'
    command_analyzer = 'colmap model_analyzer --path '+ COLMAP_TEXT
    output_analyzer =subprocess.run(command_analyzer, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = output_analyzer.stderr
    result_analysis = colmap_analyzer(info)
    num_img = result_analysis['Images'].group(1)
    num_registered = result_analysis['Registered images'].group(1)
    num_sparse_points = result_analysis['Points'].group(1)
    num_obersvation = result_analysis['Observations'].group(1)
    reprojection_error = result_analysis['Mean reprojection error'].group(1)


    database = Path()/ 'colmap.db'
    matching_feature_result = matching_result(database)
    num_inlier_pairs = matching_feature_result['num_inlier_pairs']
    num_inlier_matches = matching_feature_result['num_inlier_matches']


    return templates.TemplateResponse("sparse_reconstruction.html", {"request": request, "output": output, "num_img": num_img,
                                                                     "num_registered": num_registered, "num_sparse_points": num_sparse_points,
                                                                     "num_obersvation": num_obersvation, "reprojection_error": reprojection_error,
                                                                     "num_inlier_pairs": num_inlier_pairs, "num_inlier_matches": num_inlier_matches})

@app.get('/download_file_json')
async def download_json(request: Request):
    if os.path.exists(FILE_JSON):
        return FileResponse(path=FILE_JSON, media_type='application/octet-stream', filename='transforms.json')
    else:
        return templates.TemplateResponse("error_announcement.html", {"request": request})

@app.get('/download_file_json/return',response_class=HTMLResponse)
async def reset_folder(request: Request):
    remove()
    return templates.TemplateResponse("index.html", {"request": request})



@app.get('/reset_state/',response_class=HTMLResponse)
async def reset_folder(request: Request):
    remove()
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/error/',response_class=HTMLResponse)
async def return_home(request: Request):
    remove()
    
    return templates.TemplateResponse("index.html", {"request": request})




def remove():
    isExist = os.path.exists(UPLOAD_DIR)
    if isExist==True:
        shutil.rmtree(UPLOAD_DIR)
    os.mkdir(UPLOAD_DIR)

    if os.path.exists(FILE_JSON):
        os.remove(FILE_JSON)
    if os.path.exists(SPARSE_DIR):
        shutil.rmtree(SPARSE_DIR)
    if os.path.exists(TEXT_DIR):
        shutil.rmtree(TEXT_DIR)
    return


def colmap_analyzer(info: str):
    num_cameras = re.search(r'Cameras:\s+([0-9.]+)', info)
    num_images = re.search(r'Images:\s+([0-9.]+)', info)
    num_registered = re.search(r'Registered images:\s+([0-9.]+)', info)
    num_points = re.search(r'Points:\s+([0-9.]+)', info)
    num_obser = re.search(r'Observations:\s+([0-9.]+)', info)
    num_mean_track_length = re.search(r'Mean track length:\s+([0-9.]+)', info)
    num_observations_per_image = re.search(r'Mean obsercations per image:\s+([0-9.]+)', info)
    num_reprojection_error = re.search(r'Mean reprojection error:\s+([0-9.]+px)', info)

    colmap_result_analysis = {'Cameras': num_cameras, 'Images': num_images, 'Registered images': num_registered, 
                              'Points': num_points, 'Observations': num_obser, 'Mean track length': num_mean_track_length, 
                              'Mean observations per image': num_observations_per_image, 'Mean reprojection error': num_reprojection_error}
    
    return colmap_result_analysis


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