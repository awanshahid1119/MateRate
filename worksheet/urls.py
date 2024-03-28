from django.urls import path

from . import views

urlpatterns = [
    path('create_worksheet/', views.create_worksheet),
    path('worksheet-id/<int:id>/', views.WorksheetId.as_view()),
    path('question/', views.QuestionView.as_view()),
    path('question/<int:id>/', views.QuestionId.as_view()),
    path('solution/', views.SolutionView.as_view()),
    path('solution/<int:id>/', views.SolutionId.as_view()),
    path('assignments/', views.get_all_worksheets),
    path('worksheet_intro/', views.worksheet_intro,
         name="worksheet_intro_details"),
    path('submit/', views.worksheet_submit, name='worksheet_submit'),
    path('original_copy/<int:worksheet_id>/', views.display_original_copy, name='view_original_copy'),
    path('graded_copy/<int:worksheet_id>/', views.display_graded_copy, name='view_graded_copy')
]