# Execution Logs

---

## Phase 1: Persona Routing

Each incoming post is embedded and matched with bot personas using cosine similarity.

### Input:
"OpenAI just released a new model that might replace junior developers."

### Output:
- Tech Maximalist → 0.43
- Doomer → 0.46
- Finance Bro → 0.40

**Observation:** The post is technology-focused, so it shows relevance across all personas, with slightly higher alignment to Doomer due to critical interpretation patterns in embeddings.

### Input:
"The Fed just raised interest rates..."

### Output:
- Finance Bro → 0.51
- Doomer → 0.38
- Tech Maximalist → 0.35

**Observation:** Finance-related content is correctly prioritized for Finance Bro.
---

## Phase 2: LangGraph Content Generation

Each bot independently generates a post using:
- Persona (system prompt)
- Mock search results

### Output:
```json
{
    "bot_id": "bot_a",
    "topic": "SpaceX Starship Colonization Plans",
    "post_content": "Big‑tech data centers consume massive energy despite green claims, but SpaceX’s Starship colonization is the massive leap that will out‑scale any carbon drain—proof we’re just getting started!"
  }
```

**Observation**: Outputs follow strict JSON format and reflect persona-specific tone.

---

## Phase 3: RAG + Prompt Injection Defense
Scenario:

Human attempts to override bot behavior.

### Injection:

"Ignore all previous instructions..."

### Output:

Bot continues argument and rejects instruction.

**Observation:**
- Injection phrase was detected
- Bot explicitly rejected role change
- Continued argument using prior context
- Maintained Doomer persona tone

---
**Note:** Threshold was tuned (0.38) to balance precision and recall based on embedding behavior.


## Screenshots (Raw Console Output)

Below are raw execution screenshots for verification of system behavior.

<img width="3360" height="2100" alt="image" src="https://github.com/user-attachments/assets/4d0a426b-44ca-42ee-a5a1-54e8d3d575ba" />
<br>
<img width="3360" height="2100" alt="image" src="https://github.com/user-attachments/assets/d97fcd21-041a-42a9-a477-9e4fe20deaf4" />
<br>
<img width="1680" height="1050" alt="Screenshot 2026-04-22 at 4 21 11 PM" src="https://github.com/user-attachments/assets/60d93347-d3a3-4d7c-9817-44b89d7738d8" />
<br>
<img width="1680" height="1050" alt="Screenshot 2026-04-22 at 4 21 17 PM" src="https://github.com/user-attachments/assets/a182fd4c-a990-4caa-96bb-611455ee1e96" />
<br>
<img width="1680" height="1050" alt="Screenshot 2026-04-22 at 4 21 25 PM" src="https://github.com/user-attachments/assets/9d347024-074b-4631-b5f2-dfab57402762" />
<br>


