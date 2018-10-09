from split import AVSplit
import config
from detect import LogoDetect
from PIL import Image
import tools
import moviepy
import os

# Step1: Split video and audio
GENERATE_FRAMES = True
if GENERATE_FRAMES:
    sp = AVSplit(config.source_video)
    sp.save_frames(config.frames_output_dir)
    sp.save_audio(config.audio_output_dir, config.audio_output_name)

frame_names = tools.load_frames(config.FRAMES_PATH_BASE)

# Step2: Detect logo frame-wise
num_frames = len(frame_names)
for i, frame in enumerate(frame_names):
    try:
        print('detecting frame {0}/{1}'.format(i,num_frames))
        img = LogoDetect(config.DETECT_OBJ, frame)
        directory = tools.ensure_dir(config.save_detect_dir)
        Image.fromarray(img).save('{0}/{1}.jpeg'.format(directory, i))
    finally:
        pass

# Step3: export video file
detected_frames = tools.load_frames(config.DETECTED_PATH_BASE)
clip = moviepy.editor.ImageSequenceClip(detected_frames, fps=10)
if GENERATE_FRAMES:
    fps = sp.videoclip.fps
    clip = clip.set_fps(fps)
    if sp.audioclip is not None:
        clip = clip.set_audio(sp.audioclip)
else:
    with open(config.frames_output_dir+'/fps.txt', 'r') as f:
        fps = float(f.read())
        clip = clip.set_fps(fps)
        au_clip = None
    try:
        au_clip = moviepy.editor.AudioFileClip(os.path.join(config.audio_output_dir, config.audio_output_name))
    except OSError:
        pass
    if au_clip is not None:
        clip = clip.set_audio(au_clip)

directory = tools.ensure_dir(config.DETECTED_VDO_DIR)
filename = config.DETECTED_VDO_NAME
clip.write_videofile(directory+filename)
