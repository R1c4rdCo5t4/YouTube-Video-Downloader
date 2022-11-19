
import os
from pytube import YouTube
from pytube import Playlist
from pytube import Search


def cprint(text,color):
    print(color, text) # write in color
    print(Colors.lightgrey, "") # reset color


def main():

    cprint("Youtube MP3 Downloader", Colors.cyan)
    cprint("----------------------------", Colors.cyan)

    yt_input = str(input("Search or URL: "))

    if("playlist?list" in yt_input): # playlist url
        urls = Playlist(yt_input) # convert playlist url to individual video urls
        save_info = get_save_info()
        for url in urls:
            download(url,save_info)
    elif "youtube" in yt_input: # single video url
        download(yt_input,get_save_info()) 
    
    else: # search
        search(yt_input)
        
    cprint("Done.\n\n", Colors.green)
    main()
   
        
def show_results(s,p):
    try:
        for i in range(1+10*p,11+10*p):
            print(f"{i} - {s.results[i-1].title}")
    except IndexError:
        print("No more results.")
    
    finally:
        print("")

    
def get_save_info():
    dest = get_input("Enter destination path: ", "Path does not exist.", lambda x: os.path.exists(x))
    ext = get_input("File extension (mp3/mp4): ", "Invalid extension.", lambda x : str(x) in ['mp3','mp4'])
    return dest,ext

def get_search_input(max=0):
    
    valid = False
    id = 0
    while(not valid):
        print("Choose id or press enter for more results: ")
        resp = input("")


        if(resp == ""):
            return ""

        if(resp.isdigit()):
            id = int(resp) - 1
            if id in range(0,max):
                valid = True
            else:
                cprint("Invalid id.", Colors.red)
                
        else:
            cprint("Invalid input.", Colors.red)
        
    
    return id

def search(query):
    s = Search(query)
    i = 0
    show_results(s,i)
    resp = get_search_input(len(s.results)-1)

    while(resp == ""):
        i += 1
        if(i % 2 == 0):
            s.get_next_results()
        show_results(s,i)
        resp = get_search_input(len(s.results)-1)
    
    chosen_video = s.results[resp]
    cprint("-> " + chosen_video.title, Colors.blue)
    download(chosen_video.watch_url,get_save_info()) 


def download(url,save_info):

    dest_path = save_info[0]
    file_ext = save_info[1]
    # get file url in each line of file
    yt = YouTube(str(url))
    
    # extract audio only
    if(file_ext == "mp3"):
        file = yt.streams.filter(only_audio=True).first()
    else:
        file = yt.streams.get_highest_resolution()

    file_name = f"{file.title}.{file_ext}"

    if os.path.exists(f"{dest_path}\\{file_name}"): # try to avoid downloading file that already exists
        cprint(f"{file.title} already exists.", Colors.yellow)
        return

    # download file
    out_file = file.download(output_path=dest_path)

    # save file    
    try:
        base, ext_ = os.path.splitext(out_file)
        new_file = base + f'.{file_ext}'
        os.rename(out_file, new_file)
        cprint(f"{yt.title} has been successfully downloaded.", Colors.green)
                
    except FileExistsError: # remove file if already exists
        cprint(f"{yt.title} already exists.", Colors.yellow)
        os.remove(out_file)
       
    except:
        cprint("An error saving the file occurred.", Colors.red)


def get_input(quest, resp, cond):
    line = str(input(quest))
    while(not cond(line)):
        cprint(resp, Colors.yellow)
        line = str(input(quest))
    
    return line


class Colors:
    red='\033[31m'
    green='\033[32m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m' 
    yellow='\033[93m'
    black= '\033[30m'
    blue= '\033[34m'
    magenta= '\033[35m'
    cyan= '\033[36m'
    white= '\033[37m'
    


if __name__ == "__main__":
    os.system("cls")
    main()


