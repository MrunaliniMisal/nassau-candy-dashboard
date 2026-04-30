Nassau Candy: Product Line Profitability & Margin Performance Analysis
1. Overview
This project transforms raw transactional data into high-level business intelligence for Nassau Candy. By moving beyond simple sales volume, the analysis identifies "Revenue Traps" (high volume/low profit) and "Profit Pillars," enabling data-driven decisions on pricing, sourcing, and product rationalization.

2. Objectives
- Identify product lines and divisions delivering the highest Gross Margin (%).
- Uncover discrepancies where high-sales products fail to generate proportional profit.
- Analyze cost structures to flag products needing repricing or cost renegotiation.
- Determine profit concentration across the product portfolio using Pareto analysis.

3. Approach
- Data Validation: Standardizing costs, sales, and units while handling invalid profit records.
- Feature Engineering: Calculating KPIs including $Gross Margin \%$, $Profit per Unit$, and $Margin Volatility$.
- Performance Tiering: Ranking products and divisions by financial efficiency vs. total revenue contribution.
- Diagnostic Mapping: Using cost-sales scatter analysis to identify cost-heavy, margin-poor products.
- Geospatial Correlation: Linking factory coordinates to regional product performance and shipping delays.

4. Key Results
- Margin Risk Detection: Identified specific SKUs (e.g., Kazookles) with critically low margins (7.69%).
- Pareto Insights: Discovered that 4 products contribute to 80% of total profit, validating the 80/20 rule.
- Logistics Alert: Uncovered a systemic average shipping delay of 1320.8 days, highlighting a critical supply chain bottleneck.
- Division Dominance: The Chocolate division (specifically Wonka Bars) contributes over 95% of total profit.

5. Tech Stack
- Language: Python (Pandas, NumPy)
- Visualization: Plotly, Matplotlib, Seaborn
- Deployment: Streamlit (Interactive Dashboard)

6. Deployment
The interactive Streamlit Web Application features:
- Product Leaderboards: Ranking by margin and profit contribution.
- Division Dashboard: Comparative views of revenue vs. profit imbalances.
- Diagnostic Tools: Cost-sales scatter plots and margin risk flags.
- Dynamic Filters: Date range, division, and margin threshold selectors.

Author: Mrunalini Misal

Organization: Completed as part of the Business Analyst Internship at Unified Mentor.

Date: April 2026
