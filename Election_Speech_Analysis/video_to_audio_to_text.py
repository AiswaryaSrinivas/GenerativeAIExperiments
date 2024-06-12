## Take playlist URl and convert to audio and extract the Text associated with that audio
import argparse
from pytube import YouTube
from pytube import Playlist

import moviepy.editor as mp
import os

import pathlib
from datetime import datetime


def extractPlayListUrls(playlist_url):
    try:
        print(playlist_url)
        playlist = Playlist(playlist_url)
        return playlist.video_urls
    except Exception as e:
        print("Error ",e)
        return []

def convertVideoToAudio(video_url,folder_path,audio_folder_path):
    filename=YouTube(video_url).streams.first().download(folder_path)
    my_clip = mp.VideoFileClip(filename)
    output_audio_filename=pathlib.Path(filename).stem+".wav"
    output_audio_filename=output_audio_filename.replace(" ","_")
   

    my_clip.audio.write_audiofile(os.path.join(audio_folder_path,output_audio_filename),fps=16000)
    os.remove(filename)
    return os.path.join(audio_folder_path,output_audio_filename)



if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Enter the PlayList URL for extraction")
    parser.add_argument('url', type=str, help="The url of the playlist or video")
    parser.add_argument('--playlist', type=bool, help="This argument tells us if the URL is a playlist URL or an video URL. If true then this is the Playlist URL. Default is True", default="True")
    
    parser.add_argument('--folder_name',type=str,help="This is the folder where the Video and audio will be stored",default="")
    args = parser.parse_args()

    if args.folder_name=="":
        folder_path= datetime.now().strftime("%Y%m%d%H%M%S")
            
    else:
        folder_path=args.folder_name
    audio_output_folder=os.path.join(folder_path,"AUDIO/")
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(audio_output_folder).mkdir(parents=True, exist_ok=True)
    if args.playlist==True:
        print(args.url)
        video_urls=extractPlayListUrls(args.url)
        
        #video_urls=video_urls[0:2]
        print(video_urls)
        
        audio_paths=[]
        for urls in video_urls:
            audio_paths.append(convertVideoToAudio(urls,folder_path,audio_output_folder))
    else:
        convertVideoToAudio(args.url,folder_path,audio_output_folder)
    
        
        





    


