import json
from pathlib import Path
from typing import Dict, Any
import html

def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def _render_packet_md(bundle: Dict[str, Any]) -> str:
    case = bundle["case"]
    ex = bundle["extracted"]
    ch = bundle["checklist"]
    lines = []
    lines.append(f"# PA-Trace Packet Draft — {case.get('case_id')}\n")
    lines.append("## Exam request")
    lines.append(f"- Procedure: {case.get('exam_request', {}).get('procedure')}")
    lines.append("")
    lines.append("## Extracted facts (draft)")
    lines.append(f"- Symptoms duration (weeks): {ex.get('symptoms_duration_weeks')}")
    lines.append(f"- Conservative care duration (weeks): {ex.get('conservative_care_weeks')}")
    lines.append(f"- Treatments: {', '.join(ex.get('treatments', [])) or '—'}")
    lines.append(f"- Red flags: {', '.join(ex.get('red_flags', [])) or '—'}")
    lines.append("")
    lines.append("## Checklist")
    lines.append(f"- Overall: **{ch.get('overall_status')}**")
    if ch.get("missing_evidence"):
        lines.append(f"- Missing evidence: {', '.join(ch['missing_evidence'])}")
    lines.append("")
    lines.append("## Provenance (evidence quotes)")
    ev = ex.get("evidence", {})
    for k, spans in ev.items():
        if not spans:
            continue
        lines.append(f"- **{k}**:")
        for sp in spans:
            lines.append(f"  - ({sp.get('source')}) “{sp.get('quote')}”")
    return "\n".join(lines) + "\n"

def _apply_marks(text: str, spans: list[dict]) -> str:
    """
    Wrap given spans with <mark> tags including category classes.
    Uses indexed placeholders to allow safe HTML escaping of the text content.
    """
    # Filter valid note spans and sort by start descending to avoid offset shifts
    valid_spans = [
        s for s in spans
        if s.get("source") == "note"
        and isinstance(s.get("start"), int)
        and isinstance(s.get("end"), int)
    ]
    spans_sorted = sorted(valid_spans, key=lambda s: s["start"], reverse=True)

    out = text
    # Insert unique indexed placeholders for each span
    for i, s in enumerate(spans_sorted):
        start, end = s["start"], s["end"]
        if start < 0 or end > len(out) or start >= end:
            continue
        out = out[:end] + f"__MARK_END_{i}__" + out[end:]
        out = out[:start] + f"__MARK_START_{i}__" + out[start:]

    # Escape the text to make it HTML-safe
    out = html.escape(out)

    # Replace placeholders with actual <mark> tags containing correct classes
    for i, s in enumerate(spans_sorted):
        field_class = s.get("field", "default")
        span_id = f"span_{i}"
        tag_start = f'<mark id="{span_id}" class="highlight {html.escape(field_class)}" data-field="{html.escape(field_class)}">'
        tag_end = "</mark>"
        out = out.replace(f"__MARK_START_{i}__", tag_start)
        out = out.replace(f"__MARK_END_{i}__", tag_end)

    return out

