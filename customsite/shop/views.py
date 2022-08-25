from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
from order.models import R_photo
from user.models import User
from order.models import Cart, Order, Review
from recommendation.models import Product, Tag_list
from cs.models import Board
from shop.models import Config, Co_account
import datetime
from django.core.paginator import Paginator
from django.db.models import Max, Min, Avg, Sum
import itertools

# HOME --------------------------------------------------------------------------------
def home(req):
    context = {
        'cookies': req.COOKIES,
        'session': req.session,
        'currentpage': 'home',
        'notices': Board.objects.filter(tag="공지사항").order_by("-reg_date")[:12],
        'faqs': Board.objects.filter(tag="FAQ").order_by("-reg_date")[:4],
        'magazines': Board.objects.filter(tag="매거진").order_by("-reg_date")[:4]
    }

    # 최초 접속 config 생성 및 admin 계정 생성
    try:
        context['config'] = Config.objects.get(id=1)
    except:
        Config(name='Plain Valley', ceo='양윤직', number='1111-1111111-11', address='독도', email='plainvalley@email.com', site_name='WHITE VALLEY', sale_time='MON-FRIㅣ09:30 - 17:00', lunch_time='LUNCH ㅣ 12:30 - 13:30', holiday='SAT, SUN, HOLIDAY ㅣ OFF', sign_point=5000, return_point=10, review_point=3000, best_point=100000, min_amount=12000, max_point=18000).save()
        return redirect("/whitevalley/")

    try:
        User.objects.get(admin="True")
    except:
        print("어드민 계정 생성")
        User(admin=True, email='admin@email.com', nickname='admin', password='1234', contact='01000000000').save()
        return redirect("/whitevalley/")

    if len(Tag_list.objects.all()) > 0:
        pass
    else:
        List = ['봄', '여름', '가을', '겨울', '데일리', '힙합', '캐주얼', '모던', '러블리', '가족', '친구', '단체', '자유']
        for i in List:
            Tag_list(name=i).save()

    # best cody
    try:
        best_cody = Product.objects.get(id=Order.objects.values('product').annotate(
        count=Count('product')
        ).order_by('-count')[0]['product'])
        context['best_cody'] = best_cody
        context['best_cody_count'] = Order.objects.values('product').annotate(count=Count('product'))[0]['count']
        context['best_cody_tag'] = Tag_list.objects.get(product=best_cody)
    except:
        context['best_cody'] = "완성품없음"
    
    # best tag
    try:
        tag_dict = {}

        for t1 in Tag_list.objects.all():
            maximum = 0
            for t2 in t1.product.all().order_by('-view_cnt'):
                
                if Order.objects.filter(product=t2).count() >= maximum:
                    maximum = Order.objects.filter(product=t2).count()
                    tag_dict[t1.name] = t2

        context['all_tags'] = tag_dict.items()
        context['first_tag'] = tag_dict[next(iter(tag_dict))]
    except:
        context['first_tag'] = "태그없음"

    # best review
    try:
        context['best_review'] = Review.objects.all().order_by('-view_cnt')[0]
        context['best_review_img'] = R_photo.objects.get(review=Review.objects.all().order_by('-view_cnt')[0]).photo
        context['best_review_tag'] = Tag_list.objects.get(product=Review.objects.all().order_by('-view_cnt')[0].order.product)
    except:
        context['best_review'] = "리뷰없음"

    # best seller
    best_seller = Order.objects.values('product').annotate(Sum('amount')).order_by('-amount')

    Dict = {}

    for i in best_seller:
        Dict[Product.objects.get(id=i['product']).user] = Dict.get(Product.objects.get(id=i['product']).user, 0) + Product.objects.get(id=i['product']).type.price * i['amount__sum']

    sorted_dict = sorted(Dict.items(), key = lambda item: item[1], reverse=True)

    cnt = 0
    while 1:
        try:
            sorted_dict[cnt]
        except:
            break

        if sorted_dict[cnt][0].prized == False:
            context['best_seller'] = sorted_dict[cnt]
            today = datetime.date.today()
            first_day = today.replace(day=1)
            if first_day.strftime('%d') == today.strftime('%d'):
                
                user = User.objects.get(id=sorted_dict[cnt][0].id)
                user.point = user.point + Config.objects.get(id=1).best_point
                user.prized = True
                user.save()
                
                break

        cnt += 1


    cookie_name = 'visited'
    cookie_value = True

    context['cookie_name'] = cookie_name
    context['cookie_value'] = cookie_value

    res = render(req, 'home.html', context)

    res.set_cookie(
        key=cookie_name,
        value=cookie_value,
        expires=3600
    )

    return res


