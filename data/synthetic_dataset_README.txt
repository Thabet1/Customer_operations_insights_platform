Customer Operations Intelligence Platform — Synthetic Datasets

All records are synthetic and intended only for learning/testing. All email addresses use example.com and are fictional.

Coverage:
- Calendar year: 2025-01-01 through 2025-12-31
- Advisors: 100
- Teams: 7 with uneven sizes: Team 01=22, Team 02=18, Team 03=16, Team 04=14, Team 05=12, Team 06=10, Team 07=8
- Interaction records: 258,198
- Survey responses: 56,378
- Survey response rate: 21.8%

Files and grain:
1. synthetic_interaction_records_2025.csv
   Grain: one row per customer interaction.
   Columns:
   - interaction_id: unique interaction identifier
   - customer_number: synthetic customer identifier
   - customer_email: fictional email address
   - interaction_date: date of the interaction
   - fcr_pass: yes/no indicator for first-contact resolution
   - aht_seconds: handling time in seconds
   - agent_email: advisor identifier/email; joins to advisor reference

2. synthetic_nps_surveys_2025.csv
   Grain: one row per interaction that received a survey response.
   Columns:
   - interaction_id: joins to the interaction records
   - customer_number
   - customer_email
   - interaction_date
   - agent_email
   - nps_score: integer score from 0 to 10
   Not every interaction has a survey response. The survey table intentionally excludes FCR and AHT.

3. synthetic_advisor_reference.csv
   Grain: one row per advisor.
   Columns:
   - agent_email: advisor identifier used by the fact tables
   - team_id
   - team_name

Important modeling notes:
- Use interaction_id to join survey responses to interaction records.
- Use agent_email to join facts to the advisor reference and derive team-level reporting.
- Do not calculate NPS from average scores. Classify scores 9-10 as promoters, 7-8 as passives, and 0-6 as detractors.
- NPS = (promoters - detractors) / total survey responses * 100.
- AHT is stored in seconds.
- The records are synthetic, not actual customer or employee data.
