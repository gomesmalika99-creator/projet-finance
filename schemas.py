from pydantic import BaseModel, ConfigDict, Field


class SocieteEntree(BaseModel):
    """Données attendues pour créer ou remplacer une société."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nom: str = Field(min_length=1, max_length=100)
    secteur: str = Field(min_length=1, max_length=50)