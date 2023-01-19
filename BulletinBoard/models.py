
from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    text = models.TextField()

    #get a propper view for the admin panel
    def __str__(self):
        return f'{self.text}'


class Advert(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now_add=True)
    editTime = models.DateTimeField(null=True, blank=True)
    upload = models.FileField(upload_to='uploads/', null=True, blank=True)

    def preview(self):
        return f"{self.title[0:123]}..."
  
    def get_file_name(self):
        return f"{self.upload.name.split('/')[1]}"

    def if_picture(self):
        ext = ['jpg', 'png', 'bmp', 'jpeg', 'gif']
        exention = self.upload.name.split('/')[1].split('.')[1]
        if exention in ext:
            return True
  
    #get a propper view for the admin panel
    def __str__(self):
        return f"{self.title.title()}: {self.text[:20]} ... Created: {self.createTime.strftime('%d/%m/%Y %H:%M:%S')}"


class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    
    #get a propper view for the admin panel
    def __str__(self):
        return f"{self.text}: ... Created: {self.createTime}"

