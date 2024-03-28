from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .tools import MixkitParser, PixabayParser, PexelsParser, chunks
# Create your views here.

def index(request):
    return render(request, 'workspace/index.html')

@csrf_exempt
def find_videos(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        mixkit = True if request.POST.get('mixkit') == 'true' else False
        pexels = True if request.POST.get('pexels') == 'true' else False
        pixabay = True if request.POST.get('pixabay') == 'true' else False
        videos = []
        if mixkit:
            videos_mixkit = MixkitParser.find_videos(query=text, max_=5)
            for video in videos_mixkit:
                videos.append(video)
        if pexels:
            videos_pexels = PexelsParser.find_videos(query=text, key=settings.API_KEY_PEXELS)
            for video in videos_pexels:
                videos.append(video)
        if pixabay:
            videos_pixabay = PixabayParser.find_videos(api_key=settings.API_KEY_PIXABAY, query=text, height=1080, width=1920)
            for video in videos_pixabay:
                videos.append(video)
        content = {'pexels': videos_pexels, 'pixabay': len(videos_pixabay), 'mixkit': len(videos_mixkit)}
        return JsonResponse(content)


@csrf_exempt
def find_mixkit(request):
    if request.method == 'POST':
        videos = []
        text = request.POST.get('text')
        page = request.POST.get('page')
        videos_mixkit = MixkitParser.find_videos(query=text, page=page)
        videos_splitted = chunks(videos_mixkit['videos'], 8)
        table_html = render_to_string('workspace/10_el_table.html', {'videos_splitted': videos_splitted})
        videos_mixkit['table'] = table_html
        return JsonResponse(videos_mixkit)

@csrf_exempt
def find_pexels(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        page = request.POST.get('page')
        videos_pexels = PexelsParser.find_videos(query=text, key=settings.API_KEY_PEXELS, page=page)
        videos_splitted = chunks(videos_pexels['videos'], 8)
        table_html = render_to_string('workspace/10_el_table.html', {'videos_splitted': videos_splitted})
        videos_pexels['table'] = table_html

        return JsonResponse(videos_pexels)

@csrf_exempt
def find_pixabay(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        page = request.POST.get('page')
        videos_pexels = PixabayParser.find_videos(query=text, api_key=settings.API_KEY_PIXABAY, page=page)
        videos_splitted = chunks(videos_pexels['videos'], 8)
        table_html = render_to_string('workspace/10_el_table.html', {'videos_splitted': videos_splitted})
        videos_pexels['table'] = table_html

        return JsonResponse(videos_pexels)
