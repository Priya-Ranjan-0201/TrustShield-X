import asyncio
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
backend_root = repo_root / "backend" / "auth-service"
sys.path.insert(0, str(backend_root))

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.role import Role
from sqlalchemy import select


DEMO_USERS = [
    {
        "email": "admin@truthshield.com",
        "full_name": "SecOps Administrator",
        "role_name": "admin",
        "password": "AdminPassword123!",
    },
    {
        "email": "analyst@truthshield.com",
        "full_name": "Lead SOC Analyst",
        "role_name": "analyst",
        "password": "AnalystPassword123!",
    },
    {
        "email": "demo@truthshield.com",
        "full_name": "Demo Citizen",
        "role_name": "citizen",
        "password": "DemoPassword123!",
    },
]


async def seed():
    async with AsyncSessionLocal() as session:
        # Get roles
        roles_result = await session.execute(select(Role))
        roles_map = {r.name.lower(): r.id for r in roles_result.scalars().all()}
        
        for user_data in DEMO_USERS:
            role_id = roles_map.get(user_data["role_name"])
            if not role_id:
                # fallback to first role or create
                role_id = list(roles_map.values())[0] if roles_map else None

            existing = await session.execute(select(User).where(User.email == user_data["email"]))
            user = existing.scalar_one_or_none()
            hashed = hash_password(user_data["password"])
            
            if user:
                user.password_hash = hashed
                user.status = "active"
                user.email_verified = True
                user.full_name = user_data["full_name"]
                if role_id:
                    user.role_id = role_id
                print(f"Updated user: {user_data['email']} with password: {user_data['password']}")
            else:
                if not role_id:
                    print(f"Cannot create {user_data['email']} without role")
                    continue
                new_user = User(
                    email=user_data["email"],
                    full_name=user_data["full_name"],
                    password_hash=hashed,
                    role_id=role_id,
                    status="active",
                    email_verified=True,
                )
                session.add(new_user)
                print(f"Created user: {user_data['email']} with password: {user_data['password']}")
        
        await session.commit()
    print("Demo accounts successfully initialized!")


if __name__ == "__main__":
    asyncio.run(seed())
