class InvalidMarkException(RuntimeError):

    __DEFAULT_ERR_MSG = 'Invalid mark value, please check again'

    def __init__(self, message: str):
        self.message = message

    @staticmethod
    def default():
        return InvalidMarkException(InvalidMarkException.__DEFAULT_ERR_MSG)


class ItemNotFoundException(RuntimeError):

    __DEFAULT_STUDENT_ERR_MSG = 'Student with slug {} not found.'
    __DEFAULT_LEARNING_RESULT_ERR_MSG = 'Learning Result of Student with slug {} not found.'

    def __init__(self, message: str):
        self.message = message

    @staticmethod
    def student(slug: str):
        return ItemNotFoundException(
            ItemNotFoundException.__DEFAULT_STUDENT_ERR_MSG.format(slug))

    @staticmethod
    def learning_result(slug: str):
        return ItemNotFoundException(
            ItemNotFoundException.__DEFAULT_LEARNING_RESULT_ERR_MSG.format(slug))
