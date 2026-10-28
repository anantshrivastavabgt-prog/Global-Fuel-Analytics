from app import app

def run_tests():
    client = app.test_client()

    # Test 1: Home page
    res_home = client.get('/')
    assert res_home.status_code == 200, f"Home failed: {res_home.status_code}"
    assert b"Global Fuel Analytics" in res_home.data
    print("Test 1 Passed: Home Page 200 OK")

    # Test 2: API Data endpoint
    res_api = client.get('/api/data')
    assert res_api.status_code == 200, f"API failed: {res_api.status_code}"
    data = res_api.get_json()
    assert data['kpis']['avg_petrol'] == 2.28, f"Wrong petrol KPI: {data['kpis']['avg_petrol']}"
    assert data['kpis']['avg_diesel'] == 2.13, f"Wrong diesel KPI: {data['kpis']['avg_diesel']}"
    assert data['kpis']['avg_tax'] == 26.77, f"Wrong tax KPI: {data['kpis']['avg_tax']}"
    assert data['kpis']['count'] == 27468, f"Wrong record count: {data['kpis']['count']}"
    assert len(data['map_data']) == 84, f"Wrong country map count: {len(data['map_data'])}"
    assert len(data['yearly_trends']['years']) == 7, "Wrong years count"
    print("Test 2 Passed: API Data Global Aggregates 200 OK")

    # Test 3: API Filtered
    res_filt = client.get('/api/data?region=Europe&year=2024')
    assert res_filt.status_code == 200
    data_filt = res_filt.get_json()
    print("Test 3 Passed: API Filtered Data 200 OK (Europe 2024 records:", data_filt['kpis']['count'], ")")

    # Test 4: Story endpoint
    res_story = client.get('/api/story')
    assert res_story.status_code == 200
    scenes = res_story.get_json()
    assert len(scenes) == 7, f"Wrong scenes count: {len(scenes)}"
    print("Test 4 Passed: 7-Scene Data Story 200 OK")

    # Test 5: Documentation serving
    res_doc1 = client.get('/documentation/Project_Report.md')
    assert res_doc1.status_code == 200, "Doc report failed"
    res_doc2 = client.get('/documentation/Video_Presentation_Script.md')
    assert res_doc2.status_code == 200, "Video script failed"
    print("Test 5 Passed: Documentation & Script serving 200 OK")

    print("\n>>> ALL 5 TESTS PASSED WITH 100% SUCCESS! <<<")

if __name__ == '__main__':
    run_tests()
