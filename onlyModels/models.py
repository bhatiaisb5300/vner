from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from utilities.constants import ExamLevel, QuestionType, RoleType

from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    _token = models.CharField(max_length=500, null=True, blank=True)
    username = models.CharField(
        verbose_name="Username",
        max_length=150,
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True, max_length=150)
    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def token(self): return self._token

    def save(self, *args, **kwargs):
        self.username = f"{self.first_name.lower()}_{self.last_name.lower()}"
        return super().save(*args, **kwargs)

class TargetExamType(models.Model):
    class Meta:
        verbose_name = "Target Exam"
        verbose_name_plural = "Target Exams"
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f"{self.name}"

class Subjects(models.Model):
    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f"{self.name}"

class Profile(models.Model):
    user = models.OneToOneField(verbose_name="User", to=User, on_delete=models.CASCADE)
    # personal details
    fname = models.CharField(verbose_name="First Name", max_length=150)
    mname = models.CharField(verbose_name="Middle Name", max_length=150, blank=True, null=True)
    lname = models.CharField(verbose_name="Last Name", max_length=150)
    dob   = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    mobile = models.CharField(verbose_name="Mobile", max_length=20)
    email  = models.EmailField(verbose_name="Email", null=True, blank=True)
    # educational details
    education = models.JSONField(verbose_name="Educational Details", blank=True, null=True)
    # target exams
    target_exams = models.ManyToManyField(verbose_name="Target Exam", to=TargetExamType)
    # role
    role = models.IntegerField(verbose_name="Selected Role", choices=RoleType.choices, default=RoleType.NOT_SELECTED)
    is_completed = models.BooleanField(verbose_name="Is Profile Completed?", default=False)

    def full_name(self):
        return f"{self.fname} {self.mname+' ' if self.mname else ''}{self.lname}"
    
    def personal_details(self):
        return {
            "first_name": self.fname,
            "middle_name": self.mname,
            "last_name": self.lname,
            "date_of_birt": str(self.dob),
            "mobile": self.mobile,
            "email": self.email,
        }
    
    def educational_details(self):
        return self.education
    
    def detail(self):
        return {**self.personal_details, **self.educational_details}

    def save(self, *args, **kwargs):
        if self.pk:
            self.email = self.user.email
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.fname}'s Profile [{self.user.pk}]"


class Option(models.Model):
    opt = models.TextField(verbose_name="Options")

class Answer(models.Model):
    obj_ans = models.ManyToManyField(to=Option, verbose_name="Objective Answer", blank=True)
    sub_ans = models.TextField(verbose_name="Subjective Answer", blank=True, null=True)

class Question(models.Model):
    class Meta:
        verbose_name = "MCQ"
        verbose_name_plural = "MCQs" 
    statement = models.TextField(verbose_name="Question")
    options   = models.ManyToManyField(verbose_name="Options", to=Option)
    answer    = models.OneToOneField(verbose_name="Answer", to=Answer, on_delete=models.CASCADE)
    subject_tags = models.ManyToManyField(verbose_name="Subject Tags", to=Subjects)


class Exam(models.Model):
    name       = models.CharField(verbose_name="Exam Name", max_length=300)
    duration   = models.BigIntegerField(verbose_name="Duration(minutes)")
    questions  = models.ManyToManyField(verbose_name="Questions", to=Question, blank=True)
    exam_level = models.IntegerField(verbose_name="Exam Level", choices=ExamLevel.choices, default=ExamLevel.BEGINNER)
    allowed_attempts = models.IntegerField(verbose_name="Allowed no. of attemps", default=1)

    exam_tags = models.ManyToManyField(verbose_name="Exam Tags", to=TargetExamType)
    created_by = models.ForeignKey(verbose_name="Created By", to=User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)

    last_modified_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    def __str__(self) -> str:
        return f"Exam [ID: {self.pk}]"

class ExamAttempts(models.Model):
    exam = models.ForeignKey(verbose_name="Exam", to=Exam, on_delete=models.CASCADE)
    attempted_by = models.ForeignKey(verbose_name="Attempted by", to=User, on_delete=models.SET_NULL, null=True, blank=True)


# Signals
@receiver(post_save, sender=User)
def initiate_user_profile(sender, instance, **kwargs):
    if instance:
        try:
            profile = instance.profile
        except ObjectDoesNotExist:
            profile = Profile()
            profile.user = instance
            profile.email = instance.email
            profile.fname = instance.first_name
            profile.lname = instance.last_name
        profile.save()