"""
zones.py - All zone and challenge data for Postgres Quest
Challenge types: quiz, flag_quiz, fill_blank, sql_live (handled by PostgresChallengeRunner)
"""

ZONES = {
    "surface_tables": {
        "id": "surface_tables",
        "name": "The Surface Tables",
        "subtitle": "Basic SELECT",
        "color": "blue",
        "icon": "🗃",
        "commands": ["SELECT", "FROM", "LIMIT", "ORDER BY", "DISTINCT", "AS"],
        "challenges": [
            {
                "id": "surf_1",
                "type": "quiz",
                "title": "The Opening Keyword",
                "flavor": "The database is waiting. One word opens every read operation in SQL. What is it?",
                "lesson": (
                    "SELECT — retrieves data from one or more tables.\n\n"
                    "Syntax: SELECT column1, column2 FROM table_name;\n\n"
                    "Use * to select all columns:\n"
                    "  SELECT * FROM table_name;\n\n"
                    "SQL keywords are conventionally written in UPPERCASE, but are not case-sensitive.\n\n"
                    "Example: SELECT name, salary FROM employees;"
                ),
                "question": "What SQL keyword begins every data retrieval query?",
                "answers": ["SELECT", "select"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It's the first word in every read query.",
                    "Think: you are selecting data from the database.",
                    "The answer is: SELECT",
                ],
            },
            {
                "id": "surf_2",
                "type": "quiz",
                "title": "The Source Clause",
                "flavor": "SELECT tells the database what columns you want. What tells it which table?",
                "lesson": (
                    "FROM — specifies which table to retrieve data from.\n\n"
                    "Syntax: SELECT columns FROM table_name;\n\n"
                    "FROM comes after SELECT and before any other clauses (WHERE, ORDER BY, etc.).\n\n"
                    "Example: SELECT * FROM orders;    → all rows and columns from 'orders' table"
                ),
                "question": "What SQL clause specifies which table to query?",
                "answers": ["FROM", "from"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It describes the source of the data.",
                    "It comes directly after the column list in a SELECT.",
                    "The answer is: FROM",
                ],
            },
            {
                "id": "surf_3",
                "type": "fill_blank",
                "title": "Retrieve Everything",
                "flavor": "You need to see all columns in the table. No filtering. No selection. Everything.",
                "lesson": (
                    "SELECT * — the wildcard selector. Retrieves all columns from a table.\n\n"
                    "Syntax: SELECT * FROM table_name;\n\n"
                    "The * means 'all columns'. Useful for exploration but avoid in production\n"
                    "queries where you only need specific columns.\n\n"
                    "Example: SELECT * FROM employees;    → returns every column for every row"
                ),
                "question": "Complete this query to retrieve all columns from the 'users' table:\n\nSELECT ___ FROM users;",
                "answers": ["*"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It's a single wildcard character.",
                    "Think 'all columns'.",
                    "The answer is: *",
                ],
            },
            {
                "id": "surf_4",
                "type": "fill_blank",
                "title": "Cap the Output",
                "flavor": "The table has forty million rows. You need to see the first ten to understand the structure. Don't let it pour the whole thing onto your screen.",
                "lesson": (
                    "LIMIT — restricts the number of rows returned by a query.\n\n"
                    "Syntax: SELECT columns FROM table_name LIMIT n;\n\n"
                    "LIMIT is always the last clause in a SELECT statement.\n"
                    "Essential for exploration — never run SELECT * without a LIMIT on large tables.\n\n"
                    "Example: SELECT * FROM transactions LIMIT 10;    → returns only the first 10 rows"
                ),
                "question": "Complete this query to return only the first 5 rows from 'contracts':\n\nSELECT * FROM contracts ___ 5;",
                "answers": ["LIMIT", "limit"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It restricts how many rows come back.",
                    "It comes at the end of the SELECT statement.",
                    "The answer is: LIMIT",
                ],
            },
            {
                "id": "surf_5",
                "type": "quiz",
                "title": "Sort the Results",
                "flavor": "The data came back in no particular order. You need it sorted by date, ascending. Which clause handles that?",
                "lesson": (
                    "ORDER BY — sorts the result set by one or more columns.\n\n"
                    "Syntax: SELECT columns FROM table ORDER BY column [ASC|DESC];\n\n"
                    "  ASC   ascending order (smallest to largest, A to Z) — this is the default\n"
                    "  DESC  descending order (largest to smallest, Z to A)\n\n"
                    "You can sort by multiple columns: ORDER BY col1 ASC, col2 DESC\n\n"
                    "Example: SELECT * FROM employees ORDER BY salary DESC;    → highest-paid first"
                ),
                "question": "What SQL clause sorts query results?",
                "answers": ["ORDER BY", "order by"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It controls the sequence of rows in the output.",
                    "It's two words.",
                    "The answer is: ORDER BY",
                ],
            },
            {
                "id": "surf_boss",
                "type": "fill_blank",
                "title": "BOSS: The Surface Layer Audit",
                "flavor": "The compliance system is running a query audit. One query — all columns from 'transactions', ordered by amount descending, showing only the top 10. Clean and correct.",
                "lesson": (
                    "Combining SELECT, FROM, ORDER BY, and LIMIT:\n\n"
                    "  SELECT * FROM table ORDER BY column DESC LIMIT n;\n\n"
                    "Clause order matters in SQL:\n"
                    "  SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT\n\n"
                    "Example: SELECT * FROM transactions ORDER BY amount DESC LIMIT 10;\n"
                    "  → returns the 10 highest-value transactions"
                ),
                "question": (
                    "Complete this query — all columns from 'transactions',\n"
                    "ordered by amount descending, top 10 only:\n\n"
                    "SELECT * FROM transactions ___ BY amount DESC LIMIT 10;"
                ),
                "answers": ["ORDER", "order"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You're sorting the results.",
                    "The clause is two words: ORDER BY.",
                    "The answer is: ORDER",
                ],
            },
        ],
    },

    "filter_chambers": {
        "id": "filter_chambers",
        "name": "The Filter Chambers",
        "subtitle": "WHERE Clauses",
        "color": "cyan",
        "icon": "🔍",
        "commands": ["WHERE", "AND", "OR", "NOT", "LIKE", "IN", "BETWEEN", "IS NULL"],
        "challenges": [
            {
                "id": "filt_1",
                "type": "quiz",
                "title": "The Condition Gate",
                "flavor": "Two hundred billion rows. You need one. Which SQL keyword filters rows by condition?",
                "lesson": (
                    "WHERE — filters rows based on a condition. Only rows where the condition is TRUE are returned.\n\n"
                    "Syntax: SELECT columns FROM table WHERE condition;\n\n"
                    "Comparison operators:\n"
                    "  =     equal\n"
                    "  !=    not equal (also <>)\n"
                    "  >     greater than\n"
                    "  <     less than\n"
                    "  >=    greater than or equal\n"
                    "  <=    less than or equal\n\n"
                    "Example: SELECT * FROM employees WHERE department = 'Engineering';"
                ),
                "question": "What SQL clause filters rows based on a condition?",
                "answers": ["WHERE", "where"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It specifies a condition that rows must satisfy.",
                    "It comes after FROM in a SELECT statement.",
                    "The answer is: WHERE",
                ],
            },
            {
                "id": "filt_2",
                "type": "fill_blank",
                "title": "Compound Conditions",
                "flavor": "You need rows that match condition A AND condition B. Both must be true. What joins them?",
                "lesson": (
                    "AND — combines two conditions; both must be true for the row to be returned.\n"
                    "OR  — combines two conditions; at least one must be true.\n"
                    "NOT — negates a condition.\n\n"
                    "Syntax: WHERE condition1 AND condition2\n"
                    "        WHERE condition1 OR condition2\n"
                    "        WHERE NOT condition\n\n"
                    "Example: SELECT * FROM orders WHERE status = 'pending' AND amount > 1000;"
                ),
                "question": "Complete this query to find active employees in the Engineering department:\n\nSELECT * FROM employees WHERE department = 'Engineering' ___ status = 'active';",
                "answers": ["AND", "and"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "You need both conditions to be true.",
                    "It's a logical operator, three letters.",
                    "The answer is: AND",
                ],
            },
            {
                "id": "filt_3",
                "type": "fill_blank",
                "title": "Pattern Matching",
                "flavor": "You know the value starts with 'CORP-' but you don't know the rest. Wildcards.",
                "lesson": (
                    "LIKE — performs pattern matching on string values.\n\n"
                    "Wildcards:\n"
                    "  %    matches any sequence of characters (including empty)\n"
                    "  _    matches exactly one character\n\n"
                    "Examples:\n"
                    "  WHERE name LIKE 'Corp%'      starts with 'Corp'\n"
                    "  WHERE code LIKE 'CORP-___'   'CORP-' followed by exactly 3 chars\n"
                    "  WHERE email LIKE '%@corp.com'  ends with '@corp.com'\n\n"
                    "Note: ILIKE performs case-insensitive matching (PostgreSQL extension)"
                ),
                "question": "Complete this query to find all contract IDs starting with 'CORP-':\n\nSELECT * FROM contracts WHERE contract_id ___ 'CORP-%';",
                "answers": ["LIKE", "like"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "It performs pattern matching with wildcards.",
                    "The % wildcard matches any sequence of characters.",
                    "The answer is: LIKE",
                ],
            },
            {
                "id": "filt_4",
                "type": "fill_blank",
                "title": "Null Detection",
                "flavor": "Some records have no value in the 'terminated_at' column — those are active employees. Test for absence of data.",
                "lesson": (
                    "IS NULL / IS NOT NULL — tests whether a column value is null (absent).\n\n"
                    "NULL means no value — not zero, not empty string, just absent.\n"
                    "You CANNOT use = NULL or != NULL — these always return false.\n"
                    "You MUST use IS NULL or IS NOT NULL.\n\n"
                    "Examples:\n"
                    "  WHERE terminated_at IS NULL       still employed\n"
                    "  WHERE terminated_at IS NOT NULL   has been terminated\n\n"
                    "Example: SELECT * FROM employees WHERE terminated_at IS NULL;"
                ),
                "question": "Complete this query to find employees who haven't been terminated (terminated_at is null):\n\nSELECT * FROM employees WHERE terminated_at ___ NULL;",
                "answers": ["IS", "is"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "You can't use = to test for null.",
                    "The correct operator is two words: IS NULL.",
                    "The answer is: IS",
                ],
            },
            {
                "id": "filt_5",
                "type": "fill_blank",
                "title": "Range Filter",
                "flavor": "You need records where the amount falls between two values. There's a cleaner way than amount >= x AND amount <= y.",
                "lesson": (
                    "BETWEEN — tests if a value falls within an inclusive range.\n\n"
                    "Syntax: WHERE column BETWEEN low AND high\n\n"
                    "BETWEEN is inclusive — it includes both the low and high boundary values.\n"
                    "Equivalent to: WHERE column >= low AND column <= high\n\n"
                    "Also works with dates:\n"
                    "  WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'\n\n"
                    "Example: SELECT * FROM transactions WHERE amount BETWEEN 1000 AND 5000;"
                ),
                "question": "Complete this query to find transactions with amounts from 500 to 2000:\n\nSELECT * FROM transactions WHERE amount ___ 500 AND 2000;",
                "answers": ["BETWEEN", "between"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "It tests whether a value falls within an inclusive range.",
                    "It uses AND to specify the boundaries.",
                    "The answer is: BETWEEN",
                ],
            },
            {
                "id": "filt_boss",
                "type": "fill_blank",
                "title": "BOSS: The Anomaly Filter",
                "flavor": "The financial anomalies are in accounts with status 'flagged' OR 'suspended', created after 2022, with a balance over 50000. Extract them.",
                "lesson": (
                    "Combining multiple WHERE conditions — operator precedence:\n\n"
                    "  AND has higher precedence than OR.\n"
                    "  Use parentheses to make complex conditions explicit:\n\n"
                    "  WHERE (status = 'flagged' OR status = 'suspended')\n"
                    "    AND created_at > '2022-12-31'\n"
                    "    AND balance > 50000\n\n"
                    "Alternative using IN for the status check:\n"
                    "  WHERE status IN ('flagged', 'suspended')\n"
                    "    AND created_at > '2022-12-31'\n"
                    "    AND balance > 50000"
                ),
                "question": (
                    "Complete this query — accounts that are 'flagged' OR 'suspended',\n"
                    "created after 2022, with balance over 50000:\n\n"
                    "SELECT * FROM accounts WHERE status ___ ('flagged', 'suspended')\n"
                    "AND created_at > '2022-12-31' AND balance > 50000;"
                ),
                "answers": ["IN", "in"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "Use IN to check if a value is in a list.",
                    "IN ('value1', 'value2') is cleaner than OR conditions.",
                    "The answer is: IN",
                ],
            },
        ],
    },

    "aggregation_engine": {
        "id": "aggregation_engine",
        "name": "The Aggregation Engine",
        "subtitle": "GROUP BY & Aggregations",
        "color": "yellow",
        "icon": "📊",
        "commands": ["COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY", "HAVING"],
        "challenges": [
            {
                "id": "agg_1",
                "type": "quiz",
                "title": "Count the Records",
                "flavor": "How many rows match this condition? Not the rows themselves — just the count.",
                "lesson": (
                    "COUNT() — returns the number of rows that match a query.\n\n"
                    "Syntax: SELECT COUNT(*) FROM table;\n"
                    "        SELECT COUNT(column) FROM table;   — counts non-null values\n\n"
                    "Common variants:\n"
                    "  COUNT(*)          counts all rows including nulls\n"
                    "  COUNT(column)     counts rows where column is not null\n"
                    "  COUNT(DISTINCT c) counts distinct non-null values\n\n"
                    "Example: SELECT COUNT(*) FROM orders WHERE status = 'pending';"
                ),
                "question": "Which aggregate function counts the number of rows?",
                "answers": ["COUNT", "count", "COUNT()", "count()", "COUNT(*)", "count(*)"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: you want to count something.",
                    "It's an aggregate function that works with (*) or a column name.",
                    "The answer is: COUNT",
                ],
            },
            {
                "id": "agg_2",
                "type": "quiz",
                "title": "Sum the Values",
                "flavor": "Total revenue. Total fraud. Total anything. Which function adds up a numeric column?",
                "lesson": (
                    "SUM() — calculates the total of a numeric column.\n\n"
                    "Syntax: SELECT SUM(column) FROM table;\n\n"
                    "SUM ignores NULL values.\n"
                    "Combine with WHERE to sum only matching rows.\n\n"
                    "Example: SELECT SUM(amount) FROM transactions WHERE type = 'credit';\n"
                    "  → total credit transaction value"
                ),
                "question": "Which aggregate function calculates the total of a numeric column?",
                "answers": ["SUM", "sum"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think arithmetic — adding up all values in a column.",
                    "It's three letters.",
                    "The answer is: SUM",
                ],
            },
            {
                "id": "agg_3",
                "type": "fill_blank",
                "title": "Slice by Category",
                "flavor": "You need the total per department, not the grand total. Which clause groups the aggregation by category?",
                "lesson": (
                    "GROUP BY — groups rows that have the same values in specified columns,\n"
                    "allowing aggregate functions to operate on each group separately.\n\n"
                    "Syntax: SELECT column, AGG_FUNC(other_col)\n"
                    "        FROM table\n"
                    "        GROUP BY column;\n\n"
                    "Every column in SELECT that is not an aggregate must appear in GROUP BY.\n\n"
                    "Example:\n"
                    "  SELECT department, COUNT(*), SUM(salary)\n"
                    "  FROM employees\n"
                    "  GROUP BY department;"
                ),
                "question": "Complete this query to get total sales per region:\n\nSELECT region, SUM(amount) FROM sales ___ BY region;",
                "answers": ["GROUP", "group"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "You need to group rows by a category before aggregating.",
                    "The clause is two words: GROUP BY.",
                    "The answer is: GROUP",
                ],
            },
            {
                "id": "agg_4",
                "type": "fill_blank",
                "title": "Filter the Groups",
                "flavor": "WHERE filters individual rows before grouping. What filters group results after aggregation?",
                "lesson": (
                    "HAVING — filters groups after GROUP BY, based on aggregate values.\n\n"
                    "WHERE filters individual rows (before grouping).\n"
                    "HAVING filters groups (after grouping and aggregating).\n\n"
                    "Syntax:\n"
                    "  SELECT department, COUNT(*)\n"
                    "  FROM employees\n"
                    "  GROUP BY department\n"
                    "  HAVING COUNT(*) > 10;\n\n"
                    "Example: Show only departments with more than 10 employees."
                ),
                "question": "Complete this query to show only departments where average salary exceeds 100000:\n\nSELECT department, AVG(salary) FROM employees GROUP BY department ___ AVG(salary) > 100000;",
                "answers": ["HAVING", "having"],
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "You're filtering on an aggregate value — WHERE can't do this.",
                    "It comes after GROUP BY.",
                    "The answer is: HAVING",
                ],
            },
            {
                "id": "agg_5",
                "type": "quiz",
                "title": "Extreme Values",
                "flavor": "Highest salary. Lowest balance. Earliest transaction date. Which functions extract extreme values?",
                "lesson": (
                    "MIN() and MAX() — return the smallest and largest values in a column.\n\n"
                    "  MIN(column)  → smallest value (works with numbers, dates, strings)\n"
                    "  MAX(column)  → largest value\n"
                    "  AVG(column)  → average (mean) of numeric values\n\n"
                    "All ignore NULL values.\n\n"
                    "Example:\n"
                    "  SELECT MIN(salary), MAX(salary), AVG(salary)\n"
                    "  FROM employees\n"
                    "  WHERE department = 'Engineering';"
                ),
                "question": "Which two aggregate functions return the smallest and largest values in a column?",
                "answers": ["MIN and MAX", "MAX and MIN", "MIN, MAX", "MAX, MIN", "MIN() and MAX()", "MIN() MAX()"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Think minimum and maximum.",
                    "Both are three-letter functions.",
                    "The answer is: MIN and MAX",
                ],
            },
            {
                "id": "agg_boss",
                "type": "fill_blank",
                "title": "BOSS: The Aggregation Report",
                "flavor": "The monitoring system expects to see aggregation queries that look like standard reporting. Your cover: a report showing department headcount, only for departments with more than 5 employees.",
                "lesson": (
                    "Full aggregation query structure:\n\n"
                    "  SELECT department, COUNT(*) AS headcount\n"
                    "  FROM employees\n"
                    "  WHERE status = 'active'\n"
                    "  GROUP BY department\n"
                    "  HAVING COUNT(*) > 5\n"
                    "  ORDER BY headcount DESC;\n\n"
                    "Clause order: SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT"
                ),
                "question": (
                    "Complete this query — active employee count per department,\n"
                    "only departments with more than 5 employees:\n\n"
                    "SELECT department, COUNT(*) FROM employees WHERE status = 'active'\n"
                    "GROUP BY department ___ COUNT(*) > 5;"
                ),
                "answers": ["HAVING", "having"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You need to filter groups after aggregating.",
                    "WHERE filters rows; this clause filters groups.",
                    "The answer is: HAVING",
                ],
            },
        ],
    },

    "junction_archive": {
        "id": "junction_archive",
        "name": "The Junction Archive",
        "subtitle": "JOIN Operations",
        "color": "magenta",
        "icon": "🔗",
        "commands": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "ON", "USING"],
        "challenges": [
            {
                "id": "join_1",
                "type": "quiz",
                "title": "Connecting the Tables",
                "flavor": "The employee data is in one table. The salary data is in another. Which SQL operation combines them?",
                "lesson": (
                    "JOIN — combines rows from two or more tables based on a related column.\n\n"
                    "Syntax:\n"
                    "  SELECT columns\n"
                    "  FROM table1\n"
                    "  JOIN table2 ON table1.id = table2.table1_id;\n\n"
                    "The ON clause specifies the condition that links the two tables.\n"
                    "Typically: primary key of one table = foreign key of the other.\n\n"
                    "Example: SELECT e.name, s.salary\n"
                    "         FROM employees e\n"
                    "         JOIN salaries s ON e.id = s.employee_id;"
                ),
                "question": "What SQL operation combines rows from two tables based on a related column?",
                "answers": ["JOIN", "join"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It links two tables through a shared column.",
                    "It's a four-letter SQL keyword.",
                    "The answer is: JOIN",
                ],
            },
            {
                "id": "join_2",
                "type": "quiz",
                "title": "Inner vs Outer",
                "flavor": "An INNER JOIN only returns rows with matches in BOTH tables. What JOIN returns ALL rows from the left table, even if there's no match on the right?",
                "lesson": (
                    "JOIN types — determine how non-matching rows are handled:\n\n"
                    "  INNER JOIN   only rows with matches in BOTH tables\n"
                    "  LEFT JOIN    all rows from left table; NULL for unmatched right rows\n"
                    "  RIGHT JOIN   all rows from right table; NULL for unmatched left rows\n"
                    "  FULL JOIN    all rows from both tables; NULL where no match\n\n"
                    "LEFT JOIN is the most commonly used outer join — it preserves all records\n"
                    "from the 'main' (left) table, showing NULL for missing related data.\n\n"
                    "Example: SELECT e.name, d.department_name\n"
                    "         FROM employees e\n"
                    "         LEFT JOIN departments d ON e.dept_id = d.id;"
                ),
                "question": "Which JOIN type returns all rows from the left table, with NULLs for non-matching right rows?",
                "answers": ["LEFT JOIN", "left join", "LEFT OUTER JOIN", "left outer join"],
                "xp": 75,
                "difficulty": "medium",
                "hints": [
                    "It's named after which side is preserved completely.",
                    "It's two words: LEFT JOIN.",
                    "The answer is: LEFT JOIN",
                ],
            },
            {
                "id": "join_3",
                "type": "fill_blank",
                "title": "The Join Condition",
                "flavor": "You know which tables to join. You know the linking columns. Which keyword introduces the join condition?",
                "lesson": (
                    "ON — specifies the condition that links two tables in a JOIN.\n\n"
                    "Syntax: JOIN table2 ON table1.column = table2.column\n\n"
                    "The ON condition usually matches a primary key to a foreign key:\n"
                    "  ON orders.customer_id = customers.id\n\n"
                    "Alternative: USING — when both tables have the same column name:\n"
                    "  JOIN departments USING (department_id)\n\n"
                    "Example:\n"
                    "  SELECT o.id, c.name\n"
                    "  FROM orders o\n"
                    "  INNER JOIN customers c ON o.customer_id = c.id;"
                ),
                "question": "Complete this JOIN — connect orders to customers through customer_id:\n\nSELECT * FROM orders JOIN customers ___ orders.customer_id = customers.id;",
                "answers": ["ON", "on"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It introduces the join condition.",
                    "It's two letters.",
                    "The answer is: ON",
                ],
            },
            {
                "id": "join_4",
                "type": "fill_blank",
                "title": "Table Aliases",
                "flavor": "Writing 'employees.employee_id = salaries.employee_id' is verbose. Every table gets an alias. How?",
                "lesson": (
                    "AS — assigns an alias (short name) to a table or column.\n\n"
                    "Table alias syntax:  FROM table_name AS alias  (or just: FROM table_name alias)\n"
                    "Column alias syntax: SELECT column AS 'display_name'\n\n"
                    "Table aliases are essential in JOINs to keep queries readable:\n"
                    "  FROM employees AS e JOIN salaries AS s ON e.id = s.employee_id\n\n"
                    "Example:\n"
                    "  SELECT e.name, d.name AS department\n"
                    "  FROM employees AS e\n"
                    "  LEFT JOIN departments AS d ON e.dept_id = d.id;"
                ),
                "question": "Complete this query to alias the 'employees' table as 'e':\n\nSELECT e.name FROM employees ___ e JOIN departments d ON e.dept_id = d.id;",
                "answers": ["AS", "as"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It creates an alias — a short name for the table.",
                    "It's two letters: AS.",
                    "The answer is: AS",
                ],
            },
            {
                "id": "join_5",
                "type": "fill_blank",
                "title": "Three-Table Join",
                "flavor": "Employees, contracts, payments — three tables, two joins. The data you need lives at their intersection.",
                "lesson": (
                    "Multiple JOINs — chain as many tables as needed:\n\n"
                    "  SELECT e.name, c.title, p.amount\n"
                    "  FROM employees e\n"
                    "  JOIN contracts c ON e.id = c.employee_id\n"
                    "  JOIN payments p ON c.id = p.contract_id;\n\n"
                    "Each JOIN adds another table. Each ON specifies the linking condition.\n"
                    "The alias pattern (e, c, p) keeps column references unambiguous.\n\n"
                    "You can mix JOIN types: INNER for required relationships, LEFT for optional ones."
                ),
                "question": (
                    "Complete this three-table join to link employees, contracts, and payments:\n\n"
                    "SELECT e.name, c.title, p.amount\n"
                    "FROM employees e\n"
                    "JOIN contracts c ON e.id = c.employee_id\n"
                    "___ JOIN payments p ON c.id = p.contract_id;"
                ),
                "answers": ["INNER", "inner", "JOIN", "join", ""],
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "You're adding another JOIN clause.",
                    "INNER JOIN only returns rows with matches in both tables.",
                    "The answer is: INNER (or just omit it — plain JOIN defaults to INNER)",
                ],
            },
            {
                "id": "join_boss",
                "type": "fill_blank",
                "title": "BOSS: The Three-Table Junction",
                "flavor": "The smoking gun is at the intersection of accounts, transactions, and account_owners. Accounts LEFT JOINed to transactions (some accounts have no transactions yet), INNER JOINed to owners. Write it.",
                "lesson": (
                    "Mixing JOIN types — use the right join for each relationship:\n\n"
                    "  SELECT a.account_id, ao.owner_name, t.amount\n"
                    "  FROM accounts a\n"
                    "  LEFT JOIN transactions t ON a.id = t.account_id\n"
                    "  INNER JOIN account_owners ao ON a.id = ao.account_id;\n\n"
                    "LEFT JOIN preserves all accounts (even those with no transactions).\n"
                    "INNER JOIN requires a matching owner for every account row."
                ),
                "question": (
                    "Complete this multi-join query — accounts LEFT JOINed to transactions,\n"
                    "INNER JOINed to account_owners:\n\n"
                    "SELECT a.id, ao.name, t.amount\n"
                    "FROM accounts a\n"
                    "___ JOIN transactions t ON a.id = t.account_id\n"
                    "INNER JOIN account_owners ao ON a.id = ao.account_id;"
                ),
                "answers": ["LEFT", "left"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You want ALL accounts, even those with no transactions.",
                    "When you need all rows from one side regardless of matches: LEFT JOIN.",
                    "The answer is: LEFT",
                ],
            },
        ],
    },

    "subquery_vaults": {
        "id": "subquery_vaults",
        "name": "The Subquery Vaults",
        "subtitle": "CTEs & Subqueries",
        "color": "red",
        "icon": "🏛",
        "commands": ["WITH", "AS", "IN (subquery)", "EXISTS", "CTE"],
        "challenges": [
            {
                "id": "sub_1",
                "type": "quiz",
                "title": "Query Within a Query",
                "flavor": "Your WHERE condition depends on the result of another SELECT. What do you put in the WHERE clause?",
                "lesson": (
                    "Subquery — a SELECT statement nested inside another SQL statement.\n\n"
                    "Syntax: WHERE column IN (SELECT column FROM table WHERE condition)\n\n"
                    "The inner query runs first. Its results are used by the outer query.\n\n"
                    "Example:\n"
                    "  SELECT name FROM employees\n"
                    "  WHERE dept_id IN (\n"
                    "    SELECT id FROM departments WHERE budget > 1000000\n"
                    "  );\n"
                    "  → employees in high-budget departments"
                ),
                "question": "What is a SELECT statement nested inside another SQL statement called?",
                "answers": ["subquery", "sub-query", "nested query", "inner query"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It's a SELECT inside another SELECT.",
                    "Think 'sub' + 'query'.",
                    "The answer is: subquery",
                ],
            },
            {
                "id": "sub_2",
                "type": "fill_blank",
                "title": "The CTE",
                "flavor": "The query is getting complex. You want to name an intermediate result and reference it like a table. That's a CTE.",
                "lesson": (
                    "CTE (Common Table Expression) — a named, temporary result set defined with WITH.\n\n"
                    "Syntax:\n"
                    "  WITH cte_name AS (\n"
                    "    SELECT ...\n"
                    "  )\n"
                    "  SELECT * FROM cte_name;\n\n"
                    "CTEs run before the main query. They can reference each other.\n"
                    "They make complex queries readable and maintainable.\n\n"
                    "Example:\n"
                    "  WITH high_earners AS (\n"
                    "    SELECT id FROM employees WHERE salary > 150000\n"
                    "  )\n"
                    "  SELECT name FROM employees WHERE id IN (SELECT id FROM high_earners);"
                ),
                "question": "Complete this CTE definition:\n\n___ flagged_accounts AS (\n  SELECT id FROM accounts WHERE status = 'flagged'\n)\nSELECT * FROM flagged_accounts;",
                "answers": ["WITH", "with"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "CTEs start with a specific keyword before the name.",
                    "It's a four-letter word: WITH.",
                    "The answer is: WITH",
                ],
            },
            {
                "id": "sub_3",
                "type": "fill_blank",
                "title": "Subquery in WHERE",
                "flavor": "Find all employees whose department ID is in the list of IDs from departments with budget over a million.",
                "lesson": (
                    "IN (subquery) — filters rows where a column value matches any result from a subquery.\n\n"
                    "Syntax: WHERE column IN (SELECT column FROM table WHERE condition)\n\n"
                    "The subquery must return exactly one column.\n"
                    "NOT IN is the inverse — exclude rows that match the subquery results.\n\n"
                    "Example:\n"
                    "  SELECT name FROM employees\n"
                    "  WHERE dept_id IN (\n"
                    "    SELECT id FROM departments WHERE budget > 1000000\n"
                    "  );"
                ),
                "question": "Complete this query — employees in departments with budget over 1 million:\n\nSELECT name FROM employees WHERE dept_id ___ (SELECT id FROM departments WHERE budget > 1000000);",
                "answers": ["IN", "in"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "You're checking if the value matches any result from a subquery.",
                    "The keyword is IN.",
                    "The answer is: IN",
                ],
            },
            {
                "id": "sub_4",
                "type": "fill_blank",
                "title": "Scalar Subquery",
                "flavor": "You want to compare each employee's salary to the company average. The average is a single value computed from a subquery.",
                "lesson": (
                    "Scalar subquery — a subquery that returns exactly one value.\n\n"
                    "Can be used anywhere a single value is expected:\n"
                    "  - In SELECT (as a computed column)\n"
                    "  - In WHERE (for comparison)\n"
                    "  - In HAVING\n\n"
                    "Example:\n"
                    "  SELECT name, salary,\n"
                    "         (SELECT AVG(salary) FROM employees) AS company_avg\n"
                    "  FROM employees\n"
                    "  WHERE salary > (SELECT AVG(salary) FROM employees);"
                ),
                "question": (
                    "Complete this query — employees earning more than the company average:\n\n"
                    "SELECT name, salary FROM employees\n"
                    "WHERE salary > (SELECT ___(salary) FROM employees);"
                ),
                "answers": ["AVG", "avg"],
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "You want the average salary as a comparison point.",
                    "The aggregate function for average is three letters.",
                    "The answer is: AVG",
                ],
            },
            {
                "id": "sub_boss",
                "type": "fill_blank",
                "title": "BOSS: The CTE Chain",
                "flavor": "The extraction requires two CTEs: first find the flagged accounts, then from those, find only the ones with transactions over 10000. Reference both in the final SELECT.",
                "lesson": (
                    "Chained CTEs — multiple CTEs in a single WITH block:\n\n"
                    "  WITH\n"
                    "    flagged AS (\n"
                    "      SELECT id FROM accounts WHERE status = 'flagged'\n"
                    "    ),\n"
                    "    large_transactions AS (\n"
                    "      SELECT account_id FROM transactions WHERE amount > 10000\n"
                    "    )\n"
                    "  SELECT a.*\n"
                    "  FROM accounts a\n"
                    "  WHERE a.id IN (SELECT id FROM flagged)\n"
                    "    AND a.id IN (SELECT account_id FROM large_transactions);\n\n"
                    "Separate multiple CTEs with a comma. No second WITH keyword."
                ),
                "question": (
                    "Complete this chained CTE — two CTEs separated by a comma:\n\n"
                    "WITH\n"
                    "  flagged AS (SELECT id FROM accounts WHERE status = 'flagged'),\n"
                    "  ___ AS (SELECT account_id FROM transactions WHERE amount > 10000)\n"
                    "SELECT a.* FROM accounts a\n"
                    "WHERE a.id IN (SELECT id FROM flagged)\n"
                    "  AND a.id IN (SELECT account_id FROM large_tx);"
                ),
                "answers": ["large_tx", "large_transactions", "big_tx"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You're naming the second CTE — it's referenced as 'large_tx' later.",
                    "The CTE name must match how you reference it in the final query.",
                    "The answer is: large_tx (to match the reference in the WHERE clause)",
                ],
            },
        ],
    },

    "schema_forge": {
        "id": "schema_forge",
        "name": "The Schema Forge",
        "subtitle": "DDL — Data Definition",
        "color": "green",
        "icon": "🔨",
        "commands": ["CREATE TABLE", "ALTER TABLE", "DROP TABLE", "INSERT INTO", "data types", "constraints"],
        "challenges": [
            {
                "id": "schema_1",
                "type": "quiz",
                "title": "Build the Structure",
                "flavor": "You need a staging table. First, what SQL command creates a new table?",
                "lesson": (
                    "CREATE TABLE — defines a new table with its columns and data types.\n\n"
                    "Syntax:\n"
                    "  CREATE TABLE table_name (\n"
                    "    column1 datatype [constraints],\n"
                    "    column2 datatype [constraints],\n"
                    "    ...\n"
                    "  );\n\n"
                    "Example:\n"
                    "  CREATE TABLE staging_results (\n"
                    "    id SERIAL PRIMARY KEY,\n"
                    "    account_id INTEGER NOT NULL,\n"
                    "    extracted_at TIMESTAMP DEFAULT NOW()\n"
                    "  );"
                ),
                "question": "What SQL command creates a new table in the database?",
                "answers": ["CREATE TABLE", "create table"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It's two words: one that means 'make' and one that means 'table'.",
                    "The answer is: CREATE TABLE",
                ],
            },
            {
                "id": "schema_2",
                "type": "quiz",
                "title": "Data Types",
                "flavor": "The column holds whole numbers only. No decimals. No text. Which PostgreSQL data type?",
                "lesson": (
                    "PostgreSQL data types — define what kind of data a column can hold:\n\n"
                    "Numeric:\n"
                    "  INTEGER   whole numbers (-2147483648 to 2147483647)\n"
                    "  BIGINT    large integers\n"
                    "  DECIMAL   exact decimal numbers (use for money)\n"
                    "  REAL      floating-point (approximate)\n\n"
                    "Text:\n"
                    "  TEXT      variable-length string (preferred in PostgreSQL)\n"
                    "  VARCHAR(n) variable-length string up to n characters\n\n"
                    "Other:\n"
                    "  BOOLEAN   TRUE / FALSE\n"
                    "  TIMESTAMP date and time\n"
                    "  SERIAL    auto-incrementing integer (for primary keys)"
                ),
                "question": "Which PostgreSQL data type stores whole numbers (integers)?",
                "answers": ["INTEGER", "integer", "INT", "int", "BIGINT", "bigint"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: whole numbers, no decimals.",
                    "It's a common SQL type, seven letters.",
                    "The answer is: INTEGER",
                ],
            },
            {
                "id": "schema_3",
                "type": "fill_blank",
                "title": "Enforce Non-Null",
                "flavor": "The account_id column must always have a value. No nulls allowed. What constraint enforces this?",
                "lesson": (
                    "NOT NULL — a column constraint that prevents null values from being inserted.\n\n"
                    "Syntax: column_name datatype NOT NULL\n\n"
                    "Other common constraints:\n"
                    "  PRIMARY KEY   unique identifier for each row, implicitly NOT NULL\n"
                    "  UNIQUE        all values in the column must be distinct\n"
                    "  DEFAULT value assigns a default value when none is provided\n"
                    "  CHECK (cond)  validates that values satisfy a condition\n\n"
                    "Example:\n"
                    "  CREATE TABLE orders (\n"
                    "    id SERIAL PRIMARY KEY,\n"
                    "    customer_id INTEGER NOT NULL,\n"
                    "    status TEXT DEFAULT 'pending'\n"
                    "  );"
                ),
                "question": "Complete this column definition to disallow null values:\n\naccount_id INTEGER ___ NULL;",
                "answers": ["NOT", "not"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "The constraint is two words: NOT NULL.",
                    "The answer is: NOT",
                ],
            },
            {
                "id": "schema_4",
                "type": "fill_blank",
                "title": "Insert the Record",
                "flavor": "The staging table exists. Now you need to put data into it. Which command inserts a row?",
                "lesson": (
                    "INSERT INTO — adds new rows to a table.\n\n"
                    "Syntax:\n"
                    "  INSERT INTO table_name (column1, column2, ...)\n"
                    "  VALUES (value1, value2, ...);\n\n"
                    "You can insert multiple rows in one statement:\n"
                    "  INSERT INTO table (col1, col2)\n"
                    "  VALUES (val1, val2), (val3, val4);\n\n"
                    "Or insert from a SELECT:\n"
                    "  INSERT INTO staging SELECT * FROM source WHERE condition;"
                ),
                "question": "Complete this command to add a row to the 'audit_log' table:\n\n___ INTO audit_log (event, created_at) VALUES ('access', NOW());",
                "answers": ["INSERT", "insert"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It adds data to a table.",
                    "The full command is INSERT INTO.",
                    "The answer is: INSERT",
                ],
            },
            {
                "id": "schema_boss",
                "type": "fill_blank",
                "title": "BOSS: Build the Staging Table",
                "flavor": "The extraction needs a permanent staging structure: id (auto-increment primary key), source_account_id (integer, not null), amount (decimal, not null), extracted_at (timestamp, default now). Create it.",
                "lesson": (
                    "Complete CREATE TABLE with multiple column types and constraints:\n\n"
                    "  CREATE TABLE extraction_staging (\n"
                    "    id SERIAL PRIMARY KEY,\n"
                    "    source_account_id INTEGER NOT NULL,\n"
                    "    amount DECIMAL NOT NULL,\n"
                    "    extracted_at TIMESTAMP DEFAULT NOW()\n"
                    "  );\n\n"
                    "SERIAL automatically generates sequential integers (1, 2, 3...).\n"
                    "PRIMARY KEY = UNIQUE + NOT NULL, used to uniquely identify each row.\n"
                    "DEFAULT NOW() sets the timestamp automatically on insert."
                ),
                "question": (
                    "Complete the id column definition (auto-increment primary key):\n\n"
                    "CREATE TABLE extraction_staging (\n"
                    "  id ___ PRIMARY KEY,\n"
                    "  source_account_id INTEGER NOT NULL,\n"
                    "  amount DECIMAL NOT NULL,\n"
                    "  extracted_at TIMESTAMP DEFAULT NOW()\n"
                    ");"
                ),
                "answers": ["SERIAL", "serial"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You need an auto-incrementing integer.",
                    "PostgreSQL's auto-increment type is SERIAL.",
                    "The answer is: SERIAL",
                ],
            },
        ],
    },

    "index_sanctum": {
        "id": "index_sanctum",
        "name": "The Index Sanctum",
        "subtitle": "Performance & Query Planning",
        "color": "cyan",
        "icon": "⚡",
        "commands": ["CREATE INDEX", "EXPLAIN", "EXPLAIN ANALYZE", "DROP INDEX", "VACUUM"],
        "challenges": [
            {
                "id": "idx_1",
                "type": "quiz",
                "title": "The Performance Tool",
                "flavor": "The query is slow. Before you can fix it, you need to see what the database is actually doing. Which command shows the query execution plan?",
                "lesson": (
                    "EXPLAIN — shows the query execution plan without running the query.\n"
                    "EXPLAIN ANALYZE — runs the query AND shows actual execution statistics.\n\n"
                    "Syntax:\n"
                    "  EXPLAIN SELECT * FROM large_table WHERE column = value;\n"
                    "  EXPLAIN ANALYZE SELECT * FROM large_table WHERE column = value;\n\n"
                    "Key things to look for in the plan:\n"
                    "  Seq Scan      sequential scan — reads every row (slow on large tables)\n"
                    "  Index Scan    uses an index (fast)\n"
                    "  cost=X..Y     estimated cost range\n"
                    "  rows=N        estimated row count\n\n"
                    "If you see 'Seq Scan' on a large table with a WHERE clause,\n"
                    "you probably need an index."
                ),
                "question": "Which SQL command shows how the database will execute a query (the execution plan)?",
                "answers": ["EXPLAIN", "explain", "EXPLAIN ANALYZE", "explain analyze"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It shows the query plan without running the query.",
                    "The answer is: EXPLAIN",
                ],
            },
            {
                "id": "idx_2",
                "type": "fill_blank",
                "title": "Build the Index",
                "flavor": "EXPLAIN shows a sequential scan on the accounts table filtering by status. 50 million rows. You need an index on that column.",
                "lesson": (
                    "CREATE INDEX — builds an index on one or more columns to speed up queries.\n\n"
                    "Syntax:\n"
                    "  CREATE INDEX index_name ON table_name (column_name);\n\n"
                    "Multi-column index:\n"
                    "  CREATE INDEX idx_name ON table (col1, col2);\n\n"
                    "Partial index (only index rows matching a condition):\n"
                    "  CREATE INDEX idx_active ON employees (dept_id) WHERE status = 'active';\n\n"
                    "After creating an index, run EXPLAIN again to verify it's being used.\n\n"
                    "Example: CREATE INDEX idx_account_status ON accounts (status);"
                ),
                "question": "Complete this command to add an index on the 'status' column of 'accounts':\n\nCREATE ___ idx_accounts_status ON accounts (status);",
                "answers": ["INDEX", "index"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "The command starts with CREATE.",
                    "The full command is CREATE INDEX.",
                    "The answer is: INDEX",
                ],
            },
            {
                "id": "idx_3",
                "type": "quiz",
                "title": "Sequential vs Index Scan",
                "flavor": "EXPLAIN output shows 'Seq Scan' on a 50M-row table. What does this mean for performance?",
                "lesson": (
                    "Seq Scan vs Index Scan — understanding EXPLAIN output:\n\n"
                    "Seq Scan (Sequential Scan):\n"
                    "  - Reads every row in the table\n"
                    "  - Appropriate for small tables or when fetching most rows\n"
                    "  - Slow for filtering a tiny fraction of a large table\n\n"
                    "Index Scan:\n"
                    "  - Uses the index to jump directly to matching rows\n"
                    "  - Fast when filtering on indexed columns\n"
                    "  - The goal for large-table WHERE clause queries\n\n"
                    "Bitmap Index Scan: a hybrid for moderate result sets.\n\n"
                    "Rule of thumb: Seq Scan on large table + WHERE clause = add an index."
                ),
                "question": "In an EXPLAIN output, what does 'Seq Scan' indicate about query performance?",
                "answers": [
                    "reading every row",
                    "full table scan",
                    "sequential scan",
                    "no index used",
                    "it reads all rows",
                    "scanning all rows",
                ],
                "xp": 75,
                "difficulty": "medium",
                "hints": [
                    "Seq = Sequential. It reads rows in sequence.",
                    "It means the database is not using an index.",
                    "The answer is: reading every row (full table scan, no index)",
                ],
            },
            {
                "id": "idx_boss",
                "type": "fill_blank",
                "title": "BOSS: Diagnose and Fix",
                "flavor": "EXPLAIN ANALYZE shows a sequential scan on transactions (100M rows) filtering by account_id. The query takes 45 seconds. Add the index. Verify with EXPLAIN ANALYZE that it switches to an Index Scan.",
                "lesson": (
                    "The full optimization workflow:\n\n"
                    "  1. Run EXPLAIN ANALYZE to see the current plan\n"
                    "  2. Identify the Seq Scan on the relevant column\n"
                    "  3. Create an index: CREATE INDEX idx ON table (column);\n"
                    "  4. Run EXPLAIN ANALYZE again to verify Index Scan appears\n\n"
                    "For this table and query:\n"
                    "  CREATE INDEX idx_transactions_account ON transactions (account_id);\n\n"
                    "After the index is created, queries filtering on account_id\n"
                    "will use it automatically — no query changes needed."
                ),
                "question": (
                    "Complete this command to index the transactions table on account_id:\n\n"
                    "CREATE INDEX idx_transactions_account ON ___ (account_id);"
                ),
                "answers": ["transactions", "TRANSACTIONS"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "The table you're indexing is the one with the slow query.",
                    "You're creating an index on the transactions table.",
                    "The answer is: transactions",
                ],
            },
        ],
    },

    "transaction_core": {
        "id": "transaction_core",
        "name": "The Transaction Core",
        "subtitle": "ACID & Transactions",
        "color": "red",
        "icon": "💎",
        "commands": ["BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT", "isolation levels"],
        "challenges": [
            {
                "id": "tx_1",
                "type": "quiz",
                "title": "Start the Transaction",
                "flavor": "You're about to make several related writes. They all succeed or none of them do. How do you open a transaction boundary?",
                "lesson": (
                    "BEGIN — starts a transaction block.\n\n"
                    "In PostgreSQL, every statement is automatically wrapped in a transaction.\n"
                    "BEGIN explicitly starts a multi-statement transaction:\n\n"
                    "  BEGIN;\n"
                    "  UPDATE accounts SET balance = balance - 500 WHERE id = 1;\n"
                    "  UPDATE accounts SET balance = balance + 500 WHERE id = 2;\n"
                    "  COMMIT;\n\n"
                    "If anything fails between BEGIN and COMMIT, run ROLLBACK to undo everything.\n\n"
                    "Also valid: START TRANSACTION (equivalent to BEGIN)"
                ),
                "question": "What SQL command starts an explicit transaction block?",
                "answers": ["BEGIN", "begin", "START TRANSACTION", "start transaction"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It marks the beginning of a transaction.",
                    "It's five letters: BEGIN.",
                    "The answer is: BEGIN",
                ],
            },
            {
                "id": "tx_2",
                "type": "quiz",
                "title": "Finalize the Write",
                "flavor": "All the statements succeeded. The data is correct. Now make the changes permanent.",
                "lesson": (
                    "COMMIT — saves all changes made during the current transaction.\n\n"
                    "After COMMIT:\n"
                    "  - All changes are permanent (durable)\n"
                    "  - Other transactions can see the changes\n"
                    "  - The transaction is complete\n\n"
                    "Syntax:\n"
                    "  BEGIN;\n"
                    "  -- your statements here --\n"
                    "  COMMIT;\n\n"
                    "If you close a connection without COMMIT, PostgreSQL automatically rolls back."
                ),
                "question": "What SQL command makes a transaction's changes permanent?",
                "answers": ["COMMIT", "commit"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It finalizes and saves the transaction.",
                    "It's six letters.",
                    "The answer is: COMMIT",
                ],
            },
            {
                "id": "tx_3",
                "type": "quiz",
                "title": "Abort the Operation",
                "flavor": "Something went wrong. The second UPDATE failed. You need to undo everything and leave the database exactly as it was before BEGIN.",
                "lesson": (
                    "ROLLBACK — undoes all changes made during the current transaction.\n\n"
                    "ROLLBACK restores the database to the state it was in before BEGIN.\n"
                    "No partial changes. No corrupted state. Clean slate.\n\n"
                    "Syntax:\n"
                    "  BEGIN;\n"
                    "  UPDATE accounts SET balance = balance - 500 WHERE id = 1;\n"
                    "  -- error occurs --\n"
                    "  ROLLBACK;   -- first UPDATE is also undone\n\n"
                    "ROLLBACK is automatic if a connection drops or an exception aborts the transaction."
                ),
                "question": "What SQL command undoes all changes in the current transaction?",
                "answers": ["ROLLBACK", "rollback"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: rolling back to the previous state.",
                    "It's eight letters.",
                    "The answer is: ROLLBACK",
                ],
            },
            {
                "id": "tx_4",
                "type": "quiz",
                "title": "The ACID Promise",
                "flavor": "ACID. Four properties that define what a transaction guarantees. What does the A stand for?",
                "lesson": (
                    "ACID — the four properties that define reliable transactions:\n\n"
                    "  A — Atomicity   All operations succeed, or none do. No partial states.\n"
                    "  C — Consistency Database moves from one valid state to another.\n"
                    "  I — Isolation   Concurrent transactions don't interfere with each other.\n"
                    "  D — Durability  Committed data survives failures (power loss, crashes).\n\n"
                    "PostgreSQL is fully ACID-compliant. This is what separates it from\n"
                    "spreadsheets, CSV files, and most NoSQL databases."
                ),
                "question": "In ACID, what property guarantees that a transaction is all-or-nothing?",
                "answers": ["atomicity", "Atomicity", "atomic", "Atomic"],
                "xp": 75,
                "difficulty": "medium",
                "hints": [
                    "It's the first letter of ACID.",
                    "It means the transaction is indivisible — all or nothing.",
                    "The answer is: Atomicity",
                ],
            },
            {
                "id": "tx_5",
                "type": "quiz",
                "title": "Isolation Levels",
                "flavor": "Two transactions are running concurrently. You need to ensure Transaction B cannot see Transaction A's uncommitted changes. What isolation level prevents this?",
                "lesson": (
                    "Isolation levels — control how concurrent transactions interact:\n\n"
                    "  READ UNCOMMITTED  can see uncommitted changes (dirty reads) — rarely used\n"
                    "  READ COMMITTED    can only see committed data (PostgreSQL default)\n"
                    "  REPEATABLE READ   same row read twice gives same result within transaction\n"
                    "  SERIALIZABLE      transactions appear to execute one at a time (strictest)\n\n"
                    "Higher isolation = fewer concurrency anomalies = more locking overhead.\n\n"
                    "Set with: SET TRANSACTION ISOLATION LEVEL READ COMMITTED;\n\n"
                    "PostgreSQL default is READ COMMITTED. Use SERIALIZABLE for financial operations."
                ),
                "question": "What is PostgreSQL's default transaction isolation level?",
                "answers": ["READ COMMITTED", "read committed", "READ_COMMITTED"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "It's the most common isolation level.",
                    "It prevents dirty reads — you only see committed data.",
                    "The answer is: READ COMMITTED",
                ],
            },
            {
                "id": "tx_boss",
                "type": "fill_blank",
                "title": "FINAL BOSS: The Atomic Extraction",
                "flavor": "The complete extraction: move funds between accounts atomically. BEGIN. UPDATE both accounts. If any error occurs, the entire operation rolls back. End with the command that makes it permanent.",
                "lesson": (
                    "The complete transaction pattern:\n\n"
                    "  BEGIN;\n"
                    "  UPDATE source_accounts SET balance = balance - 10000\n"
                    "    WHERE id = 42 AND balance >= 10000;\n"
                    "  INSERT INTO extraction_staging (source_id, amount, extracted_at)\n"
                    "    VALUES (42, 10000, NOW());\n"
                    "  COMMIT;\n\n"
                    "This is atomic: if the INSERT fails (constraint violation, lock timeout),\n"
                    "the UPDATE is also rolled back. The database either processes both or neither."
                ),
                "question": (
                    "Complete this transaction — it succeeds, make the changes permanent:\n\n"
                    "BEGIN;\n"
                    "UPDATE accounts SET balance = balance - 10000 WHERE id = 42;\n"
                    "INSERT INTO extraction_log (account_id, amount) VALUES (42, 10000);\n"
                    "___;  -- make it permanent"
                ),
                "answers": ["COMMIT", "commit"],
                "xp": 300,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "The transaction succeeded. You need to finalize and save the changes.",
                    "The command that makes a transaction permanent.",
                    "The answer is: COMMIT",
                ],
            },
        ],
    },
}

ZONE_ORDER = [
    "surface_tables",
    "filter_chambers",
    "aggregation_engine",
    "junction_archive",
    "subquery_vaults",
    "schema_forge",
    "index_sanctum",
    "transaction_core",
]
