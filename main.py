from pytube import YouTube
from os import path, rename
import argparse
import sys

parser = argparse.ArgumentParser(description='Download YouTube videos')
parser.add_argument('format', metavar='FORMAT', type=str, help='Download format, can be mp3 or mp4')
parser.add_argument('url', metavar='URL', type=str, help='URL of the video')
parser.add_argument('-o', '--output', metavar='PATH', type=str, help='Output path', default=None)

args = parser.parse_args()

if args.output is not None:
  if args.output[-4:] not in ['.mp3', '.wav', '.mp4']:
    print("error : output file must be a .mp3, .wav or .mp4 file")
    sys.exit(1)
  elif args.output[-3:] != args.format:
    print("error in the output file extension")
    sys.exit(1)


def progress_bar(stream, chunk, bytes_remaining):
  contentSize = stream.filesize
  size = contentSize - bytes_remaining

  print('\r' + '[Download progress]:[%s%s]%.2f%%;' % ('█' * int(size*20/contentSize), ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)), end='')


chunk_size = 1
print(f"fetching : {args.url}")
video = YouTube(args.url)
print(f"downloading : {video.title}")

video.register_on_progress_callback(progress_bar)

match args.format:
  case 'mp3', 'wav':
    audio = video.streams.get_audio_only()
    video_title = audio.download()
  case 'mp4':
    video = video.streams.get_highest_resolution()
    video_title = video.download()
  case _:
    print("error : format not supported")
    sys.exit(1)


match args.output:
  case None:
    base, ext = path.splitext(video_title)
    new_video_title = base + '.' + args.format
  case _:
    new_video_title = args.output
    

rename(video_title, new_video_title)
sys.exit(0)