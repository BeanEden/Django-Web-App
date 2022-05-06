from django.conf import settings
from django.db import models
from PIL import Image


class Ticket(models.Model):
    titre = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TicketContributor', related_name='ticket_contributions')
    image = models.ImageField(null=True, blank=True)
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

    def review_done(self, *args, **kwargs):
        self.review_associated = True


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    contributors = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='ReviewContributor', related_name='review_contributions')
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
    word_count = models.IntegerField(null=True)

    def _get_word_count(self):
        return len(self.body.split(' '))

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        self.ticket.review_associated = False
        super().save(*args, **kwargs)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_user')

    class Meta:
        unique_together = ('user', 'followed_user')


# class FollowedUsers(models.Model):
#     # followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_user')
#     user_name = models.CharField(max_length=128)

    # blog/models.py
class TicketContributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    contribution = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('user', 'ticket')


class ReviewContributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    contribution = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('user', 'review')

class UserFollowing(models.Model):
    user_id = models.ForeignKey("User", related_name="following")

    following_user_id = models.ForeignKey("User", related_name="followers")

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)