def _render_highlights_html(bundle: Dict[str, Any]) -> str:
    case = bundle["case"]
    note = case.get("note_text", "")
    ex = bundle["extracted"]
    ev = ex.get("evidence", {})
    checklist = bundle["checklist"]

    # Flatten evidence into a list of spans
    spans = []
    for field, span_list in ev.items():
        for sp in span_list:
            if sp.get("source") == "note":
                s_copy = sp.copy()
                s_copy["field"] = field
                spans.append(s_copy)

    note_marked = _apply_marks(note, spans)

    # Prepare Policy Chunks
    policy_html = []
    for ch in bundle.get("retrieved_policy", []):
        policy_html.append(f"""
            <div class='chunk'>
                <div class='chunk_id'>{html.escape(ch['chunk_id'])}</div>
                <pre>{html.escape(ch['text'])}</pre>
            </div>
        """)

    # Prepare Fact Table Rows with data-field attributes for linking
    def make_row(key: str, label: str, value, is_list: bool = False) -> str:
        display_val = "—"
        status_class = "missing"
        if value:
            status_class = "present"
            if is_list:
                display_val = ", ".join(value) if value else "—"
            else:
                display_val = str(value)
        
        if key in checklist.get("missing_evidence", []):
            status_class = "missing"
            display_val += " <span class='badge-missing'>Evidence Missing</span>"
            
        verify_ui = f"""
        <div class="verify-controls">
            <button class="btn-icon btn-check" title="Confirm" onclick="toggleVerify(event, '{key}', 'check')">✓</button>
            <button class="btn-icon btn-x" title="Reject" onclick="toggleVerify(event, '{key}', 'x')">✕</button>
        </div>
        """
        
        return f"""
        <tr class="fact-row" data-field="{key}" onmouseover="highlightField('{key}')" onmouseout="unhighlightField('{key}')">
            <td class="label-cell">
                <span class="dot {key}"></span> {html.escape(label)}
            </td>
            <td class="value-cell">{display_val}</td>
            <td class="action-cell">{verify_ui}</td>
        </tr>
        """

    rows = []
    rows.append(make_row("symptoms_duration_weeks", "Symptoms Duration", ex.get("symptoms_duration_weeks")))
    rows.append(make_row("conservative_care_weeks", "Conservative Care", ex.get("conservative_care_weeks")))
    rows.append(make_row("treatments", "Treatments", ex.get("treatments"), is_list=True))
    rows.append(make_row("red_flags", "Red Flags", ex.get("red_flags"), is_list=True))

    rows_html = "\n".join(rows)

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PA-Trace: {html.escape(case.get('case_id',''))}</title>
  <style>
    :root {{
        --bg-color: #f8f9fa;
        --card-bg: #ffffff;
        --text-color: #202124;
        --text-subtle: #5f6368;
        --border-color: #dadce0;
        
        --c-symptoms-bg: #e0f2f1;
        --c-symptoms-text: #004d40;
        --c-symptoms-border: #80cbc4;
        
        --c-conservative-bg: #e8eaf6;
        --c-conservative-text: #1a237e;
        --c-conservative-border: #9fa8da;

        --c-treatments-bg: #fff8e1;
        --c-treatments-text: #ff6f00;
        --c-treatments-border: #ffe082;
        
        --c-redflags-bg: #ffebee;
        --c-redflags-text: #b71c1c;
        --c-redflags-border: #ef9a9a;
    }}

    body {{ 
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; 
        background-color: var(--bg-color);
        color: var(--text-color);
        margin: 0;
        padding: 24px;
        line-height: 1.5;
    }}

    .header {{ margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border-color); }}
    h1 {{ margin: 0; font-size: 24px; font-weight: 400; color: #1a73e8; display: flex; align-items: center; gap: 10px; }}
    .subtitle {{ color: var(--text-subtle); margin-top: 4px; font-size: 14px; }}
    
    .grid {{ display: grid; grid-template-columns: 3fr 2fr; gap: 24px; align-items: start; }}
    @media (max-width: 900px) {{ .grid {{ grid-template-columns: 1fr; }} }}

    .card {{ 
        background: var(--card-bg); 
        border-radius: 8px; 
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        padding: 24px;
        transition: box-shadow 0.2s ease;
    }}
    .card:hover {{ box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23); }}

    h2 {{ font-size: 18px; margin-top: 0; color: var(--text-color); }}

    .note-container {{ font-family: 'Georgia', serif; font-size: 16px; line-height: 1.6; white-space: pre-wrap; color: #3c4043; }}
    
    mark {{ 
        background-color: transparent; 
        color: inherit; 
        padding: 2px 0;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
        border-bottom: 2px solid transparent;
    }}

    mark.symptoms_duration_weeks {{ background-color: var(--c-symptoms-bg); border-bottom-color: var(--c-symptoms-border); color: var(--c-symptoms-text); }}
    mark.conservative_care_weeks {{ background-color: var(--c-conservative-bg); border-bottom-color: var(--c-conservative-border); color: var(--c-conservative-text); }}
    mark.treatments {{ background-color: var(--c-treatments-bg); border-bottom-color: var(--c-treatments-border); color: var(--c-treatments-text); }}
    mark.red_flags {{ background-color: var(--c-redflags-bg); border-bottom-color: var(--c-redflags-border); color: var(--c-redflags-text); }}

    mark.active {{ font-weight: 600; box-shadow: 0 0 0 2px rgba(0,0,0,0.2); }}

    table {{ width: 100%; border-collapse: separate; border-spacing: 0 8px; }}
    td {{ padding: 12px 16px; background: #fff; border-top: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); vertical-align: middle; }}
    td:first-child {{ border-left: 1px solid var(--border-color); border-top-left-radius: 8px; border-bottom-left-radius: 8px; font-weight: 500; color: var(--text-subtle); width: 140px; }}
    td:last-child {{ border-right: 1px solid var(--border-color); border-top-right-radius: 8px; border-bottom-right-radius: 8px; width: 60px; text-align: right; }}

    .fact-row:hover td {{ background-color: #f1f3f4; cursor: pointer; }}
    .fact-row.active td {{ background-color: #e8f0fe; border-color: #d2e3fc; }}

    /* Verification States */
    .fact-row.verified td {{ background-color: #e6f4ea !important; border-color: #34a853; }}
    .fact-row.verified .btn-check {{ background: #0f9d58; color: white; opacity: 1; }}
    .fact-row.verified .verify-controls {{ opacity: 1; }}

    .fact-row.rejected td {{ background-color: #fce8e6 !important; border-color: #db4437; }}
    .fact-row.rejected .value-cell {{ text-decoration: line-through; color: #5f6368; }}
    .fact-row.rejected .btn-x {{ background: #db4437; color: white; opacity: 1; }}
    .fact-row.rejected .verify-controls {{ opacity: 1; }}

    .dot {{ height: 10px; width: 10px; background-color: #ddd; border-radius: 50%; display: inline-block; margin-right: 8px; }}
    .dot.symptoms_duration_weeks {{ background-color: var(--c-symptoms-text); }}
    .dot.conservative_care_weeks {{ background-color: var(--c-conservative-text); }}
    .dot.treatments {{ background-color: var(--c-treatments-text); }}
    .dot.red_flags {{ background-color: var(--c-redflags-text); }}

    .badge-missing {{ font-size: 11px; background: #eee; color: #666; padding: 2px 6px; border-radius: 12px; margin-left: 8px; text-transform: uppercase; font-weight: bold; }}

    .verify-controls {{ opacity: 0.2; transition: opacity 0.2s; white-space: nowrap; }}
    .fact-row:hover .verify-controls {{ opacity: 1; }}
    .btn-icon {{ border: none; background: transparent; cursor: pointer; font-size: 14px; padding: 4px; border-radius: 50%; width: 24px; height: 24px; }}
    .btn-check {{ color: #0f9d58; }} .btn-check:hover {{ background: #e6f4ea; }}
    .btn-x {{ color: #db4437; }} .btn-x:hover {{ background: #fce8e6; }}

    .filters {{ margin-bottom: 16px; display: flex; gap: 10px; flex-wrap: wrap; }}
    .filter-btn {{ border: 1px solid var(--border-color); background: white; padding: 6px 12px; border-radius: 16px; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.2s; }}
    .filter-btn:hover {{ background: #f1f3f4; }}
    .filter-btn.inactive {{ opacity: 0.5; text-decoration: line-through; }}

    .chunk {{ padding: 12px; border-left: 3px solid #eee; margin-bottom: 12px; background: #fafafa; border-radius: 0 4px 4px 0; }}
    .chunk_id {{ font-size: 11px; font-weight: 700; color: #1967d2; text-transform: uppercase; margin-bottom: 4px; }}
    .chunk pre {{ font-family: 'Roboto Mono', monospace; font-size: 12px; color: #444; margin: 0; white-space: pre-wrap; }}

    .hidden {{ display: none !important; }}
  </style>
</head>
<body>

  <div class="header">
    <h1><span style="font-size: 28px;">⚕️</span> PA-Trace <span style="font-weight: 300; color: var(--text-subtle);">| Prior Auth Evidence Extraction</span></h1>
    <div class="subtitle">Case ID: {html.escape(case.get('case_id',''))} &bull; Generated by MedGemma 4B</div>
  </div>

  <div class="grid">
    
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 10px;">
          <h2 style="margin: 0;">Clinical Note</h2>
          <div class="filters">
              <span style="font-size: 12px; color: #666; margin-right: 4px; align-self: center;">Show:</span>
              <button class="filter-btn" onclick="toggleFilter(this, 'symptoms_duration_weeks')"><span class="dot symptoms_duration_weeks"></span> Symptoms</button>
              <button class="filter-btn" onclick="toggleFilter(this, 'conservative_care_weeks')"><span class="dot conservative_care_weeks"></span> Conservative</button>
              <button class="filter-btn" onclick="toggleFilter(this, 'treatments')"><span class="dot treatments"></span> Treatments</button>
              <button class="filter-btn" onclick="toggleFilter(this, 'red_flags')"><span class="dot red_flags"></span> Red Flags</button>
          </div>
      </div>
      <div class="note-container" id="clinical-note">{note_marked}</div>
    </div>

    <div class="card">
      <h2>Extracted Evidence</h2>
      <div class="subtitle" style="margin-bottom: 12px;">Review and verify each extracted fact. Hover to trace to source.</div>
      <table>{rows_html}</table>
      
      <h3 style="margin-top: 20px; font-size: 14px; color: var(--text-subtle);">Overall Status</h3>
      <div style="font-size: 18px; font-weight: 600; color: {'#0f9d58' if checklist.get('overall_status') == 'MET' else '#db4437' if checklist.get('overall_status') == 'NOT_MET' else '#f9a825'};">
        {html.escape(str(checklist.get('overall_status', 'UNKNOWN')))}
      </div>
    </div>
  </div>

  <div class="card" style="margin-top: 24px;">
    <h2>Policy Chunks (Traceability)</h2>
    {''.join(policy_html) or '<div class="subtitle">No policy chunks retrieved.</div>'}
  </div>

  <script>
    // Brushing and Linking: Highlight related elements
    function highlightField(field) {{
      document.querySelectorAll('mark[data-field="' + field + '"]').forEach(el => el.classList.add('active'));
      document.querySelectorAll('tr[data-field="' + field + '"]').forEach(el => el.classList.add('active'));
    }}
    function unhighlightField(field) {{
      document.querySelectorAll('mark[data-field="' + field + '"]').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('tr[data-field="' + field + '"]').forEach(el => el.classList.remove('active'));
    }}

    // Also add hover listeners to marks in the note
    document.querySelectorAll('mark.highlight').forEach(mark => {{
      mark.addEventListener('mouseover', () => highlightField(mark.dataset.field));
      mark.addEventListener('mouseout', () => unhighlightField(mark.dataset.field));
    }});

    // Category Filter Toggles
    function toggleFilter(btn, field) {{
      btn.classList.toggle('inactive');
      const isActive = !btn.classList.contains('inactive');
      document.querySelectorAll('mark[data-field="' + field + '"]').forEach(el => {{
        if (isActive) {{
          el.classList.remove('hidden');
        }} else {{
          el.classList.add('hidden');
        }}
      }});
    }}

    // Verification Logic (Visual State)
    function toggleVerify(event, field, type) {{
        event.stopPropagation(); // Prevent row highligting issues
        const row = document.querySelector('tr[data-field="' + field + '"]');
        if (!row) return;

        // Clean existing states
        const isVerified = row.classList.contains('verified');
        const isRejected = row.classList.contains('rejected');
        row.classList.remove('verified', 'rejected');

        // Apply new state if it wasn't already active (toggle behavior)
        if (type === 'check' && !isVerified) {{
            row.classList.add('verified');
        }} else if (type === 'x' && !isRejected) {{
            row.classList.add('rejected');
        }}
    }}
  </script>

</body>
</html>
"""

def write_packet_bundle(bundle: Dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    # Packet: merge "form-like" fields (minimal)
    case = bundle["case"]
    ex = bundle["extracted"]
    checklist = bundle["checklist"]

    packet = {
        "case_id": case.get("case_id"),
        "exam_request": case.get("exam_request", {}),
        "patient": case.get("patient", {}),
        "requesting_provider": case.get("requesting_provider", {}),
        "clinical_summary": {
            "symptoms_duration_weeks": ex.get("symptoms_duration_weeks"),
            "conservative_care_weeks": ex.get("conservative_care_weeks"),
            "treatments": ex.get("treatments", []),
            "red_flags": ex.get("red_flags", []),
        },
        "checklist_overall": checklist.get("overall_status"),
    }

    _write_json(out_dir / "packet.json", packet)
    _write_json(out_dir / "checklist.json", checklist)
    _write_json(out_dir / "provenance.json", ex.get("evidence", {}))
    (out_dir / "packet.md").write_text(_render_packet_md(bundle), encoding="utf-8")
    (out_dir / "highlights.html").write_text(_render_highlights_html(bundle), encoding="utf-8")