# CART ----------------------------------------------------------------------------------
def cart(req):
    try:
        req.session['user']
        context = {
            'session': req.session,
            'config': Config.objects.get(id=1),
            'currentpage': 'cart',
            'carts': Cart.objects.filter(user=User.objects.get(id=req.session['user'])),
            'current_time': datetime.datetime.now() + datetime.timedelta(days=2),
        }
        if req.method == "POST":
            cart = Cart.objects.filter(user=User.objects.get(id=req.session['user']))
            for i in cart:
                i.checked = req.POST['item_all_bool']
                i.save()

        return render(req, 'cart.html', context)
    
    except:
        return HttpResponse(f'''
            <script>
                alert("로그인이 필요합니다.");
                location.href='/whitevalley/shopping/loading2/';
            </script>
        ''')

        

def cart_number(req, id):
    try:
        cart = Cart.objects.get(id=id)

        cart.amount = req.POST['amount']

        cart.save()

        
        return redirect("/whitevalley/cart/")
        
    except:
        return HttpResponse(f'''
            <script>
                alert("올바른 경로가 아닙니다!");
                location.href = "/whitevalley/";
            </script>
        ''')

def cart_checked(req, id):
    try:
        cart = Cart.objects.get(id=id)

        if cart.checked:
            cart.checked = False
        else:
            cart.checked = True

        cart.save()

        
        return redirect("/whitevalley/cart/")

    except:
        return HttpResponse(f'''
            <script>
                alert("올바른 경로가 아닙니다!");
                location.href = "/whitevalley/";
            </script>
        ''')

def cart_delete(req, id):
    try:
        cart = Cart.objects.get(id=id)

        cart.delete()

        return HttpResponse(f'''
            <script>
                alert("제거되었습니다!");
                location.href = '/whitevalley/cart/';
            </script>
        ''')

    except:
        return HttpResponse(f'''
            <script>
                alert("올바른 경로가 아닙니다!");
                location.href = "/whitevalley/";
            </script>
        ''')
    



# ADMIN -----------------------------------------------------------------------------------
def admin(req):
    context = {
        'session': req.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'admin',
    }

    if req.method == "GET":
        try:
            if req.session['admin']:
                return render(req, 'admin.html', context)
            else:
                return HttpResponse(f'''
                    <script>
                        alert("권한이 없습니다!!");
                        location.href='/whitevalley/';
                    </script>
                ''')
            
        except:
            return HttpResponse(f'''
                <script>
                    alert("관리자 계정의 로그인이 필요합니다.");
                    location.href='/whitevalley/login/';
                </script>
            ''')

    elif req.method == "POST":
        config = Config.objects.get(id=1)

        config.name = req.POST['name']
        config.ceo = req.POST['ceo']
        config.email = req.POST['email']
        config.number = req.POST['number']
        config.address = req.POST['address']
        config.site_name = req.POST['site_name']
        config.sale_time = req.POST['sale_time']
        config.lunch_time = req.POST['lunch_time']
        config.holiday = req.POST['holiday']
        config.tag_show = req.POST['tag_expose']

        config.save()

        return redirect('/whitevalley/admin/')


