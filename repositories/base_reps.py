import logging
from abc import abstractmethod
from typing import TypeVar, Generic
from uuid import UUID

from sqlalchemy import func
from sqlmodel import select, SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    # TODO: Add create, update, delete, get pagination
    def __init__(self, session):
        self.session = session
        self.model = self.__get_model__()

    @abstractmethod
    def __get_model__(self) -> type[ModelType]:
        """Return the SQLAlchemy model class."""
        raise NotImplementedError

    async def get_all(self, skip: int = 0, limit: int = 100, filters: dict = None):
        query = select(self.model).offset(skip).limit(limit)
        if filters:
            for key, value in filters.items():
                query = query.where(getattr(self.model, key) == value)
        result = await self.session.execute(query)
        total = await self.session.execute(select(func.count()).select_from(self.model))
        return {
            "items": result.scalars().all(),
            "total": total.scalar_one(),
        }

    async def get(self, id: UUID):
        """
        Retrieve a paginated list of records, optionally filtered by criteria.

        :param skip: Number of records to skip (for pagination).
        :param limit: Maximum number of records to return.
        :param filters: Key-value pairs to filter the records.
        :return: A list of records.
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalars().first()

    async def get_count(self) -> int:
        """
        Retrieve a paginated list of records, optionally filtered by criteria.

        :param skip: Number of records to skip (for pagination).
        :param limit: Maximum number of records to return.
        :param filters: Key-value pairs to filter the records.
        :return: A list of records.
        """
        result = await self.session.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new database record for the given input.

        :param obj_in: The input data to create a new record with.
        :return: The newly created record.
        """
        try:
            db_obj = self.model.from_orm(obj_in)  # fits the input to the model
            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj
        except Exception as e:
            await self.session.rollback()
            logging.error(f"Failed to create record: {e}")
            raise self._translate_exception(e)

    async def update(self, id: UUID, obj_in: UpdateSchemaType) -> ModelType:
        """
        Update an existing record with the given input data.

        :param id: The unique identifier of the record to update.
        :param obj_in: The input data to update the record with.
        :return: The updated record.
        """
        try:
            db_obj = await self.get(id)
            if not db_obj:
                raise LookupError("Resource not found")

            update_data = obj_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_obj, key, value)
            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj
        except Exception as e:
            await self.session.rollback()
            raise self._translate_exception(e)

    async def delete(self, id: UUID) -> bool:
        """
        Delete a record from the database by its unique identifier.

        :param id: The unique identifier of the record to delete.
        :return: True if the record was successfully deleted, False if the record was not found.
        :raises Exception: If an error occurs during the deletion process.
        """
        db_obj = await self.get(id)
        if db_obj:
            await self.session.delete(db_obj)
            await self.session.commit()
            return True
        return False

    def _translate_exception(self, exc: Exception) -> Exception:
        """
        Map SQLAlchemy exceptions to domain exceptions

        :param exc: SQLAlchemy exception
        :return: Domain exception
        """
        from sqlalchemy.exc import (
            IntegrityError,
            NoResultFound,
            MultipleResultsFound
        )

        if isinstance(exc, IntegrityError):
            return ValueError("Data integrity error occurred")
        if isinstance(exc, NoResultFound):
            return LookupError("Resource not found")
        if isinstance(exc, MultipleResultsFound):
            return LookupError("Multiple resources found")
        return exc
