#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

import uuid, os

# 借鉴
from django.db import models
from django import forms
from library import loginSpider

def custom_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename

class Reader(models.Model):
    class Meta:
        verbose_name = '读者'
        verbose_name_plural = '读者'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='读者')
    name = models.CharField(max_length=16, unique=True, verbose_name='姓名')
    phone = models.IntegerField(unique=True, verbose_name='电话')
    max_borrowing = models.IntegerField(default=5, verbose_name='可借数量')
    balance = models.FloatField(default=0.0, verbose_name='余额')
    photo = models.ImageField(blank=True, upload_to=custom_path, verbose_name='头像')

    STATUS_CHOICES = (
        (0, 'normal'),
        (-1, 'overdue')
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
    )

    def __str__(self):
        return self.name

class Book(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'

    ISBN = models.CharField(max_length=13, primary_key=True, verbose_name='ISBN')
    title = models.CharField(max_length=128, verbose_name='书名')
    author = models.CharField(max_length=32, verbose_name='作者')
    press = models.CharField(max_length=64, verbose_name='出版社')

    description = models.CharField(max_length=1024, default='', verbose_name='详细')
    price = models.CharField(max_length=20, null=True, verbose_name='价格')

    category = models.CharField(max_length=64, default=u'文学', verbose_name='分类')
    cover = models.ImageField(blank=True, upload_to=custom_path, verbose_name='封面')
    index = models.CharField(max_length=16, null=True, verbose_name='索引')
    location = models.CharField(max_length=64, default=u'图书馆1楼', verbose_name='位置')
    quantity = models.IntegerField(default=1, verbose_name='数量')

    def __str__(self):
        return self.title + self.author

# class Book(models.Model):
#     # ISBN码
#     ISBN = models.CharField(max_length=100,null=True)
#     # 书名
#     bookName = models.TextField(null=True)
#     # 书籍URL
#     bookUrl = models.CharField(max_length=200,null=True)
#     # 作者
#     author = models.CharField(max_length=200,null=True)
#     # 内容简介
#     content = models.TextField(default="",null=True)
#     # 出版日期
#     publishYear = models.CharField(max_length=50,null=True)
#     # 索书号
#     bookIndex = models.CharField(max_length=50,null=True)
#     # 出版社
#     publisher = models.CharField(max_length=100,null=True)
#     # 目录
#     catalog = models.TextField(null=True)
#     # 系统号
#     systemNumber = models.CharField(max_length=50,default="0",null=True)
#     # 豆瓣ID
#     douBanId = models.CharField(max_length=50,default="0",null=True)
#     # 豆瓣评分
#     doubanRating = models.FloatField(default=0,null=True)
#     # 豆瓣评分人数
#     doubanRatingPeron = models.IntegerField(default=0,null=True)
#     # 丛书系列标题
#     seriesTitle = models.CharField(max_length=70,default="",null=True)
#     # 豆瓣内容摘要
#     doubanSummary = models.TextField(default="",null=True)
#     def __str__(self):
#         return 'name[{name}]'.format(name=self.bookName)


class Borrowing(models.Model):
    class Meta:
        verbose_name = '借阅'
        verbose_name_plural = '借阅'

    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='ISBN')
    date_issued = models.DateField(verbose_name='借出时间')
    date_due_to_returned = models.DateField(verbose_name='应还时间')
    date_returned = models.DateField(null=True, verbose_name='还书时间')
    amount_of_fine = models.FloatField(default=0.0, verbose_name='欠款')

    def __str__(self):
        return '{} 借了 {}'.format(self.reader, self.ISBN)

#
# # 登录表单
# #====================================
# class LoginForm(forms.Form):
#     user = forms.CharField(label='username',max_length=100)
#     password = forms.CharField(label='password',max_length=100)
#     cookietime = forms.CharField(label='cookietime',max_length=100)
#     def is_valid(self):
#         if loginSpider.login(self.data['username'],self.data['password'])[0]:
#             return True
#         else:
#             return False