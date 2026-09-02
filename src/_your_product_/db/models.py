"""Tables — not request/response schemas, those live in api/schemas.py.

Live code needs SQLAlchemy, which the template does not depend on.
"""

# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
#
# class Base(DeclarativeBase):
#     pass
#
# class YourRow(Base):
#     __tablename__ = "_your_table_"
#     id: Mapped[int] = mapped_column(primary_key=True)
