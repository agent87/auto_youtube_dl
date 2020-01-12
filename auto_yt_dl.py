#This is python script to scan my Google Chrome Bookmarks
#!/home/sangman/anaconda3/envs/sng_kqx/bin/python
from __future__ import unicode_literals
import json
import time
import youtube_dl
import os
import sys

bookmark_dir = '/home/sangman/.config/google-chrome/Default/Bookmarks'#.format(os.system('whoami'))
songs_bk_name = 'Youtube Songs'
docu_bk_name = 'Youtube Documentary Videos'

#bk stands for bookmarks
#import bookmarks for parsing
def bk_import():
    with open(bookmark_dir) as myfile:
        return json.load(myfile)

    
class MyLogger(object):
    def debug(self, msg):
        global debug_msg
        debug_msg = msg

    def warning(self, msg):
        global warning_msg
        warning_msg = msg

    def error(self, msg):
        global error_msg
        error_msg = msg

def progress_logger(d):
    global progress_log 
    progress_log = d

#Takes in url and format of the url(Documentary or Songs)
#Return a True Value if The bookmark is the archive file
#Return a False value if the bookmark url is not in the archive file
def downloaded(url, type): 
    if type == 'docu':
        downloaded = False
        for downloads in range(len(list(open('ytd_archive.txt', 'r')))):
            if url[32:43] == list(open('ytd_archive.txt', 'r'))[downloads][8:19]:
                downloaded = True
                break
            else:
                continue
        return downloaded
    if type == 'song':
        downloaded = False
        for downloads in range(len(list(open('yts_archive.txt', 'r')))):
            if url[32:43] == list(open('yts_archive.txt', 'r'))[downloads][8:19]:
                downloaded = True
                break
            else:
                continue
        return downloaded
            


#Youtube Video to MP3 Songs
def songs_dl(bk_rdata):
    dl_count = 0
    song_dl_status = False
    for i in range(len(bk_rdata['roots']['bookmark_bar']['children'])):
        if bk_rdata['roots']['bookmark_bar']['children'][i]['name'] == songs_bk_name:
            for d in range(len(bk_rdata['roots']['bookmark_bar']['children'][i]['children'])):
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '~/Music/Rhythmbox/%(title)s.mp3',        
                    'noplaylist' : True,
                    'retries' : 11,
                    'verbose': False,
                    'download_archive' : 'yts_archive.txt',
                    'logger': MyLogger(),
                    #'progress_hooks': [progress_logger],
                    'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',}],
                    }
                if downloaded(bk_rdata['roots']['bookmark_bar']['children'][i]['children'][d]['url'], 'song') == True:
                    dl_count = dl_count + 1
                    pass
                else:
                    try:
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            print('Downloading {} of {} '.format(d,len(bk_rdata['roots']['bookmark_bar']['children'][i]['children'])))
                            ydl.download([bk_rdata['roots']['bookmark_bar']['children'][i]['children'][d]['url']])
                            dl_count = dl_count + 1
                    except youtube_dl.utils.DownloadError:
                        print(error_msg)
                        pass
                if dl_count == len(bk_rdata['roots']['bookmark_bar']['children'][i]['children']):
                    song_dl_status = True     
            break
        else:
            pass
    return song_dl_status


def docu_dl(bk_rdata):
    for i in range(len(bk_rdata['roots']['bookmark_bar']['children'])):
        if bk_rdata['roots']['bookmark_bar']['children'][i]['name'] == docu_bk_name:
            for d in range(len(bk_rdata['roots']['bookmark_bar']['children'][i]['children'])):
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '~/Videos/Documentaries/%(title)s',        
                    'noplaylist' : True,
                    'retries' : 5,
                    'download_archive' : 'ytd_archive.txt',
                    'logger': MyLogger(),
                    #'progress_hooks': [progress_logger]
                    }
                if downloaded(bk_rdata['roots']['bookmark_bar']['children'][i]['children'][d]['url'], 'docu') == True:
                    print(bk_rdata['roots']['bookmark_bar']['children'][i]['children'][d]['name'],' is Already Downloaded!')
                else:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([bk_rdata['roots']['bookmark_bar']['children'][i]['children'][d]['url']])
                        #if progress_log['status'] == 'finished':
                        #print('Done downloading {}, \n now converting ...'.format(bk_rdata['roots']['bookmark_bar']['children'][i]['children'][d]['name']))
                     



def engine_start():
    bk_rdata = bk_import()
    read_checksum = open('checksum','r')
    if bk_rdata['checksum'] == list(read_checksum)[0]:
        read_checksum.close()
        print('No new Bookmarks')
    elif bk_rdata['checksum'] is not list(open('checksum','r'))[0]:
        read_checksum.close()
        songs_dl_state = songs_dl(bk_rdata)
        #docu_dl(bk_rdata)
        if songs_dl_state is True:
            open('checksum', 'w').write(bk_rdata['checksum'])
        
        
if __name__ == '__main__':
    try:
        start_time = time.time()
        engine_start()
        end_time = time.time()
        print(end_time-start_time)
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
