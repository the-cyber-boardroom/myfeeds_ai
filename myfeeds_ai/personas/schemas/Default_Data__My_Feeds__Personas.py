from myfeeds_ai.personas.schemas.Schema__Persona__Types import Schema__Persona__Types

# Executive Leadership Personas
Default_Data__EXEC__CEO = dict(description = ("The Chief Executive Officer (CEO) leads strategic direction for a mid-sized technology company "
                                               "with growing cybersecurity concerns. Responsible for shareholder value and board reporting, "
                                               "they prioritize business continuity, reputational risk, and regulatory compliance. "
                                               "The CEO oversees digital transformation initiatives leveraging cloud services, AI/ML technologies, "
                                               "and business intelligence platforms, while adhering to SOX, GDPR, and industry-specific regulations. "
                                               "They must maintain awareness of significant security incidents, data breaches, and emerging "
                                               "cyber threats that could impact stock price, customer trust, or regulatory standing. "
                                               "The CEO collaborates closely with the CFO, CISO, CTO, and legal counsel to balance security "
                                               "investments against business growth opportunities and profitability targets."))

Default_Data__EXEC__CISO = dict(description = ("The Chief Information Security Officer (CISO), who reports to the CEO, at a FinTech company collaborates closely "
                                                "with compliance officers and risk assessors to manage cybersecurity risks. "
                                                "The company leverages Digital Payment Platforms, Mobile Banking Solutions, "
                                                "and Identity and Access Management Systems, aligning with ISO/IEC 27001 and NIST Cybersecurity Framework. "
                                                "They actively employ Intrusion Detection Systems, Data Loss Prevention Tools, Incident Management Tools, "
                                                "and Security Information and Event Management (SIEM) platforms. Ensuring data protection through Privacy "
                                                "Policies, Data Encryption, and Anonymisation Techniques, the CISO maintains regulatory compliance adhering to "
                                                "GDPR, SOX, PCI DSS, and NIST SP 800-53 standards. Additionally, they utilize Threat Intelligence and Incident "
                                                "Response strategies, supported by Security Analysts, Incident Responders, and Threat Hunters, to proactively "
                                                "manage operational risks and information assurance."))

Default_Data__EXEC__CTO = dict(description = ("The Chief Technology Officer (CTO) drives technological innovation and digital strategy "
                                               "for a technology-focused enterprise. Reporting to the CEO, they oversee engineering teams, "
                                               "software development lifecycles, and technical architecture decisions. The CTO leads cloud migration "
                                               "initiatives, microservices adoption, and DevOps practices while collaborating with the CISO on "
                                               "secure-by-design principles and DevSecOps integration. They evaluate emerging technologies including "
                                               "containerization, serverless computing, edge computing, and AI/ML platforms, while maintaining "
                                               "technical debt awareness and system reliability. The technology stack includes CI/CD pipelines, "
                                               "Kubernetes orchestration, API gateways, and distributed database systems. The CTO must balance "
                                               "innovation velocity with secure coding practices, dependency management, and supply chain integrity "
                                               "while adhering to relevant technical standards from NIST, ISO, and industry consortiums."))

# Investor Personas
Default_Data__INVESTOR__ANGEL = dict(description = ("The Angel Investor specializes in early-stage cybersecurity startups, typically investing "
                                                     "between $50K-$250K in pre-seed and seed rounds. With a technical background in network security "
                                                     "and previous exits from two security companies, they evaluate founders' technical expertise, "
                                                     "innovation potential, and market timing. They focus on disruptive technologies in zero trust, "
                                                     "API security, supply chain security, and identity solutions. The investor participates in "
                                                     "pitch competitions, security incubators, and maintains relationships with accelerators like "
                                                     "Y Combinator and Techstars. They require awareness of emerging attack vectors, evolving compliance "
                                                     "landscapes, and competitor funding to identify market gaps and investment opportunities. "
                                                     "The investor seeks a 10x return within 5-7 years and actively advises portfolio companies on "
                                                     "go-to-market strategies, customer acquisition, and subsequent funding rounds."))

