from onlyModels.models import Exam
from utilities.constants import ExamLevel


def validate_exam_meta_data(data):
    exam_level = data.get("exam_level", None)
    if exam_level is None:
        return False, "Exam level not provided."
    
    if exam_level not in ExamLevel:
        return False, "Invalid exam level provided."
    
    return True, "Successfully created."
    

def validate_question_meta_data(data):    
    exam_id = data.get("exam_id", None)
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return False, "Invalid exam id."
    
    return True, "Successfully created."