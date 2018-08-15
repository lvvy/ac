# coding:utf-8
from django.db import models
from django.conf import settings


class CommonInfo(models.Model):
    name = models.CharField(u'名称', max_length=50)
    add_time = models.DateField(u'添加时间', auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        if settings.VER == 3:
            return self.name
        return self.name.encode('utf-8')


class Personage(CommonInfo):
    """涉及人物"""
    POSITION = (
        (1, u'国家领导人'),
        (2, u'元帅'),
        (3, u'上将')
    )
    SEX = (
        (1, u'男'),
        (2, u'女')
    )
    TYPE = (
        (1, u'人物'),
        (2, u'军队')
    )
    birthday = models.DateField(blank=True, null=True)
    die = models.DateField(blank=True, null=True)
    position = models.IntegerField(u'职位', default=0, choices=POSITION)
    sex = models.IntegerField(u'性别', default=1, choices=SEX)
    abstract = models.TextField(u'简介', blank=True, null=True)
    type = models.IntegerField(u'类型', choices=TYPE, default=1)
    nation = models.ForeignKey("Country", verbose_name=u'国家', blank=True, null=True,on_delete=models.CASCADE)

    class Meta:
        db_table = "war_personage"
        verbose_name = u'涉及人物'

    @property
    def photo(self):
        if not hasattr(self, '_photo'):
            self._photo = Photo.objects.filter(type=2, relation=self.id).first()
        return self._photo

    @property
    def photos(self):
        if not hasattr(self, '_photos'):
            self._photos = Photo.objects.filter(type=2, relation=self.id).all()
        return self._photos


class Event(CommonInfo):
    """保存事件记录"""
    TYPE = (
        (1, u'战役'),
        (10, u'其他')
    )

    personage = models.ManyToManyField(Personage, verbose_name=u'参与者')
    abstract = models.TextField(u'摘要', blank=True, null=True)
    detail = models.TextField(u'详情', blank=True, null=True)
    location = models.ForeignKey("Country", blank=True, null=True, verbose_name=u'发生地', on_delete=models.CASCADE,)
    deaths = models.IntegerField(u'死亡人数', default=0, blank=True, null=True)
    begin_time = models.DateField(u'开始时间', blank=True, null=True)
    end_time = models.DateField(u'结束时间', blank=True, null=True)
    type = models.IntegerField(u'事件类型', blank=True, null=True, choices=TYPE, default=1)

    class Meta:
        db_table = "war_event"
        verbose_name = u'事件记录'


class Country(CommonInfo):
    """国家详情"""
    CONTINENT = (
        (1, u'亚洲'),
        (2, u'欧洲'),
        (3, u'非洲'),
        (4, u'大洋洲'),
        (5, u'北美洲'),
        (6, u'南美洲'),

    )
    TYPE = (
        (0, u'中立'),
        (1, u'同盟国'),
        (-1, u'轴心国')
    )
    LEVEL = (
        (0, u'国家'),
        (1, u'地区')
    )
    leader = models.ForeignKey(Personage, verbose_name=u'领导人',on_delete=models.CASCADE,)
    abstract = models.TextField(u'摘要', blank=True, null=True)
    continent = models.IntegerField(u'大州', choices=CONTINENT)
    latitude = models.CharField(u'纬度', blank=True, null=True, max_length=20)
    longitude = models.CharField(u'经度', blank=True, null=True, max_length=20)
    level = models.IntegerField(choices=LEVEL)
    type = models.IntegerField(u'类型', default=0, choices=TYPE)
    pid = models.IntegerField(u'父ID', default=0, blank=True, null=True)


    class Meta:
        db_table = "war_country"
        verbose_name = u'国家/地区'

    @property
    def photo(self):
        if not hasattr(self, '_photo'):
            self._photo = Photo.objects.filter(type=1, relation=self.id).first()
        return self._photo

    @property
    def photos(self):
        if not hasattr(self, '_photos'):
            self._photos = Photo.objects.filter(type=1, relation=self.id).all()
        return self._photos


class Armament(CommonInfo):
    MODEL = (
        (1, 'fire'),
        (2, 'fire')
    )
    model = models.IntegerField(u'型号', default=0, choices=MODEL)
    country = models.ManyToManyField(Country, verbose_name=u'所属国家', )

    class Meta:
        db_table = "war_armament"
        verbose_name = u'军备/武器'


class Photo(CommonInfo):
    TYPE = (
        (1, u'国家'),
        (2, u'人物'),
        (3, u'事件'),
        (4, u'装备')
    )
    type = models.IntegerField(u'所属类型', blank=True, null=True, default=0, choices=TYPE)
    relation = models.IntegerField(u'关联外键', blank=True, null=True, default=0)
    url = models.CharField(u'图片地址', blank=True, null=True, max_length=150)
    abstract = models.TextField(u'摘要', blank=True, null=True)
