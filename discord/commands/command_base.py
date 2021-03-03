
# Validate if the user have permission to use the command
user = "Administrator"

valid_permissions = ["Administrator", "Example"]

def valid_permission(user, command):
    if str(user) in valid_permissions:
        print("The user got permission to run this command")
        return True
    else:
        print("The user have not permission to run this command") # Throw error?
        return False