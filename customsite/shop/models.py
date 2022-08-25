from tabnanny import verbose
from django.db import models

# Config
class Config(models.Model):
    name = models.CharField(max_length=30, verbose_name="회사명")

    ceo = models.CharField(max_length=40, verbose_name="회사대표")

    number = models.CharField(max_length=30, verbose_name="사업자등록번호")

    address = models.CharField(max_length=600, verbose_name="회사주소")

    email = models.CharField(max_length=100, verbose_name="회사메일")

    site_name = models.CharField(max_length=30, verbose_name="사이트명")

    sale_time = models.CharField(max_length=300, verbose_name="영업시간")

    lunch_time = models.CharField(max_length=300, verbose_name="점심시간")

    holiday = models.CharField(max_length=300, verbose_name="휴일")

    sign_point = models.IntegerField(default=0, verbose_name="회원가입 적립금")

    return_point = models.IntegerField(default=0, verbose_name="구매 반환 적립금")

    review_point = models.IntegerField(default=0, verbose_name="포토후기 적립금")

    best_point = models.IntegerField(default=0, verbose_name="BEST 적립금")

    min_amount = models.IntegerField(default=0, verbose_name="최소 적용 가능 금액")

    max_point = models.IntegerField(default=0, verbose_name="최대 적용 가능 포인트")

    tag_show = models.BooleanField(default=True, verbose_name="태그 노출 여부")

    class Meta:
        db_table = 't_config'
        verbose_name = '환경 설정'
        verbose_name_plural = '환경 설정(들)'

    def __str__(self):
        return self.site_name

# Coporation Account
class Co_account(models.Model):
    bank = models.CharField(max_length=30, primary_key=True, verbose_name="은행명")

    number = models.CharField(max_length=60, verbose_name="계좌번호")

    depositer = models.CharField(max_length=30, verbose_name="예금주")

    class Meta:
        db_table = 't_co_account'
        verbose_name = '회사계좌'
        verbose_name_plural = '회사계좌(들)'

    def __str__(self):
        return self.bank