def admin_member(req):
    context = {
        'session': req.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'admin'
    }
    
    if req.method == "GET":
        try:
            if req.session['admin']:
                context['date'] = "전체"
                context['order'] = "가입일순"
                context['users'] = User.objects.filter(admin=False).order_by('-reg_date')
                page = int(req.GET.get('page', 1))
            else:
                return HttpResponse(f'''
                    <script>
                        alert("권한이 없습니다!!");
                        location.href='/whitevalley/';
                    </script>
                ''')
            
        except:
            return HttpResponse(f'''
                <script>
                    alert("관리자 계정의 로그인이 필요합니다.");
                    location.href='/whitevalley/';
                </script>
            ''')
    
    elif req.method == "POST":
        date_filter = req.POST['date_filter']
        context['date'] = date_filter
        order_filter = req.POST['order_filter']
        context['order'] = order_filter
        

        if date_filter == "전체":
            datepicker1 = "2000-01-01"
            datepicker2 = datetime.datetime.now().date() + datetime.timedelta(days=1)
        elif date_filter == "오늘":
            datepicker1 = datetime.datetime.now().date()
            datepicker2 = datetime.datetime.now().date() + datetime.timedelta(days=1)
        elif date_filter == "1주일":
            datepicker1 = datetime.datetime.now().date() + datetime.timedelta(days=-7)
            datepicker2 = datetime.datetime.now().date() + datetime.timedelta(days=1)
        elif date_filter == "1개월":
            datepicker1 = datetime.datetime.now().date() + datetime.timedelta(days=-30)
            datepicker2 = datetime.datetime.now().date() + datetime.timedelta(days=1)
        elif date_filter == "3개월":
            datepicker1 = datetime.datetime.now().date() + datetime.timedelta(days=-90)
            datepicker2 = datetime.datetime.now().date() + datetime.timedelta(days=1)
        elif date_filter == "직접선택":
            datepicker1 = req.POST['datepicker1']
            context['datepicker1_value'] = datepicker1
            datepicker2 = req.POST['datepicker2']
            context['datepicker2_value'] = datepicker2
                

        if order_filter == "가입일순":
            context['order'] = "가입일순"
            context['users'] = User.objects.filter(reg_date__range=[datepicker1, datepicker2]).order_by('-reg_date')
        elif order_filter == "ID순":
            context['order'] = "ID순"
            context['users'] = User.objects.filter(reg_date__range=[datepicker1, datepicker2]).order_by('-id')
        elif order_filter == "닉네임순":
            context['order'] = "닉네임순"
            context['users'] = User.objects.filter(reg_date__range=[datepicker1, datepicker2]).order_by('-nickname')
        elif order_filter == "연락처순":
            context['order'] = "연락처순"
            context['users'] = User.objects.filter(reg_date__range=[datepicker1, datepicker2]).order_by('-contact')

    # 한 페이지에 글 몇개?
    per_page = int(req.session.get('per_page', 5))

    # 현재 몇 페이지?
    page = int(req.GET.get('page', 1))

    # 한페이지당 per_page 씩
    paginator = Paginator(context['users'], per_page)

    # Page는 pagintor에 대한 정보도 담고 있음
    page_obj = paginator.get_page(page)

    write_pages = int(req.session.get('write_pages', 10))
    start_page = (int((page_obj.number - 1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages - 1

    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages

    context['users'] = page_obj
    context['write_pages'] = write_pages
    context['start_page'] = start_page
    context['end_page'] = end_page
    context['page_range'] = range(start_page, end_page + 1)
            
    return render(req, 'admin_member.html', context)


def member_delete(req, id):
    User.objects.get(id=id).delete()

    return HttpResponse(f'''
        <script>
            alert("해당 유저가 회원탈퇴 처리되었습니다!!");
            location.href = '/whitevalley/admin/member/'
        </script>
    ''')


def admin_point(req):
    context = {
        'session': req.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'admin',
    }

    if req.method == "GET":
        try:
            if req.session['admin']:
                return render(req, 'admin_point.html', context)
            else:
                return HttpResponse(f'''
                    <script>
                        alert("권한이 없습니다!!");
                        location.href='/whitevalley/';
                    </script>
                ''')
            
        except:
            return HttpResponse(f'''
                <script>
                    alert("관리자 계정의 로그인이 필요합니다.");
                    location.href='/whitevalley/login/';
                </script>
            ''')

    elif req.method == "POST":
        if (int(req.POST['sign_point']) < 0 or
            int(req.POST['return_point']) < 0 or
            int(req.POST['review_point']) < 0 or
            int(req.POST['best_point']) < 0 or
            int(req.POST['min_amount']) < 0 or
            int(req.POST['max_point']) < 0):
            return HttpResponse(f'''
                <script>
                    alert("0 이상의 숫자를 기입해주세요!");
                    location.href = '/whitevalley/admin/point/'
                </script>
            ''')

        config = Config.objects.get(id=1)

        config.sign_point = req.POST['sign_point']
        config.return_point = req.POST['return_point']
        config.review_point = req.POST['review_point']
        config.best_point = req.POST['best_point']
        config.min_amount = req.POST['min_amount']
        config.max_point = req.POST['max_point']

        config.save()

        return HttpResponse(f'''
            <script>
                alert("수정되었습니다!");
                location.href = '/whitevalley/admin/point/'
            </script>
        ''')


def admin_account(req):
    context = {
        'session': req.session,
        'config': Config.objects.get(id=1),
        'accounts': Co_account.objects.all(),
        'currentpage': 'admin',
    }

    if req.method == "GET":
        try:
            if req.session['admin']:
                return render(req, 'admin_account.html', context)
            else:
                return HttpResponse(f'''
                    <script>
                        alert("권한이 없습니다!!");
                        location.href='/whitevalley/';
                    </script>
                ''')
            
        except:
            return HttpResponse(f'''
                <script>
                    alert("관리자 계정의 로그인이 필요합니다.");
                    location.href='/whitevalley/login/';
                </script>
            ''')

    elif req.method == "POST":

        return redirect('/whitevalley/admin/account/')


def account_add(req):
    bank = req.POST['bank']
    depositer = req.POST['depositer']
    number = req.POST['number']

    try:
        Co_account.objects.get(bank=bank)
        return HttpResponse(f'''
            <script>
                alert("{bank}계좌가 이미 존재합니다!");
                location.href = '/whitevalley/admin/account/'
            </script>
        ''')
    
    except:
        Co_account(bank=bank, depositer=depositer, number=number).save()
        return HttpResponse(f'''
            <script>
                alert("계좌가 추가되었습니다!");
                location.href = '/whitevalley/admin/account/'
            </script>
        ''')
        


def account_delete(req, bank):
    Co_account.objects.get(bank=bank).delete()

    return HttpResponse(f'''
        <script>
            alert("{bank} 계좌가 삭제되었습니다!!");
            location.href = '/whitevalley/admin/account/'
        </script>
    ''')