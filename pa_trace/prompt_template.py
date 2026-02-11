PROMPT_TEMPLATE = r"""
You are extracting structured fields for a prior-authorization (PA) packet draft.
You MUST follow these rules:

1) Output MUST be valid JSON (no markdown, no extra keys).
2) For every non-null field you output, you MUST include at least one evidence span
   pointing to the exact substring in the NOTE or POLICY chunks.
3) If you cannot find evidence, output null/empty and list it under missing_evidence.

EVIDENCE REQUIREMENTS (STRICT):
- Every evidence.quote MUST be copied VERBATIM from note_text (exact substring match).
- Do NOT expand or normalize abbreviations inside evidence.quote.
- Prefer quotes with enough context: at least 2 words or >= 10 characters.
  Good: "6 weeks of physical therapy", "failed PT x 6 weeks"
  Bad: "PT", "6"
- If you cannot find an exact supporting quote in note_text, omit the evidence
  and mark the field under missing_evidence.

FIELD-SPECIFIC GUIDANCE:
- symptoms_duration_weeks: Extract duration of symptoms (e.g., "8 weeks", "3 months").
  Do NOT confuse with patient age (e.g., "45-year-old" is age, not duration).
  If onset is acute/sudden with no stated duration, mark as missing_evidence.
- conservative_care_weeks: Extract duration of conservative treatment attempted.
  Must be explicit (e.g., "6 weeks of PT", "failed 8 weeks of therapy").
- acute_onset: If the note states "acute" or "since this morning", set symptoms_duration_weeks to 0.
- treatments: Extract ONLY therapies/medications tried. 
  Do NOT include symptoms (e.g., "incontinence"), exam findings (e.g., "weakness"), or diagnoses.
  If a treatment is NOT mentioned in the text, do NOT list it.

COMMON ERRORS TO AVOID:
- Do NOT extract patient age as symptom duration.
  WRONG: "29-year-old" -> symptoms_duration_weeks: 29
  RIGHT: If no duration stated, output null and list in missing_evidence.

Input NOTE (string):
{note_text}

Retrieved POLICY CHUNKS (array of objects with chunk_id,text):
{policy_chunks_json}

Return JSON with this schema:
{{
  "symptoms_duration_weeks": <int|null>,
  "conservative_care_weeks": <int|null>,
  "treatments": <array of strings>,
  "red_flags": <array of strings>,
  "red_flags_present": <bool>,
  "evidence": {{
     "symptoms_duration_weeks": [{{"source":"note","start":<int>,"end":<int>,"quote":"..."}}] | [],
     "conservative_care_weeks": [{{...}}] | [],
     "treatments": [{{...}}] | [],
     "red_flags": [{{...}}] | []
  }},
  "missing_evidence": <array of strings>,
  "extraction_mode": "llm"
}}

Allowed red_flags values: ["cauda_equina","progressive_neuro_deficit","cancer","infection","fracture_trauma"]
Allowed treatments values: ["pt","nsaids","home_exercise","chiropractic","steroid","injection"]
"""
