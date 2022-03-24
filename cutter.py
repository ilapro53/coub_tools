import os
import shutil

import moviepy
from moviepy.editor import VideoFileClip
import cv2
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io import ffmpeg_tools

def with_opencv(filename):
    import cv2
    video = cv2.VideoCapture(filename)

    duration = video.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    return duration, frame_count

def with_moviepy(filename):
    if isinstance(filename, str):
        clip = VideoFileClip(filename)
    else:
        clip = moviepy.editor.VideoFileClip(filename)

    duration       = clip.duration
    fps            = clip.fps
    width, height  = clip.size
    return (duration*100-8)/100, fps, (width, height)

if __name__ == '__main__':
    # ID = '2otm76'
    # ln = with_moviepy(f'K:\\CoubData\\{ID}.mp4')[0]
    # ffmpeg_extract_subclip(f'K:\\Coubs\\ilya-pro\\{ID}.mp4', 0, round(ln-0.05), targetname='cut1.mp4')
    # ln2 = with_moviepy('cut1.mp4')[0]
    # print(ln, ln2)
    print(with_moviepy(r'K:\Coubs\musecollexion\30gtsq (1).mp4'))