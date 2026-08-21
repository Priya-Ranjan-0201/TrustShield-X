"""Alembic Migration 022: DEX Instruction & Opcode Intelligence Schema (Phase 3.7 Part 1A.14).

Creates tables:
- dex_instructions
- dex_operands
- dex_basic_blocks
- dex_control_flow
- dex_opcode_statistics
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 022_dex_instruction
Revises: 021_dex_structure
Create Date: 2026-08-06
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "022_dex_instruction"
down_revision: Union[str, None] = "021_dex_structure"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create dex_instructions table
    op.create_table(
        "dex_instructions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("class_name", sa.String(length=512), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("opcode_name", sa.String(length=64), nullable=False),
        sa.Column("opcode_val", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("length", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="'UNKNOWN'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_instructions_scan_id", "dex_instructions", ["scan_id"])
    op.create_index("ix_dex_instructions_class_name", "dex_instructions", ["class_name"])
    op.create_index("ix_dex_instructions_method_name", "dex_instructions", ["method_name"])
    op.create_index("ix_dex_instructions_opcode_name", "dex_instructions", ["opcode_name"])

    # 2. Create dex_operands table
    op.create_table(
        "dex_operands",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("instruction_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("dex_instructions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("operand_type", sa.String(length=64), nullable=False),
        sa.Column("operand_val", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_operands_instruction_id", "dex_operands", ["instruction_id"])

    # 3. Create dex_basic_blocks table
    op.create_table(
        "dex_basic_blocks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("method_name", sa.String(length=512), nullable=False),
        sa.Column("start_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("end_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("instruction_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_basic_blocks_scan_id", "dex_basic_blocks", ["scan_id"])

    # 4. Create dex_control_flow table
    op.create_table(
        "dex_control_flow",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("target_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("branch_type", sa.String(length=64), nullable=False, server_default="'JUMP'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_control_flow_scan_id", "dex_control_flow", ["scan_id"])

    # 5. Create dex_opcode_statistics table
    op.create_table(
        "dex_opcode_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("total_instructions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unique_opcodes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("most_common_opcode", sa.String(length=64), nullable=True),
        sa.Column("avg_instructions_per_method", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_dex_opcode_statistics_scan_id", "dex_opcode_statistics", ["scan_id"])


def downgrade() -> None:
    op.drop_index("ix_dex_opcode_statistics_scan_id", table_name="dex_opcode_statistics")
    op.drop_table("dex_opcode_statistics")

    op.drop_index("ix_dex_control_flow_scan_id", table_name="dex_control_flow")
    op.drop_table("dex_control_flow")

    op.drop_index("ix_dex_basic_blocks_scan_id", table_name="dex_basic_blocks")
    op.drop_table("dex_basic_blocks")

    op.drop_index("ix_dex_operands_instruction_id", table_name="dex_operands")
    op.drop_table("dex_operands")

    op.drop_index("ix_dex_instructions_opcode_name", table_name="dex_instructions")
    op.drop_index("ix_dex_instructions_method_name", table_name="dex_instructions")
    op.drop_index("ix_dex_instructions_class_name", table_name="dex_instructions")
    op.drop_index("ix_dex_instructions_scan_id", table_name="dex_instructions")
    op.drop_table("dex_instructions")
