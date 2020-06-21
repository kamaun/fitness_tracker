from django.contrib.auth.models import User, Group
from phone_field import PhoneField, PhoneNumber
from django.db import models
from decouple import config
from PIL import Image
import os
from trainer import models as trainer_models


# Create your models here.

def profile_picture(instance, filename):
    return os.path.join('client-profile', instance, filename)


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    cell = PhoneField(blank=True)
    trainer = models.ForeignKey('trainer.TrainerProfile', on_delete=models.DO_NOTHING)
    image = models.ImageField(default='default.jpg', upload_to=profile_picture)
    bio = models.TextField(blank=True)

    class Meta:
        managed = True
        app_label = 'client'
        verbose_name = 'Client Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        group = Group.objects.get(name='Clients')
        group.user_set.add(self.user)

        if not config('ONSERVER', cast=bool):
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class BodyComposition(models.Model):
    profile = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    date = models.DateField()
    height = models.IntegerField()
    weight = models.IntegerField()
    bmi = models.IntegerField(verbose_name='Body Mass Index(BMI)')

    circumference_neck_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_neck_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_chest_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_chest_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_waist_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_waist_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_hips_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_hips_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_thighs_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_thighs_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_calves_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_calves_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_biceps_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    circumference_biceps_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Waist-to-Hip Ratio')

    skinfold_subscapular_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skinfold_subscapular_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skinfold_iliac_crest_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skinfold_iliac_crest_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skinfold_triceps_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skinfold_triceps_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skinfold_biceps_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skinfold_biceps_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    totals_one = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    totals_two = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        managed = True
        app_label = 'client'
        verbose_name = 'Body Composition'

    def __str__(self):
        return self.profile


def rating(check):
    if check == 'ymca':
        return [(y, y) for y in range(1, 11)]
    else:
        return [(r, r) for r in range(1, 6)]


class CardiorespiratoryAssessment(models.Model):
    profile = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    date = models.DateField()
    rhr = models.IntegerField(verbose_name='Resting Heart Rate')
    hr_max = models.IntegerField(verbose_name='Max Heart Rate')
    bp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Blood Pressure')
    ymca_rhr = models.IntegerField(verbose_name='Resting Heart Rate')
    ymca_rating = models.IntegerField(choices=rating('ymca'), verbose_name='Rating')
    rockport_time = models.IntegerField(verbose_name='Time')
    rockport_hr = models.IntegerField(verbose_name='Heart Rate ')
    rockport_ox_score = models.DecimalField(verbose_name='Oxygen Score', max_digits=8, decimal_places=4)

    class Meta:
        managed = True
        app_label = 'client'
        verbose_name = 'Cardiorespiratory Assessment'

    def __str__(self):
        return self.profile


class DynamicPosturalAssessment(models.Model):
    profile = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    date = models.DateField()

    # Overhead Squat
    overhead_squat_foot_observation = models.CharField(max_length=200, blank=True)
    overhead_squat_left_foot_notes = models.CharField(max_length=200, blank=True)
    overhead_squat_right_foot_notes = models.CharField(max_length=200, blank=True)
    overhead_squat_knee_movement = models.CharField(choices=[('In', 'In'), ('Out', 'Out')], max_length=4, blank=True)
    overhead_squat_left_knee_notes = models.CharField(max_length=200, blank=True)
    overhead_squat_right_knee_notes = models.CharField(max_length=200, blank=True)
    overhead_squat_LPHC_excessive_forward_lean = models.CharField(max_length=200, blank=True)
    overhead_squat_LPHC_low_back_arches = models.CharField(max_length=200, blank=True)
    overhead_squat_shoulder_arms_falling_forward = models.CharField(max_length=200, blank=True)

    # Single - Leg Squat
    single_leg_squat_knee_movement = models.CharField(choices=[('In', 'In'), ('Out', 'Out')], max_length=4, blank=True)
    single_leg_squat_left_knee_notes = models.CharField(max_length=200, blank=True)
    single_leg_squat_right_knee_notes = models.CharField(max_length=200, blank=True)

    # Pushing / Pulling
    LPHC_low_back_arch_pull_notes = models.CharField(max_length=200, blank=True)
    LPHC_low_back_arch_push_notes = models.CharField(max_length=200, blank=True)
    shoulder_elevation_pull = models.CharField(max_length=200, blank=True)
    shoulder_elevation_push = models.CharField(max_length=200, blank=True)
    head_forward_movement_pull = models.CharField(max_length=200, blank=True)
    head_forward_movement_push = models.CharField(max_length=200, blank=True)

    overactive_muscles = models.CharField(max_length=200, blank=True)
    under_active_muscles = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = True
        app_label = 'client'
        verbose_name = 'Dynamic Postural Assessment'


