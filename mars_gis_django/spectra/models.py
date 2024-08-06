# from django.db import models ###usui, sqlite3(default)の場合
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.contrib.gis.db import models ###usui, geodjango, postgisの場合
from accounts.models import Project

class Spectrum(models.Model):
    instrument = models.CharField(max_length=10)
    obs_id = models.CharField(max_length=50, blank=True)
    path = models.TextField()
    image_path = models.TextField()
    x_pixel = models.IntegerField()
    y_pixel = models.IntegerField()
    x_image_size = models.IntegerField()
    y_image_size = models.IntegerField()
    wavelength = models.TextField()
    reflectance = models.TextField()
    # band_number = models.IntegerField()
    mineral_id = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    point = models.PointField(null=True, blank=True) ###usui, PointFieldはgeodjangoによるもの
    description = models.TextField(null=True, blank=True)
    permission = models.TextField(default="private")
    share_project = models.ManyToManyField(Project)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    # spectra_collection_id = models.IntegerField()
    data_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.instrument}___{self.obs_id}"
        # return "%s_%s(%s)" % (self.instrument, self.id,self.user)



from django.contrib.auth.models import Group
class Collection(models.Model):
    created_date = models.DateTimeField()
    description = models.TextField()
    owner = models.CharField(max_length=20)
    spectra = models.ManyToManyField(Spectrum)

    # group = models.ForeignKey(Group, on_delete=models.CASCADE)#collectionとgroupが直接結びつくのはよく分からない
#defaultでcollectionにspectrumついか
#ユーザが見るのはcollectionでいいんではないか
#spectrumからcollectionにいちいち追加するのはユーザが面倒臭がると思うから
#解析段階ではgroupまででも、最終的な結果は一般公開するかもよ？
#Groupの管理はadminじゃないほうがいいかも -> 独自開発？
#collectionごとにどこまで公開するかは変わってくる
#collectionはgroup毎じゃない
#個人のcollection, groupに公開するcollection, 全体に公開するcollection...

#研究課題は？
#今あるのはなに？ないのは？他のプロジェクトは？
#IFFFとか、アノテーション使える有名なサイトと比較しろ

class MineralList(models.Model):
    list_id = models.IntegerField()
    mineral = models.TextField()
