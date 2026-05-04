# MORPHEUS-X Person 3: Detection Engineering Documentation

## 📋 Overview

Person 3 is responsible for building the **Detection Engineering** system - converting malware analysis into detection rules and finding similar threats.

Your modules receive analysis data from **Person 1** (Static Analyzer) and behaviors from **Person 2** (Intelligence Engine) and produce:

- ✅ YARA detection rules
- ✅ Malware similarity analysis
- ✅ Threat clustering and grouping
- ✅ Detection rule export/download

---

## 🎯 Your Two Core Modules

### 1️⃣ **yara_generator.py** - YARA Rule Generation

**Purpose**: Generate detection rules that can identify variants and similar malware

**Key Functions**:

```python
generate_yara_rule(analysis_result, rule_name, include_strings, include_sections)
  ↓ Returns: Complete YARA rule with metadata, strings, and conditions

generate_strings_rule(suspicious_strings, rule_name)
  ↓ Returns: String-only detection rule (simplest)

generate_api_rule(imports, rule_name)
  ↓ Returns: API pattern detection rule

generate_combined_rule(analysis_result, behavior_result, rule_name)
  ↓ Returns: Comprehensive multi-vector detection rule

export_rule_to_file(rule, file_path, format)
  ↓ Returns: (success, message) - saves .yar or .json

download_rule(rule, format)
  ↓ Returns: Download package with content and metadata
```

**YARA Rule Generation Strategy**:

The YARA rules use a **multi-vector detection approach**:

1. **Suspicious Strings** (25% weight)
   - High-confidence strings: Most specific, highest accuracy
   - Medium-confidence strings: Broader detection, more false positives possible
   - Automatically filters short/invalid strings

2. **API Import Patterns** (30% weight)
   - Critical API combinations (VirtualAllocEx + WriteProcessMemory)
   - DLL import structure
   - Function call sequences

3. **Section Characteristics** (20% weight)
   - Suspicious section names (UPX, .packed, etc.)
   - High entropy sections indicating packing/obfuscation
   - Unusual section permissions (RWX)

4. **Metadata Patterns** (15% weight)
   - File size ranges
   - Packer indicators
   - Missing digital signatures

5. **Behavioral Signals** (10% weight)
   - Predicted malware behaviors
   - High-signal API combinations
   - Obfuscation/packing indicators

**Rule Output Formats**:

- **YARA Text** (.yar): Standard YARA syntax for use in Yara engines
- **JSON**: Structured format for database storage or programmatic use

**Rule Complexity Score**: 0-100 indicating detection rule sophistication

---

### 2️⃣ **similarity_engine.py** - Malware Similarity Analysis

**Purpose**: Identify variants and families by comparing malware samples

**Key Functions**:

```python
calculate_similarity(analysis1, analysis2, behavior1, behavior2, weights)
  ↓ Returns: Comprehensive similarity report with all metrics

compare_strings(strings1, strings2, threshold)
  ↓ Returns: String pattern similarity with matches and unique items

compare_apis(imports1, imports2)
  ↓ Returns: API import similarity with DLL and function matching

compare_behaviors(behavior1, behavior2)
  ↓ Returns: Behavioral pattern similarity

compare_sections(sections1, sections2)
  ↓ Returns: PE section structure similarity

compare_metadata(analysis1, analysis2)
  ↓ Returns: File metadata similarity

calculate_overall_score(metrics, weights)
  ↓ Returns: Weighted composite similarity score (0.0-1.0)

find_similar_samples(target_analysis, all_samples, threshold)
  ↓ Returns: List of samples similar to target with scores

cluster_samples(all_samples, threshold)
  ↓ Returns: Groups of similar malware samples
```

**Similarity Metrics Explained**:

1. **String Similarity** (Default Weight: 25%)
   - Exact string matching
   - Fuzzy matching for variations
   - High confidence when >70% match

2. **API Similarity** (Default Weight: 30%) ⭐ Most Important
   - DLL import structure matching
   - Imported function matching
   - Critical API overlap detection (process injection, etc.)
   - Strongest signal for malware families

