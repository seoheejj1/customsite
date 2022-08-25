import re
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from cs.models import Board, Inquire, B_Photo, Photo_Upload
from user.models import User
from shop.models import Config
from django.forms import ValidationError
from django.utils.datastructures import MultiValueDictKeyError

# 공지사항 페이지
def notice_write(request):
    if request.method == 'GET':
        context = {
            'session': request.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cs'
        }
        return render(request, 'notice_write.html', context)

    elif request.method == 'POST':
        user = User.objects.get(id=request.session['user'])
        tag = request.POST['notice']
        title = request.POST['title']
        content = request.POST['content']

        notice = Board(user=user, title=title, content=content, tag=tag)
        notice.save()
        
        return render(request, 'notice_writeOk.html', {"pk": notice.pk})


def notice_detail(request, pk):
    notice = Board.objects.get(pk=pk)
    notice.view_cnt += 1
    notice.save()

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs',
        'notice': notice
    }
    return render(request, 'notice_detail.html', context)


def notice_list(request):
    keyword = request.GET.get('keyword')
    
    if keyword:
        all_notices = Board.objects.filter(tag='공지사항',title__contains=keyword).order_by('-reg_date')
    else:
        all_notices = Board.objects.filter(tag='공지사항').order_by('-reg_date')

    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_notices, 10)
    notices = paginator.get_page(page)

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs',
        'notices': notices,
        'all_notices': all_notices,
        # 'keyword': keyword
    }
        

    return render(request, 'notice_list.html', context)


def notice_update(request, pk):
    if request.method == 'GET':
        notice = Board.objects.get(pk=pk)
        context = {
            'session': request.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cs',
            'notice': notice
        }

        return render(request, 'notice_update.html', context)

    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        notice = Board.objects.get(pk=pk)
        notice.title = title
        notice.content = content
        notice.save()

        return render(request, 'notice_updateOk.html', {"pk": notice.pk})


def notice_delete(request):
    if request.method == 'POST':
        id = request.POST['id']
        notice = Board.objects.get(id=id)
        notice.delete()

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs'
    }
    return render(request, 'notice_deleteOk.html', context)


# 이벤트 페이지
def event_write(request):
    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs'
    }
    
    if request.method == 'GET':
        return render(request, 'event_write.html', context)

    elif request.method == 'POST':
        user = User.objects.get(id=request.session['user'])
        tag = request.POST['event']
        title = request.POST['title']
        content = request.POST['content']
        e_start = request.POST['e_start']
        e_end = request.POST['e_end']
        uploadedFile = request.FILES["uploadedFile"]


        if len(re.findall(r'[^a-z | 0-9 | . | " " | ( | )]', uploadedFile.name)) > 0:
            return HttpResponse(f'''
                <script>
                    alert("파일 이름에 특수문자가 포함되어 있습니다!");
                    history.back();
                </script>
            ''')

        photo = Photo_Upload(title=uploadedFile.name, photo=uploadedFile)
        photo.save()

        board = Board(
            user=user, 
            title=title, 
            content=content, 
            tag=tag,
            e_start=e_start,
            e_end=e_end,
        )
        
        board.save()

        B_Photo(board=board, photo=f'/static/image/{photo.title}').save()

        return render(request, 'event_writeOk.html', {"pk": board.pk})


def event_detail(request, pk):
    event = Board.objects.get(pk=pk)
    event.view_cnt += 1
    event.save()

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs',
        'event': event
    }
    return render(request, 'event_detail.html', context)


def event_list(request):
    all_events = Board.objects.filter(tag='이벤트').order_by('-reg_date')

    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_events, 6)
    events = paginator.get_page(page)
    photos = B_Photo.objects.all()

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs',
        'events': events,
        'all_events': all_events,
        'photos': photos
    }
    return render(request, 'event_list.html', context)


def event_update(request, pk):
    
    if request.method == 'GET':
        event = Board.objects.get(pk=pk)
        context = {
            'session': request.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cs',
            'event': event
        }
        return render(request, 'event_update.html', context)

    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        e_start = request.POST['e_start']
        e_end = request.POST['e_end']
        uploadedFile = request.FILES.get("uploadedFile")

        if len(re.findall(r'[^a-z | 0-9 | . | " " | ( | )]', uploadedFile.name)) > 0:
            return HttpResponse(f'''
                <script>
                    alert("파일 이름에 특수문자가 포함되어 있습니다!");
                    history.back();
                </script>
            ''')

        Photo_Upload(title=uploadedFile.name, photo=uploadedFile).save()

        event = Board.objects.get(pk=pk)
        event.title = title
        event.content = content
        event.e_start = e_start
        event.e_ent = e_end
        event.save()
        
        context = {
            'session': request.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cs',
            'pk': event.pk
        }

        photo = B_Photo.objects.get(board=event)
        photo.photo = f'/static/image/{uploadedFile}'
        photo.save()

        return render(request, 'event_updateOk.html', context)



