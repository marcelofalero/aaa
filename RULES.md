# Alternity Roll Logic

## Case: Has Broad Skill
- **Roll Broad Skill**:
  - Score: Full Ability Score
  - Default: +1 Step (+d4)
- **Roll Specialty Skill**:
  - **With Ranks**:
    - Score: Ability + Specialty Ranks
    - Default: None (+0)
  - **No Ranks**:
    - **Trained Only**: Not allowed (Score 0, Default None)
    - **Non-Trained Only**:
      - Score: Ability Score
      - Default: +1 Step (+d4)

## Case: No Broad Skill
- **Roll Broad Skill**:
  - Score: Ability Score / 2 (rounded down)
  - Default: +1 Step (+d4)
  - Output: Mark as "Untrained"
- **Roll Specialty Skill**:
  - **No Ranks**:
    - **Trained Only**: Not allowed (Score 0, Default None)
    - **Non-Trained Only**:
      - Score: Ability Score / 2 (rounded down)
      - Default: +1 Step (+d4)
      - Mark as "Untrained"
