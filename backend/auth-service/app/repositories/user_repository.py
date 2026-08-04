import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.user import User, UserStatus
from app.models.role import Role


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(User.id == user_id).options(selectinload(User.role))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower()).options(selectinload(User.role))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> User | None:
        stmt = select(User).where(User.phone == phone).options(selectinload(User.role))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_role_by_name(self, role_name: str) -> Role | None:
        stmt = select(Role).where(Role.name == role_name.upper())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user, attribute_names=["role"])
        return user

    async def create_user(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        role_id: uuid.UUID,
        phone: str | None = None,
        email_verified: bool = False,
    ) -> User:
        user = User(
            full_name=full_name,
            email=email.lower(),
            password_hash=password_hash,
            role_id=role_id,
            phone=phone,
            email_verified=email_verified,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user, attribute_names=["role"])
        return user

    async def update(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user, attribute_names=["role"])
        return user
