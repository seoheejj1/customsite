from django.db import models

class Type(models.Model):
    title = models.CharField(max_length=200, primary_key=True, verbose_name='타입명')
    description = models.CharField(max_length=5000, verbose_name='타입설명')
    img = models.CharField(max_length=5000, verbose_name='이미지')
    price = models.IntegerField(default=0, verbose_name='타입가격')

    class Meta:
        db_table = 't_type'
        verbose_name = '타입'
        verbose_name_plural = '타입(들)'

    def __str__(self):
        return self.title

class T_photo(models.Model):
    title = models.ForeignKey('recommendation.Type', on_delete=models.CASCADE, verbose_name="타입명")
    photo = models.CharField(max_length=300, verbose_name='타입이미지')
    color = models.CharField(max_length=300, verbose_name='타입색')

    class Meta:
        db_table = 't_photo'
        verbose_name = '타입사진'
        verbose_name_plural = '타입사진(들)'

    def __str__(self):
        return self.title

        
class Product(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name="작성자")
    type = models.ForeignKey('recommendation.Type', on_delete=models.CASCADE, verbose_name="타입명")
    size = models.CharField(max_length=10, verbose_name='크기')
    request = models.CharField(max_length=200, null=True, verbose_name='요청사항')
    view_cnt = models.IntegerField(default=0, verbose_name='조회수')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='상품등록일')
    img = models.CharField(max_length=300, verbose_name='이미지')

    class Meta:
        db_table = 't_product'
        verbose_name = '상품'
        verbose_name_plural = '상품(들)'

    def __str__(self):
        return f'{self.user}: {self.type}'

class P_photo(models.Model):
    product = models.ForeignKey('recommendation.Product', on_delete=models.CASCADE, verbose_name="상품")
    photo = models.CharField(max_length=300, verbose_name='완성품이미지')

    class Meta:
        db_table = 'p_photo'
        verbose_name = '완성품사진'
        verbose_name_plural = '완성품사진(들)'

    def __str__(self):
        return f'{self.product}: {self.photo}'


class Tag_list(models.Model):
    name = models.CharField(max_length=30, primary_key=True, verbose_name='태그이름')
    product = models.ManyToManyField('recommendation.Product', verbose_name='물품')
    
    class Meta:
        db_table = 't_tag_list'
        verbose_name = '태그'
        verbose_name_plural = '태그(들)'

    def __str__(self):
        return f'{self.name}: {self.product}에 연결됨'