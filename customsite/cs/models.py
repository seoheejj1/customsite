from django.db import models

class Board(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name="작성자")
    tag = models.CharField(max_length=30, verbose_name='게시글 종류')
    title = models.CharField(max_length=60, verbose_name='제목')
    content = models.TextField(blank=True, verbose_name='내용') 
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    view_cnt = models.IntegerField(default=0, verbose_name='조회수')
    e_start = models.DateField(null=True, verbose_name='이벤트 시작일')
    e_end = models.DateField(null=True, verbose_name='이벤트 종료일')

    class Meta:
        db_table = 't_board'
        verbose_name = '게시글'
        verbose_name_plural = '게시글(들)'

    def __str__(self):
        return self.title

class Inquire(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=60, verbose_name='제목')
    contents = models.TextField(blank=True, verbose_name='내용')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    answer = models.TextField(null=True, verbose_name='답변') 
    answer_date = models.DateTimeField(auto_now=True, verbose_name='답변일')

    class Meta:
        db_table = 't_inquire'
        verbose_name = '답변'
        verbose_name_plural = '답변(들)'

    def __str__(self):
        return f'{self.user}: {self.title}'

class B_Photo(models.Model):
    board = models.ForeignKey('cs.Board', on_delete=models.CASCADE)
    photo = models.CharField(max_length=300, null=True, verbose_name='게시물이미지')

    class Meta:
        db_table = 'b_photo'
        verbose_name = '게시물사진'
        verbose_name_plural = '게시물사진(들)'

class Photo_Upload(models.Model):
    title = models.CharField(max_length=3000)

    photo = models.FileField(upload_to="static/image/")

    class Meta:
        db_table = 'u_photo'