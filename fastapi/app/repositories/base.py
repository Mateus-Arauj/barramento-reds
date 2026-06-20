"""
Repository base com operações CRUD genéricas
"""
from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Repository genérico com operações CRUD básicas
    """

    def __init__(self, db: Session, model: Type[T]):
        """
        Inicializa o repository

        Args:
            db: Sessão do SQLAlchemy
            model: Classe do modelo
        """
        self.db = db
        self.model = model

    def get_by_id(self, id: str) -> Optional[T]:
        """
        Busca um registro por ID
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_by_id_or_404(self, id: str, resource_type: str = "Resource") -> T:
        """
        Busca um registro por ID, levanta 404 se não encontrado
        """
        result = self.get_by_id(id)
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"{resource_type}/{id} not found"
            )
        return result

    def get_all(self, limit: int = 50) -> List[T]:
        """
        Retorna todos os registros com limite
        """
        return self.db.query(self.model).limit(limit).all()

    def create(self, obj: T) -> T:
        """
        Cria um novo registro
        """
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        """
        Atualiza um registro existente
        """
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        """
        Remove um registro
        """
        self.db.delete(obj)
        self.db.commit()

    def delete_by_id(self, id: str, resource_type: str = "Resource") -> None:
        """
        Remove um registro por ID
        """
        obj = self.get_by_id_or_404(id, resource_type)
        self.delete(obj)