3. **Behavior Similarity** (Default Weight: 25%)
   - Predicted behavior matching
   - Severity correlation
   - Technique overlap

4. **Metadata Similarity** (Default Weight: 10%)
   - File size similarity ratio
   - Packer detection match
   - PE format consistency

5. **Section Similarity** (Default Weight: 10%)
   - Section name matching
   - Entropy profile similarity

**Similarity Levels**:

| Score    | Level              | Meaning                                  |
| -------- | ------------------ | ---------------------------------------- |
| 0.9+     | NEAR_IDENTICAL     | Likely exact copies or trivial variants  |
| 0.7-0.89 | HIGHLY_SIMILAR     | Same malware family, close variants      |
| 0.5-0.69 | MODERATELY_SIMILAR | Related malware, possible variants       |
| 0.3-0.49 | SOMEWHAT_SIMILAR   | Shared characteristics, distant relation |
| <0.3     | DISSIMILAR         | Different malware or unrelated           |

**Use Cases**:

- **Threat Intelligence**: Link new samples to known malware families
- **Incident Response**: Find all variants during investigation
- **Detection Optimization**: Identify common patterns for rule generation
- **Malware Clustering**: Group related samples for analysis

---

## 🔄 Integration with Other Components

### Receiving Data From Person 1 (Static Analyzer)

```
Person 1 Output (analysis_result) contains:
├── file metadata (size, hashes, name)
├── PE structure (sections, imports)
├── suspicious_strings
├── high_confidence_suspicious_apis
├── high_signal_combinations ← Most valuable for YARA rules
└── packer_indicators
```

### Receiving Data From Person 2 (Intelligence Engine)

```
Person 2 Output (behavior_result) contains:
├── predicted_behaviors (list of detected malware behaviors)
├── behavior confidence levels
└── behavior severity ratings
```

---
5
## 📊 Data Flow

```
Person 1 (Static Analyzer)
       ↓
analysis_result (JSON)
       ├──→ Person 2 (Intelligence Engine)
       │           ↓
       │      behavior_result
       │           │
       ├───────────┴→ Person 3 (Detection Engineering)
       │                      ↓
       └────────────────→ YARA Generator ──→ .yar files
                         Similarity Engine ──→ Clustering & Grouping
```

---

## 🛠️ Common Workflows

### Workflow 1: Generate Detection Rule for New Malware

```python
from core.analyzer import analyze_file
from core.yara_generator import generate_yara_rule, export_rule_to_file

# Step 1: Analyze file (Person 1)
analysis = analyze_file("data/uploads/sample.exe")

# Step 2: Generate YARA rule
rule = generate_yara_rule(analysis, rule_name="trojan_banker_v1")

# Step 3: Export rule
success, message = export_rule_to_file(rule, "rules/trojan_banker.yar")
```

### Workflow 2: Find Similar Samples

```python
from core.similarity_engine import calculate_similarity, find_similar_samples

# Step 1: Compare two known samples
report = calculate_similarity(sample1_analysis, sample2_analysis)

print(f"Similarity: {report['overall_similarity_score']:.2%}")
print(f"Level: {report['similarity_level']}")

# Step 2: Search database for similar samples
matches = find_similar_samples(sample1_analysis, database_samples)
for match in matches["matches_found"]:
    print(f"  - {match['sample']}: {match['similarity_score']:.2%}")
```

### Workflow 3: Cluster Malware Family

```python
from core.similarity_engine import cluster_samples

# Cluster all samples
clusters = cluster_samples(all_samples, threshold=0.65)

for cluster in clusters["clusters"]:
    print(f"\n{cluster['cluster_id']}:")
    for member in cluster["members"]:
        print(f"  - {member['sample']} ({member['score']:.2%})")
```

---

## ⚙️ Configuration & Customization

### Custom Weights for Similarity Scoring

