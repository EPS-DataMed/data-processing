import pytest
from unittest.mock import patch, Mock
from app.scraping import scrape_users

def test_scrape_users():
    html_content = """
    <div class="user">
        <span class="name">Luiz Gustavo</span>
        <span class="email">luiz.gustavo@example.com</span>
    </div>
    <div class="user">
        <span class="name">Maria Silva</span>
        <span class="email">maria.silva@example.com</span>
    </div>
    """
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.content = html_content
        mock_get.return_value = mock_response
        
        users = scrape_users("http://example.com")
        assert len(users) == 2
        assert users[0]["name"] == "Luiz Gustavo"
        assert users[0]["email"] == "luiz.gustavo@example.com"
        assert users[1]["name"] == "Maria Silva"
        assert users[1]["email"] == "maria.silva@example.com"