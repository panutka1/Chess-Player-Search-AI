from rag import search, conversation, search_and_response

def test_conversation(mocker):
    mock_response = mocker.Mock()
    mock_response.text = "Magnus has a rating of 2830."
    mocker.patch("rag.client_ai.models.generate_content", return_value=mock_response)
    result = conversation("KWhat is the Magnus Carlsen's rating?", "Magnus Carlsen has a GM title and his rating is 2830.")
    assert result == mock_response.text


def test_search(mocker):
    mock_embedding_item = mocker.Mock()
    mock_embedding_item.values = [0.1, 0.2, 0.3]

    mock_embed_result = mocker.Mock()
    mock_embed_result.embeddings = [mock_embedding_item]

    mocker.patch("rag.client_ai.models.embed_content", return_value = mock_embed_result)
    
    mocker.patch("rag.collection.query", return_value={"documents": [["text 1", "text 2"]]})

    result = search("Question?")

    assert result == ["text 1", "text 2"]

def test_search_and_response(mocker):
    mocker.patch("rag.search", return_value = ["text 1", "text 2"])
    mocker.patch("rag.conversation", return_value = "This is the response for the question.")

    result = search_and_response("Question?")

    assert result == "This is the response for the question."


    