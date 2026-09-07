from django.urls import path
from .views import (
    SubjectListView, SubjectDetailView,
    CurriculumOverviewView, TopicDetailView, ProblemDetailView,
    StaffSubjectCreateView, StaffSubjectDetailView,
    StaffModuleCreateView, StaffModuleDetailView,
    StaffTopicCreateView, StaffTopicDetailView,
    StaffProblemCreateView, StaffProblemDetailView,
    StaffCodeExampleCreateView, StaffCodeExampleDetailView
)

urlpatterns = [
    # Subjects (Public)
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subjects/<slug:slug>/', SubjectDetailView.as_view(), name='subject-detail'),

    # Public / Student read endpoints
    path('curriculum/', CurriculumOverviewView.as_view(), name='curriculum-overview'),
    path('curriculum/topics/<slug:topic_id>/', TopicDetailView.as_view(), name='topic-detail'),
    path('curriculum/problems/<int:pk>/', ProblemDetailView.as_view(), name='problem-detail'),

    # Staff Subject CRUD
    path('staff/subjects/', StaffSubjectCreateView.as_view(), name='staff-subject-create'),
    path('staff/subjects/<int:pk>/', StaffSubjectDetailView.as_view(), name='staff-subject-detail'),

    # Staff Module & Topic CRUD endpoints
    path('staff/modules/', StaffModuleCreateView.as_view(), name='staff-module-create'),
    path('staff/modules/<int:pk>/', StaffModuleDetailView.as_view(), name='staff-module-detail'),
    path('staff/topics/', StaffTopicCreateView.as_view(), name='staff-topic-create'),
    path('staff/topics/<int:pk>/', StaffTopicDetailView.as_view(), name='staff-topic-detail'),
    path('staff/problems/', StaffProblemCreateView.as_view(), name='staff-problem-create'),
    path('staff/problems/<int:pk>/', StaffProblemDetailView.as_view(), name='staff-problem-detail'),
    path('staff/examples/', StaffCodeExampleCreateView.as_view(), name='staff-example-create'),
    path('staff/examples/<int:pk>/', StaffCodeExampleDetailView.as_view(), name='staff-example-detail'),
]
