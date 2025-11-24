from fastapi import APIRouter,status,Depends,HTTPException
import os
from sqlalchemy.ext.asyncio import AsyncSession
from models.schemas import UserCreate,UserOut,Token,LoginIn,BookOut,BookCreate,BorrowOut
from sqlalchemy import select
from models.models import User,RoleEnum,Book,Borrow
from services.pwd_hashing_service import hash_password,verify_password
from Auth.dependencies import get_db,get_current_user,require_role
from utils.jwt_utils import create_access_token
from typing import List,Optional
from datetime import datetime,timedelta,date
from database.config import FINE_PER_DAY
from utils.logging_config import logger


router = APIRouter()



@router.get("/")
async def root():
    return {
        "app": "Async Library Management API",
        "notes": "Use /register, /login. Protect endpoints with HTTP Bearer token. Roles: admin, librarian, user."
    }


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # check unique username and email using select
    stmt = select(User).where((User.username == user_in.username) | (User.email == user_in.email))
    res = await db.execute(stmt)
    existing = res.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    logger.info("User created")
    return user

@router.post("/login", response_model=Token)
async def login(data: LoginIn, db: AsyncSession = Depends(get_db)):
    # find user by username or email (ORM select)
    stmt = select(User).where((User.username == data.username_or_email) | (User.email == data.username_or_email))
    res = await db.execute(stmt)
    user_obj = res.scalars().first()
    if user_obj is None or not verify_password(data.password, user_obj.hashed_password):
        logger.error("Login Failed due to invalid credentials")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    

    access_token = create_access_token(subject=user_obj.id)
    logger.info("User login successful")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users", response_model=List[UserOut])
async def list_users(current_user: User = Depends(require_role(RoleEnum.admin)),
                     db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User))
   
    users = res.scalars().all()
    
    return users

@router.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, current_user: User = Depends(require_role(RoleEnum.librarian, RoleEnum.admin)),
                      db: AsyncSession = Depends(get_db)):
    book = Book(
        title=book_in.title,
        author=book_in.author,
        isbn=book_in.isbn,
        total_copies=book_in.total_copies,
        available_copies=book_in.total_copies
    )
    db.add(book)
    await db.commit()
    await db.refresh(book)
    logger.info("Book added succesfully")
    return book

@router.get("/books", response_model=List[BookOut])
async def list_books(q: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Book)
    if q:
        stmt = select(Book).where((Book.title.ilike(f"%{q}%")) | (Book.author.ilike(f"%{q}%")))
    res = await db.execute(stmt)
    books = res.scalars().all()
    return books

@router.get("/books/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=BookOut)
async def update_book(book_id: int, book_in: BookCreate, current_user: User = Depends(require_role(RoleEnum.librarian, RoleEnum.admin)),
                      db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    delta = book_in.total_copies - book.total_copies
    book.title = book_in.title
    book.author = book_in.author
    book.isbn = book_in.isbn
    book.total_copies = book_in.total_copies
    book.available_copies = max(0, book.available_copies + delta)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    logger.info(f"{book} Book details changed")
    return book

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, current_user: User = Depends(require_role(RoleEnum.admin)),
                      db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(book)
    await db.commit()
    logger.info(f"The Book {book} deleted successfully")
    return {"deleted":book_id}


# Borrow / Return Endpoints

DEFAULT_BORROW_DAYS = int(os.getenv("DEFAULT_BORROW_DAYS", "14"))

@router.post("/borrow/{book_id}", response_model=BorrowOut)
async def borrow_book(book_id: int, days: Optional[int] = DEFAULT_BORROW_DAYS,
                      current_user: User = Depends(require_role(RoleEnum.user, RoleEnum.librarian, RoleEnum.admin)),
                      db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_copies < 1:
        raise HTTPException(status_code=400, detail="No available copies to borrow")

    due = date.today() + timedelta(days=days)
    borrow = Borrow(user_id=current_user.id, book_id=book.id, due_date=due)
    book.available_copies -= 1

    db.add(borrow)
    db.add(book)
    await db.commit()
    await db.refresh(borrow)
    logger.info(f"The book_id {book_id} broowed by user :{current_user}")
    return borrow

@router.post("/return/{borrow_id}", response_model=BorrowOut)
async def return_book(borrow_id: int,
                      current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    borrow = await db.get(Borrow, borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if borrow.user_id != current_user.id and current_user.role not in (RoleEnum.admin, RoleEnum.librarian):
        raise HTTPException(status_code=403, detail="Not allowed to return this borrow")

    if borrow.returned_at is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    borrow.returned_at = datetime.utcnow()
    returned_date = borrow.returned_at.date()
    days_late = (returned_date - borrow.due_date).days
    fine = 0.0
    if days_late > 0:
        fine = days_late * FINE_PER_DAY
    borrow.fine_amount = fine

    book = await db.get(Book, borrow.book_id)
    if book:
        book.available_copies = min(book.total_copies, book.available_copies + 1)
        db.add(book)

    db.add(borrow)
    await db.commit()
    await db.refresh(borrow)
    logger.info(f"The borrow id {borrow_id} returned success")
    return borrow

@router.get("/my-borrows", response_model=List[BorrowOut])
async def my_borrows(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    stmt = select(Borrow).where(Borrow.user_id == current_user.id)
    res = await db.execute(stmt)
    borrows = res.scalars().all()
    return borrows

@router.get("/borrows", response_model=List[BorrowOut])
async def list_borrows(current_user: User = Depends(require_role(RoleEnum.librarian, RoleEnum.admin)),
                       db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Borrow))
    borrows = res.scalars().all()
    return borrows

@router.get("/my-fines")
async def my_fines(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    stmt = select(Borrow).where(Borrow.user_id == current_user.id)
    res = await db.execute(stmt)
    borrows = res.scalars().all()
    total_fine = 0.0
    details = []
    for b in borrows:
        fine = b.fine_amount or 0.0
        if b.returned_at is None:
            days_late = (date.today() - b.due_date).days
            if days_late > 0:
                fine = days_late * FINE_PER_DAY
        total_fine += fine
        details.append({"borrow_id": b.id, "book_id": b.book_id, "fine": fine, "due_date": b.due_date, "returned_at": b.returned_at})
    return {"total_fine": total_fine, "details": details}

@router.post("/borrows/{borrow_id}/clear-fine", response_model=BorrowOut)
async def clear_fine(borrow_id: int, current_user: User = Depends(require_role(RoleEnum.admin)),
                     db: AsyncSession = Depends(get_db)):
    borrow = await db.get(Borrow, borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    borrow.fine_amount = 0.0
    db.add(borrow)
    await db.commit()
    await db.refresh(borrow)
    return borrow