def event_delete(request):
    if request.method == 'POST':
        id = request.POST['id']
        event = Board.objects.get(id=id)
        event.delete()

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs'
    }
    return render(request, 'event_deleteOk.html', context)


# 1:1문의 페이지
def oto_write(request):
    if request.method == 'GET':        
        context = {
            'session': request.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cs'
        }
        context['user'] = User.objects.get(id=request.session['user'])

        return render(request, 'oto_write.html', context)
    
    elif request.method == 'POST':
        user = User.objects.get(id=request.session['user'])
        title = request.POST['title']
        contents = request.POST['contents']

        oto = Inquire(user = user, title=title, contents=contents)
        oto.save()
        
        return render(request, 'oto_writeOk.html', {"pk": oto.pk})


def oto_detail(request, pk): 
    oto = Inquire.objects.get(pk=pk)

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs',
        'oto': oto
    }

    context['user'] = User.objects.get(id=request.session['user'])
    
    return render(request, 'oto_detail.html', context)


def oto_list(request):
    try:
        if request.session['admin']:
            all_otos = Inquire.objects.all().order_by('-reg_date')

        else:
            all_otos = Inquire.objects.filter(user=User.objects.get(id=request.session['user'])).order_by('-reg_date')
        
        page = int(request.GET.get('p', 1))
        paginator = Paginator(all_otos, 5)
        otos = paginator.get_page(page)

        context = {
            'session': request.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cs',
            'otos': otos,
        }

        return render(request, 'oto_list.html', context)
        
    except:
        return HttpResponse(f'''
        
            <script>
                alert("로그인이 필요합니다.");
                location.href='/whitevalley/cs/oto_loading/';
            </script>
        ''')
  

def oto_answer(request, pk):
    if request.method == 'GET':
        oto = Inquire.objects.get(pk=pk)
        context = {
            'session': request.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cs',
            'oto': oto
        }
        
        return render(request, 'oto_answer.html', context)

    elif request.method == 'POST':
        title = request.POST['title']
        contents = request.POST['contents']
        answer = request.POST['answer']

        oto = Inquire.objects.get(pk=pk)
        oto.title = title
        oto.contents = contents
        oto.answer = answer
        oto.save()

        return render(request, 'oto_answerOk.html', {"pk": oto.pk})


def oto_loading(request):
    return render(request, 'oto_loading.html')


# FAQ 페이지
def faq_write(request):
    if request.method == 'GET':
        context = {
            'session': request.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cs'
        }
        return render(request, 'faq_write.html', context)

    elif request.method == 'POST':
        user = User.objects.get(id=request.session['user'])
        tag = request.POST['faq']
        title = request.POST['title']
        content = request.POST['content']

        notice = Board(user=user, title=title, content=content, tag=tag)
        notice.save()
        

        return render(request, 'faq_writeOk.html', {"pk": notice.pk})


def faq_detail(request, pk):
    faq = Board.objects.get(pk=pk)
    faq.view_cnt += 1
    faq.save()

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs',
        'faq': faq
    }
    return render(request, 'faq_detail.html', context)


def faq_list(request):
    keyword = request.GET.get('keyword')
    
    if keyword:
        all_faqs = Board.objects.filter(title__contains=keyword, tag='FAQ')
    else:
        all_faqs = Board.objects.filter(tag='FAQ')
    
    # btn = request.GET.get('btn')
    # if btn:
    #     all_faqs = Board.objects.filter(title__contains=btn)
    # else:
    #     all_faqs = Board.objects.filter(tag='FAQ')

    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_faqs, 7)
    faqs = paginator.get_page(page)

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs',
        'faqs': faqs,
        'all_faqs': all_faqs,
    }
    return render(request, 'faq_list.html', context)


def faq_update(request, pk):
    if request.method == 'GET':
        faq = Board.objects.get(pk=pk)
        context = {
            'session': request.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cs',
            'faq': faq
        }

        return render(request, 'faq_update.html', context)

    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        faq = Board.objects.get(pk=pk)
        faq.title = title
        faq.content = content
        faq.save()

        return render(request, 'faq_updateOk.html', {"pk": faq.pk})


def faq_delete(request):
    if request.method == 'POST':
        id = request.POST['id']
        faq = Board.objects.get(id=id)
        faq.delete()

    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'cs'
    }
    return render(request, 'faq_deleteOk.html', context)
