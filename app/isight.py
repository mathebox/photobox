from app import DEFAULT_IMAGE_PATH
import os
import subprocess
from datetime import datetime

FAKECAM_DIR = 'fakecam'


def init():
    if not os.path.exists(FAKECAM_DIR):
        os.makedirs(FAKECAM_DIR)


def current_photo_count():
    ls_proc = subprocess.Popen(['ls', FAKECAM_DIR], stdout=subprocess.PIPE)
    return len(list(ls_proc.stdout))


def download_latest_photo(photo_nr):
    default_image_path_app = 'app/%s' % DEFAULT_IMAGE_PATH
    if photo_nr == 0:
        rm_proc = subprocess.Popen(['rm', default_image_path_app],
                                   stdout=subprocess.PIPE)
        rm_proc.wait()
        return
    ls_proc = subprocess.Popen(['ls', '-t', FAKECAM_DIR],
                               stdout=subprocess.PIPE)
    file_name = list(ls_proc.stdout)[0].strip().decode('UTF-8')
    new_image_path = '%s/%s' % (FAKECAM_DIR, file_name)
    cp_proc = subprocess.Popen(['cp', new_image_path, default_image_path_app],
                               stdout=subprocess.PIPE)
    cp_proc.wait()


def capture_photo():
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    snapshot_path_old = 'snapshot.jpg'
    snapshot_path_new = '%s/snapshot-%s.jpg' % (FAKECAM_DIR, timestamp)
    image_proc = subprocess.Popen(['imagesnap', '-q'], stdout=subprocess.PIPE)
    image_proc.wait()
    mv_proc = subprocess.Popen(['mv',
                                snapshot_path_old,
                                snapshot_path_new],
                               stdout=subprocess.PIPE)
    mv_proc.wait()
