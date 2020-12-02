from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.http import FileResponse
from django.utils.encoding import escape_uri_path

import os
import json

HonCloud = 'static/cloudfiles'
FileTypeMap = {
            'md': {'typen': 'Markdown文档', 'ctype': 'text/plain',},
            'zip': {'typen': '压缩文件', 'ctype': 'application/x-zip-compressed',},
            'rar': {'typen': '压缩文件', 'ctype': 'application/octet-stream'},
            '7z': {'typen': '压缩文件', 'ctype': 'text/plain',},
            'exe': {'typen': '应用程序', 'ctype': 'application/x-msdownload',},
            'ino': {'typen': 'Arduino源码', 'ctype': 'text/plain',},
            'tif': {'typen': '图片', 'ctype': 'image/tiff',},
            'png': {'typen': '图片', 'ctype': 'image/png',},
            'txt': {'typen': '文本文档', 'ctype': 'text/plain',},
            'docx': {'typen': 'Word文档', 'ctype': 'application/msword',},
            'py': {'typen': 'Python源码', 'ctype': 'application/octet-stream',},
        }

def index(request):
    return render(request, '404.html')

def honcloud(request):
    return render(request, 'honcloud.html')

def upload(request):
    obj = request.FILES.get('wj')

    try:
        on = obj.name
        # print(on)
    except AttributeError:
        return render(request, 'back.html', context={'ps': '主人您还没有选择文件哦～'})

    fn = f'{HonCloud}/{on}'
    with open(fn, 'wb') as f:
        for line in obj.chunks():
            f.write(line)

    return render(request, 'back.html', context={'ps': '上传成功'})

def fsuffix(fn, mode):
    suffix = fn[fn.rfind('.')+1:]
    if mode == 0:
        return FileTypeMap[suffix]['typen'] if suffix in FileTypeMap else suffix
    if mode == 1:
        return FileTypeMap[suffix]['ctype'] if suffix in FileTypeMap else 'application/octet-stream'

def honcloudd(request):
    files = sorted(os.listdir(HonCloud))
    try:
        key = request.GET['keyWord']
        files = [{'name': x, 'type': fsuffix(x, 0)} for x in files if key in x]
    except:
        files = [{'name': x, 'type': fsuffix(x, 0)} for x in files]
    ct = {
        'listName': 'GHOST Cloud',
        'filePath': HonCloud,
        'files': files,
    }
    # return render(request, 'filelist.html', context=ct)
    return render(request, 'honcloudd.html', context=ct)

def download(request):
    fn = request.GET.get('fn')
    file = open(f'{HonCloud}/{fn}','rb')
    response = FileResponse(file)
    # print(f'fn = {fn}')
    response['Content-Type']=fsuffix(fn, 1)
    response['Content-Disposition'] = f'attachment;filename={escape_uri_path(fn)}'
    return response

# 配置异常页面
def page_400(request, e):
    return render(request, '404.html', status=400)

def page_403(request, e):
    return render(request, '404.html', status=403)

def page_404(request, e):
    return render(request, '404.html', status=404)

def page_500(request):
    return render(request, '404.html', status=500)

