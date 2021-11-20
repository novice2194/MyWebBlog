import markdown
import codecs
import os
from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path

MDDIR = Path(__file__).resolve().parent.parent
MDDIR = (MDDIR / 'statics/Markdown')
dirURL = []


# Create your views here.
def index(request):
    title = "BeYoung首页"
    # mddir = (MDDIR / '八股文.md')
    # f = codecs.open(mddir, 'r', 'utf-8')
    # content = f.read()
    # content = markdown.markdown(content,
    #                             extensions=[
    #                                 'markdown.extensions.codehilite',
    #                                 'markdown.extensions.extra',
    #                                 'markdown.extensions.fenced_code',
    #                                 'markdown.extensions.tables',
    #                                 'markdown.extensions.toc',
    #                             ])
    dirURL = []
    for _, _, filename in os.walk(f'{MDDIR}'):
        for name in filename:
            if name == "index.html":
                continue
            elif name[-3:] == ".md":
                dirURL.append(os.path.splitext(name)[0])
    dirURL.sort()
    # print(ret)
    # if request.META.get('HTTP_X_FORWARDED_FOR'):
    #     ip = request.META.get("HTTP_X_FORWARDED_FOR")
    # else:
    #     ip = request.META.get("REMOTE_ADDR")
    # print("ip:", ip)
    # print(request.META)

    return render(request, "index.html", locals())


def content(request, contenturl):
    title = "BeYoung:" + contenturl
    if contenturl in dirURL:
        mddir = contenturl + ".md"
        mddir = (MDDIR / mddir)
        f = codecs.open(mddir, 'r', 'utf-8')
        content = f.read()
        content = markdown.markdown(content,
                                    extensions=[
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.extra',
                                        'markdown.extensions.fenced_code',
                                        'markdown.extensions.tables',
                                        'markdown.extensions.toc',
                                    ])
        return render(request, "template.html", locals())
    return HttpResponse("404")
