from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Publication
from core.schemas.publication import PublicationRead, PublicationCreate, PublicationUpdate
from crud import publications as publication_crud
from crud.dependencies import publication_by_id

router = APIRouter(tags=['Publications'])


@router.get('', response_model=list[PublicationRead])
async def get_publications(session: AsyncSession = Depends(db_helper.session_getter)):
    publications = await publication_crud.get_all_publications(session=session)
    return publications


@router.get('/{publication_id}')
async def get_publication(publication: Publication = Depends(publication_by_id)):
    return publication


@router.post('/create_publication', response_model=PublicationRead, status_code=status.HTTP_201_CREATED)
async def create_publication(publication_create: PublicationCreate,
                             session: AsyncSession = Depends(db_helper.session_getter)):
    publication = await publication_crud.create_publication(session=session, publication_create=publication_create)
    return publication


@router.put('/{publication_id}', response_model=PublicationRead)
async def update_publication(publication_update: PublicationUpdate,
                             publication: Publication = Depends(publication_by_id),
                             session: AsyncSession = Depends(db_helper.session_getter)):
    return await publication_crud.update_publication(session=session, publication_update=publication_update,
                                                     publication=publication)


@router.delete('/{publication_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_publications(publication: Publication = Depends(publication_by_id),
                              session: AsyncSession = Depends(db_helper.session_getter)):
    return await publication_crud.delete_publication(session=session, publication=publication)
