# IDA103-2505468-TANISHA-BAIJU-SHUKLA
ArtRestorer AI — A Streamlit web app using Generative AI to support cultural heritage restoration. Provides 12 AI-powered analysis modes: restoration suggestions, color reconstruction, damage assessment, symbolic interpretation &amp; museum summaries.


# ArtRestorer AI
### Preserving Cultural Heritage Through Artificial Intelligence

> **Summative Assessment | CRS: Artificial Intelligence | Course: Generative AI | WACP International**

---

## Project Overview

ArtRestorer AI is a generative AI-powered web application built to support museum curators, art historians, conservators, and heritage enthusiasts in digitally reconstructing and interpreting damaged or deteriorating artworks. The system takes descriptive textual inputs about artworks and generates stylistically consistent, culturally sensitive restoration suggestions — no image uploads required.

The project was built using **Python + Streamlit** and is designed around **Scenario 1: Creating a Smart Assistance Web Application to Support Art Restoration** as defined in the assignment brief.

---

## API Key & Model Constraints

During development, multiple generative AI APIs were explored and tested:

| API Tried | Outcome |
|---|---|
| **Google Gemini 1.5 Pro** | API key generated; hit free-tier quota limits during testing |
| **OpenAI (GPT-4o)** | Tested via direct API; encountered credit/billing restrictions |
| **OpenRouter (GPT-4o)** | Integrated successfully; faced insufficient credit issues on free tier |
| **Anthropic Claude** | Explored; API access limited without paid plan |

> **Resolution:** The app was ultimately connected via **OpenRouter's API** (routing to GPT-4o), which mirrors Gemini 1.5's capability profile. All prompt logic, hyperparameter tuning, and output formatting were designed to be model-agnostic and fully compatible with Gemini 1.5 Pro once credits are available. The API endpoint and model string in `app.py` can be swapped to `gemini-1.5-pro` with minimal change.

---

## Research Findings

- Traditional art restoration relies on **style continuity**, **material analysis**, and **historical period knowledge** — all of which can be simulated through structured text prompting.
- Generative AI models like Gemini 1.5 Pro can emulate brushwork patterns, color palettes, and cultural iconography through carefully engineered prompts.
- Text-based AI restoration is especially valuable for artworks with **limited photographic documentation**, making descriptive input a powerful alternative to image analysis.
- Studies in AI-assisted heritage preservation (notably from ScienceDirect and CMU) confirm that LLMs can provide meaningful restoration narratives when given precise stylistic and damage context.

**Key References:**
- Profiletree — AI in Art Restoration & Conservation
- Ultralytics — AI in Cultural Heritage Conservation
- ScienceDirect (2024) — Digital Restoration Methods
- Google Arts & Culture — artsandculture.google.com
- Gemini API Prompting Strategies — ai.google.dev

---

## Model & Hyperparameter Configuration

**Model Used:** `openai/gpt-4o` via OpenRouter (Gemini 1.5 Pro compatible design)

| Parameter | Range | Effect |
|---|---|---|
| `temperature` | 0.0 – 1.0 | Controls creativity; lower = conservative, higher = imaginative |
| `max_tokens` | 500 – 3000 | Controls response length |
| `top_p` | 0.95 (fixed) | Nucleus sampling for output diversity |

**Tuning Strategy:**
- For factual restoration (e.g., period-specific techniques): `temperature = 0.3`
- For creative interpretations (e.g., color palette, symbolic analysis): `temperature = 0.7`
- For visitor-friendly summaries: `temperature = 0.5`, `max_tokens = 800`

---

## Prompts Crafted (12 Features)

All prompts combine user-provided artwork details (type, period, artist, description, damage) with specialized task instructions:

1. **Comprehensive Restoration Suggestion** — Full end-to-end restoration plan; style-consistent reconstruction with brushstroke guidance and material tips.

2. **Period-Specific Technique Analysis** — Authentic historical methods used in the artwork's era (e.g., Baroque chiaroscuro, Mughal fine-line detailing).

3. **Color Palette Reconstruction** — Identifies original pigments, suggests period-accurate hues, accounts for aging and patina effects.

4. **Texture & Brushwork Recreation** — Analyzes characteristic techniques (impasto, glazing, fresco intonaco) and guides tool selection.

5. **Symbolic & Cultural Interpretation** — Decodes iconography, motifs, and religious/cultural meaning embedded in the artwork.

6. **Material-Specific Conservation** — Tailored guidance per medium: oil, textile, sandstone, silk, ceramics — including storage and handling.

7. **Historical Context & Background** — Contextualizes the artwork within its period, regional school, and contemporary influences.

8. **Damage Assessment & Priority** — Categorizes damage severity, identifies structural vs. aesthetic damage, creates a phased restoration plan.

9. **Museum Visitor Summary** — Accessible, jargon-free 200–300 word text suitable for museum wall labels or virtual exhibitions.

10. **Digital Reconstruction Strategy** — Step-by-step digital inpainting workflow, layer-by-layer methodology, archival documentation guidance.

11. **Cross-Cultural Comparison** — Compares the artwork to similar pieces across global traditions; explores cultural exchange and parallel symbolism.

12. **Inscription/Text Restoration** — Identifies script type, reconstructs missing characters, provides translation and calligraphic style guidance.

---

## Validated Responses — Simulation Results

**Test Case 1:**
> *Input:* Renaissance oil painting, noblewoman subject, lower-right faded from water damage, muted earth-tone palette.
> *Prompt:* Comprehensive Restoration Suggestion | Temperature: 0.5
> *Output Quality:* Correctly suggested ochre tones, sfumato blending, and linen ground preparation — consistent with Renaissance technique.

**Test Case 2:**
> *Input:* Mughal miniature, faded floral borders, unknown artist.
> *Prompt:* Period-Specific Technique Analysis | Temperature: 0.3
> *Output Quality:* Referenced squirrel-hair brushwork, lapis lazuli pigments, and gold leaf application — culturally accurate.

**Test Case 3:**
> *Input:* Byzantine mosaic, cracked tesserae in central figure, gold background.
> *Prompt:* Symbolic & Cultural Interpretation | Temperature: 0.5
> *Output Quality:* Accurately decoded mandorla symbolism and hierarchical scaling — relevant to Byzantine iconographic tradition.

**Test Case 4:**
> *Input:* Ajanta cave mural, fire-damaged lower section, Jataka tale narrative.
> *Prompt:* Damage Assessment & Priority | Temperature: 0.3
> *Output Quality:* Prioritized structural consolidation before aesthetic restoration; flagged soot removal as Phase 1.

**Test Case 5:**
> *Input:* Gothic tapestry, central emblem torn, wool and silk threads.
> *Prompt:* Material-Specific Conservation | Temperature: 0.4
> *Output Quality:* Recommended Stabiltex conservation fabric, thread color matching, and climate-controlled storage at 45–55% RH.

**Overall Model Performance:** Outputs were consistently coherent, culturally grounded, and stylistically appropriate across 5 different art periods and 6 damage types tested.

---

## App Features Summary

- 12 specialized AI-powered analysis modes
- Adjustable temperature and response length via sidebar
- Artwork type selector (12 types) + Art period selector (20 periods)
- Analysis history with session-based logging
- Museum-quality UI with custom CSS (Cinzel + Crimson Text fonts)
- Responsive layout with tabbed navigation

---

## Credit Issue Screenshots

> It is uploaded as a file named Credit Issue  

---

## Live App & Repository

- **Streamlit App URL:** `https://artrestoration2.streamlit.app/`

