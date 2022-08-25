from django.shortcuts import render, redirect
from shop.models import Config, Co_account
from django.http import HttpResponse
import urllib.request
from user.models import User
from order.models import Cart, Order, Type_Photo_Upload
from recommendation.models import Type, T_photo, Product, Tag_list
import os.path
import re
import requests
import json
from django.template import loader
# from flask import Flask, session, render_template, request, jsonify, escape


# Create your views here.
def order(request):
    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',
        'types': Type.objects.all()
    }


    if request.method == "POST":
        uploadedFile = request.FILES['image_input']

        try:
            Type.objects.get(title=request.POST['title_input'])
        except:
            if len(re.findall(r'[^a-z | 0-9 | . | " " | ( | )]', uploadedFile.name)) > 0:
                return HttpResponse(f'''
                    <script>
                        alert("파일 이름에 특수문자가 포함되어 있습니다!");
                        history.back();
                    </script>
                ''')

            Type_Photo_Upload(title=uploadedFile.name, photo=uploadedFile).save()

            Type(
                title=request.POST['title_input'],
                description=request.POST['description_input'],
                price=request.POST['price_input'],
                img=f'/static/image/products/{uploadedFile}'
            ).save()
            
            return HttpResponse(f'''
                <script>
                    alert("타입이 추가되었습니다!");
                    location.href='/whitevalley/shopping/order/';
                </script>
            ''')


    if (len(Type.objects.all()) != 0):
        pass
    else:
        Type(title="티셔츠", description="반팔입니다.", img="/static/image/products/shortw.png", price=19800).save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/shortw.png', color="흰색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_yellow.png', color="노란색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_red.png', color="빨간색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_purple.png', color="보라색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_orange.png', color="오렌지색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_navy.png', color="군청색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_ivory.png', color="아이보리색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_green.png', color="초록색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_gray.png', color="회색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_blue.png', color="파란색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_black.png', color="검은색").save()
        T_photo(title=Type.objects.get(title="티셔츠"), photo='/static/image/products/s_babypink.png', color="핑크색").save()
        Type(title="긴팔", description="긴팔입니다.", img="/static/image/products/mtmw.png", price=25800).save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/mtmw.png', color="흰색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_yellow.png', color="노란색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_red.png', color="빨간색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_purple.png', color="보라색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_orange.png', color="오렌지색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_navy.png', color="군청색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_ivory.png', color="아이보리색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_green.png', color="초록색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_gray.png', color="회색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_blue.png', color="파란색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_black.png', color="검은색").save()
        T_photo(title=Type.objects.get(title="긴팔"), photo='/static/image/products/m_babypink.png', color="핑크색").save()
        Type(title="후드티", description="후드입니다.", img="/static/image/products/hoodw.png", price=31200).save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/hoodw.png', color="흰색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_yellow.png', color="노란색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_red.png', color="빨간색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_purple.png', color="보라색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_orange.png', color="오렌지색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_navy.png', color="군청색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_ivory.png', color="아이보리색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_green.png', color="초록색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_gray.png', color="회색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_blue.png', color="파란색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_black.png', color="검은색").save()
        T_photo(title=Type.objects.get(title="후드티"), photo='/static/image/products/h_babypink.png', color="핑크색").save()
        redirect('/whitevalley/shopping/order/')

    try:
        request.session['user']
        
        return render(request, 'order.html', context)

    except:
        return HttpResponse(f'''
            <script>
                alert("로그인이 필요합니다.");
                location.href='/whitevalley/shopping/loading2/';
            </script>
        ''')

def order_delete(req):
    Type.objects.get(title=req.POST['type_delete']).delete()

    return HttpResponse(f'''
        <script>
            alert("성공적으로 타입을 삭제하였습니다!");
            location.href='/whitevalley/shopping/order/';
        </script>
    ''')
        
    
def order_des(request):
    try:
        request.session['user']

        try:
            context = {
                'session': request.session,
                'config': Config.objects.get(id=1),
                'currentpage': 'shopping',
                'type_price': request.GET['type_price'],
                'type_desc': request.GET['type_desc'],
                'type_img': request.GET['type_img'],
                'type_title': request.GET['type_title']
            }
            
            return render(request, 'order_des.html', context)

        except:
            return HttpResponse(f'''
                <script>
                    alert("타입 설정이 완료되지 않았습니다!");
                    location.href='/whitevalley/shopping/order/';
                </script>
            ''')

    except:
        return HttpResponse(f'''
            <script>
                alert("로그인이 필요합니다.");
                location.href='/whitevalley/shopping/loading2/';
            </script>
        ''')

    

