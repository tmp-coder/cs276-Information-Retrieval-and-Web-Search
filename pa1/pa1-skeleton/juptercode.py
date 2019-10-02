import urllib.request
import zipfile

import os.path


data_url = 'http://web.stanford.edu/class/cs276/pa/pa1-data.zip'
data_dir = 'pa1-data'

if not os.path.isfile(data_dir+'.zip'):
    print("download zip file from ",data_url)
    urllib.request.urlretrieve(data_url, data_dir+'.zip')
else:
    print("file has been download!")
zip_ref = zipfile.ZipFile(data_dir+'.zip', 'r') # too slow
zip_ref.extractall()
zip_ref.close()