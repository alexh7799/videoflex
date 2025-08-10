import os
import subprocess

def convert480p(source):
    base_name = os.path.splitext(os.path.basename(source))[0]
    target_dir = os.path.join(os.path.dirname(source), '..', 'hls', '480p', base_name)
    target_dir = os.path.abspath(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    m3u8_file = os.path.join(target_dir, 'index.m3u8')
    cmd = (
        f'ffmpeg -i "{source}" -profile:v baseline -level 3.0 -s 854x480 -start_number 0 '
        f'-hls_time 10 -hls_list_size 0 -f hls "{m3u8_file}"'
    )
    subprocess.run(cmd, shell=True, capture_output=True)

def convert720p(source):
    base_name = os.path.splitext(os.path.basename(source))[0]
    target_dir = os.path.join(os.path.dirname(source), '..', 'hls', '720p', base_name)
    target_dir = os.path.abspath(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    m3u8_file = os.path.join(target_dir, 'index.m3u8')
    cmd = (
        f'ffmpeg -i "{source}" -profile:v baseline -level 3.0 -s 1280x720 -start_number 0 '
        f'-hls_time 10 -hls_list_size 0 -f hls "{m3u8_file}"'
    )
    subprocess.run(cmd, shell=True, capture_output=True)

def convert1080p(source):
    base_name = os.path.splitext(os.path.basename(source))[0]
    target_dir = os.path.join(os.path.dirname(source), '..', 'hls', '1080p', base_name)
    target_dir = os.path.abspath(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    m3u8_file = os.path.join(target_dir, 'index.m3u8')
    cmd = (
        f'ffmpeg -i "{source}" -profile:v baseline -level 3.0 -s 1920x1080 -start_number 0 '
        f'-hls_time 10 -hls_list_size 0 -f hls "{m3u8_file}"'
    )
    subprocess.run(cmd, shell=True, capture_output=True)