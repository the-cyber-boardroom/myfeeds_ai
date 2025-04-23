from typing                          import List
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Schema__OWASP__Factor(Type_Safe):
    """Statistical factors related to the OWASP category."""
    cwes_mapped         : int       # Number of Common Weakness Enumerations mapped to this category
    max_incidence_rate  : str       # Maximum incidence rate of the category (e.g., "55.97%")
    avg_incidence_rate  : str       # Average incidence rate of the category (e.g., "3.81%")
    avg_weighted_exploit: float     # Average weighted exploit score
    avg_weighted_impact : float     # Average weighted impact score
    max_coverage        : str       # Maximum coverage (e.g., "94.55%")
    avg_coverage        : str       # Average coverage (e.g., "47.72%")
    total_occurrences   : int       # Total number of occurrences
    total_cves          : int       # Total number of CVEs

class Schema__OWASP__AttackScenario(Type_Safe):
    """Example attack scenario for an OWASP category."""
    number         : int            # Scenario number
    description    : str            # Description of the scenario
    code_examples  : List[str]      # Optional code examples related to the scenario

class Schema__OWASP__Reference(Type_Safe):
    """Reference to additional resources for an OWASP category."""
    title          : str            # Title of the reference
    url            : str            # URL of the reference

class Schema__OWASP__CWE(Type_Safe):
    """Common Weakness Enumeration mapped to an OWASP category."""
    cwe_id         : str            # CWE identifier (e.g., "CWE-200")
    name           : str            # Name of the CWE
    url            : str            # URL to the CWE definition

class Schema__OWASP__Prevention(Type_Safe):
    """Prevention information for an OWASP category."""
    intro: str                      # Introduction paragraph for prevention
    items: List[str]                # List of prevention methods/items

class Schema__OWASP__Description(Type_Safe):
    """OWASP category description."""
    intro: str                      # Introduction paragraph for this category
    items: List[str]                # Bullet points inside description

class Schema__Owasp__Top_10__Category(Type_Safe):
    """Individual OWASP Top 10 category."""
    identifier              : str                              # The identifier of the category (e.g., "A01:2021")
    name                    : str                              # The name of the category
    icon                    : str                              # The icon of the category
    factors                 : Schema__OWASP__Factor
    overview                : str                              # Brief overview of the category
    description             : Schema__OWASP__Description       # Detailed description of the category
    how_to_prevent          : Schema__OWASP__Prevention        # Prevention information with intro and items
    example_attack_scenarios: List[Schema__OWASP__AttackScenario]
    references              : List[Schema__OWASP__Reference]
    mapped_cwes             : List[Schema__OWASP__CWE]