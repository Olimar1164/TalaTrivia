# trivia/management/commands/generate_test_data.py
from django.core.management.base import BaseCommand
from trivia.models import User, Entity, Player, Question, AnswerOption, Trivia, Participation, UserAnswer
import random

class Command(BaseCommand):
    help = 'Generate test data for TalaTrivia'

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_questions()
        self.create_trivias()
        self.create_participations()
        self.stdout.write(self.style.SUCCESS('Successfully generated test data'))

    def create_users(self):
        for i in range(10):
            username = f'user{i}'
            email = f'user{i}@example.com'
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password',
                    name=f'User {i}',
                    role='player'
                )
                if not Entity.objects.filter(user=user).exists():
                    entity = Entity.objects.create(user=user, name=user.name, email=user.email)
                    Player.objects.create(entity=entity, role='player')

    def create_questions(self):
        difficulties = ['easy', 'medium', 'hard']
        for i in range(30):
            question = Question.objects.create(
                question_text=f'Question {i}',
                difficulty=random.choice(difficulties)
            )
            for j in range(4):
                AnswerOption.objects.create(
                    question=question,
                    option_text=f'Option {j} for Question {i}',
                    is_correct=(j == 0)
                )

    def create_trivias(self):
        for i in range(5):
            trivia = Trivia.objects.create(
                name=f'Trivia {i}',
                description=f'Description for Trivia {i}'
            )
            questions = Question.objects.all().order_by('?')[:10]
            trivia.questions.set(questions)


    def create_participations(self):
        users = User.objects.all()
        trivias = Trivia.objects.all()
        for user in users:
            for trivia in trivias:
                for _ in range(2):  # Cada jugador participa 2 veces en cada trivia
                    participation = Participation.objects.create(
                        user=user,
                        trivia=trivia,
                        score=random.randint(0, 30),
                        completed=True
                    )
                    questions = trivia.questions.all()
                    for question in questions:
                        correct_option = question.options.filter(is_correct=True).first()
                        UserAnswer.objects.create(
                            user=user,
                            question=question,
                            selected_option=correct_option
                        )