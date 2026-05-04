# Detection Engineering - Quick Reference

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

# Compare APIs
sim = compare_apis(imports1, imports2)

# Compare behaviors
sim = compare_behaviors(behavior1, behavior2)

# Compare PE sections
sim = compare_sections(sections1, sections2)

# Compare metadata
sim = compare_metadata(analysis1, analysis2)

# Calculate weighted overall score
score = calculate_overall_score(metrics, weights)

# Find similar samples from database
matches = find_similar_samples(target_analysis, all_samples, threshold=0.5)

# Cluster all samples into families
clusters = cluster_samples(all_samples, threshold=0.65)
```

---

## 🔢 Return Value Schemas

### `generate_yara_rule()` Returns:

```python
{
    "rule_name": "malware_MX_0001",
    "rule_type": "complete",
    "strings": [{"name": "str_1", "type": "wide", "value": "..."}],
    "complexity_score": 65,  # 0-100
    "generated_at": "2026-05-01T12:00:00"
}
```

### `calculate_similarity()` Returns:

```python
{
    "overall_similarity_score": 0.82,  # 0.0-1.0
    "similarity_level": "HIGHLY_SIMILAR",
    "metrics": {
        "string_similarity": 0.75,
        "api_similarity": 0.88,
        "behavior_similarity": 0.80
    },
    "recommendations": ["...", "..."]
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

# Generate rule
rule = generate_yara_rule(analysis, rule_name="trojan_banker_v1")

# Export
export_rule_to_file(rule, "rules/trojan_banker.yar")
```

### Task: Check if two malware are variants

```python
from core.similarity_engine import calculate_similarity

# Compare
report = calculate_similarity(sample1_analysis, sample2_analysis)

# Check results
score = report["overall_similarity_score"]
if score > 0.85:
    print("Very likely same malware family!")
elif score > 0.65:
    print("Likely related malware")
else:
    print("Different malware families")
```

### Task: Find similar samples in database

```python
from core.similarity_engine import find_similar_samples

# Search
matches = find_similar_samples(target_analysis, all_samples, threshold=0.60)

print(f"Found {len(matches['matches_found'])} similar samples:")
for match in matches["matches_found"]:
    print(f"  • {match['sample']}: {match['similarity_score']:.0%}")
```

### Task: Group malware into families

```python
from core.similarity_engine import cluster_samples

# Cluster
families = cluster_samples(all_samples, threshold=0.65)

for cluster in families["clusters"]:
    print(f"\n{cluster['cluster_id']} ({len(cluster['members'])} members):")
```

---

## ⚙️ Configuration Shortcuts

### Default Similarity Weights

```python
weights = {
    "strings": 0.25,          # 25% weight
    "apis": 0.30,             # 30% weight (strongest signal)
    "behaviors": 0.25,        # 25% weight
    "metadata": 0.10,         # 10% weight
    "sections": 0.10,         # 10% weight
}
```

---

## 📊 Similarity Score Interpretation

| Score         | Interpretation     |
| ------------- | ------------------ |
| **0.9-1.0**   | Near identical     |
| **0.8-0.89**  | Highly similar     |
| **0.65-0.79** | Similar            |
| **0.50-0.64** | Moderately similar |
| **<0.50**     | Dissimilar         |

---

## 🚀 Performance Tips

### Generate multiple YARA rules efficiently

```python
from core.yara_generator import generate_yara_rule, export_rule_to_file

rules = []
for analysis in all_analyses:
    rule = generate_yara_rule(analysis, rule_name=f"rule_{analysis['case_id']}")
    rules.append(rule)
```

---

## 📚 Quick Answers

**Q: How do I use the detection engine?**

A: See GUIDE.md for comprehensive documentation.

**Q: Can I customize the similarity weights?**

A: Yes, pass a custom `weights` dictionary to `calculate_similarity()`.

**Q: What formats can I export YARA rules to?**

A: .yar (YARA syntax) and .json (structured data).

**Q: How do I know if two samples are variants?**

A: Use `calculate_similarity()` - scores > 0.85 indicate variants.
