from django.db import models
from recommendation.models import Product

class Order(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name="구매자")
    product = models.ForeignKey('recommendation.Product', on_delete=models.CASCADE, verbose_name='상품번호')
    amount = models.IntegerField(verbose_name='상품갯수')
    date = models.DateTimeField(auto_now_add=True, verbose_name='구매일')
    state = models.CharField(max_length=10, verbose_name='상태')
    reviewed = models.BooleanField(default=False, verbose_name='리뷰작성여부')
    delivery_req = models.CharField(max_length=100, null=True, verbose_name='배송요청사항')
    r_name = models.CharField(max_length=80, verbose_name='받는분이름')
    r_adress = models.CharField(max_length=300, verbose_name='받는분주소')
    r_contact = models.CharField(max_length=300, verbose_name='연락처')
    r_location = models.CharField(max_length=80, verbose_name='배송위치')
    r_pw = models.CharField(max_length=80, null=True, verbose_name='공동현관비밀번호')

    class Meta:
        db_table = 't_order'
        verbose_name = '주문'
        verbose_name_plural = '주문(들)'

    def __str__(self):
        return f'{self.user} {self.product}'

class Cart(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name="디자이너")
    product = models.ForeignKey('recommendation.Product', on_delete=models.CASCADE, verbose_name="완성품")
    checked = models.BooleanField(default=True, verbose_name='체크여부')
    amount = models.IntegerField(default=1, verbose_name='갯수')

    class Meta:
        db_table = 't_cart'
        verbose_name = '장바구니'
        verbose_name_plural = '장바구니(들)'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user} {self.product}'

class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="주문번호")
    title = models.CharField(max_length=70, verbose_name='후기제목')
    contents = models.CharField(max_length=300, verbose_name='후기내용')
    view_cnt = models.IntegerField(default=0, verbose_name='후기조회수')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    class Meta:
        db_table = 't_review'
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰(들)'

    def __str__(self):
        return f'{self.order.product.id} {self.title}'

class R_photo(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, verbose_name="주문번호")
    photo = models.CharField(max_length=300, verbose_name='사진')
    
    class Meta:
        db_table = 'r_photo'
        verbose_name = '리뷰사진'
        verbose_name_plural = '리뷰사진(들)'

    def __str__(self):
        return f'{self.review} {self.photo}'

class Review_photo_Upload(models.Model):
    title = models.CharField(max_length=3000)
    photo = models.FileField(upload_to="static/image/product_review/")

    class Meta:
        db_table = 'u_photos'

class Type_Photo_Upload(models.Model):
    title = models.CharField(max_length=3000)

    photo = models.FileField(upload_to="static/image/products/")

    class Meta:
        db_table = 't_photo_upload'