import pytest
from eva_data_analysis import text_to_duration, calculate_crew_size

def test_test_to_duration_float():
    """
    Test that text_to_duration returns expected ground truth values
    for typical durations with a non-zero minute component
    """
    assert text_to_duration("10:20") == pytest.approx(10.333333333)

def test_text_to_duration_integer():
    """
    Test that text_to_duration returns expected ground truth values
    for typical whole hour durations
    """
    assert text_to_duration("10:00") == 10

@pytest.mark.parametrize("input_value, expected_result",
                         [
                            ("Valentina Tereshkova;", 1),
                            ("Judith Resnik; Sally Ride;", 2)
                         ]
                         )
def test_calculate_crew_size(input_value, expected_result): 
    """
    Test that the test_calculate_crew_size function is correct.
    """
    actual_result = calculate_crew_size(input_value)
    assert actual_result == expected_result
    
    actual_result = calculate_crew_size("Judith Resnik; Sally Ride;")
    expected_result = 2
    assert actual_result == expected_result

def test_calculate_crew_size_edge_cases():
    """
    Test it returns expected values for edge cases where crew is an empty string
    """
    actual_result = calculate_crew_size("")
    assert actual_result is None