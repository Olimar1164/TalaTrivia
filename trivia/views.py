import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from trivia.models import Player, User, Question, Trivia, Participation, UserAnswer
from trivia.permissions import IsAdminUser, IsPlayerUser
from trivia.serializers import ParticipationSerializer, PlayerCreateSerializer, PlayerListSerializer, QuestionCreateSerializer, QuestionListSerializer, TriviaCreateSerializer, TriviaListSerializer, UserAnswerSerializer, UserCreateSerializer, UserListSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MyTokenRefreshView(TokenRefreshView):
    pass


class PlayerListCreateAPIView(APIView):
    queryset = Player.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlayerCreateSerializer
        return PlayerListSerializer
    
    def get(self, request):
        players = self.queryset.all()
        serializer = self.get_serializer_class()(players, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PlayerDetailAPIView(APIView):
    queryset = Player.objects.all()
    serializer_class = PlayerCreateSerializer
    
    def get(self, request, pk):
        player = self.queryset.get(pk=pk)
        serializer = self.serializer_class(player)
        return Response(serializer.data)
    
    def put(self, request, pk):
        player = self.queryset.get(pk=pk)
        serializer = self.serializer_class(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class UserListCreateAPIView(APIView):
    queryset = User.objects.all()
   
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer
    
    def get(self, request):
        users = self.queryset.all()
        serializer = self.get_serializer_class()(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserDetailAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    
    def get(self, request, pk):
        user = self.queryset.get(pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.queryset.get(pk=pk)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class TriviaListCreateAPIView(APIView):
    queryset = Trivia.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TriviaCreateSerializer
        return TriviaListSerializer
    
    def get(self, request):
        trivias = self.queryset.all()
        serializer = self.get_serializer_class()(trivias, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class TriviaDetailAPIView(APIView):
    queryset = Trivia.objects.all()
    serializer_class = TriviaCreateSerializer
    
    def get(self, request, pk):
        trivia = self.queryset.get(pk=pk)
        serializer = self.serializer_class(trivia)
        return Response(serializer.data)
    
    def put(self, request, pk):
        trivia = self.queryset.get(pk=pk)
        serializer = self.serializer_class(trivia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ParticipationView(View):
    permission_classes = [IsAuthenticated, IsPlayerUser]

    def get(self, request, trivia_id, user_id):
        try:
            participation = Participation.objects.get(trivia_id=trivia_id, user_id=user_id)
            return JsonResponse({
                'user': participation.user.name,
                'trivia': participation.trivia.name,
                'score': participation.score
            })
        except Participation.DoesNotExist:
            return JsonResponse({'error': 'Participation not found'}, status=404)

    @method_decorator(csrf_exempt)
    def post(self, request, trivia_id, user_id):
        data = json.loads(request.body)
        try:
            participation = Participation.objects.get(trivia_id=trivia_id, user_id=user_id)
        except Participation.DoesNotExist:
            participation = Participation.objects.create(trivia_id=trivia_id, user_id=user_id)
        
        # Calculate score based on correct answers
        score = 0
        for question_id, answer in data['answers'].items():
            question = Question.objects.get(id=question_id)
            if question.answer_text == answer:
                if question.difficulty == 'easy':
                    score += 1
                elif question.difficulty == 'medium':
                    score += 2
                elif question.difficulty == 'hard':
                    score += 3
        
        participation.score = score
        participation.save()
        return JsonResponse({'score': participation.score})
    

class RankingView(APIView):
    serializer_class = ParticipationSerializer

    def get_queryset(self):
        trivia_id = self.kwargs.get('trivia_id')
        user_id = self.kwargs.get('user_id')
        if trivia_id and user_id:
            return Participation.objects.filter(trivia_id=trivia_id, user_id=user_id)
        elif trivia_id:
            return Participation.objects.filter(trivia_id=trivia_id)
        elif user_id:
            return Participation.objects.filter(user_id=user_id)
        else:
            return Participation.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        response_data = serializer.data

        # Calcular el puntaje total por usuario
        user_scores = {}
        for participation in queryset:
            user_id = participation.user.id
            if user_id not in user_scores:
                user_scores[user_id] = {
                    'user': participation.user.username,
                    'total_score': 0,
                    'trivias': []
                }
            user_scores[user_id]['total_score'] += participation.score
            user_scores[user_id]['trivias'].append({
                'trivia_name': participation.trivia.name,
                'score': participation.score
            })

        # Convertir el diccionario a una lista ordenada por puntaje total
        ranking = sorted(user_scores.values(), key=lambda x: x['total_score'], reverse=True)

        return Response(ranking)
    


class QuestionListCreateAPIView(APIView):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionListSerializer
    
    def get(self, request):
        questions = self.queryset.all()
        serializer = self.get_serializer_class()(questions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class QuestionDetailAPIView(APIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    
    def get(self, request, pk):
        question = self.queryset.get(pk=pk)
        serializer = self.serializer_class(question)
        return Response(serializer.data)
    
    def put(self, request, pk):
        question = self.queryset.get(pk=pk)
        serializer = self.serializer_class(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class UserAnswerCreateAPIView(APIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        question = serializer.validated_data['question']
        selected_option = serializer.validated_data['selected_option']
        is_correct = selected_option.is_correct

        # Calcular el puntaje basado en la dificultad de la pregunta
        if is_correct:
            if question.difficulty == 'easy':
                score = 1
            elif question.difficulty == 'medium':
                score = 2
            elif question.difficulty == 'hard':
                score = 3
        else:
            score = 0

        # Actualizar la participación del usuario
        participation = Participation.objects.get(user=user, trivia=question.trivia_set.first())
        participation.score += score
        participation.save()

        serializer.save(user=user)
    
    def get(self, request):
        user_answers = self.queryset.all()
        serializer = self.serializer_class(user_answers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class ParticipationListCreateAPIView(APIView):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    
    def get(self, request):
        participations = self.queryset.all()
        serializer = self.serializer_class(participations, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ParticipationDetailAPIView(APIView):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    
    def get(self, request, pk):
        participation = self.queryset.get(pk=pk)
        serializer = self.serializer_class(participation)
        return Response(serializer.data)
    
    def put(self, request, pk):
        participation = self.queryset.get(pk=pk)
        serializer = self.serializer_class(participation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    


    