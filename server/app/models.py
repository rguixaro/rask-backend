from django.db import models

class Session(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    urls_created = models.IntegerField(default=0)

    def __str__(self):
        return self.id

class Link(models.Model):
    url = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Session, on_delete=models.CASCADE)
    visits = models.IntegerField(default=0)

    def __str__(self):
        return self.slug
    
