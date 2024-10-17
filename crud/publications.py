from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from core.models import Publication
from core.schemas.publication import PublicationCreate, PublicationUpdate


async def get_all_publications(session: AsyncSession) -> Sequence[Publication]:
    stmt = select(Publication).order_by(Publication.id)
    res = await session.scalars(stmt)
    return res.all()


async def get_publication(session: AsyncSession, publication_id: int) -> Publication | None:
    return await session.get(Publication, publication_id)


async def create_publication(session: AsyncSession, publication_create: PublicationCreate) -> Publication:
    publication = Publication(**publication_create.model_dump())
    session.add(publication)
    await session.commit()
    return publication


async def update_publication(
    session: AsyncSession, publication_update: PublicationUpdate, publication: Publication) -> Publication:
    for name, value in publication_update.model_dump().items():
        setattr(publication, name, value)
    await session.commit()
    return publication


async def delete_publication(session: AsyncSession, publication:Publication) -> None:
    await session.delete(publication)
    await session.commit()