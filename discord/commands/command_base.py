role = "Administrator"

valid_access = ["Administrator", "Example"]

def validate_access(role):
    if role in valid_access:
        print("The role got access")
    else:
        print("Access denied") # Throw error?

validate_access(role)