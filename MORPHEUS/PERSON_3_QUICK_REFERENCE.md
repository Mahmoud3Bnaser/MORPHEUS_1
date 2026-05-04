# PERSON 3: DETECTION ENGINEERING - QUICK REFERENCE

## 🚀 Quick Start (30 seconds)

```python
from core.yara_generator import generate_yara_rule, export_rule_to_file
from core.similarity_engine import calculate_similarity

# Generate YARA rule
rule = generate_yara_rule(analysis_result)
export_rule_to_file(rule, "rules/malware.yar")

# Compare similarity
report = calculate_similarity(sample1, sample2)
print(f"Similarity: {report['overall_similarity_score']:.0%}")
```

---

## 📚 All Functions at a Glance

### YARA Generator Module

```python
# Generate complete YARA rule
rule = generate_yara_rule(analysis_result, rule_name="trojan_v1",
                          include_strings=True, include_sections=True)

# Generate simple string-based rule
rule = generate_strings_rule(suspicious_strings, rule_name="rule_name")

# Generate API pattern rule
rule = generate_api_rule(imports, rule_name="rule_name")

# Generate comprehensive multi-vector rule
rule = generate_combined_rule(analysis_result, behavior_result)

# Export to file (.yar or .json)
success, msg = export_rule_to_file(rule, "path/to/rule.yar", format="yar")

# Prepare rule for download
download = download_rule(rule, format="yar")
print(download["filename"])  # → "rule_name.yar"
```

### Similarity Engine Module

```python
# Calculate complete similarity between two samples
report = calculate_similarity(analysis1, analysis2,
                             behavior1, behavior2, weights=None)

# Compare strings
sim = compare_strings(strings1, strings2, threshold=0.6)
print(f"Match: {len(sim['matching_strings'])} strings")

# Compare APIs
sim = compare_apis(imports1, imports2)
print(f"Match: {len(sim['matching_apis'])} APIs")

# Compare behaviors
sim = compare_behaviors(behavior1, behavior2)
print(f"Similarity: {sim['score']:.0%}")

# Compare PE sections
sim = compare_sections(sections1, sections2)

# Compare metadata
sim = compare_metadata(analysis1, analysis2)

# Calculate weighted overall score
score = calculate_overall_score(metrics, weights)

# Find similar samples from database
matches = find_similar_samples(target_analysis, all_samples, threshold=0.5)
for match in matches["matches_found"]:
    print(f"{match['sample']}: {match['similarity_score']:.0%}")

# Cluster all samples into families
clusters = cluster_samples(all_samples, threshold=0.65)

# Create visualization data
viz = visualize_similarity(similarity_report)
```

---

## 🔢 Return Value Schemas

### `generate_yara_rule()` Returns:

```python
{
    "rule_name": "malware_MX_0001",
    "rule_type": "complete",
    "strings": [{"name": "str_1", "type": "wide", "value": "..."}],
    "conditions": ["2 of (str_hc_*)"],
    "metadata": {"author": "...", "date": "...", ...},
    "final_condition": "condition_string",
    "yara_rule_text": "rule malware_MX_0001 { ... }",
    "complexity_score": 65,  # 0-100
    "generated_at": "2026-05-01T12:00:00"
}
```

### `calculate_similarity()` Returns:

```python
{
    "sample1": {"name": "...", "md5": "...", "sha256": "..."},
    "sample2": {"name": "...", "md5": "...", "sha256": "..."},
    "overall_similarity_score": 0.82,  # 0.0-1.0
    "similarity_level": "HIGHLY_SIMILAR",
    "metrics": {
        "string_similarity": 0.75,
        "api_similarity": 0.88,
        "behavior_similarity": 0.80,
        "metadata_similarity": 0.65,
        "section_similarity": 0.70
    },
    "analysis": {
        "strings": {...},
        "apis": {...},
        "behaviors": {...},
        "metadata": {...},
        "sections": {...}
    },
    "recommendations": ["...", "..."],
    "created_at": "2026-05-01T12:00:00"
}
```

---

## 🎯 Common Tasks

### Task: Generate YARA rule for new malware

```python
from core.analyzer import analyze_file
from core.yara_generator import generate_yara_rule, export_rule_to_file

# Analyze file
analysis = analyze_file("data/uploads/suspicious.exe")

# Generate rule with custom name
rule = generate_yara_rule(analysis, rule_name="trojan_banker_v1")

# Export to .yar file
success, message = export_rule_to_file(rule, "rules/trojan_banker.yar")
print(message)

# Also save as JSON
export_rule_to_file(rule, "rules/trojan_banker.json", format="json")
```

### Task: Check if two malware are variants

```python
from core.similarity_engine import calculate_similarity

# Compare two samples
report = calculate_similarity(sample1_analysis, sample2_analysis)

# Check results
score = report["overall_similarity_score"]
if score > 0.85:
    print("✓ Very likely same malware family!")
elif score > 0.65:
    print("⚠ Likely related malware")
else:
    print("✗ Different malware families")

# See detailed breakdown
for metric, value in report["metrics"].items():
    print(f"  {metric}: {value:.0%}")
```

### Task: Find all similar samples in database

```python
from core.similarity_engine import find_similar_samples

# Search for samples similar to target
matches = find_similar_samples(
    target_analysis,
    all_samples_from_database,
    threshold=0.60  # Find 60%+ similar samples
)

print(f"Found {len(matches['matches_found'])} similar samples:")
for match in matches["matches_found"]:
    print(f"  • {match['sample']}: {match['similarity_score']:.0%}")
```

