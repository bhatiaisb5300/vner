import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from onlyModels.models import Exam, Subjects, TargetExamType
from utilities.profile import complete_profile as completeProfile, validate_profile_data
from utilities.utility import validate_exam_meta_data, validate_question_meta_data

@ensure_csrf_cookie
def complete_profile_api(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.POST.get("profileData", {}))
        validated, errors = validate_profile_data(data)

        if validated:
            data = completeProfile(request.user, data)
            data.update({
                "task_completed": True
            })
        else:
            data = {
                "task_completed": False,
                "errors": errors,
                "status": "Validation error(s)."
            }

        return JsonResponse(data)
    
    return JsonResponse({
        "task_complete": False,
        "status": "Unauthorized"
    })

@ensure_csrf_cookie
def getUserNameAndMail(request):
    if request.user.is_authenticated:
        return JsonResponse({
            "task_completed": True,
            "email": request.user.email,
            "first_name": request.user.profile.fname if request.user.profile.fname else request.user.first_name,
            "last_name": request.user.profile.lname if request.user.profile.lname else  request.user.last_name
        })
    return JsonResponse({
        "task_completed": False,
        "error": "Only authorized request allowed."
    })


def getTargetExams(request):
    return JsonResponse({
        "task_completed": True,
        "exams": [[exam.id, exam.name] for exam in TargetExamType.objects.all()]
    })

def authStatus(request):
    return JsonResponse({
        "user_logged_in": request.user.is_authenticated
    })

def getExamTags(request):
    return JsonResponse({
        "tags": [tag for tag in TargetExamType.objects.all()]
    })

def getSubjectTags(request):
    return JsonResponse({
        "tags": [sub for sub in Subjects.objects.all()]
    })

# TODO : remove all csrf_exempt decorators before deploying 
# @ensure_csrf_cookie
@csrf_exempt
def createExam(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.POST.get("data", {}))

        name = data.get("name", '')
        tags = data.get("tags", [])
        exam_level = data.get("exam_level", 0)
        allowed_attempts = data.get("allowed_attempts", 1)

        validated, msg = validate_exam_meta_data(data)
        if not validated:
            return JsonResponse({
                "task_completed": False,
                "msg" : msg
            })

        # TODO : create exam instance and return meta data
        return JsonResponse({
            "task_completed": True,
            "_id": 1,
            **data,
            "created_by": request.user,
            "created_at": 0,
            "last_modified": 0
        })

    return JsonResponse({
        "task_completed": False,
        "msg": "Only authorized POST Request allowed"
    })

# @ensure_csrf_cookie
@csrf_exempt
def addQuestion2Exam(request):
    # if request.method == "POST" and request.user.is_authenticated:
    if request.method == "POST":
        data = json.loads(request.POST.get("data", {}))
        exam_id = data.get("exam_id", None)

        if exam_id is None:
            return JsonResponse({
                "task_completed": False,
                "msg" :"No exam id provided"
            })
        
        validated, msg = validate_question_meta_data(data)
        # TODO : validate questions data as well
        if not validated:
            return JsonResponse({
                "task_completed": False,
                "msg" : msg
            })

        # TODO : create question instance and add it to the exam.
        
        return JsonResponse({
            "task_completed": True,
            "msg": "Question added to the exam successfully."
        })
    
    return JsonResponse({
        "task_completed": False,
        "msg": "Only authorized POST Request allowed"
    })


# @ensure_csrf_cookie
@csrf_exempt
def changeExamName(request):
    # if request.method == "POST" and request.user.is_authenticated:
    if request.method == "POST":
        data = json.loads(request.POST.get("data", {}))
        exam_id = data.get("exam_id", None)
        exam_name = data.get("exam_name", "")

        if exam_id is None:
            return JsonResponse({
                "task_completed": False,
                "msg" :"No exam id provided"
            })

        if not exam_name:
            return JsonResponse({
                "task_completed": False,
                "msg" :"Exam name cannot be empty."
            })

        try:
            exam = Exam.objects.get(id=exam_id)

            if request.user != exam.created_by:
                return JsonResponse({
                    "task_completed": False,
                    "msg": f"Only the creator of the exam is allowed to edit."
                })

            exam.name = exam_name.strip()
            exam.save()
        except Exam.DoesNotExist:
            return JsonResponse({
                "task_completed": False,
                "msg": f"Exam with exam id:{exam_id} does not exists."
            })

        return JsonResponse({
            "task_completed": True,
            "msg": "Exam name successfully changed.",
            "data": {
                "name": exam_name
            }
        })

    return JsonResponse({
        "task_completed": False,
        "msg": "Only authorized POST Request allowed"
    })


# @ensure_csrf_cookie
@csrf_exempt
def changeExamDuration(request):
    # if request.method == "POST" and request.user.is_authenticated:
    if request.method == "POST":
        data = json.loads(request.POST.get("data", {}))
        exam_id = data.get("exam_id", None)
        exam_duration = data.get("exam_duration", 0)

        if exam_id is None:
            return JsonResponse({
                "task_completed": False,
                "msg" :"No exam id provided"
            })

        if exam_duration <= 0:
            return JsonResponse({
                "task_completed": False,
                "msg" :"Exam duration can not be less than or eqaul to 0 minutes."
            })

        try:
            exam = Exam.objects.get(id=exam_id)

            if request.user != exam.created_by:
                return JsonResponse({
                    "task_completed": False,
                    "msg": f"Only the creator of the exam is allowed to edit."
                })

            exam.duration = exam_duration
            exam.save()
        except Exam.DoesNotExist:
            return JsonResponse({
                "task_completed": False,
                "msg": f"Exam with exam id:{exam_id} does not exists."
            })

        return JsonResponse({
            "task_completed": True,
            "msg": "Exam duration successfully changed.",
            "data": {
                "duration": exam_duration
            }
        })

    return JsonResponse({
        "task_completed": False,
        "msg": "Only authorized POST Request allowed"
    })