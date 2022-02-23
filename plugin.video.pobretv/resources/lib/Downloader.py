import os
import xbmcgui
import xbmc
import time
import urllib.request
from . import controlo

class Downloader:
    def __init__(self,):
            pass

    def download(self,path,url,name):
        if os.path.isfile(path) is True:
            xbmc.log("SIM")
            while os.path.exists(path):
                try: os.remove(path); break
                except: pass

        dp = xbmcgui.DialogProgress()
        dp.create('Pobre.tv downloader')
        dp.update(0, 'A começar o download do ficheiro')
        xbmc.sleep(500)
        start_time = time.time()

        #urllib.URLopener.version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0'

        try:
            urllib.request.urlretrieve(url, path, lambda nb, bs, fs: self.dialogdown(name,nb, bs, fs, dp, start_time))
            dp.close()
            return True
        except Exception as e:
            controlo.log(str(e))
            while os.path.exists(path):
                    try: os.remove(path); break
                    except: pass
            dp.close()
            return False

    def dialogdown(self,name,numblocks, blocksize, filesize, dp, start_time):
        try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
            kbps_speed = numblocks * blocksize / (time.time() - start_time)
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed
            else: eta = 0
            kbps_speed = kbps_speed / 1024
            total = float(filesize) / (1024 * 1024)
            mbs = '%.02f MB %s %.02f MB' % (currently_downloaded,' baixado de ', total)
            e = ' (%.0f Kb/s) ' % kbps_speed
            tempo = ' Tempo:' + ' %02d:%02d' % divmod(eta, 60)
            dp.update(int(percent), name + ' - '+ mbs + e + tempo)
        except Exception as e:
            controlo.log(str(e))
            dp.update(100,'Erro ao fazer download: ' + str(e))

        if dp.iscanceled():
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
    def __init__(self, value): self.value = value
    def __str__(self): return repr(self.value)