```python
custom_weights = {
    "string_similarity": 0.20,      # Less weight for strings
    "api_similarity": 0.40,         # More weight for APIs
    "behavior_similarity": 0.20,
    "metadata_similarity": 0.10,
    "section_similarity": 0.10,
}

report = calculate_similarity(
    sample1, sample2,
    weights=custom_weights
)
```

### Custom YARA Rule Configuration

```python
rule = generate_yara_rule(
    analysis,
    rule_name="custom_rule_name",
    include_strings=True,      # Include suspicious strings
    include_sections=True,     # Include section patterns
    include_metadata=True      # Include metadata section
)
```

---

## 📈 Output Examples

### YARA Rule Output

```yara
rule malware_MX_0001
{
    meta:
        author = "MORPHEUS Detection Engineering"
        date = "2026-05-01"
        case_id = "MX-0001"
        file_name = "suspicious.exe"
        md5 = "5d41402abc4b2a76b9719d911017c592"
        risk_level = "critical"

    strings:
        $str_hc_1 = "powershell.exe" wide
        $str_hc_2 = "WriteProcessMemory" wide
        $sec_name_1 = "UPX0"
        $api_1 = "VirtualAllocEx"
        $api_2 = "CreateRemoteThread"

    condition:
        2 of (str_hc_*) or 2 or more apis_detected
}
```

### Similarity Report Output

```json
{
  "overall_similarity_score": 0.82,
  "similarity_level": "HIGHLY_SIMILAR",
  "metrics": {
    "string_similarity": 0.75,
    "api_similarity": 0.88,
    "behavior_similarity": 0.8,
    "metadata_similarity": 0.65,
    "section_similarity": 0.7
  },
  "analysis": {
    "apis": {
      "matching_apis": [
        "VirtualAllocEx",
        "WriteProcessMemory",
        "CreateRemoteThread"
      ],
      "high_signal_overlap": true
    },
    "behaviors": {
      "matching_behaviors": ["Process Injection", "Persistence"],
      "shared_severity": [{ "severity": "high", "count": 2 }]
    }
  },
  "recommendations": [
    "⚠️ ALERT: High similarity detected between samples.",
    "📊 Samples likely share common malware source or toolkit.",
    "🎯 Consider consolidated threat response.",
    "⚙️ Similar API patterns: Check for process injection or data theft."
  ]
}
```

---

## 🎓 Best Practices

### YARA Rule Generation

✅ **DO:**

- Use `generate_combined_rule()` for comprehensive detection
- Include both string and API patterns
- Export rules to .yar format for immediate use
- Version your rules (rule_name_v1, rule_name_v2)

❌ **DON'T:**

- Create rules with only 1-2 strings (too many false positives)
- Use very generic strings (e.g., "the", "and")
- Mix unrelated patterns in one rule (hard to maintain)

### Similarity Analysis

✅ **DO:**

- Use `find_similar_samples()` for batch threat intelligence
- Set threshold >0.65 for meaningful matches
- Consider behavior analysis for variant detection
- Cluster samples to identify malware families

❌ **DON'T:**

- Trust API similarity alone (use combined scoring)
- Set threshold <0.50 (too many false matches)
- Compare samples without sufficient data

---

## 🔍 Troubleshooting

**Q: My YARA rule has no strings matching**

- **A**: Check that `include_strings=True` and that suspicious_strings exist in analysis

**Q: Similarity score seems too low**

- **A**: Verify both samples have complete analysis data, check weights configuration

**Q: Generated YARA rule syntax invalid**

- **A**: Use `download_rule(format='json')` to verify data structure

---

## 📚 Module Statistics

| Module               | Lines | Functions | Key Features                     |
| -------------------- | ----- | --------- | -------------------------------- |
| yara_generator.py    | ~550  | 12        | 5 rule types, export formats     |
| similarity_engine.py | ~650  | 14        | 5 similarity metrics, clustering |

---

## 🎯 Next Steps

1. Read **PERSON_3_QUICK_REFERENCE.md** for quick API reference
2. Check **PERSON_3_USAGE_EXAMPLES.py** for code examples
3. Run **test_detection_engine.py** to verify everything works
4. Start generating YARA rules for your samples!