def custom1(request):
    try:
        request.session['user']
        try:
            context = {
                'session': request.session,
                'config': Config.objects.get(id=1),
                'currentpage': 'shopping',
                'type_title': request.GET['type_title'],
                'type_price': request.GET['type_price'],
                'type_colors': T_photo.objects.filter(title=Type(title=request.GET['type_title'])),
                'type_current': Type.objects.get(title=Type(title=request.GET['type_title']))
            }

            return render(request, 'custom1.html', context)

        except:
            return HttpResponse(f'''
                <script>
                    alert("타입 설정이 완료되지 않았습니다!");
                    location.href='/whitevalley/shopping/order/';
                </script>
            ''')

    except:
        return HttpResponse(f'''
            <script>
                alert("로그인이 필요합니다.");
                location.href='/whitevalley/shopping/loading2/';
            </script>
        ''')

    

def custom2(request):
    try:
        request.session['user']
        try:
            context = {
                'session': request.session,
                'config': Config.objects.get(id=1),
                'currentpage': 'shopping',
                'color': request.GET.get('color_input'),
                'type_size': request.GET.get('type_size'),
                'type_price': request.GET['type_price'],
                'type_title': request.GET['type_title']
            }

            return render(request, 'custom2.html', context)

        except:
            return HttpResponse(f'''
                <script>
                    alert("타입 설정이 완료되지 않았습니다! 차례대로 진행해 주세요!");
                    location.href='/whitevalley/shopping/order/';
                </script>
            ''')

    except:
        return HttpResponse(f'''
            <script>
                alert("로그인이 필요합니다.");
                location.href='/whitevalley/shopping/loading2/';
            </script>
        ''')



def customend(request):
    try:
        user = User.objects.get(id=request.session['user'])

        try:
            context = {
                'session': request.session,
                'config': Config.objects.get(id=1),
                'currentpage': 'shopping',
                'type_size':request.POST['type_size'],
                'type_price': request.POST['type_price'],
                'type_title': request.POST['type_title'],
                'user': user
            }

            if request.method == "POST":
                if request.POST['t_input'] == "0" and request.POST['s_input'] == "0" and request.POST['i_input'] == "0":
                    return HttpResponse(f'''
                        <script>
                            alert("적어도 하나 이상이 커스텀을 적용시켜 완성해주세요!");
                            history.back();
                        </script>
                    ''')
                else:
                
                    url = request.POST['file_base']

                    mem = urllib.request.urlopen(url).read()
                    cnt = 0
                    name = f'img{cnt}.jpg'

                    while os.path.exists(f'static/image/uploaded_img/{name}'):
                        cnt += 1
                        name = f'img{cnt}.jpg'

                        if os.path.exists(f'static/image/uploaded_img/{name}') == False:
                            break
                        

                    with open(f"static/image/uploaded_img/{name}", mode="wb") as f:
                        f.write(mem)
                        context['img_path'] = f'/static/image/uploaded_img/{name}'
                        print("이미지 저장 완료되었습니다.")

                    return render(request, 'customend.html', context)

        except:
            return HttpResponse(f'''
                <script>
                    alert("커스텀 상품이 초기화됩니다.");
                    history.go(-3);
                </script>
            ''')

    except:
        return HttpResponse(f'''
            <script>
                alert("로그인이 필요합니다.");
                location.href='/whitevalley/shopping/loading2/';
            </script>
        ''')


def payment(request):
    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'accounts': Co_account.objects.all(),
        'currentpage': 'shopping'
    }
    try:
        user = User.objects.get(id=request.session['user'])
    except:
        return HttpResponse(f'''
            <script>
                alert("로그인이 필요합니다.");
                location.href='/whitevalley/shopping/loading2/';
            </script>
        ''')

    context['user'] = user
    cart = Cart.objects.filter(user=user, checked="True")
    context['cart'] = cart

    context['adress'] = user.adress.split("_")

    total_price = 0
    for i in cart:
        total_price += i.product.type.price * i.amount

    if total_price == 0:
        return HttpResponse(f'''
            <script>
                alert("구매하실 수 있는 물품이 없습니다!");
                location.href = '/whitevalley/shopping/order/';
            </script>
        ''')
        
    else:
        context['total_price'] = total_price
        context['total_point'] = (total_price * int(Config.objects.get(id=1).return_point)) // 100

    if request.method == 'POST':
       
        List = []
        for i in range(5):
            List.append(request.POST[f'adress{i}'])

        adress = "_".join(List)

        for i in cart:
            Order(
                user = User.objects.get(id=request.session['user']),
                product = i.product,
                amount = i.amount,
                state = "배송준비",
                delivery_req = request.POST['del_req'],
                r_name = request.POST['receiver'],
                r_adress = adress,
                r_contact = request.POST['contact'],
                r_location = request.POST['location_etc'] if request.POST['location'] == "기타사항" else request.POST['location'],
                r_pw = request.POST['r_pw_etc'] if request.POST['r_pw'] == "기타사항" else request.POST['r_pw']
            ).save()

            i.delete()
        
        
        user.point = user.point + (total_price // 10)

        try:
            user.point = user.point - int(request.POST['use_point'])
        except:
            pass

        user.save()

        return HttpResponse(f'''
            <script>
                alert("구매가 완료되었습니다!!");
                location.href = '/whitevalley/';
            </script>
        ''')

    if request.method == 'GET':
        _context = {'check':False}
        if request.session.get('access_token'):
            _context['check'] = True



    return render(request, 'payment.html', context)
    

def loading(request):
    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',
    }

    product = Product(
        user = User.objects.get(id=request.session['user']),
        type = Type.objects.get(title=request.POST['type_title']),
        size = request.POST['type_size'],
        request = request.POST['order_req'],
        img = request.POST['img_path']
    )

    product.save()

    tag = Tag_list(name=request.POST['product_tag'])

    tag.save()

    tag.product.add(product)

    Cart(user=product.user, product=product, amount=request.POST['order_amount']).save()

    return render(request, 'loading.html',context)

