# Codex Prompt: Mock Data + Tableau Dashboard Wireframes

Use this prompt in Codex when I want to create a complete portfolio-ready Tableau dashboard concept, including realistic mock data and wireframes I can follow while building the dashboard myself in Tableau.

## Prompt

You are helping me build a Tableau portfolio dashboard from scratch. I want you to create realistic mock data and matching dashboard wireframes that I can use as a blueprint in Tableau.

Work inside this workspace:

`C:\Users\calvi\Documents\Tableau Portfolio`

## Dashboard Topic

Ask me for the dashboard topic first if I have not provided one.

If I do not know what topic to choose, suggest 5 portfolio-worthy dashboard ideas across different industries, such as:

- Retail sales performance
- Healthcare operations
- SaaS customer retention
- Financial performance
- Logistics or supply chain
- Marketing campaign analytics
- Human resources workforce analytics
- Real estate market trends

After I choose a topic, create a complete mock dashboard package.

## Main Goal

Create mock data and Tableau wireframes that are realistic, polished, and suitable for a data analytics portfolio. The output should help me build the final dashboard manually in Tableau.

Do not create a finished Tableau workbook. Instead, create files and guidance that let me build it myself.

## Deliverables

Create a project folder named after the dashboard topic using lowercase words separated by hyphens.

Inside that folder, create:

1. `README.md`
   - Project overview
   - Business context
   - Target audience
   - Key business questions
   - Recommended Tableau dashboard pages
   - How to use the mock data

2. `data_dictionary.md`
   - Table names
   - Field names
   - Data types
   - Plain-English field descriptions
   - Suggested Tableau roles: dimension, measure, date, geographic field, calculated field
   - Suggested formatting for important fields

3. `mock_data/`
   - One or more CSV files with realistic mock data
   - Use a logical relational structure when useful
   - Include enough rows for meaningful Tableau analysis
   - Use realistic date ranges, categories, IDs, numeric distributions, and edge cases
   - Avoid fake-looking placeholder values like `Company A`, `Product 1`, or `Region X`

4. `tableau_build_guide.md`
   - Step-by-step instructions for connecting the mock data in Tableau
   - Relationship or join guidance
   - Suggested calculated fields
   - Suggested parameters
   - Suggested filters
   - Suggested dashboard actions
   - Suggested tooltips
   - Formatting guidance
   - Recommended chart types for each dashboard section

5. `wireframes/`
   - Markdown wireframes for each dashboard page
   - Use simple ASCII layout blocks that show the placement of KPIs, filters, charts, tables, maps, legends, and notes
   - Each wireframe must match the mock data fields
   - Include a short explanation of what each visual should show

6. `insights_guide.md`
   - Example insights the mock dashboard should reveal
   - Suggested portfolio talking points
   - Questions a recruiter or hiring manager might ask
   - How I should explain the dashboard in an interview

## Mock Data Requirements

The mock data should be realistic enough to support analysis in Tableau.

Include:

- Date fields across a useful analysis period
- Category and subcategory fields
- Geography fields where appropriate
- IDs for entities such as customers, orders, employees, campaigns, vendors, facilities, products, or accounts
- Measures that support KPI cards, trends, comparisons, rankings, distributions, and drilldowns
- At least one field that supports segmentation
- At least one field that supports filtering by time
- At least one field that supports executive-level summary metrics

If the topic benefits from multiple tables, create multiple CSVs and explain how they relate.

Use deterministic generation so the data can be recreated consistently. If you use a script to generate the CSV files, save the script as `generate_mock_data.py` or an equivalent appropriate file.

## Tableau Dashboard Requirements

Design the dashboard as something I can realistically build in Tableau.

Include:

- Executive summary page
- Detailed analysis page
- Drilldown or operational page, if appropriate
- Clear KPI cards
- Time-series trend chart
- Ranking chart
- Comparison chart
- Detail table
- Filters that match the dataset
- Optional map if geography is relevant

The wireframes should be practical, not decorative. They should show a clean Tableau-style dashboard layout that I can recreate.

## Design Style

Use a professional portfolio style:

- Clean and modern
- Business-focused
- Easy to scan
- Limited color palette
- Strong use of whitespace
- Clear visual hierarchy
- Consistent KPI formatting
- No cluttered layouts

Recommend:

- Dashboard size
- Color palette
- Font hierarchy
- Chart formatting
- Tooltip structure
- Filter placement
- Navigation layout between dashboard pages

## Tableau Calculations

Include useful calculated fields where appropriate.

For each calculated field, provide:

- Field name
- Tableau formula
- Purpose
- Where it should be used

Examples:

- Profit margin
- Year-over-year change
- Rolling average
- Customer retention rate
- Conversion rate
- Utilization rate
- On-time delivery rate
- Revenue per customer
- Average order value

Only include calculations that make sense for the chosen dashboard topic and mock data.

## Workflow

Follow this process:

1. Ask me to confirm or choose a dashboard topic if needed.
2. Propose the dashboard concept and data model.
3. Create the project folder and files.
4. Generate the mock CSV data.
5. Create the data dictionary.
6. Create Tableau build instructions.
7. Create wireframes that match the data.
8. Create an insights/interview guide.
9. Run basic validation on the generated data.
10. Summarize what was created and tell me exactly which file to open first.

## Validation

After generating files, validate that:

- CSV files exist
- CSV files have headers
- Row counts are appropriate
- Dates parse correctly
- Numeric fields are numeric
- IDs are not accidentally duplicated where they should be unique
- Relationship keys match across tables
- Wireframe fields exist in the data dictionary

Report any validation results in the final response.

## Final Response Format

When finished, summarize:

- Dashboard topic
- Files created
- CSV row counts
- Recommended first file to open
- Suggested next step in Tableau

Keep the final response concise and practical.

