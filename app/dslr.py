from app import DEFAULT_IMAGE_PATH
import os
import subprocess
# import time

IMAGE_FOLDER = "/store_00020001/DCIM/100CANON"


def init():
    global IMAGE_FOLDER
    detect_proc = subprocess.Popen(['gphoto2', '--auto-detect', '--quiet'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    _, _ = detect_proc.communicate()
    target_proc = subprocess.Popen(['gphoto2',
                                    '--get-config',
                                    'capturetarget'],
                                   stdout=subprocess.PIPE)
    for raw_line in target_proc.stdout:
        line = str(raw_line)
        if line.startswith('Choice:') and line.endswith('Memory card'):
            choice_nr = line.split()[1]
            set_proc = subprocess.Popen(['gphoto2',
                                         '--set-config',
                                         'capturetarget=%s' % choice_nr])
            print('Set capture target to memory card')
            set_proc.wait()

    folder_proc = subprocess.Popen(['gphoto2', '--list-folders'],
                                   stdout=subprocess.PIPE)
    for raw_line in folder_proc.stdout:
        line = str(raw_line)
        stripped_line = line.strip()
        if stripped_line.startswith('-') and stripped_line.endswith('CANON'):
            IMAGE_FOLDER = line.split()[1]
            print('Use photos for folder %s' % IMAGE_FOLDER)


def current_photo_count():
    ls_proc = subprocess.Popen(['gphoto2',
                                '--num-files',
                                '--folder=%s' % IMAGE_FOLDER],
                               stdout=subprocess.PIPE)
    stdout = list(ls_proc.stdout)
    if len(stdout) > 0:
        try:
            return int(stdout[0].split()[-1])  # extract file count
        except Exception:
            pass
    return -1


def download_latest_photo(photo_nr):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    raw_default_image_path_app = current_dir + '/static/img/raw.jpg'
    default_image_path_app = current_dir + '/' + DEFAULT_IMAGE_PATH
    if photo_nr == 0:
        rm_proc = subprocess.Popen(['rm', default_image_path_app],
                                   stdout=subprocess.PIPE)
        rm_proc.wait()
        return
    # t1 = time.time()
    cp_proc = subprocess.Popen(['gphoto2',
                                '--get-file=%d' % photo_nr,
                                '--filename=%s' % raw_default_image_path_app,
                                '--force-overwrite'])
    cp_proc.wait()
    # t2 = time.time()
    convert_proc = subprocess.Popen(['epeg',
                                     '--max=%d' % 1000,
                                     '--quality=%d' % 50,
                                     raw_default_image_path_app,
                                     default_image_path_app])
    convert_proc.wait()
    # t3 = time.time()

    # print('cp:', (t2 - t1), ' ---- convert:', (t3 - t2))


def capture_photo():
    capture_proc = subprocess.Popen(['gphoto2', '--capture-image', '--keep'])
    capture_proc.wait()
