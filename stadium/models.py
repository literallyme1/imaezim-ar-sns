from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    score = models.IntegerField(default=1000)

    def __str__(self):
        return self.username

class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.CharField(max_length=10)  # 'win' or 'lose'
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.result}"
