from pydantic import BaseModel

class MoviesReportSummaryDTO(BaseModel):
    total_movies: int
    total_units: int
    total_price: float
