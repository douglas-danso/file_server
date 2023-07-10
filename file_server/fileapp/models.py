from django.db import models
from django.urls import reverse
from authentication.models import CustomUser


class File(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='files')
    downloads = models.PositiveIntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
    thumbnail = models.FileField(upload_to='thumbnails/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('fileapp:file_detail', args=[str(self.id)])

class FileSearch(models.Model):
    name = models.CharField(max_length=100)

    def search(self, query):
        return File.objects.filter(title_icontains=query)
    

