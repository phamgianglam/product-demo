from typing import Optional
from fastapi import Query
from pydantic import BaseModel as Schema
from sqlalchemy import or_
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.sqltypes import String
from ..model.models import BaseModel


class SearcherParams(Schema):
    search: Optional[str] = Query(None, description="search term")
    df: Optional[str] = Query(None, description="default search field")
    order: Optional[str] = Query(None, description="order filter")


class Seracher:
    def __init__(self, params: SearcherParams, model: BaseModel, schema: Schema, default_field=None) -> None:
        self.search = params.search
        self.order = params.order
        self.schema = schema
        self.model = model
        if params.df:
            self.df = params.df
        else:
            self.df = default_field

    async def _map_field(self, field: str) -> str:
        for model_key, model_field in self.schema.__fields__.items():
            if model_field.alias:
                alias_key = model_field.alias
            else:
                alias_key = model_key

            if field.lower() in map(str.lower, (model_key, alias_key)):
                field = model_key
                if hasattr(self.model, field):
                    break
                else:
                    raise ValueError("Field not found")
            return field

    async def _parse_term(self):
        if not self.search:
            return None

        terms = self.search.split("+")
        filter = []
        for term in terms:
            parts = term.strip().split(":")
            if len(parts) > 2:
                raise ValueError("Term should follow format key:value")
            if len(parts) == 1:
                if self.df:
                    parts.insert(0, self.df)
                else:
                    raise ValueError("No default filed state")

            parts[0] = await self._map_field(parts[0])

            attr = getattr(self.model, parts[0])
            filter.append(attr.ilike(f"%{parts[1]}%"))

        return filter

    async def _order(self):
        order = "asc"
        if not self.order:
            if not self.df:
                raise ValueError("Invalid params")
            else:
                field = self.df
        else:
            parts = self.order.split(":")
            if len(parts) > 2:
                raise ValueError("Invalid order term")

            if len(parts) == 1:
                if not self.df:
                    raise ValueError("Invalid order term")
                parts.insert(0, self.df)
            if parts[1] not in ["asc", "desc"]:
                raise ValueError("Invalid order term")

            field = await self._map_field(parts[0])

        if self.order:
            if len(parts) == 2:
                order = parts[1].lower()
        order_clause = getattr(getattr(self.model, field), order)
        return order_clause

    async def apply_searcher(self, query: Select):
        if query is not None:
            self.stmt = query
        else:
            self.stmt = select(self.model)

        order = await self._order()

        if not self.search:
            return self.stmt.order_by(order())
        filters = await self._parse_term()

        if filters:
            filters_expression = or_(*filters)
            print(filters_expression)
            print(self.stmt)
            self.stmt = self.stmt.filter(filters_expression)
        self.stm = self.stmt.order_by(order())
        print(self.stmt)
        return self.stm
