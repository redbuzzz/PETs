from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.core.mail import send_mail
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="auth_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="auth_user_set",
        related_query_name="user",
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Executor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="executor")

    def __str__(self):
        return str(self.user)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")

    def __str__(self):
        return str(self.user)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_customer = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class Task(models.Model):
    title = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, blank=False, null=True
    )
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return self.title


class Bid(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.PositiveIntegerField()

    def __str__(self):
        return f"{str(self.task)}"


class Order(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.PositiveIntegerField()
    STATUS_CHOICES = (
        ("active", "Active"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_reviews"
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="customer_reviews",
        null=True,
        blank=True,
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        related_name="executor_reviews",
        null=True,
        blank=True,
    )
    text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("author", "customer", "executor")
        indexes = [
            models.Index(fields=["author", "customer", "executor"]),
        ]


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.text}"


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
