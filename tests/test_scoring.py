from app.scoring import compute_accessibility_score, compute_delay_penalty


def test_accessibility_score_formula():
    result = compute_accessibility_score(nearby_metro_count=2, nearby_bus_count=6, live_delay_penalty=1)
    assert result["score"] == 11
    assert result["rating"] == "High"


def test_accessibility_score_low_medium_high_bands():
    assert compute_accessibility_score(0, 2, 0)["rating"] == "Low"
    assert compute_accessibility_score(1, 1, 0)["rating"] == "Medium"
    assert compute_accessibility_score(2, 1, 0)["rating"] == "High"


def test_delay_penalty_only_counts_medium_and_high_nearby():
    events = [
        {"severity": "medium", "lat": 24.7136, "lon": 46.6753},
        {"severity": "low", "lat": 24.7136, "lon": 46.6753},
        {"severity": "high", "lat": 25.0, "lon": 47.0},
    ]
    assert compute_delay_penalty(24.7136, 46.6753, events, 1.5) == 1
