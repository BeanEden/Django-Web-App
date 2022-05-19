from django.conf import settings
from django.db import models
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    titre = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default="default_book.png")
    time_created = models.DateTimeField(auto_now_add=True)
    review_associated = models.BooleanField(default=False)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def review_done(self):
        self.review_associated = True

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self))

                # if field.verbose_name != 'genre'
                #
                # else
                # (field.verbose_name,
                #  Genre.objects.get(pk=field.value_from_object(self)).name)

                for field in self.__class__._meta.fields[1:]
                ]

class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.ticket.review_associated = False
        super().save(*args, **kwargs)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # def create