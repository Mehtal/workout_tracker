from django.db import models
from django.urls import reverse
from django.utils import timezone
from accounts.models import User


class Musclegroup(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# class Muscle(models.Model):
#     name = models.CharField(max_length=20)
#     musclegroup = models.ForeignKey('Musclegroup', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


class Exercice(models.Model):
    name = models.CharField(max_length=100)
    primarymg = models.ForeignKey('Musclegroup', on_delete=models.CASCADE)
    # muscle = models.ManyToManyField('Muscle', related_name="muscles")
    secondarymg = models.ManyToManyField('Musclegroup', related_name="secondarymg")
    image = models.ImageField(upload_to="Workout/images")

    class Meta:
        ordering = ['primarymg', 'name']

    def __str__(self):
        return self.name


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now,)
    body_weight = models.PositiveIntegerField(blank=True, null=True)

    def get_body_weight(self):
        if self.body_weight is None:
            weight = Session.objects.filter(body_weight__isnull=False).first()
            self.body_weight = weight.body_weight
            self.save()
        return self.body_weight

    def __str__(self):
        return str(self.date)

    def get_total_volume(self):
        session = self
        total_volume = 0
        for item in session.rep_set.all():
            print(item)
            total_volume += (item.weight * item.repition)
        return f'your total volume is {total_volume}'

    def get_chest_volume(self, pmg_volume=0):
        _pmg = self.rep_set.filter(exercice__primarymg__id=1)
        for obj in _pmg:
            pmg_volume += (obj.weight * obj.repition)
        return pmg_volume

    def get_absolute_url(self):
        return reverse('session_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-date']


class Rep(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    exercice = models.ForeignKey('Exercice', on_delete=models.CASCADE, related_name='exercices')
    repition = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)

    def get_volume(self):
        rep_volume = self.repition * self.weight
        return rep_volume

    def delete_rep(self):
        return self.delete()

    def __str__(self):
        return self.exercice.name + ' ' + str(self.weight)
