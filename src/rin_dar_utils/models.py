from sqlalchemy import Column, String

from .db_base import Base


class DARData(Base):

    __tablename__ = "rin_dar_data"
    uuid = Column(String(255), primary_key=True)
    access_token = Column(String(255))
    refresh_token = Column(String(255))

    def __iter__(self):
        yield "uuid", self.uuid
        yield "access_token", self.access_token
        yield "refresh_token", self.refresh_token

    def __repr__(self):
        return f"DARData(uuid={self.uuid!r}, access_token={self.access_token!r}, refresh_token={self.refresh_token!r})"
