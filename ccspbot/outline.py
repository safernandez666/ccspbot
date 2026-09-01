"""The CCSP exam outline in force since 1 August 2026.

Domain weights and subdomain identifiers come from the official ISC2 outline:
https://www.isc2.org/certifications/ccsp/ccsp-certification-exam-outline

Content validation checks every question against this module, so keeping it
accurate is what stops the bank drifting away from the exam.
"""

DOMAINS = {
    1: ("Cloud Concepts, Architecture and Design", 0.17),
    2: ("Cloud Data Security", 0.20),
    3: ("Cloud Platform and Infrastructure Security", 0.17),
    4: ("Cloud Application Security", 0.16),
    5: ("Cloud Security Operations", 0.17),
    6: ("Legal, Risk and Compliance", 0.13),
}

SUBDOMAINS = {
    "1.1": "Understand cloud computing concepts",
    "1.2": "Describe cloud reference architecture",
    "1.3": "Understand security concepts relevant to cloud computing",
    "1.4": "Understand design principles of secure cloud computing",
    "1.5": "Evaluate cloud service providers",
    "1.6": "Comprehend artificial intelligence / machine learning",

    "2.1": "Describe cloud data concepts",
    "2.2": "Design and implement cloud data storage architectures",
    "2.3": "Design and apply data security technologies and strategies",
    "2.4": "Implement data discovery",
    "2.5": "Plan and implement data classification",
    "2.6": "Design and implement Information Rights Management",
    "2.7": "Plan and implement data retention, deletion, and archiving policies",
    "2.8": "Design and implement auditability, traceability, and accountability of data events",
    "2.9": "Comprehend data protection of AI and machine learning data",

    "3.1": "Comprehend cloud infrastructure and platform components",
    "3.2": "Design a secure data center",
    "3.3": "Analyze risks associated with cloud infrastructure and platforms",
    "3.4": "Plan and implementation of security controls",
    "3.5": "Plan business continuity and disaster recovery",

    "4.1": "Advocate training and awareness for application security",
    "4.2": "Describe the Secure Software Development Life Cycle process",
    "4.3": "Apply the Secure Software Development Life Cycle",
    "4.4": "Apply cloud software assurance and validation",
    "4.5": "Use verified secure software",
    "4.6": "Comprehend and apply the specifics of cloud application architecture",
    "4.7": "Design appropriate Identity and Access Management solutions",

    "5.1": "Build and implement physical and logical infrastructure for cloud environment",
    "5.2": "Operate and maintain physical and logical infrastructure for cloud environment",
    "5.3": "Implement operational controls and standards",
    "5.4": "Support digital forensics",
    "5.5": "Manage communication with relevant parties",
    "5.6": "Manage security operations",

    "6.1": "Articulate legal requirements and unique risks within the cloud environment",
    "6.2": "Understand privacy issues",
    "6.3": "Understand audit process, methodologies, and required adaptations for a cloud environment",
    "6.4": "Understand implications of cloud to enterprise risk management",
    "6.5": "Understand outsourcing and cloud contract design",
}

#: Bank size we are building towards.
TARGET_BANK_SIZE = 600

#: Difficulty levels. 1 recalls a fact, 2 applies it, 3 needs a judgement call
#: between defensible options - which is what the real exam mostly asks.
DIFFICULTIES = {1: "recall", 2: "applied", 3: "scenario"}


def domain_of(subdomain: str) -> int:
    """Return the domain number a subdomain belongs to ('2.3' -> 2)."""
    return int(subdomain.split(".", 1)[0])


def target_count(domain: int, bank_size: int = TARGET_BANK_SIZE) -> int:
    """How many questions a domain should hold at a given bank size."""
    return round(DOMAINS[domain][1] * bank_size)
