from unittest.mock import patch, MagicMock
import pytest

from app.Utilities.Calculations import calculate_score
from app.Utilities.Conversions import Conversions


def test_calculate_score_with_expected_values():
    # Arrange
    _converter = MagicMock(spec=Conversions) # mock converter as we are not testing that
    _converter.convert_iso_time_to_minutes.return_value = 1440
    price_weighting = 0.5
    expected_score = (0.5 / 1000) + ((1 - price_weighting) / 1440)

    # Act
    score = calculate_score(price_weighting, _converter, 1000., "PT24H")

    # Assert
    assert score == expected_score

def test_calculate_score_with_negative_price_weighting_raises_value_error():
    # Arrange
    _converter = MagicMock(spec=Conversions) # mock converter as we are not testing that
    _converter.convert_iso_time_to_minutes.return_value = 1440
    price_weighting = -1

    # Act & Assert
    with pytest.raises(ValueError):
        calculate_score(price_weighting, _converter, 1000., "PT24H")

def test_calculate_score_with_weighting_greater_than_1_raises_value_error():
    # Arrange
    _converter = MagicMock(spec=Conversions) # mock converter as we are not testing that
    _converter.convert_iso_time_to_minutes.return_value = 1440
    price_weighting = 2

    # Act & Assert
    with pytest.raises(ValueError):
        calculate_score(price_weighting, _converter, 1000., "PT24H")