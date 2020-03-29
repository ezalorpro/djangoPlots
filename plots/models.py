from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

genero = (
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='plots', default='plots/default.png')
    location = models.CharField(max_length=140)
    gender = models.CharField(max_length=140, choices=genero)
    information = models.TextField()

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)
    
    def save(self, *args, **kwargs):
        try:
            this = UserProfile.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass
        super(UserProfile, self).save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    post_text = models.TextField()
    post_date = models.DateTimeField(editable=False)
    post_modified = models.DateTimeField(editable=False)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.post_date = timezone.now()
        self.post_modified = timezone.now()
        return super(Post, self).save(*args, **kwargs)
        
