# Contributing to TruthShield X

Thank you for contributing to **TruthShield X**, the National Digital Trust Platform.

---

## 1. Development Workflow & Guidelines

### Layering Discipline
TruthShield X follows a strict microservices layering architecture:
`Routes (Validation & Routing) -> Services (Business Logic) -> Repositories (Database Access) -> Models`.
- Route handlers must **never** contain raw SQLAlchemy queries, hashing logic, or direct JWT manipulation.
- All errors must use standardized `TSX-AUTH-XXX` error codes.

### Code Style & Formatting
- **Backend (Python)**: PEP 8 guidelines, explicit type annotations, and Pydantic v2 schemas.
- **Frontend (TypeScript / React)**: TypeScript strict mode enabled, Tailwind CSS styling matching `05-Design.md`, and React Hook Form + Zod for validation.

---

## 2. Testing Requirements
Before submitting a pull request, ensure all test suites pass:
```bash
cd backend/auth-service
pytest --cov=app --cov-report=term-missing
```

---

## 3. Pull Request Checklist
- [ ] Code follows project layering conventions.
- [ ] Added unit/integration tests for new features.
- [ ] Pytest suite passes 100% with no regressions.
- [ ] Updated documentation files (`README.md`, `CHANGELOG.md`).
