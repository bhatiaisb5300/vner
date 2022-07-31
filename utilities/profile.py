from onlyModels.models import TargetExamType

def validate_profile_data(data):
    REQ_FIELDS = ['first_name', 'middle_name', 'last_name', 'date_of_birth', "countryCode", 'mobile', 'email', 'target_exams', 'role', 'education']
    errors = [field for field in REQ_FIELDS if field not in data]
    return len(errors) == 0, ["Some fields are missing"]

def complete_profile(user, data):
    profile = user.profile
    profile.fname = data["first_name"]
    profile.mname = data["middle_name"]
    profile.lname = data["last_name"]
    profile.dob = data["date_of_birth"]
    profile.mobile = f'+{data["countryCode"]}-{data["mobile"]}'
    profile.email = data["email"]
    profile.education = data["education"]
    if profile.target_exams.count() > 0: profile.target_exams.clear()
    for exam_name in data["target_exams"]:
        exam = TargetExamType.objects.get(name=exam_name)
        profile.target_exams.add(exam)
    profile.role = data["role"]
    profile.is_completed = True
    profile.save()
    return {
        "status": "Profile updated succcessfully"
    }