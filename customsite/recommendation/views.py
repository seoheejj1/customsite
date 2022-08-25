import datetime
from django.shortcuts import render
from shop.models import Config
from user.models import User
from cs.models import Board
from order.models import Review
from order.models import R_photo, Order, Review_photo_Upload, Cart
from recommendation.models import Product, P_photo, Tag_list
from django.core.paginator import Paginator
from math import ceil
from django.http import Http404, HttpResponse
import re
import urllib 
from urllib.parse import quote_plus 
from urllib.parse import unquote_plus





# 리뷰 리스트
def reviews(request):
   
    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',

    }
    try:
        context['orders'] = Order.objects.filter(user=request.session['user']).order_by('-date')
    except:
        pass

    List = []

    if request.method == "GET":
        for order in Order.objects.all():
            try:
                List.append([Review.objects.get(order=order), R_photo.objects.filter(review=Review.objects.get(order=order))[0]])
            except:
                pass
            
        List = sorted(List, key=lambda r: r[0].reg_date, reverse=True)

    elif request.method == "POST":
        if request.POST['order_selector'] == "new_list":
            context['order_method'] = 'new_list'
            for order in Order.objects.all():
                try:
                    List.append([Review.objects.get(order=order), R_photo.objects.filter(review=Review.objects.get(order=order))[0]])
                except:
                    pass
            List = sorted(List, key=lambda r: r[0].reg_date, reverse=True)
            
        else:
            context['order_method'] = 'good_list'
            for order in Order.objects.all():
                try:
                    List.append([Review.objects.get(order=order), R_photo.objects.filter(review=Review.objects.get(order=order))[0]])
                except:
                    pass
            
            List = sorted(List, key=lambda r: r[0].view_cnt, reverse=True)

    context['reviews'] = List


    write_pages = int(request.session.get('write_pages', 5)) # 페이징당 몇개의 페이지가 표시되는지
    page = request.GET.get('page', '1')
    paginator = Paginator(List, 9)  # 페이지당 몇개씩 보여주기
    page_obj = paginator.get_page(page)
    context['question_list'] = page_obj

    start_page = ((int)((page_obj.number - 1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages - 1

    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages

    context['write_pages']= write_pages
    context['start_page']= start_page
    context['end_page']= end_page
    context['page_range']= range(start_page, end_page + 1)

    reviews2 = []
    List = reviews2
    context['reviews2'] = page_obj

    return render(request, 'reviews.html',context)

    

       

# 리뷰작성 (order id)
def product_reviews(request, id):
    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',
        'order' : Order.objects.get(id=id),
    }
    context['user'] = User.objects.get(id=request.session['user'])
    if request.method == 'GET':
        return render(request, 'product_reviews.html', context)

    elif request.method == 'POST':
        title = request.POST['title']
        contents = request.POST['contents']
        uploadedFile = request.FILES["uploadedFile"]

        if len(re.findall(r'\W | [^.]', uploadedFile.name)) > 0:
            return HttpResponse(f'''
                <script>
                    alert("파일 이름에 특수문자가 포함되어 있습니다!");
                    history.back();
                </script>
            ''')
        Review_photo_Upload(title=uploadedFile.name, photo=uploadedFile).save()
        
        rev = Review(
            order=Order.objects.get(id=id),
            title=title, 
            contents=contents, 
        )

        rev.save()
        
        R_photo(review=rev, photo=f'/static/image/product_review/{uploadedFile.name}').save()

        order = Order.objects.get(id=id)
        order.reviewed = True
        order.save()

        user = User.objects.get(id=request.session['user'])
        user.point = user.point + Config.objects.get(id=1).review_point
        user.save()

        context['pk'] = rev.pk

        return render(request, 'product_reviews_ok.html', context)


# 리뷰 업데이트
def product_reviews_update(request, pk):
    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',
        
    }
    context['user'] = User.objects.get(id=request.session['user'])

    if request.method == 'GET':
        try:
            context['review'] =  Review.objects.get(order=pk)
        except Review.DoesNotExist:
            raise Http404('해당 리뷰를 찾을 수 없습니다.')   
        return render(request, 'product_reviews_update.html', context)

    elif request.method == 'POST':
        title = request.POST['title']
        contents = request.POST['contents']
        uploadedFile = request.FILES["uploadedFile"]
        
        if len(re.findall(r'\W | [^.]', uploadedFile.name)) > 0:
            return HttpResponse(f'''
                <script>
                    alert("파일 이름에 특수문자가 포함되어 있습니다!");
                    history.back();
                </script>
            ''')
        Review_photo_Upload(title=uploadedFile.name, photo=uploadedFile).save()
        
       
        rev = Review.objects.get(pk=pk)
        rev.title = title
        rev.contents = contents
        rev.save()


        

        review = R_photo.objects.get(review=pk)
        review.photo = f'/static/image/product_review/{uploadedFile.name}'
        review.save()

        context['pk'] = review.pk

    return render(request, 'product_reviews_update_ok.html',context)


# 리뷰 디테일
def reviews_detail(request,pk):
    context = {
       'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',
    }

    try:
        review = Review.objects.get(pk=pk)
        context['review'] = review
        photo = R_photo.objects.get(review=review)
        context['photo'] = photo

        review.view_cnt += 1
        review.save()
    except Review.DoesNotExist:
        raise Http404('해당 게시글을 찾을 수 없습니다.')

    if request.method == "POST":
        try:
            Cart(
                user=User.objects.get(id=request.session['user']),
                product=Review.objects.get(pk=pk).order.product,
                amount=1,
                checked=True
            ).save()

            return HttpResponse(f'''
                <script>
                    alert("장바구니에 성공적으로 담겼습니다!");
                    location.href = '/whitevalley/cart/';
                </script>
            ''')
        except:
            return HttpResponse(f'''
                <script>
                    alert("이미 장바구니에 해당 상품이 존재합니다!");
                    history.back();
                </script>
            ''')

    return render(request, 'reviews_detail.html',context)

# 리뷰 삭제
def product_reviews_delete(request, id):
    context = {
       'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping'
    }

    if request.method == 'POST':
        order = Order.objects.get(id=id)
        order.reviewed = False
        order.save()
        
        review = Review.objects.get(order=order)
        review.delete()
        # try:
        # except:
        #     return HttpResponse('''
        #         <script>
        #         alert('리뷰작성이 완료되지 않았습니다.')
        #         </script>
        #     ''')
    

    return render(request, 'product_reviews_delete_ok.html',context)


# 태그 리뷰리스트
def tag_reviews(request):
    
    list = []
    tag_list = {}

    if len(request.GET.getlist("tag",None)) == 0:
        for i in Product.objects.all():
            list.append((i, i.tag_list_set.all()[0].name))
            tag_list[i.tag_list_set.all()[0].name] = tag_list.get(i.tag_list_set.all()[0].name, 0) + 1
    else:
        for i in Product.objects.all():
            tag1 = i.tag_list_set.all()[0].name
            if tag1==request.GET.getlist("tag",None)[0]:
                list.append((i, i.tag_list_set.all()[0].name))
                tag_list[i.tag_list_set.all()[0].name] = tag_list.get(i.tag_list_set.all()[0].name, 0) + 1
        
    
    
    write_pages = int(request.session.get('write_pages', 5)) # 페이징당 몇개의 페이지가 표시되는지
    page = request.GET.get('page', '1')
    
    paginator = Paginator(list, 12)  # 페이지당 몇개씩 보여주기
    page_obj = paginator.get_page(page)
    
    start_page = ((int)((page_obj.number - 1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages - 1

    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages


    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',
        'question_list': page_obj,
        'tag_product' : page_obj,
        'write_pages': write_pages,
        'start_page': start_page,
        'end_page': end_page,
        'page_range': range(start_page, end_page + 1),

    }

    for i in Tag_list.objects.all():
        context[i.name] = tag_list.get(i.name, 1) * 50

    return render(request, 'tag_reviews.html',context)

# 태그 리뷰 디테일
def tag_reviews_detail(request,pk):
    context = {
       'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',
        
    }
    tag_product = Product.objects.get(pk=pk)
    tag_product.save()

    context['tag_product'] = tag_product

    if request.method == "POST":
        try:
            Cart(
                user=User.objects.get(id=request.session['user']),
                product=tag_product,
                amount=1,
                checked=True
            ).save()

            return HttpResponse(f'''
                <script>
                    alert("장바구니에 성공적으로 담겼습니다!");
                    location.href = '/whitevalley/cart/';
                </script>
            ''')
        except:
            return HttpResponse(f'''
                <script>
                    alert("이미 장바구니에 해당 상품이 존재합니다!");
                    history.back();
                </script>
            ''')

    
    # 태그를 불러오는 파트
    tag = Tag_list.objects.filter(product=Product.objects.get(pk=pk))
    context['tag'] = tag

    return render(request, 'tag_reviews_detail.html',context)

# 완성품 리스트
def finished(request):
    context = {
        'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',
    }
    if request.method == "GET":
        all_product = Product.objects.all().order_by('reg_date')
        context['order_method'] = "최신순"
    elif request.method == "POST":
        if request.POST['order_filter'] == "new_list":
            all_product = Product.objects.all().order_by('reg_date')
            context['order_method'] = "최신순"
        else:
            all_product = Product.objects.all().order_by('-view_cnt')
            context['order_method'] = "인기순"

    write_pages = int(request.session.get('write_pages', 5)) # 페이징당 몇개의 페이지가 표시되는지
    page = request.GET.get('page', '1')
    paginator = Paginator(all_product, 9)  # 페이지당 몇개씩 보여주기
    page_obj = paginator.get_page(page)
    
    start_page = ((int)((page_obj.number - 1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages - 1

    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages

    context['write_pages']= write_pages
    context['start_page']= start_page
    context['end_page']= end_page
    context['page_range']= range(start_page, end_page + 1)


    context['question_list'] = page_obj
    context['products'] = page_obj

        
    return render(request, 'finished.html',context)


# 완성품 디테일
def finished_detail(request,pk):
    context = {
       'session': request.session,
        'config': Config.objects.get(id=1),
        'currentpage': 'shopping',

    }
    
    product = Product.objects.get(pk=pk)
    product.view_cnt += 1
    product.save()
    
    context['product'] = product

    if request.method == "POST":
        try:
            Cart(
                user=User.objects.get(id=request.session['user']),
                product=product,
                amount=1,
                checked=True
            ).save()

            return HttpResponse(f'''
                <script>
                    alert("장바구니에 성공적으로 담겼습니다!");
                    location.href = '/whitevalley/cart/';
                </script>
            ''')
        except:
            return HttpResponse(f'''
                <script>
                    alert("이미 장바구니에 해당 상품이 존재합니다!");
                    history.back();
                </script>
            ''')



    return render(request, 'finished_detail.html',context)


def finished_delete(request, id):
    Product.objects.get(id=id).delete()

    return HttpResponse(f'''
        <script>
            alert("완성품이 삭제되었습니다!");
            location.href = '/whitevalley/shopping/finished/';
        </script>
    ''')
          

    