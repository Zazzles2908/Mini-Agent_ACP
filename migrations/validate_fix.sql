-- VALIDATION QUERY: Test if exec_sql function works
SELECT * FROM exec_sql('SELECT 1 as test_value');

-- EXPECTED RESULT: Should return a row with test_value = 1