"""
AI Quality Audit runner: executes 7 benchmark cases against live FastAPI endpoint
and records outputs for scientific accuracy verification.
"""
import json
import httpx

base_url = "http://localhost:8000/api/v1"

cases = {
    "1_quantitative": (
        "Solid-state lithium-metal batteries represent a high-energy density alternative to conventional intercalation systems. "
        "Here, we investigate a bilayer solid electrolyte comprising Li6.4La3Zr1.4Ta0.6O12 (LLZTO) and a fluorinated poly(ether-electrolyte) "
        "interfacial layer. Coin cell cycling against a 50 um lithium anode and high-loading LiNi0.8Mn0.1Co0.1O2 (NMC811, 4.2 mAh/cm2) cathode "
        "demonstrated an initial discharge capacity of 204.8 mAh/g at 0.1C. Under 1C continuous cycling at 30 deg C, the cells delivered "
        "91.2% capacity retention after 800 cycles with a mean Coulombic efficiency exceeding 99.94%. Symmetrical Li/Li cells showed stable "
        "plating and stripping for over 2,500 hours at 2.0 mA/cm2 without short-circuiting."
    ),
    "2_qualitative": (
        "Clinician burnout within acute emergency medicine environments represents a pervasive challenge undermining patient care quality. "
        "Through a six-month grounded theory ethnographic inquiry involving 42 observational shifts and semi-structured interviews across two "
        "urban trauma centers, we explored the coping mechanisms utilized by nursing staff. Grounded coding revealed that peer-to-peer debriefing "
        "circles significantly mitigate acute emotional distress and foster perceived psychological safety. Participants highlighted informal "
        "micro-interactions as vital buffers against depersonalization, whereas institutional administrative interventions were often perceived "
        "as performative."
    ),
    "3_no_numerical_findings": (
        "Distributed consensus algorithms operating within adversarial asynchronous networks face fundamental trade-offs between safety and liveness. "
        "This theoretical study formalizes a modular consensus framework separating transaction ordering from state-machine execution. "
        "By utilizing directed acyclic graph (DAG) topological validation, our formal proofs demonstrate deterministic finality under Byzantine "
        "fault thresholds without relying on synchronized global clocks. The framework proves strictly resilient against fork-choice manipulation, "
        "establishing a foundation for censorship-resistant state machine replication."
    ),
    "4_clearly_stated_objectives": (
        "The primary objective of this investigation is to evaluate whether sparse multi-head attention mechanisms can eliminate quadratic "
        "computational complexity in long-document transformers while maintaining translation accuracy. Specifically, we sought to determine "
        "if restricting attention to sliding local windows augmented by randomized global tokens preserves BLEU scores on the WMT14 English-to-German "
        "benchmark. Our secondary objective was to measure GPU peak memory utilization during 16,384-token document processing."
    ),
    "5_missing_objectives": (
        "A previously uncharacterized clade of deep-subsurface extremophilic archaea was isolated from hypersaline subterranean brine pools at a depth "
        "of 1.4 kilometers. Morphological examination identified flagellated pleomorphic cocci possessing novel ether-linked membrane lipid architectures "
        "rich in cyclopentane rings. Metagenomic sequencing assembled a 2.1-megabase circular chromosome containing genes encoding halo-tolerant ATP "
        "synthase complexes and betaine biosynthesis pathways. The organisms grow optimally at 45 degrees Celsius and 3.5 molar sodium chloride concentrations."
    ),
    "6_containing_limitations": (
        "A novel nanoparticle-conjugated peptide was synthesized to selectively target glioblastoma stem cells across the blood-brain barrier. "
        "In orthotopic xenograft models, the conjugate demonstrated high tumor localized fluorescence. However, this study is subject to several key "
        "limitations. First, the experimental cohort was limited to a small sample size (n=12 mice). Second, the pharmacokinetic evaluation was truncated "
        "at 72 hours, leaving chronic biodistribution and potential renal toxicity unassessed. Third, the synthetic yield of the peptide conjugate was below "
        "14%, posing severe manufacturing scalability constraints."
    ),
    "7_contradictory_claims": (
        "Nanoscale lipid vesicles functionalized with synthetic amphiphilic polymers were tested for targeted intracellular drug delivery. "
        "Preliminary in vitro MTT viability assays in human embryonic kidney (HEK293) cells showed virtually negligible cytotoxicity "
        "(cell viability > 97% at concentrations up to 500 uM). Conversely, in vivo systemic administration in Balb/c murine models induced severe, "
        "dose-dependent acute hepatotoxicity and elevated alanine aminotransferase (ALT) levels within 48 hours of injection. The discrepancy between "
        "benign cellular tolerance and fatal systemic organ toxicity remains unresolved, indicating potential undisclosed immunological cascade activations."
    ),
}

results = {}

for name, text in cases.items():
    print(f"Executing case: {name}...")
    try:
        resp = httpx.post(f"{base_url}/research/analyze", json={"text": text}, timeout=60.0)
        if resp.status_code == 200:
            data = resp.json()["result"]
            results[name] = {
                "status": 200,
                "summary": data["summary"],
                "objectives": data["objectives"],
                "findings": data["findings"],
                "keywords": data["keywords"],
                "questions": data["questions"],
            }
            print(f"  [PASS] {name} analyzed successfully.")
        else:
            results[name] = {"status": resp.status_code, "error": resp.text}
            print(f"  [FAIL] {name} returned HTTP {resp.status_code}")
    except Exception as exc:
        results[name] = {"status": 500, "error": str(exc)}
        print(f"  [ERROR] {name}: {exc}")

with open("ai_quality_evidence.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nAudit finished. Evidence written to ai_quality_evidence.json")
