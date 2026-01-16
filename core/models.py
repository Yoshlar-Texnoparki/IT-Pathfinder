from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)
    test_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Design', 'Design'),
        ('Mobile', 'Mobile'),
    ]
    text = models.TextField()
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True) # Optional direct mapping

    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    weight_category = models.CharField(max_length=20, choices=Question.CATEGORY_CHOICES)
    weight_value = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.question.id} - {self.text}"

class Result(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    scores = models.JSONField()
    top_category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.top_category}"
