from app.Utilities import Conversions

    
def calculate_score(price_weighting: float, converter: Conversions, price: float, duration: str):
    if price_weighting > 1 or price_weighting < 0:
        raise ValueError("Weighting value msut be between 0 and 1")
    duration_weighting = 1 - price_weighting
    duration_minutes = converter.convert_iso_time_to_minutes(duration)

    return (price_weighting / price ) + (duration_weighting / duration_minutes)