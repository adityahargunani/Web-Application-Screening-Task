from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UploadCSVView,
    DatasetHistoryView,
    DatasetSummaryView,
    DatasetReportView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("upload/", UploadCSVView.as_view()),
    path("history/", DatasetHistoryView.as_view()),
    path("summary/<int:pk>/", DatasetSummaryView.as_view()),
    path("report/<int:pk>/", DatasetReportView.as_view()),
]
