from pytube import YouTube, Playlist
from os import path, rename, makedirs
import argparse, sys

parser = argparse.ArgumentParser(description='Download YouTube videos')
parser.add_argument('format', metavar='FORMAT', type=str, help='Download format, can be mp3 or mp4')
parser.add_argument('url', metavar='URL', type=str, help='URL of the video')
parser.add_argument('-o', '--output', metavar='PATH', type=str, help='Output path', default=None)
parser.add_argument('-p', '--playlist', action='store_true', help='Download a playlist', default=False)

args = parser.parse_args()

if args.output[-1] == '/':
  output_type = 'directory'
  makedirs(args.output, exist_ok=True)
else:
  output_type = 'file'


if args.output is not None:
  if args.playlist == False:
    if args.output[-4:] not in ['.mp3', '.wav', '.mp4']:
      print("error : output file must be a .mp3, .wav or .mp4 file")
      sys.exit(1)
    elif args.output[-3:] != args.format:
      print("error in the output file extension")
      sys.exit(1)
  elif args.output[-1]!='/' and args.playlist == True:
    print("error : when working with a playlist, output file must be a directory")
    sys.exit(1)


def progress_bar(stream, chunk, bytes_remaining):
  contentSize = stream.filesize
  size = contentSize - bytes_remaining

  print('\r' + '[Download progress]:[%s%s]%.2f%%;' % ('█' * int(size*20/contentSize), ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)), end='')


chunk_size = 1
if args.playlist == False:
  print(f"fetching : {args.url}")
  video = YouTube(args.url)
  print(f"downloading : {video.title}")

  video.register_on_progress_callback(progress_bar)

  match args.format:
    case 'mp3':
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
      if output_type == 'directory':
        new_video_title = args.output + path.splitext(video.title)[0] + '.' + args.format
      else:
        new_video_title = args.output
      

  rename(video_title, new_video_title)

else:
  print(f"fetching : {args.url}")
  playlist = Playlist(args.url)
  
  print(args.format)
  
  for video in playlist.videos:
    print(f"downloading : {video.title}")
    video.register_on_progress_callback(progress_bar)
    
    match args.format:
      case 'mp3':
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
        new_video_title = args.output + path.splitext(video.title)[0] + '.' + args.format
    
    rename(video_title, new_video_title)
  
sys.exit(0)