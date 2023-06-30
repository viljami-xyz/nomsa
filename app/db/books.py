""" Database operations for books. """
import uuid

from sqlalchemy.future import select


from app.db.settings import async_session_maker
from app.db.models import Book
from app.models.books import BookModel


async def get_book(book_id: uuid.UUID, user_id: uuid.UUID):
    """Get a book from database"""
    async with async_session_maker() as session:
        stmt = (
            select(Book)
            .where(Book.user_id == user_id)
            .where(Book.book_id == str(book_id))
        )
        result = await session.execute(stmt)
        my_book = result.scalars().first()
        return my_book


async def get_books(user_id: uuid.UUID):
    """Get all books from database"""
    async with async_session_maker() as session:
        stmt = select(Book).where(Book.user_id == user_id)
        result = await session.execute(stmt)
        my_books = result.scalars().all()
        return my_books


async def create_book(book: BookModel, user_id: uuid.UUID):
    """Insert new book into database"""
    async with async_session_maker() as session:
        new_book = Book(
            book_id=str(uuid.uuid4()),
            name=book.name,
            author=book.author,
            user_id=user_id,
            type_of=book.type_of,
            state=book.state,
        )
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
    return new_book


async def delete_book(book_id: uuid.UUID, user_id: uuid.UUID):
    """Delete book from database"""
    async with async_session_maker() as session:
        stmt = (
            select(Book)
            .where(Book.book_id == str(book_id))
            .where(Book.user_id == str(user_id))
        )
        result = await session.execute(stmt)
        book = result.scalars().first()
        await session.delete(book)
        await session.commit()
    return book


async def update_book(book_update: BookModel, book_id: uuid.UUID, user_id: uuid.UUID):
    """Update book status in database"""
    async with async_session_maker() as session:
        stmt = (
            select(Book)
            .where(Book.book_id == str(book_id))
            .where(Book.user_id == str(user_id))
        )
        result = await session.execute(stmt)
        book = result.scalars().first()
        book.name = book_update.name
        book.author = book_update.author
        await session.commit()
        await session.refresh(book)


async def set_book_state(book_id: uuid.UUID, state: str, user_id: uuid.UUID):
    """Update book status in database"""
    async with async_session_maker() as session:
        stmt = (
            select(Book)
            .where(Book.book_id == str(book_id))
            .where(Book.user_id == str(user_id))
        )
        result = await session.execute(stmt)
        book = result.scalars().first()
        book.state = state
        await session.commit()
        await session.refresh(book)
        return book
