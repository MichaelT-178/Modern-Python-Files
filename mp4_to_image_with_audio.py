from moviepy.editor import AudioFileClip, ImageClip
#Need to have pygame installed

video_path = 'path/to/video/file.mp4'

image_path = 'path/to/image/to/use'

# Get audio from the mp4
audio_clip = AudioFileClip(video_path)

# Create an ImageClip object with the same duration as the audio
image_clip = ImageClip(image_path, duration=audio_clip.duration)

# Set the fps (frames per second) for the video if necessary, this could be set to the original video's fps
image_clip = image_clip.set_fps(24)

# Set the audio of the image clip to be the audio from the video
image_clip = image_clip.set_audio(audio_clip)

# Write the result to a file (the filename of the output video)
output_path = 'output_video.mp4'

#Write video
image_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