Default_Data__INVESTOR__SERIES_A = dict(description = ("The Series A Investor works at a venture capital firm specializing in cybersecurity and "
                                                        "enterprise software investments. Managing a $150M fund, they lead rounds between $5M-$15M for "
                                                        "companies with proven product-market fit and initial traction. They evaluate cybersecurity "
                                                        "startups based on recurring revenue growth, customer retention metrics, and differentiated "
                                                        "technology addressing enterprise security challenges. The investor seeks companies leveraging "
                                                        "artificial intelligence, blockchain, quantum-resistant cryptography, or cloud-native security. "
                                                        "They monitor regulatory changes like NIS2, DORA, and evolving SEC requirements that drive security "
                                                        "spending. With board positions in 5-7 portfolio companies, they advise on executive hiring, "
                                                        "enterprise sales strategies, and partnership development. The investor collaborates with CISOs "
                                                        "at Fortune 500 companies to understand enterprise security priorities, budget cycles, and "
                                                        "emerging requirements that signal market opportunities."))

# Corporate Governance Personas
Default_Data__PRIVATE__CISO = dict(description = ("The Private Company CISO oversees information security for a mid-sized private enterprise "
                                                   "with 2,500 employees across multiple locations. Reporting to the COO, they manage a team "
                                                   "of 12 security professionals and a $5.8M annual budget. The company operates critical "
                                                   "business applications in a hybrid cloud environment using AWS and Azure, alongside legacy "
                                                   "on-premises infrastructure. The CISO implements security controls aligned with NIST CSF, "
                                                   "CIS Controls, and ISO 27001 frameworks, though formal certification is not required. "
                                                   "They utilize EDR solutions, SIEM platforms, vulnerability management tools, and IAM systems "
                                                   "from vendors including CrowdStrike, SentinelOne, and Okta. Their risk management approach "
                                                   "balances security requirements with business flexibility, focusing on protecting intellectual "
                                                   "property, customer data, and business operations. The CISO collaborates closely with IT, legal, "
                                                   "and business unit leaders while preparing for potential private equity investment or acquisition."))

Default_Data__PRIVATE__BOARD_MEMBER = dict(description = ("The Private Company Board Member serves on the board of directors for a privately-held "
                                                            "SaaS company with annual revenue of $75M. With a background in corporate finance "
                                                            "and business operations, they chair the audit committee and provide oversight on "
                                                            "risk management and cybersecurity governance. The board member evaluates quarterly "
                                                            "security briefings from the CIO, cyber insurance coverage, and incident response "
                                                            "readiness while ensuring adequate security investments to protect customer data and "
                                                            "intellectual property. They help the company prepare for eventual acquisition or IPO "
                                                            "by implementing governance structures that will satisfy future regulatory requirements "
                                                            "and due diligence processes. The board member collaborates with external auditors, "
                                                            "private equity investors, and fellow board members to balance growth objectives with "
                                                            "security requirements, particularly as the company expands into international markets "
                                                            "and enterprise customer segments with stringent security expectations."))

Default_Data__PUBLIC__CISO = dict(description = ("The Public Company CISO directs cybersecurity strategy and operations for a publicly-traded "
                                                  "enterprise subject to SEC oversight and reporting requirements. Reporting to the CIO with "
                                                  "dotted-line responsibility to the Risk Committee of the Board, they manage a security organization "
                                                  "of 35 staff across security operations, governance/compliance, architecture, and identity management. "
                                                  "The CISO maintains SOC 2 Type II certification, implements controls supporting SOX compliance, "
                                                  "and ensures adherence to evolving SEC cybersecurity disclosure requirements. They deploy "
                                                  "enterprise-grade security technologies including cloud security posture management, data loss "
                                                  "prevention, privileged access management, and threat intelligence platforms. The security program "
                                                  "undergoes regular assessment against NIST CSF, with quarterly metrics reported to the board. "
                                                  "The CISO manages relationships with external auditors, cyber insurance providers, and security "
                                                  "assessors while ensuring security controls support the company's digital transformation initiatives "
                                                  "and regulatory compliance obligations across multiple jurisdictions."))

Default_Data__PUBLIC__BOARD_MEMBER = dict(description = ("The Public Company Board Member serves on the risk committee for a publicly-traded "
                                                           "financial services company with market capitalization exceeding $2B. With expertise in "
                                                           "risk management and corporate governance, they provide oversight on enterprise risk "
                                                           "including cybersecurity, data privacy, and regulatory compliance. The board member "
                                                           "evaluates the company's cybersecurity posture against regulatory requirements including "
                                                           "SOX, GLBA, SEC disclosure rules, and applicable international regulations like GDPR and DORA. "
                                                           "They review quarterly security updates, annual penetration testing results, and metrics "
                                                           "on security program maturity while ensuring adequate board-level visibility into cyber "
                                                           "risks. The board member approves cyber insurance policies, influences security budget "
                                                           "allocation, and evaluates CISO performance. They coordinate with audit committees, "
                                                           "external auditors, and regulators to ensure appropriate security governance and controls, "
                                                           "particularly focusing on third-party risk management and incident response protocols "
                                                           "that could impact shareholder value and regulatory standing."))

