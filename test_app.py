"""
End-to-end Verification and Unit Tests for ClinicalTrial Match AI
HealthTech & Bio-Innovation Hackathon
"""

import sys
import os
import json

# Ensure project path is accessible
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import app
from backend.clinical_api import search_studies, get_study_by_nct_id, parse_age_to_years
from backend.matcher import match_study_with_profile
from backend.explainer import explain_trial


def run_all_tests():
    print("==================================================")
    print("Running ClinicalTrial Match AI Verification Suite")
    print("==================================================")

    # 1. Test age parser
    print("\n[Test 1] Age Parser...")
    assert parse_age_to_years("18 Years") == 18.0
    assert parse_age_to_years("65 Years") == 65.0
    assert parse_age_to_years("6 Months") == 0.5
    assert parse_age_to_years(None) is None
    print("  -> PASSED: Age parser correctly handles years, months, None.")

    # 2. Test Real API Search
    print("\n[Test 2] Real ClinicalTrials.gov API v2 Search...")
    search_res = search_studies(condition="Non-Small Cell Lung Cancer", status="RECRUITING", page_size=3)
    assert search_res.get("success") is True, f"Search failed: {search_res.get('error')}"
    studies = search_res.get("studies", [])
    assert len(studies) > 0, "No studies returned from ClinicalTrials.gov API!"
    sample = studies[0]
    nct_id = sample.get("nctId")
    print(f"  -> Retrieved real study: {nct_id}")
    print(f"  -> Title: {sample.get('briefTitle')[:70]}...")
    print(f"  -> Sponsor: {sample.get('leadSponsor')}")
    print(f"  -> Status: {sample.get('overallStatus')}")
    print(f"  -> Age limits: Min={sample.get('eligibility', {}).get('minimumAge')}, Max={sample.get('eligibility', {}).get('maximumAge')}")
    print("  -> PASSED: Real public API v2 connected and retrieved legitimate study records.")

    # 3. Test Explainable Matching Engine
    print("\n[Test 3] Explainable Matching Logic...")
    profile_fit = {
        "condition": "Lung Cancer",
        "age": 55,
        "sex": "ALL",
        "location": "United States"
    }
    match_fit = match_study_with_profile(sample, profile_fit)
    print(f"  -> Overall Match: {match_fit.get('overallStatus')} ({match_fit.get('overallBadge')})")
    print(f"  -> Alignment Text: {match_fit.get('alignmentText')}")
    print(f"  -> Criteria breakdown count: {len(match_fit.get('breakdown', []))}")
    assert match_fit.get("overallStatus") in ["Supported", "Unknown", "Potential Conflict"]
    assert "disclaimer" in match_fit
    assert "eligibility probability" not in match_fit["disclaimer"].lower() or "not an eligibility probability" in match_fit["disclaimer"].lower()
    print("  -> PASSED: Match engine operates with correct status labels and disclaimers.")

    # 4. Test Conflict Detection (e.g. Underage)
    print("\n[Test 4] Conflict Detection (e.g. Underage Patient)...")
    profile_underage = {
        "condition": "Lung Cancer",
        "age": 10,  # Underage for adult trial
        "sex": "ALL"
    }
    match_conflict = match_study_with_profile(sample, profile_underage)
    print(f"  -> Overall for age 10: {match_conflict.get('overallStatus')}")
    age_eval = next((c for c in match_conflict["breakdown"] if c["title"] == "Age Criteria"), None)
    if sample.get("eligibility", {}).get("minAgeYears", 0) > 10:
        assert age_eval["status"].upper() == "POTENTIAL CONFLICT"
        print(f"  -> Conflict explanation: {age_eval['explanation']}")
    print("  -> PASSED: Criteria conflict properly flagged without false claims.")

    # 5. Test AI Plain-Language Explainer
    print("\n[Test 5] AI Plain-Language Explainer (NLP & Protocol Grounding)...")
    explanation = explain_trial(sample, profile_fit)
    assert explanation.get("nctId") == nct_id
    assert len(explanation.get("plainLanguageSummary", "")) > 20
    assert len(explanation.get("keyInclusionCriteria", [])) > 0
    assert len(explanation.get("keyExclusionCriteria", [])) > 0
    assert len(explanation.get("missingInformation", [])) > 0
    assert len(explanation.get("questionsToAsk", [])) >= 4
    print(f"  -> Engine used: {explanation.get('engineUsed')}")
    print(f"  -> Plain Summary: {explanation.get('plainLanguageSummary')[:120]}...")
    print(f"  -> Questions count: {len(explanation.get('questionsToAsk'))}")
    print("  -> Sample question: " + explanation.get("questionsToAsk")[0])
    print("  -> PASSED: Plain-language explanation generated with all required sections.")

    # 6. Test Flask HTTP Endpoints via test_client
    print("\n[Test 6] Flask Client Integration...")
    client = app.test_client()

    # Health check
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json["status"] == "healthy"
    print("  -> /api/health: OK (200)")

    # Search API
    res_search = client.post("/api/search", json={
        "condition": "Type 2 Diabetes",
        "age": 52,
        "sex": "ALL",
        "status": "RECRUITING",
        "pageSize": 2
    })
    assert res_search.status_code == 200
    assert res_search.json["success"] is True
    assert len(res_search.json["studies"]) > 0
    first_study = res_search.json["studies"][0]
    assert "matchAssessment" in first_study
    assert "overallStatus" in first_study["matchAssessment"]
    print(f"  -> /api/search: OK (200), returned {len(res_search.json['studies'])} matched studies")

    # Single Study endpoint
    res_study = client.get(f"/api/study/{first_study['nctId']}")
    assert res_study.status_code == 200
    assert res_study.json["study"]["nctId"] == first_study["nctId"]
    print(f"  -> /api/study/{first_study['nctId']}: OK (200)")

    # Explain endpoint
    res_explain = client.post("/api/explain", json={
        "study": first_study,
        "profile": {"condition": "Type 2 Diabetes", "age": 52, "sex": "ALL"}
    })
    assert res_explain.status_code == 200
    assert res_explain.json["success"] is True
    assert "plainLanguageSummary" in res_explain.json["explanation"]
    print("  -> /api/explain: OK (200)")

    # Assistant chat endpoint
    res_chat = client.post("/api/assistant/chat", json={
        "study": first_study,
        "question": "What treatment is being tested?"
    })
    assert res_chat.status_code == 200
    assert res_chat.json["success"] is True
    assert len(res_chat.json["answer"]) > 20
    print("  -> /api/assistant/chat: OK (200)")

    # Glossary endpoint
    res_glossary = client.get("/api/glossary")
    assert res_glossary.status_code == 200
    assert "randomized" in res_glossary.json["glossary"]
    print("  -> /api/glossary: OK (200)")

    # Compare endpoint
    res_compare = client.post("/api/compare", json={
        "studies": [first_study]
    })
    assert res_compare.status_code == 200
    assert len(res_compare.json["trials"]) == 1
    print("  -> /api/compare: OK (200)")

    # Regression check on NCT07282743
    print("\n[Regression Test] NCT07282743 Study Lookup...")
    reg_study = get_study_by_nct_id("NCT07282743")
    assert reg_study.get("success") is True
    assert reg_study["study"]["nctId"] == "NCT07282743"
    print(f"  -> NCT07282743 verified: Status={reg_study['study']['overallStatus']}, Phase={reg_study['study']['phases']}")

    # Error test: Missing condition returns 400
    res_err = client.post("/api/search", json={"condition": ""})
    assert res_err.status_code == 400
    assert res_err.json["success"] is False
    print("  -> /api/search validation: OK (400 on empty query)")

    print("\n==================================================")
    print("ALL 6 VERIFICATION TEST SUITES PASSED SUCCESSFULLY!")
    print("==================================================")


if __name__ == "__main__":
    run_all_tests()
