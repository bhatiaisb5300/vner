from django.urls import path
from apis.api import addQuestion2Exam, authStatus, changeExamDuration, changeExamName, complete_profile_api, createExam, getExamTags, getSubjectTags, getTargetExams, getUserNameAndMail
from apis.views import complete_profile

urlpatterns = [
    # Authorization and authentication end-point
    path("authStatus/", authStatus, name="authStatus"),
    # End-points that require authentication
    path("complete_profile/", complete_profile_api, name="complete-profile-api"),
    # Data fetching end-points, no authentication required
    path("getSubjectTags/", getSubjectTags, name="getSubjectTags"),
    path("getExamTags/", getExamTags, name="getExamTags"),
    path("getTargetExams/", getTargetExams, name="getTargetExams"),
    path("getUserNameAndMail/", getUserNameAndMail, name="getUserNameAndMail"),

    # exam related api end-points
    path("createExam/", createExam, name="create-exam"),
    path("addQuestion/", addQuestion2Exam, name="add-question"),
    path("change_examName/", changeExamName, name="change-exam-name"),
    path("change_examDuration/", changeExamDuration, name="change-exam-duration"),
]