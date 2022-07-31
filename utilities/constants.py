from django.db.models import IntegerChoices

class RoleType(IntegerChoices):
    NOT_SELECTED = 0, "Not Selected"
    STUDENT  = 1, "Student"
    EXAMINER = 2, "Examiner"

class QuestionType(IntegerChoices):
    MCQ = 0, "MCQ"
    SUB = 1, "Subjective"
    MUL = 2, "Multiple Answer"

class ExamLevel(IntegerChoices):
    BEGINNER = 0, "Beginner"
    INTERMEDIATE = 1, "Intermediate"
    ADVANCE = 2, "Advance"