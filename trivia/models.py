from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='player', **extra_fields):
        if not username:
            raise ValueError('El username es obligatorio')
        if not email:
            raise ValueError('El email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, role='admin', **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, default='player')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'ENTITY'

    def __str__(self):
        return self.name

class Player(models.Model):
    entity = models.OneToOneField(Entity, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('player', 'Player'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='player')

    class Meta:
        db_table = 'PLAYER'

    def __str__(self):
        return f"{self.entity.name} ({self.role})"

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Fácil'),
        ('medium', 'Medio'),
        ('hard', 'Difícil'),
    ]

    question_text = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)

    class Meta:
        db_table = 'QUESTION'

    def __str__(self):
        return self.question_text


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'ANSWER_OPTION'

    def __str__(self):
        return self.option_text

    
class Trivia(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField(Question)
    users = models.ManyToManyField('User', through='Participation')
    
    class Meta:
        db_table = 'TRIVIA'
    
    def __str__(self):
        return self.name


class Participation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    trivia = models.ForeignKey('Trivia', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'PARTICIPATION'

    def __str__(self):
        return f"{self.user.name} - {self.trivia.name}"
   

class UserAnswer(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)

    class Meta:
        db_table = 'USER_ANSWER'
