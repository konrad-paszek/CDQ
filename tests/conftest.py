from pathlib import Path
from uuid import uuid4

import pytest
from bson import ObjectId
from faker import Faker

from cdq.infra.mongodb import mongoclient

from .util import seed_mongo_from_file, teardown_mongo


def pytest_addoption(parser):
    parser.addoption(
        "--seed",
        action="store_true",
        default=False,
        help="Seeds test database before executing tests",
    )


def pytest_sessionstart(session):
    config = session.config

    if config.getoption("--seed"):
        storage_one = Path(__file__).parent / "data" / "storage_one.json"
        teardown_mongo()
        seed_mongo_from_file(
            storage_one.as_posix(), "BUSINESS_PARTNER_STORAGE", "storage_one"
        )