### Task: Group malware into families

```python
from core.similarity_engine import cluster_samples

# Cluster all samples
families = cluster_samples(all_samples, threshold=0.65)

for cluster in families["clusters"]:
    print(f"\n{cluster['cluster_id']} ({len(cluster['members'])} members):")
    for member in cluster["members"]:
        print(f"  - {member['sample']} ({member['score']:.0%})")

print(f"\nUnclustered: {len(families['unclustered'])} samples")
```

### Task: Download generated YARA rule

```python
from core.yara_generator import generate_yara_rule, download_rule
import json

# Generate rule
rule = generate_yara_rule(analysis)

# Prepare for download
download_yar = download_rule(rule, format="yar")
download_json = download_rule(rule, format="json")

# Access download metadata
print(f"File: {download_yar['filename']}")
print(f"Size: {download_yar['size_bytes']} bytes")
print(f"Type: {download_yar['content_type']}")
print(f"Content:\n{download_yar['content']}")
```

---

## ⚙️ Configuration Shortcuts

### Default Similarity Weights

```python
# Default weights (what's used if you don't specify)
weights = {
    "strings": 0.25,       # 25% weight
    "apis": 0.30,          # 30% weight (strongest signal)
    "behaviors": 0.25,     # 25% weight
    "metadata": 0.10,      # 10% weight
    "sections": 0.10,      # 10% weight
}

# Custom weights (emphasize API matching)
custom_weights = {
    "strings": 0.15,
    "apis": 0.50,          # Boost API matching
    "behaviors": 0.20,
    "metadata": 0.10,
    "sections": 0.05,
}

report = calculate_similarity(s1, s2, weights=custom_weights)
```

### Similarity Thresholds

```python
# Conservative (only very similar)
matches = find_similar_samples(target, all_samples, threshold=0.80)

# Moderate (similar variants)
matches = find_similar_samples(target, all_samples, threshold=0.65)

# Aggressive (related malware)
matches = find_similar_samples(target, all_samples, threshold=0.50)
```

---

## 📊 Similarity Score Interpretation

| Score         | Interpretation     | Action                           |
| ------------- | ------------------ | -------------------------------- |
| **0.9-1.0**   | Near identical     | Use same detection rule for both |
| **0.8-0.89**  | Highly similar     | Variants of same malware         |
| **0.65-0.79** | Similar            | Same malware family              |
| **0.50-0.64** | Moderately similar | Possible relation                |
| **0.30-0.49** | Somewhat similar   | Shared techniques only           |
| **<0.30**     | Dissimilar         | Different malware                |

---

## 🚀 Performance Tips

### Generate multiple YARA rules efficiently

```python
from core.yara_generator import generate_yara_rule, export_rule_to_file

rules = []
for analysis in all_analyses:
    rule = generate_yara_rule(analysis, rule_name=f"rule_{analysis['case_id']}")
    rules.append(rule)

# Export all at once
for i, rule in enumerate(rules):
    export_rule_to_file(rule, f"rules/rule_{i}.yar")
```

### Batch similarity search

```python
from core.similarity_engine import find_similar_samples

# Fast batch search with lower threshold
matches_all = find_similar_samples(target, database, threshold=0.50)

# Then manually review or filter high-confidence matches
high_confidence = [m for m in matches_all['matches_found'] if m['similarity_score'] > 0.75]
```

---

## 🔗 Integration Points

### With Person 1 (Static Analyzer)

```python
from core.analyzer import analyze_file
analysis = analyze_file("file.exe")
# Use analysis['suspicious_strings'], analysis['imports'], etc.
```

### With Person 2 (Intelligence Engine)

```python
from core.behavior_predictor import predict_behaviors
behaviors = predict_behaviors(analysis)
# Use for enhanced YARA rules and similarity
```

### Export Formats

```python
# YARA format (.yar) - for Yara scanning engines
export_rule_to_file(rule, "rules/malware.yar", format="yar")

# JSON format - for storage, APIs, database
export_rule_to_file(rule, "rules/malware.json", format="json")
```

---

## 📝 Example Workflows

### Full Pipeline: Analysis → YARA → Similarity

```python
from core.analyzer import analyze_file
from core.behavior_predictor import predict_behaviors
from core.yara_generator import generate_combined_rule, export_rule_to_file
from core.similarity_engine import find_similar_samples

# Step 1: Analyze new sample
new_sample = analyze_file("malware.exe")
behaviors = predict_behaviors(new_sample)

# Step 2: Generate detection rule
rule = generate_combined_rule(new_sample, behaviors, rule_name="new_malware_v1")
export_rule_to_file(rule, "rules/new_malware.yar")

# Step 3: Find similar samples in database
similar = find_similar_samples(new_sample, database, threshold=0.65)
print(f"Found {len(similar['matches_found'])} related samples")

# Step 4: Report findings
print(f"Detection rule saved to: rules/new_malware.yar")
print(f"Threat family size: {len(similar['matches_found'])} samples")
```

---

## ❓ Quick Answers

**Q: What's the best way to generate a rule?**
A: Use `generate_combined_rule()` - it uses all available data for best detection.

**Q: Which similarity metric matters most?**
A: API similarity (30% weight) - strongest signal for malware families.

**Q: How similar do samples need to be?**
A: 0.65+ for same family, 0.85+ for likely variants.

**Q: Can I export rules for Yara scanning?**
A: Yes! Use `export_rule_to_file(rule, path, format="yar")`

**Q: How do I use similarity for threat hunting?**
A: Use `find_similar_samples()` to build threat intelligence on known families.
