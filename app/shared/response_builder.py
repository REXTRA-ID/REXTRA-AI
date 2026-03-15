class APIResponse:
    @staticmethod
    def success(data, message="Success"):
        return {
            "status": "success",
            "message": message,
            "data": data
        }

    @staticmethod
    def error(message="Error", code=400):
        return {
            "status": "error",
            "message": message,
            "error_code": code
        }

    @staticmethod
    def processing(message="Processing"):
        return {
            "status": "processing",
            "message": message
        }