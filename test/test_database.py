import sys
import os
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import pytest
from app.database import get_db, SessionLocal

def test_get_db():
    mock_session = MagicMock(spec=Session)
    
    with patch('app.database.SessionLocal', return_value=mock_session):
        generator = get_db()
        db = next(generator)
        assert db == mock_session

        with pytest.raises(StopIteration):
            next(generator)