import requests,os,time,multiprocessing
from lxml import etree
from tqdm import tqdm
import subprocess
import json

requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36',
    'Referer':'https://www.bilibili.com/'
}

username=os.path.expanduser('~')

cookies='buvid3=F3FC11A5-036E-CDC4-FDEE-6355DACD927214141infoc; b_nut=1676218314; i-wanna-go-back=-1; _uuid=A9B9B13D-D109B-8FAE-86910-9F910D10410C82213931infoc; CURRENT_FNVAL=4048; buvid4=C6D2D1AD-BA3C-F634-5637-58726330F24E15723-023021300-4oktwJy4h5/fs28zDGN7aA==; buvid_fp_plain=undefined; rpdid=0zbfVG68m5|9UESlxNW|45D|3w1PreZF; CURRENT_PID=87179bd0-ab78-11ed-a608-95ac477b26dd; header_theme_version=CLOSE; nostalgia_conf=-1; LIVE_BUVID=AUTO3816765476517826; fingerprint=89910a2907d5e060df2da4ad7defbd87; share_source_origin=weibo; is-2022-channel=1; bsource=search_bing; b_ut=5; DedeUserID=16379181; DedeUserID__ckMd5=b1edbd7861bc08c3; CURRENT_QUALITY=120; b_lsid=4767467D_186DFC12A53; SESSDATA=03dc6b6b,1694343227,040c5*32; bili_jct=c5d8cc5af07ed72efe27a29dfb52d867; sid=7geeh86c; bp_video_offset_16379181=772877715880542500; PVID=2; buvid_fp=89910a2907d5e060df2da4ad7defbd87; home_feed_column=4; innersign=0'
cookies={i.split('=')[0]:i.split('=')[1] for i in cookies.split(';')}

def getbilibilivideo(url):
    res=requests.get(url=url,headers=headers,verify=False,cookies=cookies)
    _element=etree.HTML(res.content)

    videoPlayInfo=str(_element.xpath('//head/script[3]/text()')[0][20:])
    videojson=json.loads(videoPlayInfo)
    videotitle=str(_element.xpath('/html/head/title/text()')[0]).rstrip('_哔哩哔哩bli').replace('|','').replace(' ','').replace('?','')

    try:
        videoUrl=videojson['data']['dash']['video'][0]['baseUrl']
        audioUrl=videojson['data']['dash']['audio'][0]['baseUrl']
        flag=0
        return (videotitle,flag,videoUrl,audioUrl)
    except:
        videoUrl=videojson['data']['dash']['audio'][0]['baseUrl']
        return (videotitle,flag,videoUrl)
        flag=1

def fileDownload(sourceUrl,url,filename):
    _headers=headers
    _headers.update({'Referer':sourceUrl})
    res=requests.get(url=url,headers=_headers,cookies=cookies,verify=False,stream=True)
    chunk_size=1024
    file_size=int(res.headers['Content-Length'])
    pbar=tqdm(total=file_size, unit='B', unit_scale=True)
    with open(username+'\\videos\\'+filename,'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            f.write(chunk)
            pbar.update(chunk_size)
    pbar.close()

def combineVideoAudio(videopath,audiopath,outpath):
    subprocess.call("D:\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg -i " + videopath + " -i " + audiopath + " -c copy "+ outpath,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    os.remove(videopath)
    os.remove(audiopath)

def download_video(url,bv,p=''):
    videodata=getbilibilivideo(url=url)
    if videodata[1]==0:
        fileDownload(sourceUrl=url,url=videodata[2],filename=bv+'_video'+p+'.mp4')
        fileDownload(sourceUrl=url,url=videodata[3],filename=bv+'_audio'+p+'.mp3')
        videopath=username+'\\Videos\\'+bv+'_video'+p+'.mp4'
        audiopath=username+'\\Videos\\'+bv+'_audio'+p+'.mp3'
        outpath=username+'\\Videos\\'+videodata[0]+p+'.mp4'
        combineVideoAudio(videopath=videopath,audiopath=audiopath,outpath=outpath.encode('utf-8').decode('utf-8'))
    else:
        fileDownload(sourceUrl=url,url=videodata[2],filename=bv+'_video'+p+'.mp4')

def task(bv_data):
    bv=bv_data[0]
    if len(bv_data)==1:
        download_video('https://www.bilibili.com/video/'+bv,bv=bv_data[0])
    elif len(bv_data)==2:
        download_video('https://www.bilibili.com/video/'+bv+'/?p='+bv_data[1],bv=bv_data[0],p='_'+str(bv_data[1])+'p')
    elif len(bv_data)==3:
        for i in range(int(bv_data[1]),int(bv_data[2])+1):
            download_video('https://www.bilibili.com/video/'+bv+'/?p='+str(i),bv=bv_data[0],p='_'+str(i)+'p')
    print('Task done')

if __name__=='__main__':
    while True:
        bv_data=input('请输入bv号和p数(如果有的话，可以输入起始p到终止p)，用空格隔开,输入-1结束:').split(' ')
        if bv_data[0]=='-1':
            break
        task(bv_data=bv_data)




    