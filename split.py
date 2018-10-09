from moviepy.editor import VideoFileClip
from PIL import Image
import os
import tools
import config


class AVSplit:
    # sift
    # lbp
    # hog
    def __init__(self, video_dir):
        self.videoclip = VideoFileClip(video_dir)
        self.audioclip = self.videoclip.audio

    def get_frames(self):
        return [frame for frame in self.videoclip.iter_frames()]

    def get_video_clip(self):
        return self.videocip

    def get_audio_clip(self):
        return self.audioclip

    def save_frames(self, save_video_dir):
        dir = tools.ensure_dir(save_video_dir)
        num_frame = int(self.videoclip.fps * self.videoclip.duration)
        for i, frame in enumerate(self.videoclip.iter_frames()):
            Image.fromarray(frame).save('{0}/{1}.jpeg'.format(dir, i))
            print('saving frame {0}/{1}'.format(i, num_frame - 1))
        with open(config.frames_output_dir+'/fps.txt', 'w') as f:
            f.write(str(self.videoclip.fps))

    def save_audio(self, save_audio_dir, save_audio_name):
        dir = tools.ensure_dir(save_audio_dir)
        if self.audioclip is None:
            print('Video has no audio')
        else:
            self.audioclip.write_audiofile(os.path.join(save_audio_dir, save_audio_name), nbytes=2, codec='pcm_s16le',
                                           bitrate='1000k', verbose=True)

if __name__ == '__main__':
    import config
    sp = AVSplit(config.source_video)
    sp.save_frames(config.frames_output_dir)
    sp.save_audio(config.audio_output_dir, config.audio_output_name)

