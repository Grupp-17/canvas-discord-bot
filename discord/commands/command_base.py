
# Validate if the user have permission to use the command
user = ""

def valid_permission(user, command, permissions):
    if str(user) in permissions:
        print("The user got permission to run this command")
        return True
    else:
        print("The user does not have permission to run this command") # Throw error?
        return False