from django.urls import path
from trivia.views import ParticipationDetailAPIView, ParticipationListCreateAPIView, PlayerDetailAPIView, PlayerListCreateAPIView, QuestionDetailAPIView, QuestionListCreateAPIView, TriviaDetailAPIView, RankingView, TriviaListCreateAPIView, UserAnswerCreateAPIView, UserDetailAPIView, UserListCreateAPIView

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('players/', PlayerListCreateAPIView.as_view(), name='player-list-create'),
    path('players/<uuid:pk>/', PlayerDetailAPIView.as_view(), name='player-detail'),
    path('questions/', QuestionListCreateAPIView.as_view(), name='question_list'),
    path('questions/<int:question_id>/', QuestionDetailAPIView.as_view(), name='question_detail'),
    path('trivias/', TriviaListCreateAPIView.as_view(), name='trivia_list'),
    path('trivias/<uuid:trivia_id>/', TriviaDetailAPIView.as_view(), name='trivia_detail'),
    path('answers/', UserAnswerCreateAPIView.as_view(), name='user-answer-create'),
    path('participations/', ParticipationListCreateAPIView.as_view(), name='participation-list-create'),
    path('participations/<int:pk>/', ParticipationDetailAPIView.as_view(), name='participation-detail'),
    path('rankings/', RankingView.as_view(), name='ranking'),
    path('rankings/<int:trivia_id>/', RankingView.as_view(), name='ranking_by_trivia'),
    path('rankings/<int:trivia_id>/<uuid:user_id>/', RankingView.as_view(), name='ranking_by_trivia_and_user'),
    path('rankings/user/<uuid:user_id>/', RankingView.as_view(), name='ranking_by_user'),
]