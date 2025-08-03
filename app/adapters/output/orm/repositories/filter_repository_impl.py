from app.domain.repositories.filter_match_repository import FilterMatchRepository
from app.domain.entities.filter_match import FilterMatch
from app.domain.repositories.filter_match_repository import FilterMatchRepository
from app.domain.entities.filter_match import FilterMatch
from app.adapters.output.orm.models.filter_match_model import FilterMatchModel

class FilterMatchRepositoryImpl(FilterMatchRepository):
    def __init__(self, session):
        self.session = session
    # ...aquí solo van métodos de persistencia y consulta de filter_match...