from main import calculate_overall_result


def test_overall_result_passes_when_all_tests_pass():
    results = [
        {"result": "PASS"},
        {"result": "PASS"},
        {"result": "PASS"}
    ]

    overall_result = calculate_overall_result(results)

    assert overall_result == "PASS"


def test_overall_result_fails_when_one_test_fails():
    results = [
        {"result": "PASS"},
        {"result": "FAIL"},
        {"result": "PASS"}
    ]

    overall_result = calculate_overall_result(results)

    assert overall_result == "FAIL"


def test_overall_result_fails_when_all_tests_fail():
    results = [
        {"result": "FAIL"},
        {"result": "FAIL"},
        {"result": "FAIL"}
    ]

    overall_result = calculate_overall_result(results)

    assert overall_result == "FAIL"
    
def test_overall_result_returns_no_tests_when_results_are_empty():
    results = []

    overall_result = calculate_overall_result(results)

    assert overall_result == "NO TESTS"