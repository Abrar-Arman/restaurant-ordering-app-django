
def validate_required_fields(data, required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
           return False, missing_fields
        return True, None
