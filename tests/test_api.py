from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "It works!"}

def test_get_player(mocker):
    mocker.patch("api.chess_player_search", return_value="GM Magnus Carlsen has 305220 followers and is from Norway")

    response = client.get("/player/magnuscarlsen")
    assert response.status_code == 200
    assert response.json() == "GM Magnus Carlsen has 305220 followers and is from Norway"

def test_get_player_404(mocker):
    mocker.patch("api.chess_player_search", return_value="User not found")

    response = client.get("/player/User_not_found")
    assert response.status_code == 200
    assert response.json() == "User not found"

def test_chat(mocker):
    mocker.patch("api.chess_player_search", return_value="GM Magnus Carlsen has 305220 followers and is from Norway")
    mock_client_instance = mocker.Mock()
    mocker.patch("api.genai.Client", return_value = mock_client_instance)
    mock_response = mocker.Mock()
    mock_response.text = "Magnus has a rating of 2830."
    mock_client_instance.models.generate_content.return_value = mock_response
    response = client.post("/chat", json={"name": "magnuscarlsen", "question": "What is Magnus Carlsen's rating?"})
    assert response.status_code == 200
    assert response.json() == "Magnus has a rating of 2830."


def test_rag(mocker):
    mocker.patch("api.search_and_response", return_value = "Magnus has a rating of 2830.")
    response = client.post("/rag", json={"question": "What is Magnus Carlsen's rating?"})
    assert response.status_code == 200
    assert response.json() == "Magnus has a rating of 2830."