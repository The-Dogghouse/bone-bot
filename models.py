from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class ChannelJoin(Base):
    __tablename__ = "channel_join"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    user_id: Mapped[int] = mapped_column(BigInteger)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int] = mapped_column(BigInteger)

    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_channel_join_user_joined_at", "user_id", "joined_at"),
        Index("ix_channel_join_channel_joined_at", "channel_id", "joined_at"),
    )

    def __repr__(self) -> str:
        return f"ChannelJoin(user_id={self.user_id}, channel_id={self.channel_id}, joined_at={self.joined_at})"