class ClientReadinessForExercise(models.Model):
    profile = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    date = models.DateField()

    # Physical Activity Readiness Questionnaire(PAR - Q)
    heart_condition = models.BooleanField(default=False)
    chest_pain_during_activity = models.BooleanField(default=False)
    chest_pain_without_activity = models.BooleanField(default=False)
    balance_or_consciousness_loss = models.BooleanField(default=False)
    bone_or_joint_problem = models.BooleanField(default=False)
    heart_blood_medication = models.BooleanField(default=False)
    reason_for_not_exercising = models.BooleanField(default=False)

    # General and Medical History
    # Occupational
    current_occupation = models.CharField(max_length=200, blank=True)
    sedentary_occupation = models.BooleanField(default=False)
    active_occupation = models.BooleanField(default=False)
    active_occupation_description = models.BooleanField(default=False)
    occupation_with_dress_shoes = models.BooleanField(default=False)
    occupation_mental_stress = models.BooleanField(default=False)

    # Recreational
    recreational_physical_activities = models.CharField(max_length=200, blank=True)
    additional_hobbies = models.CharField(max_length=200, blank=True)

    # Medical
    injuries_or_chronic_pain = models.CharField(max_length=200, blank=True)
    surgeries = models.CharField(max_length=200, blank=True)
    chronic_diseases = models.CharField(max_length=200, blank=True)
    medication = models.CharField(max_length=200, blank=True)

    additional_information = models.TextField()

    class Meta:
        managed = True
        app_label = 'client'
        verbose_name = 'Client Readiness For Exercise'


class StaticPosturalAssessment(models.Model):
    profile = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    date = models.DateField()

    # Anterior View
    anterior_foot_observation = models.CharField(max_length=200, blank=True)
    anterior_knee_observation = models.CharField(max_length=200, blank=True)
    anterior_LPHC_observation = models.CharField(max_length=200, blank=True)
    anterior_shoulder_observation = models.CharField(max_length=200, blank=True)
    anterior_head_observation = models.CharField(max_length=200, blank=True)

    # Posterior View
    posterior_foot_observation = models.CharField(max_length=200, blank=True)
    posterior_knee_observation = models.CharField(max_length=200, blank=True)
    posterior_LPHC_observation = models.CharField(max_length=200, blank=True)
    posterior_shoulder_observation = models.CharField(max_length=200, blank=True)
    posterior_head_observation = models.CharField(max_length=200, blank=True)

    # Lateral View
    lateral_foot_observation = models.CharField(max_length=200, blank=True)
    lateral_knee_observation = models.CharField(max_length=200, blank=True)
    lateral_LPHC_observation = models.CharField(max_length=200, blank=True)
    lateral_shoulder_observation = models.CharField(max_length=200, blank=True)
    lateral_head_observation = models.CharField(max_length=200, blank=True)

    # Evidence of Postural Distortion Syndrome?
    lower_crossed = models.CharField(max_length=200, blank=True)
    upper_crossed = models.CharField(max_length=200, blank=True)
    pronation_distortion = models.CharField(max_length=200, blank=True)

    shortened_muscles = models.CharField(max_length=200, blank=True)
    lenghened_muscles = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = True
        app_label = 'client'
        verbose_name = 'Static Postural Assessment'