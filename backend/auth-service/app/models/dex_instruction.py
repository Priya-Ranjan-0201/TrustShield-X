"""SQLAlchemy 2.0 ORM Models for DEX Instruction & Opcode Intelligence Engine (Phase 3.7 Part 1A.14).

Defines database models for dex_instructions, dex_operands, dex_basic_blocks,
dex_control_flow, and dex_opcode_statistics.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class DEXInstructionModel(Base):
    __tablename__ = "dex_instructions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    class_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    opcode_name: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    opcode_val: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    length: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    category: Mapped[str] = mapped_column(String(64), nullable=False, default="UNKNOWN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    operands: Mapped[List["DEXOperandModel"]] = relationship("DEXOperandModel", back_populates="instruction", cascade="all, delete-orphan", lazy="selectin")


class DEXOperandModel(Base):
    __tablename__ = "dex_operands"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instruction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dex_instructions.id", ondelete="CASCADE"), nullable=False, index=True)
    operand_type: Mapped[str] = mapped_column(String(64), nullable=False)
    operand_val: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    instruction: Mapped["DEXInstructionModel"] = relationship("DEXInstructionModel", back_populates="operands")


class DEXBasicBlockModel(Base):
    __tablename__ = "dex_basic_blocks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    method_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    start_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    end_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    instruction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DEXControlFlowModel(Base):
    __tablename__ = "dex_control_flow"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    target_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    branch_type: Mapped[str] = mapped_column(String(64), nullable=False, default="JUMP")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DEXOpcodeStatisticsModel(Base):
    __tablename__ = "dex_opcode_statistics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    total_instructions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unique_opcodes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    most_common_opcode: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    avg_instructions_per_method: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
