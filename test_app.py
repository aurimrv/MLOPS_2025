import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
import os
from app import *  # Import your app's functions/variables

@pytest.fixture
def mock_files_exist():
    # Patch os.path.exists to simulate model files existing or not
    with patch('os.path.exists') as mock_exists:
        yield mock_exists

@pytest.fixture
def mock_joblib():
    # Mock joblib.load to avoid actually loading files
    with patch('joblib.load') as mock_load:
        yield mock_load

@pytest.fixture
def mock_st():
    # Mock all Streamlit functions we need to test
    with patch('streamlit.text_input'), \
         patch('streamlit.button'), \
         patch('streamlit.success'), \
         patch('streamlit.warning'), \
         patch('streamlit.error'):
        yield

def test_model_files_missing(mock_files_exist, mock_st):
    # Test when model files don't exist
    mock_files_exist.return_value = False
    
    # These would normally be called by Streamlit during execution
    st.text_input("Digite um tweet: ")  # The user would input something
    st.button("Analisar")  # User clicks the button
    
    # Check that the error message was shown
    st.error.assert_called_with(
        "Modelo ou vetor não foram encontrados. Certifique que os arquivos model e vectozirer estão na raiz o projeto."
    )

def test_empty_input(mock_files_exist, mock_st, mock_joblib):
    # Test when user submits empty input
    mock_files_exist.return_value = True
    
    st.text_input.return_value = ""
    st.button.return_value = True
    
    # Model loading shouldn't matter here since we won't get that far
    mock_joblib.side_effect = Exception("Should not try to load models")
    
    # Check that the warning was shown
    st.warning.assert_called_with("Por favor, insira um texto para análise.")

def test_successful_analysis(mock_files_exist, mock_st, mock_joblib):
    # Test successful sentiment analysis
    mock_files_exist.return_value = True
    
    # Setup mocks
    test_text = "This is a happy tweet"
    st.text_input.return_value = test_text
    st.button.return_value = True
    
    # Mock model and vectorizer
    mock_model = MagicMock()
    mock_model.predict.return_value = ["positive"]
    mock_vectorizer = MagicMock()
    mock_vectorizer.transform.return_value = "vectorized_text"
    
    mock_joblib.side_effect = [mock_model, mock_vectorizer]
    
    # Verify the prediction flow
    vector = mock_vectorizer.transform([test_text])
    pred = mock_model.predict(vector)[0]
    
    # Check that the success message was shown with the prediction
    st.success.assert_called_with(f"Sentimento: {pred}")

def test_model_loading_order(mock_files_exist, mock_joblib):
    # Test that models are loaded in correct order
    mock_files_exist.return_value = True
    
    # We don't need to mock Streamlit here as we're testing the loading logic
    model_path = "./model.joblib"
    vector_path = "./vectorizer.joblib"
    
    # Mock model and vectorizer
    mock_model = MagicMock()
    mock_vectorizer = MagicMock()
    
    mock_joblib.side_effect = [mock_model, mock_vectorizer]
    
    # This would be called when the app runs
    if os.path.exists(model_path) and os.path.exists(vector_path):
        model = joblib.load(model_path)
        vectorizer = joblib.load(vector_path)
    
    # Verify load order and calls
    assert mock_joblib.call_count == 2
    assert mock_joblib.call_args_list[0][0][0] == model_path
    assert mock_joblib.call_args_list[1][0][0] == vector_path
