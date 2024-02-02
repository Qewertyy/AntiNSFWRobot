import logging
from enum import Enum
from typing import Optional

from pony import orm
from datetime import datetime

from config import Config

logger = logging.getLogger(__name__)
db = orm.Database()

FILE_HASHES = []

class FileHashes(db.Entity):
    __table__ = "hashes"
    hash = orm.PrimaryKey(str)

if not any((Config.DB_HOST, Config.DB_USER, Config.DB_PASSWORD, Config.DB_NAME)):
    logger.warning("External Database not configured. Using SQLite instead.")
    db.bind(provider="sqlite", filename="data.db", create_db=True)

else:
    db.bind(
        provider="postgres",
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        sslmode="require",
    )
    logger.info("Postgres Database configured.")

db.generate_mapping(create_tables=True)

async def addFileHash(fileHash: str):
    with orm.db_session:
        if not FileHashes.exists(hash=fileHash):
            try:
                FileHashes(hash=fileHash)
                db.commit()
                __loadFileHashes()
            except (orm.IntegrityError, orm.TransactionIntegrityError):
                return

def __loadFileHashes() -> list[str]:
    global FILE_HASHES
    with orm.db_session:
        FILE_HASHES = list(orm.select(h.hash for h in FileHashes))

def isNSFW(fileHash: str) -> Optional[bool]:
    return fileHash in FILE_HASHES

__loadFileHashes()