from rest_framework import serializers
from trivia.models import AnswerOption, Participation, Player, Question, Trivia, User, Entity, UserAnswer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token
    
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.pop('role', 'player')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            role=role
        )
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya está registrado")
        return value

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name']

class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'email', 'role']

    def create(self, validated_data):
        entity = Entity.objects.create(
            name=validated_data['name'],
            email=validated_data['email']
        )
        player = Player.objects.create(
            entity=entity,
            role=validated_data.get('role', 'player')
        )
        return player

class PlayerListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='entity.name')
    email = serializers.EmailField(source='entity.email')
    class Meta:
        model = Player
        fields = ['id', 'name', 'email']
        
        
class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'option_text', 'is_correct']

class QuestionCreateSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'difficulty', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            AnswerOption.objects.create(question=question, **option_data)
        return question

    def validate_question_text(self, value):
        if Question.objects.filter(question_text=value).exists():
            raise serializers.ValidationError("La pregunta ya está registrada")
        return value

class QuestionListSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'options']

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['id', 'user', 'question', 'selected_option']

class ParticipationSerializer(serializers.ModelSerializer):
    trivia_name = serializers.CharField(source='trivia.name', read_only=True)
    
    class Meta:
        model = Participation
        fields = ['id', 'user', 'trivia', 'trivia_name', 'score', 'completed']
        
class TriviaCreateSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True)

    class Meta:
        model = Trivia
        fields = ['id', 'name', 'description', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        trivia = Trivia.objects.create(**validated_data)
        for question_data in questions_data:
            question = Question.objects.get(id=question_data['id'])
            trivia.questions.add(question)
        return trivia

class TriviaListSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True)

    class Meta:
        model = Trivia
        fields = ['id', 'name', 'description', 'questions']
        

