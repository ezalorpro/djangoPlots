from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

genero = (
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
)


class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='plots', default='plots/default.png')
    location = models.CharField(max_length=140)
    gender = models.CharField(max_length=140, choices=genero)
    information = models.TextField()

    def __str__(self):
        return 'Usuario: {}'.format(self.username)

    def save(self, *args, **kwargs):
        try:
            this = UserModel.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass
        super(UserModel, self).save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    post_text = models.TextField()
    post_date = models.DateTimeField(editable=False)
    post_modified = models.DateTimeField(editable=False)

    def __str__(self):
        return (
            f'Post de {self.user.username:<40} - Titulo: {self.title:>60} - Ultima modificacion:'
            f' {self.post_date}'
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.post_date = timezone.now()
        self.post_modified = timezone.now()
        return super(Post, self).save(*args, **kwargs)
