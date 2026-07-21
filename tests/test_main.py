from main import player_data, chess_player_search
import requests

def test_player_data():
    
    test_player = {
        "username": "panutka",
        "title": "WGM",
        "name": "panutka",
        "followers": 100,
        "location": "Poland"
    }

    result = player_data(test_player)

    assert result == "WGM panutka has 100 followers and is from Poland"


def test_chess_player_search_200(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "username": "magnuscarlsen",
        "title": "GM",
        "name": "Magnus Carlsen",
        "followers": 305220,
        "location": "Norway"
        }

    mocker.patch("main.requests.request", return_value=mock_response)

    result = chess_player_search("magnuscarlsen")
    assert result == "GM Magnus Carlsen has 305220 followers and is from Norway"


def test_chess_player_search_404(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {
        "message": "User not found"
        }

    mocker.patch("main.requests.request", return_value=mock_response)

    result = chess_player_search("NotExistingUser")
    assert result == "User not found"


def test_chess_player_search_empty():
    empty_player = ''
    result = chess_player_search(empty_player)
    assert result == "Enter username!"

def test_chess_player_search_error(mocker):
    mocker.patch("main.requests.request", side_effect=requests.exceptions.ConnectionError("Connection failed"))

    result = chess_player_search("Connection failed")
    assert result == (f"Server error, try later: Connection failed")