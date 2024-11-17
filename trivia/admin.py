from django.contrib import admin
from .models import AnswerOption, Player, Question, User, Trivia, Participation, UserAnswer, Entity


admin.site.register(User)
admin.site.register(Question)
admin.site.register(Trivia)
admin.site.register(Participation)
admin.site.register(AnswerOption)
admin.site.register(Player)
admin.site.register(Entity)
admin.site.register(UserAnswer)
