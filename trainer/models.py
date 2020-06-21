from django.db import models
import os
from django.contrib.auth.models import User, Group
from decouple import config
from PIL import Image
from datetime import datetime
from client.models import ClientProfile
from phone_field import PhoneField, PhoneNumber

# Create your models here.


def get_date(**kwargs):
    if kwargs['date'] == "day":
        return [(d, d) for d in range(0, 32)]
    elif kwargs['date'] == "month":
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        return [(m, m) for m in months]
    elif kwargs['date'] == "year":
        years = [y for y in range(1993, datetime.now().year + 6)]
        return [(y, y) for y in years]


def get_file_url(instance, filename):
    return os.path.join('files', str(instance.id), filename)


def profile_pictures(instance, filename):
    return os.path.join('trainer-profile', instance, filename)


def session_types():
    return [(s, s) for s in ['hr', 'day', 'week', 'month', 'year']]


class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=profile_pictures)
    city = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=10, blank=True)
    cell = PhoneField(blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        app_label = 'trainer'
        verbose_name = 'Trainer Profile'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        group = Group.objects.get(name='Trainers')
        group.user_set.add(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not config('ONSERVER', cast=bool):
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return self.user.username


class Certification(models.Model):
    profile = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    issuer = models.CharField(max_length=100)
    date = models.DateField()
    link = models.URLField(blank=True)
    file = models.FileField(upload_to=get_file_url, null=True)

    class Meta:
        managed = True
        app_label = 'trainer'

    def __str__(self):
        return self.profile


class Experience(models.Model):
    profile = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=10)
    country = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    website = models.URLField(null=True)
    from_month = models.CharField(max_length=10, choices=get_date(date='month'))
    from_year = models.IntegerField(choices=get_date(date='year'))
    current_job = models.BooleanField(default=False)
    end_month = models.CharField(max_length=10, choices=get_date(date='month'), blank=True)
    end_year = models.IntegerField(choices=get_date(date='year'), null=True, blank=True)
    description = models.TextField(max_length=600, default="Enter job description")
    extra = models.BooleanField(default=False)

    class Meta:
        managed = True
        app_label = 'trainer'

    def __str__(self):
        return self.position

    def is_current_job(self):
        return self.current_job

    def start_date(self):
        return f'{self.from_month} {self.from_year}'

    def end_date(self):
        return f'{self.end_month} {self.end_year}'


class Package(models.Model):
    profile = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    rate = models.CharField(max_length=10)

    class Meta:
        managed = True
        app_label = 'trainer'


class Service(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        app_label = 'trainer'


class Workout(models.Model):
    # Workout created by a trainer
    profile = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    client = models.ManyToManyField('client.ClientProfile')
    name = models.CharField(max_length=30)
    date = models.DateField()
    time = models.IntegerField(null=True)

    class Meta:
        managed = True
        app_label = 'trainer'

    def __str__(self):
        return self.name


class Session(models.Model):
    # Each workout can have several sessions
    # i.e Warmup session, chest session
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        managed = True
        app_label = 'trainer'

    def __str__(self):
        return self.name


class Round(models.Model):
    # Each Session can have multiple rounds
    # A round can have multiple Exercises of a singular set and can be repeated as needed
    # i.e. 10 squats followed by 10 sit-ups and 10 push ups as one round repeated 3 times
    # A round can also have multiple exercises with independent sets
    # i.e. 3 sets of 10 rep push up, rest and 3 sets of 10 rep sit up
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    round = models.IntegerField()


class Exercise(models.Model):
    round = models.ManyToManyField(Round)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        managed = True
        app_label = 'trainer'

    def __str__(self):
        return self.name


def exercise_image(instance, filename):
    return os.path.join('Exercises', instance.exercise.id, filename)


class ExerciseImage(models.Model):
    excercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=exercise_image)
    caption = models.CharField(max_length=30, null=True)

    class Meta:
        managed = True
        app_label = 'trainer'
        verbose_name = 'Exercise Image'

    def __str__(self):
        return self.excercise


class Equipment(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=30)
    instructions = models.TextField(null=True)

    class Meta:
        managed = True
        app_label = 'trainer'

    def __str__(self):
        return self.name


class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField(null=True)
    timed = models.BooleanField(default=False)
    secs = models.IntegerField(null=True)
    weighted = models.BooleanField(default=False)
    weight = models.IntegerField(null=True)
    metric = models.CharField(max_length=10, choices=[('lbs', 'lbs'), ('kgs', 'kgs')])

    class Meta:
        managed = True
        app_label = 'trainer'

    def __str__(self):
        return self.exercise


class Post(models.Model):
    profile = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    caption = models.TextField()

    class Meta:
        managed = True
        app_label = 'trainer'


def post_images(instance, filename):
    return os.path.join('Post', instance.post.profile, instance, filename)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=post_images)

    class Meta:
        managed = True
        app_label = 'trainer'
        verbose_name = 'Post Image'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not config('ONSERVER', cast=bool):
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)