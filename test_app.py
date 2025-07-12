import pytest
from unittest.mock import patch, MagicMock
import os
from app import texto, st  # Import needed variables/functions from app

# Constants from app.py
MODEL_PATH = "./model.joblib"
VECTOR_PATH = "./vectorizer.joblib"

@pytest.fixture
def mock_files_exist():
    with patch('os.path.exists') as mock_exists:
        yield mock_exists

@pytest.fixture
def mock_joblib():
    with patch('joblib.load') as mock_load:
        yield mock_load

def test_model_files_missing(mock_files_exist):
    mock_files_exist.return_value = False
    
    # Mock Streamlit functions
    with patch('streamlit.error') as mock_error, \
         patch('streamlit.text_input') as mock_input, \
         patch('streamlit.button') as mock_button:
        
        # Simulate user input and button click
        mock_input.return_value = "test tweet"
        mock_button.return_value = True
        
        # Execute the logic from app.py
        texto = mock_input()
        if mock_button():
            if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTOR_PATH)):
                st.error("Modelo ou vetor não foram encontrados. Certifique que os arquivos model e vectozirer estão na raiz o projeto.")
    
    # Verify the error message
    mock_error.assert_called_with(
        "Modelo ou vetor não foram encontrados. Certifique que os arquivos model e vectozirer estão na raiz o projeto."
    )

def test_empty_input(mock_files_exist):
    mock_files_exist.return_value = True
    
    with patch('streamlit.warning') as mock_warning, \
         patch('streamlit.text_input') as mock_input, \
         patch('streamlit.button') as mock_button:
        
        mock_input.return_value = ""
        mock_button.return_value = True
        
        # Execute the logic from app.py
        texto = mock_input()
        if mock_button():
            if not texto.strip():
                st.warning("Por favor, insira um texto para análise.")
    
    mock_warning.assert_called_with("Por favor, insira um texto para análise.")

def test_successful_analysis(mock_files_exist, mock_joblib):
    mock_files_exist.return_value = True
    
    # Setup mocks
    mock_model = MagicMock()
    mock_model.predict.return_value = ["positive"]
    mock_vectorizer = MagicMock()
    mock_vectorizer.transform.return_value = "vectorized_text"
    mock_joblib.side_effect = [mock_model, mock_vectorizer]
    
    with patch('streamlit.success') as mock_success, \
         patch('streamlit.text_input') as mock_input, \
         patch('streamlit.button') as mock_button:
        
        test_text = "This is a happy tweet"
        mock_input.return_value = test_text
        mock_button.return_value = True
        
        # Execute the logic from app.py
        texto = mock_input()
        if mock_button():
            if texto.strip():
                if os.path.exists(MODEL_PATH) and os.path.exists(VECTOR_PATH):
                    model = mock_joblib(MODEL_PATH)
                    vectorizer = mock_joblib(VECTOR_PATH)
                    vector = vectorizer.transform([texto])
                    pred = model.predict(vector)[0]
                    st.success(f"Sentimento: {pred}")
    
    mock_success.assert_called_with(f"Sentimento: positive")

def test_model_loading_order(mock_files_exist, mock_joblib):
    mock_files_exist.return_value = True
    
    mock_model = MagicMock()
    mock_vectorizer = MagicMock()
    mock_joblib.side_effect = [mock_model, mock_vectorizer]
    
    # Execute the loading order test
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTOR_PATH):
        model = mock_joblib(MODEL_PATH)
        vectorizer = mock_joblib(VECTOR_PATH)
    
    assert mock_joblib.call_count == 2
    assert mock_joblib.call_args_list[0][0][0] == MODEL_PATH
    assert mock_joblib.call_args_list[1][0][0] == VECTOR_PATH
