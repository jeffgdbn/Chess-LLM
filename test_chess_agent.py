from unittest.mock import patch

from chess_agent import explain_blunder_with_gemini


@patch("chess_agent.analyse_position")
@patch("chess_agent.genai.Client")
def test_explain_blunder_uses_analyse_position(mock_client_cls, mock_analyse):
    mock_analyse.return_value = {"evaluation": 1.3, "best_line": ["e4"]}
    mock_client = mock_client_cls.return_value
    mock_client.models.generate_content.return_value.text = "This is a blunder because it loses the queen."

    result = explain_blunder_with_gemini(
        "8/8/8/8/8/8/8/8 w - - 0 1",
        "d4",
        player_to_move="white",
        api_key="test-key",
    )

    assert result == "This is a blunder because it loses the queen."
    mock_analyse.assert_called_once_with(
        "8/8/8/8/8/8/8/8 w - - 0 1", depth=15, moves=["d4"]
    )


@patch("chess_agent.analyse_position")
@patch("chess_agent.genai.Client")
def test_explain_blunder_passes_tool_schema_to_gemini(mock_client_cls, mock_analyse):
    mock_analyse.return_value = {"evaluation": 1.3, "best_line": ["e4"]}
    mock_client = mock_client_cls.return_value
    mock_client.models.generate_content.return_value.text = "This is a blunder because it loses the queen."

    explain_blunder_with_gemini(
        "8/8/8/8/8/8/8/8 w - - 0 1",
        "d4",
        player_to_move="white",
        api_key="test-key",
    )

    config = mock_client.models.generate_content.call_args.kwargs["config"]
    assert config["automatic_function_calling"] == {"ignore_call_history": True}
    assert config["tools"][0]["function_declarations"][0]["name"] == "consult_engine"
    assert config["tools"][0]["function_declarations"][0]["parameters"]["properties"]["fen"]["type"] == "STRING"


@patch("chess_agent.analyse_position")
@patch("chess_agent.genai.Client")
def test_explain_blunder_sends_illegal_move_to_gemini(mock_client_cls, mock_analyse):
    mock_analyse.return_value = {"error": "Illegal move at index 0: 'd4'"}
    mock_client = mock_client_cls.return_value
    mock_client.models.generate_content.return_value.text = "The move is illegal."

    result = explain_blunder_with_gemini(
        "8/8/8/8/8/8/8/8 w - - 0 1",
        "d4",
        api_key="test-key",
    )

    assert result == "The move is illegal."
    prompt = mock_client.models.generate_content.call_args.kwargs["contents"]
    assert "Illegal move at index 0: 'd4'" in prompt


@patch("chess_agent.analyse_position")
@patch("chess_agent.genai.Client")
def test_explain_blunder_uses_real_consult_engine_tool(mock_client_cls, mock_analyse):
    mock_analyse.return_value = {"evaluation": 1.3, "best_line": ["e4"]}
    mock_client = mock_client_cls.return_value
    mock_client.models.generate_content.return_value.text = "This is a blunder."

    explain_blunder_with_gemini(
        "8/8/8/8/8/8/8/8 w - - 0 1",
        "d4",
        player_to_move="white",
        api_key="test-key",
    )

    config = mock_client.models.generate_content.call_args.kwargs["config"]
    assert config["automatic_function_calling"] == {"ignore_call_history": True}
    assert config["tools"][0]["function_declarations"][0]["name"] == "consult_engine"
    assert config["tools"][0]["function_declarations"][0]["description"].startswith("Get Stockfish")
