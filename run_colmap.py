import os
import shutil
import subprocess as sp
from argparse import ArgumentParser

parser = ArgumentParser("Colmap converter")
parser.add_argument("--source_path", "-s", required=True, type=str)
args = parser.parse_args()

def feature_extraction(project_path):
    result = sp.run(['colmap', 'feature_extractor', \
                    '--database', os.path.join(project_path, 'database.db'), \
                    '--image_path', os.path.join(project_path, 'images')], capture_output=True, text=True)
    return result

def exhaustive_matching(project_path):
    result = sp.run(['colmap', 'exhaustive_matcher', \
                    '--database', os.path.join(project_path, 'database.db'), \
                    '--SiftMatching.gpu_index=0,0'], capture_output=True, text=True)
    return result

def mapping(project_path):
    result = sp.run(['colmap', 'mapper', \
                    '--database', os.path.join(project_path, 'database.db'), \
                    '--image_path', os.path.join(project_path, 'images'), \
                    '--output_path', os.path.join(project_path, 'sparse')], capture_output=True, text=True)
    return result
    
def image_undistortion(project_path):
    result = sp.run(['colmap', 'image_undistorter', \
                    '--image_path', os.path.join(project_path, 'images'), \
                    '--input_path', os.path.join(project_path, 'sparse/0'), \
                    '--output_path', os.path.join(project_path, 'dense/0'), \
                    '--output_type', 'COLMAP', \
                    '--max_image_size', '1600'], capture_output=True, text=True)
    return result
    
def patch_matching(project_path):
    result = sp.run(['colmap', 'patch_match_stereo', \
                    '--workspace_path', os.path.join(project_path, 'dense/0'), \
                    '--PatchMatchStereo.cache_size', '8', \
                    '--PatchMatchStereo.max_image_size', '1000'], capture_output=True, text=True)
    return result
    
def stereo_fusion(project_path):
    result = sp.run(['colmap', 'stereo_fusion', \
                    '--workspace_path', os.path.join(project_path, 'dense/0'), \
                    '--output_path', os.path.join(project_path, 'dense/0/fused.ply'), \
                    '--StereoFusion.cache_size', '8', \
                    '--StereoFusion.max_image_size', '1000'], capture_output=True, text=True)
    return result

if __name__=="__main__":

    # project_path = os.path.join('./projects/', args.project_name)
    project_path = source_path
    print(project_path)

    if not os.path.exists(os.path.join(project_path, 'sparse')):
        os.makedirs(os.path.join(project_path, 'sparse'))

    if not os.path.exists(os.path.join(project_path, 'dense')):
        os.makedirs(os.path.join(project_path, 'dense'))

    feature_extraction(project_path)
    print("Finished extracting features")

    exhaustive_matching(project_path)
    print("Finished exhaustive matching")

    mapping(project_path)
    print("Finished mapping")

    image_undistortion(project_path)
    print("Finished undistorting images")

    print("Finished preparing data")