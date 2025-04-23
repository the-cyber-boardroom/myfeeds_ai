from enum import Enum


class Owasp__Top_10__Category(Enum):
    A01_2021__BROKEN_ACCESS_CONTROL : str = "A01_2021-Broken_Access_Control"
    A02_2021__CRYPTOGRAPHIC_FAILURES: str = "A02_2021-Cryptographic_Failures"
    A03_2021__INJECTION             : str = "A03_2021-Injection"
    A04_2021__INSECURE_DESIGN       : str = "A04_2021-Insecure_Design"
