class Validate:
    def phone(number):
        print(number.isnumeric)
        if number.isnumeric():
            if(len(number)==12):
                checkCode=number[0:4]
                if checkCode=="2547":
                    print("phone")
                    return "success"
                else:
                    return "only kenyan numbers are supported,+254"        
            else:
                print(len(number))
                return "invalid phone number"  
            
        else:
            print("not numeric")
            return "invalid phone number"
    def username(name):
        if len(name)>4:
            return "success"
        else:
            return "username must have atleast 4 characters"
    def CheckCode(code):
        pass