Default_Data__STARTUP__CISO = dict(description = ("The Startup CISO leads security for a rapidly growing Series B startup with 120 employees "
                                                   "and a cloud-native SaaS platform. Reporting to the CTO, they operate as a security team of one "
                                                   "with limited budget while building security foundations to support 200% annual growth and "
                                                   "enterprise customer requirements. The CISO implements essential security controls using "
                                                   "primarily open-source and cloud-native tools, focusing on cloud security posture, CI/CD pipeline "
                                                   "security, and identity management. They prioritize security measures that directly enable "
                                                   "sales by addressing customer security questionnaires, supporting SOC 2 certification, and "
                                                   "implementing sufficient controls to pass enterprise security reviews. The CISO works closely "
                                                   "with developers to embed security into DevOps workflows, manages the bug bounty program, and "
                                                   "leverages automated security testing to compensate for limited resources. They balance "
                                                   "immediate security needs against building scalable security architecture that will support "
                                                   "future growth, potential IPO requirements, and expanding compliance obligations as the company "
                                                   "targets larger enterprise customers and regulated industries."))

Default_Data__STARTUP__BOARD_MEMBER = dict(description = ("The Startup Board Member represents a venture capital firm that led the company's "
                                                            "Series A round, holding a 22% stake in a cybersecurity startup valued at $45M. "
                                                            "With previous experience scaling B2B SaaS companies, they provide governance oversight "
                                                            "and strategic guidance on growth strategy, fundraising, and risk management. The board "
                                                            "member evaluates security practices primarily through the lens of business enablement - "
                                                            "ensuring the startup can pass customer security reviews, achieve necessary certifications, "
                                                            "and protect intellectual property without impeding rapid development cycles. "
                                                            "They help recruit security advisors, connect the company with CISO customers, and review "
                                                            "security investments that directly support sales acceleration or risk reduction for key "
                                                            "enterprise deals. The board member balances growth imperatives against foundational "
                                                            "security requirements, particularly focusing on securing the product development process, "
                                                            "demonstrating security capabilities to customers, and preparing for security due diligence "
                                                            "in future funding rounds or potential acquisition."))

# Security Team Personas
Default_Data__TEAM__APP_SEC = dict(description = ("The Application Security Team Lead manages a team of five AppSec engineers responsible for "
                                                    "securing the company's customer-facing applications and internal development processes. "
                                                    "They implement and maintain the secure development lifecycle across 15 development teams using "
                                                    "Agile methodologies and CI/CD pipelines. The AppSec Lead evaluates and deploys SAST, DAST, SCA, "
                                                    "and API security testing tools integrated into Jenkins and GitHub workflows, while managing the "
                                                    "vulnerability management process for discovered application weaknesses. They enforce secure coding "
                                                    "standards based on OWASP guidelines, conduct security architecture reviews for new features, "
                                                    "and perform threat modeling sessions for critical application components. The AppSec team monitors "
                                                    "for new vulnerability classes, tracks dependency security using software composition analysis, "
                                                    "and manages the application-level WAF rules. The AppSec Lead collaborates closely with development "
                                                    "managers, cloud security specialists, and the DevOps team to balance security requirements with "
                                                    "release velocity while maintaining compliance with security frameworks relevant to the application tier."))

Default_Data__TEAM__EXTERNAL_COMMS = dict(description = ("The External Communications Manager leads cybersecurity communications strategy for "
                                                           "a multinational corporation, reporting to the Chief Communications Officer with close "
                                                           "collaboration with the CISO office. They develop and maintain the security incident "
                                                           "communications playbook, prepare executive statements for potential breaches, and manage "
                                                           "security-related media inquiries. The communications manager crafts messaging for "
                                                           "security certifications, compliance achievements, and security program enhancements that "
                                                           "demonstrate the company's commitment to data protection. They coordinate security awareness "
                                                           "campaigns for customers, translate technical vulnerabilities into business impact statements "
                                                           "for executive briefings, and monitor industry security incidents to prepare contingency "
                                                           "messaging. The communications specialist works with legal, investor relations, and government "
                                                           "affairs teams to ensure consistent security messaging across stakeholder groups. They maintain "
                                                           "relationships with industry analysts, prepare security content for the annual report, and "
                                                           "develop crisis communication plans for various security scenario types while ensuring "
                                                           "regulatory compliance with disclosure requirements."))

