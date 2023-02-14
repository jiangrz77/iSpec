import os, sys, time
import requests

class Downloader(object):
    def __init__(self, url):
        self.url = url
        self.file_path = url.split('/')[-1]
        self.start_time = time.time()

    def start(self):
        res_length = requests.get(self.url, stream=True)
        total_size = int(res_length.headers['Content-Length'])
        # print(res_length.headers)
        # print(res_length)
        if os.path.exists(self.file_path):
            temp_size = os.path.getsize(self.file_path)
            print('Continuing unfinished download: %s'%(self.file_path))
            print('Current: %.2f MB. Total：%.2f MB, Downdloaded：%2.2f%%'%(temp_size/1_048_576, total_size/1_048_576, 100*temp_size/total_size))
        else:
            temp_size = 0
            print('Downloading file: %s'%(self.file_path))
            print('Total: %.2f MB'%(total_size/1048576,))

        headers = {'Range': 'bytes=%d-' % temp_size,}
        res_left = requests.get(self.url, stream=True)
        start_time = time.time()


        with open(self.file_path, "ab") as f:
            for chunk in res_left.iter_content(chunk_size=1024):
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                timelapse = time.time()-start_time
                if timelapse>1:
                    done = int(50*temp_size/total_size)
                    start_time = time.time()
                    speed = len(chunk)/timelapse
                    if 0<=speed<1e3:
                        sys.stdout.write(
                            '\rDownloading: [%s%s] %d%%%9.2f B/s'\
                                %('█'*done,' '*(50-done),100*temp_size/total_size,speed)
                        )
                        sys.stdout.flush()
                    if 1e3<=speed<1e6:
                        sys.stdout.write(
                            '\rDownloading: [%s%s] %d%%%8.2f KB/s'\
                                %('█'*done,' '*(50-done),100*temp_size/total_size,speed/1024,)
                        )
                        sys.stdout.flush()
                    elif 1e6<=speed:
                        sys.stdout.write(
                            '\rDownloading: [%s%s] %d%%%8.2f MB/s'\
                                %('█'*done,' '*(50-done),100*temp_size/total_size,speed/1048576,)
                        )
                        sys.stdout.flush()