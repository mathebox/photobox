from app import DEFAULT_IMAGE_PATH
import os
import subprocess


def init():
    detect_proc = subprocess.Popen(['gphoto2', ' --auto-detect'])
    detect_proc.wait()
    target_proc = subprocess.Popen(['gphoto2', ' --get-config', 'capturetarget'], stdout=subprocess.PIPE)
    for line in target_proc.stdout:
        if line.startswith('Choice:') and line.endswith('Memory card'):
            choice_nr = line.split()[1]
            set_proc = subprocess.Popen(['gphoto2', ' --set-config', 'capturetarget=%s' % choice_nr])
            print 'Set capture target to memory card.'
            set_proc.wait()


def current_photo_count():
    ls_proc = subprocess.Popen(['gphoto2', '--num-files', '--folder=/store_00020001/DCIM/100CANON'], stdout=subprocess.PIPE)
    response = list(ls_proc.stdout)
    if len(response) > 0:
        try:
            return int(response[0].split()[-1])  # extract file count
        except Exception:
            pass
    return -1


def download_latest_photo(photo_nr):
    default_image_path_app = 'app/%s' % DEFAULT_IMAGE_PATH
    if photo_nr == 0:
        rm_proc = subprocess.Popen(['rm', default_image_path_app],
                                   stdout=subprocess.PIPE)
        return
    cp_proc = subprocess.Popen(['gphoto2',
                                '--get-file=%d' % photo_nr,
                                '--filename=%s' % default_image_path_app,
                                '--force-overwrite'],
                               stdout=subprocess.PIPE)
    cp_proc.wait()


def capture_photo():
    capture_proc = subprocess.Popen(['gphoto2', '--capture-image', '--keep'])
    capture_proc.wait()