Default_Data__TEAM__INCIDENT_RESPONSE = dict(description = ("The Incident Response Team Lead manages a security operations team of eight analysts "
                                                              "responsible for 24/7 monitoring, detection, and response to security incidents across "
                                                              "the enterprise environment. They oversee the security operations center using a SIEM platform, "
                                                              "EDR solutions, network monitoring tools, and threat intelligence feeds to detect and "
                                                              "investigate potential security breaches. The IR Lead maintains the incident response "
                                                              "playbook, conducts tabletop exercises, and coordinates response activities during active "
                                                              "incidents involving cross-functional teams from IT, legal, and business units. "
                                                              "They implement and tune detection rules based on MITRE ATT&CK framework, industry threat "
                                                              "intelligence, and internal risk assessments. The team utilizes digital forensics tools, "
                                                              "malware analysis capabilities, and automated response workflows to contain and remediate "
                                                              "threats. The IR Lead reports incident metrics to the CISO, maintains documentation for "
                                                              "compliance and insurance requirements, and continuously refines detection and response "
                                                              "capabilities based on lessons learned and evolving threat landscape."))

Default_Data__TEAM__GRC = dict(description = ("The Governance, Risk and Compliance (GRC) Manager leads a team of five specialists responsible for "
                                               "the company's security compliance programs, risk management framework, and security policies. "
                                               "They maintain certifications including ISO 27001, SOC 2, and PCI DSS while coordinating security "
                                               "activities to satisfy regulatory requirements across GDPR, CCPA, HIPAA, and industry-specific "
                                               "regulations. The GRC Manager implements an integrated risk management framework aligned with "
                                               "NIST CSF, conducts regular risk assessments, and manages the remediation tracking process for "
                                               "identified control gaps. They oversee vendor security assessments, maintain the security exception "
                                               "process, and develop metrics for board-level security reporting. The GRC team documents security "
                                               "policies and procedures, manages the security awareness training program, and coordinates external "
                                               "security audits and assessments. The GRC Manager collaborates with legal, privacy, IT, and business "
                                               "units to implement controls that satisfy multiple compliance requirements simultaneously while "
                                               "optimizing audit activities and evidence collection to reduce compliance overhead."))

Default_Data__TEST__PERSONA = dict(description = ("This is a test persona that is used in the unit tests for the MyFeeds.ai site. The areas of "
                                                  "responsibility are the sames as a cyber security engineer"))
# Comprehensive Dictionary
Default_Data__My_Feeds__Personas = {
    Schema__Persona__Types.EXEC__CEO              : Default_Data__EXEC__CEO                 ,
    Schema__Persona__Types.EXEC__CISO             : Default_Data__EXEC__CISO                ,
    Schema__Persona__Types.EXEC__CTO              : Default_Data__EXEC__CTO                 ,
    Schema__Persona__Types.INVESTOR__ANGEL        : Default_Data__INVESTOR__ANGEL           ,
    Schema__Persona__Types.INVESTOR__SERIES_A     : Default_Data__INVESTOR__SERIES_A        ,
    Schema__Persona__Types.PRIVATE__CISO          : Default_Data__PRIVATE__CISO             ,
    Schema__Persona__Types.PRIVATE__BOARD_MEMBER  : Default_Data__PRIVATE__BOARD_MEMBER     ,
    Schema__Persona__Types.PUBLIC__CISO           : Default_Data__PUBLIC__CISO              ,
    Schema__Persona__Types.PUBLIC__BOARD_MEMBER   : Default_Data__PUBLIC__BOARD_MEMBER      ,
    Schema__Persona__Types.STARTUP__CISO          : Default_Data__STARTUP__CISO             ,
    Schema__Persona__Types.STARTUP__BOARD_MEMBER  : Default_Data__STARTUP__BOARD_MEMBER     ,
    Schema__Persona__Types.TEAM__APP_SEC          : Default_Data__TEAM__APP_SEC             ,
    Schema__Persona__Types.TEAM__EXTERNAL_COMMS   : Default_Data__TEAM__EXTERNAL_COMMS      ,
    Schema__Persona__Types.TEAM__INCIDENT_RESPONSE: Default_Data__TEAM__INCIDENT_RESPONSE   ,
    Schema__Persona__Types.TEAM__GRC              : Default_Data__TEAM__GRC                 ,
    Schema__Persona__Types.TEST__PERSONA          : Default_Data__TEST__PERSONA
}