def loading2(request):
    return render(request, 'loading2.html')



def kakaoPayLogic(request):
    if request.method == "GET":
        return render(request,'payment.html')
        
    elif request.method == "POST":
        user = User.objects.get(id=request.session['user'])
        cart = Cart.objects.filter(user=user, checked="True")

        List = []
        for i in range(5):
            List.append(request.POST[f'adress{i}'])

        request.session['r_adress'] = "_".join(List)
        request.session['delivery_req'] = request.POST['del_req']
        request.session['r_name'] = request.POST['receiver']
        request.session['r_contact'] = request.POST['contact']
        request.session['r_location'] = request.POST['location_etc'] if request.POST['location'] == "기타사항" else request.POST['location']
        request.session['r_pw'] = request.POST['r_pw_etc'] if request.POST['r_pw'] == "기타사항" else request.POST['r_pw']
        request.session['use_point'] = request.POST['use_point']
        
        total_price = 0
        for i in cart:
            total_price += i.product.type.price * i.amount

        if total_price == 0:
            return HttpResponse(f'''
                <script>
                    alert("구매하실 수 있는 물품이 없습니다!");
                    location.href = '/whitevalley/shopping/order/';
                </script>
            ''')

        _admin_key = '8c7cf512e39e107d1612cd3f23c6f0ec' # 입력필요
        _url = f'https://kapi.kakao.com/v1/payment/ready'
        _headers = {
            'Authorization': f'KakaoAK {_admin_key}',
        }
        _data = {
            'cid': 'TC0ONETIME',
            'partner_order_id':'partner_order_id',
            'partner_user_id':'partner_user_id',
            'item_name': 'whitevalley 완성품',
            'quantity':'1',
            'total_amount': f'{total_price}',
            'vat_amount':'200',
            'tax_free_amount':'0',
            # 내 애플리케이션 -> 앱설정 / 플랫폼 - WEB 사이트 도메인에 등록된 정보만 가능합니다
            # 등록 : http://IP:8000 
            'approval_url':'http://127.0.0.1:8000/whitevalley/shopping/paySuccess', 
            'fail_url':'http://127.0.0.1:8000/whitevalley/shopping/payFail',
            'cancel_url':'http://127.0.0.1:8000/whitevalley/shopping/payCancel'
        }
        _res = requests.post(_url, data=_data, headers=_headers)
        _result = _res.json()
        request.session['tid'] = _result['tid']

        return redirect(_result['next_redirect_pc_url'])
    



def paySuccess(request):
    _url = 'https://kapi.kakao.com/v1/payment/approve'
    _admin_key = '8c7cf512e39e107d1612cd3f23c6f0ec' # 입력필요
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}'
    }
    _data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'],
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'pg_token': request.GET['pg_token']
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    if _result.get('msg'):
        return HttpResponse(f'''
            <script>
                alert("오류가 발생하였습니다!");
                history.back();
            </script>
        ''')
    else:
        user = User.objects.get(id=request.session['user'])
        cart = Cart.objects.filter(user=user, checked="True")

        for i in cart:
            Order(
                user = User.objects.get(id=request.session['user']),
                product = i.product,
                amount = i.amount,
                state = "배송준비",
                delivery_req = request.session['delivery_req'],
                r_name = request.session['r_name'],
                r_adress = request.session['r_adress'],
                r_contact = request.session['r_contact'],
                r_location = request.session['r_location'],
                r_pw = request.session['r_pw']
            ).save()

            i.delete()
        
        total_price = 0
        for i in cart:
            total_price += i.product.type.price * i.amount

        if total_price == 0:
            return HttpResponse(f'''
                <script>
                    alert("비정상적인 루트입니다!");
                    location.href = '/whitevalley/shopping/payment/';
                </script>
            ''')
            
        else:
            total_point = (total_price * int(Config.objects.get(id=1).return_point)) // 100
            user.point = user.point + total_point
        try:
            user.point = user.point - int(request.POST['use_point'])
        except:
            pass

        user.save()

        return HttpResponse(f'''
            <script>
                alert("결제에 성공하였습니다!");
                location.href="/whitevalley/";
            </script>
        ''')



def payFail(request):
    return HttpResponse(f'''
        <script>
            alert("결제에 실패하였습니다!");
            history.back();
        </script>
    ''')
def payCancel(request):
    return HttpResponse(f'''
        <script>
            alert("결제가 취소되었습니다!");
            history.back();
        </script>
    ''')

