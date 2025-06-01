from app.model import LearningResult
from app.repository.crud import CRUDRepository


class LearningResultRepository(CRUDRepository[LearningResult]):
    _model_type = LearningResult
