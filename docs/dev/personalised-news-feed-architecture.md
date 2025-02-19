# The Cyber Boardroom: Personalised News Feed Architecture

The modern cybersecurity landscape presents a unique challenge for board members and executives who must make critical decisions while processing an overwhelming volume of technical information. The Cyber Boardroom platform addresses this challenge through its innovative personalized news feed architecture, which transforms complex cybersecurity news into actionable insights tailored to each stakeholder's needs and expertise.

This technical documentation outlines the sophisticated system architecture that powers The Cyber Boardroom's personalized news feed. At its core, the system combines advanced RSS feed processing, knowledge graph generation, and multi-model Language Learning Model (LLM) orchestration to create a scalable, provider-agnostic platform. The architecture emphasizes both performance and flexibility, while maintaining deployment options across cloud and air-gapped environments.

The system's differentiation lies in its ability to maintain technical accuracy while adapting content presentation to each user's context and persona. Rather than simply simplifying complex information, the platform leverages sophisticated personalization workflows to translate cybersecurity concepts into relevant business frameworks, enabling more effective decision-making at the board level.

## System Architecture

### Data Collection Layer

The Data Collection Layer represents the foundation of the news feed system, implementing a sophisticated approach to gathering, processing, and storing cybersecurity news content. This layer emphasizes scalability, efficiency, and data integrity through its provider-agnostic architecture and robust processing pipeline.

#### RSS Feed Processing

The RSS feed processing component implements a scalable approach to collecting cybersecurity news from multiple sources while maintaining strict control over resource utilization and data integrity.

##### Feed Collection Strategy
This system provides the [MyFeeds.ai](https://github.com/the-cyber-boardroom/myfeeds_ai) service (cyber.myfeeds.ai) which is response for managing the RSS feed collection and implementing several key optimizations:

- Single Request Pattern: Only one request per hour is made to each source, minimizing load on source servers and reducing bandwidth consumption
- Standardized Metadata: Extracts and normalizes metadata fields including categories, authors, and publication dates
- Error Resilience: Implements robust error handling and retry mechanisms for intermittent feed availability issues
- Rate Limiting: Enforces configurable rate limits to prevent overwhelming source servers
- Content Validation: Verifies feed integrity and content structure before processing

##### Storage Architecture
The system implements a time-based hierarchical storage structure in S3, optimizing for both write performance and read access patterns:

```
root/
├── {source_name}/                     # Separate namespace for each feed source
│   ├── latest/                        # Quick access to current content
│   │   ├── feed.xml                   # Most recent RSS feed
│   │   ├── feed.json                  # JSON-transformed feed
│   │   └── articles/                  # Current articles semantic graphs
│   └── {year}/                        # Historical archive
│       ├── {month}/                   # Monthly grouping
│       │   ├── {day}/                 # Daily grouping
│       │   │   ├── {hour}/            # Hourly snapshots
│       │   │   │   ├── raw_rss.xml    # Original feed
│       │   │   │   ├── rss_json.json  # Transformed feed
│       │   │   │   └── articles/      # Individual articles and semantic graphs
```

This structure provides several advantages:
- Efficient temporal navigation of content
- Quick access to latest information through dedicated latest folder
- Clear separation between current and historical content
- Natural partitioning for backup and retention policies
- Optimized for both write-heavy collection and read-heavy consumption patterns

#### Data Transformation Pipeline

The transformation pipeline represents a critical component in the Cyber Boardroom's news processing architecture, converting raw RSS feeds into structured, queryable data formats. This pipeline implements a multi-stage approach that preserves data provenance while optimizing for downstream processing efficiency. Each stage of the pipeline maintains strict validation controls to ensure data integrity, while the overall design emphasizes scalability and maintainability.

The pipeline's architecture reflects the platform's commitment to data quality and traceability. By implementing a series of discrete transformation stages, the system can maintain detailed audit trails of all modifications while enabling efficient error recovery and data verification at each step. This approach also facilitates parallel processing capabilities, allowing the platform to handle increased load by distributing transformation tasks across multiple processing nodes.

##### XML Processing 

The XML processing stage serves as the foundation of the transformation pipeline, handling the critical conversion of RSS XML into structured JSON format. This stage implements sophisticated parsing logic that accommodates the various RSS specifications and vendor-specific extensions commonly found in cybersecurity news feeds.

At its core, the XML processor maintains strict compliance with RSS standards while providing flexible handling for non-standard elements. This balance ensures reliable processing of feeds from diverse sources while preserving valuable metadata that might exist in custom extensions.

Key capabilities include:

- Feed Format Standardization: Implements comprehensive normalization of RSS feeds across multiple versions and specifications
- Content Validation: Enforces strict data quality controls throughout the transformation process

##### JSON Enhancement

The JSON enhancement stage builds upon the basic XML-to-JSON conversion by implementing sophisticated data enrichment processes. This stage transforms raw JSON structures into rich, contextually-aware representations that support the platform's advanced analysis and personalization capabilities.

Primary enhancement functions include:

- Content Load: Imports basic RSS data with additional semantic context  
- Reference Management: Establishes and maintains content relationships across feeds
- Resource Standardization: Normalizes various resource identifiers and references
- Temporal Processing: Standardizes temporal information across multiple formats


##### Article Processing

The article processing stage represents the core transformation layer where individual news items are converted into platform-native formats. This stage implements sophisticated processing logic that ensures consistent identification, type safety, and efficient data representation across the entire platform. 

Key processing components include:

- **Unique Identification System**: Implements a identification strategy using the UID3 algorithm that ensures consistent and reliable article tracking across the platform
  - Generates deterministic identifiers based on article URLs, ensuring stable references even when content is updated
  - Maintains identifier stability through content updates and modifications
  - Creates traceable relationships between different versions of the same content

- **Type-Safe Content Handling**: Leverages the [OSBot Utils](https://github.com/owasp-sbot/OSBot-Utils) [Type_Safe](https://github.com/owasp-sbot/OSBot-Utils/blob/dev/docs/code/osbot_utils/type_safe/Type_Safe.py.md) framework to implement robust data processing with strict type checking
  - Enforces strong typing across all article attributes, preventing type-related errors during processing
  - Implements automatic validation of required fields with clear error reporting
  - Provides safe conversion between different data representations
  - Maintains type consistency through all processing stages
  - Enables compile-time and runtime type checking for early error detection

- **Object Serialization Framework**: Creates efficient Python representations of articles optimized for both storage and runtime access
  - Implements intuitive object navigation through properties (e.g., accessing article titles via RSS_feed.articles.title)
  - Creates memory-efficient storage structures that minimize resource usage
  - Optimizes common access patterns through intelligent caching
  - Maintains bidirectional compatibility between storage and runtime formats
  - Provides streaming capabilities for large content handling

The article processing stage also implements sophisticated caching strategies that optimize performance while maintaining data consistency. By carefully managing the lifecycle of processed articles, the system can efficiently handle large volumes of content while ensuring that downstream components always have access to the latest verified data.

This stage's output serves as the foundation for subsequent processing phases, including semantic analysis and personalization. The careful attention to data integrity and type safety at this stage significantly reduces the complexity of downstream processing while enabling more sophisticated content analysis and transformation capabilities.


### Knowledge Graph Layer

The Knowledge Graph Layer implements a provider-agnostic LLM architecture that transforms raw article content into rich, semantic knowledge representations. Following the platform's ["LLMs as a Commodity"](https://github.com/the-cyber-boardroom/cbr-investment/blob/dev/docs/strategy/llms-as-a-commodity-strategy.md) strategy, this layer leverages multiple language models through a sophisticated orchestration layer, treating the LLMs themselves as interchangeable components while creating value through advanced prompt engineering and knowledge integration.

The layer's architecture enables seamless switching between different LLM providers (including OpenAI, Anthropic, Google, and open-source models) while maintaining consistent semantic interpretation. This provider-independent approach ensures reliable operation even in air-gapped environments, where locally hosted models can provide complete functionality without compromising security.

#### Semantic Processing

The semantic processing component implements a multi-stage LLM pipeline that extracts, validates, and integrates knowledge from cybersecurity news content. Each stage leverages specific LLM capabilities through carefully crafted prompts, with the orchestration layer selecting optimal models based on task requirements and performance characteristics.

The system's prompt engineering framework combines ontological knowledge with query-specific requirements, enabling precise control over LLM outputs while maintaining semantic consistency. This approach ensures reliable knowledge extraction regardless of the underlying model, creating a robust foundation for the platform's knowledge management capabilities.

Key semantic capabilities include:

- **LLM-Powered Graph Generation**: Implements sophisticated prompt engineering for knowledge extraction
  - Constructs detailed prompts combining article content and platform ontology
  - Leverages multiple LLMs for cross-validation of extracted knowledge
  - Maintains clear provenance between source text and LLM outputs
  - Implements parallel model operations for critical validations
  - Optimizes model selection based on task requirements

- **Multi-Model Knowledge Integration**: Creates consistent semantic representations across different LLMs
  - Implements provider-agnostic knowledge representation
  - Handles model-specific output variations
  - Maintains semantic consistency across different providers
  - Enables seamless provider switching
  - Supports both cloud and local model deployment

- **Graph Hierarchy Creation**: Uses LLMs to generate and maintain multiple knowledge views
  - **Article-Level Analysis**: 
    - Extracts semantic graphs using targeted LLM queries
    - Validates extracted relationships through cross-model verification
    - Maps content to standardized cybersecurity concepts
    - Maintains source traceability

  - **Temporal Integration**:
    - Hour-Level Aggregation: Combines recent articles through LLM-powered graph merging
    - Daily/Monthly Summaries: Creates temporal views through semantic consolidation
    - Latest News Synthesis: Maintains current state through continuous LLM processing
    - Historical Context: Preserves temporal relationships while updating knowledge

  - **Knowledge Synthesis**:
    - Implements LLM-based graph merging strategies
    - Resolves conflicts through multi-model validation
    - Creates unified views while preserving source context
    - Maintains confidence scoring for merged knowledge

The Knowledge Graph Layer's design reflects the platform's strategic approach to LLM utilization, creating value through sophisticated orchestration and integration rather than model development. By treating LLMs as commodity components, the system can leverage continued improvements in model capabilities while focusing on higher-order value creation through knowledge management and semantic integration.

#### Graph Storage Strategy

The Graph Storage Strategy implements a sophisticated time-based hierarchy that optimizes both write performance and read access patterns. This approach leverages the platform's serverless architecture to create a highly efficient storage system that scales seamlessly while maintaining fast access to both current and historical knowledge graphs.

The storage architecture is designed around the concept of pre-computed query patterns, where commonly requested views are automatically maintained and updated. This strategy creates a one-time computation cost during content ingestion while enabling near-instantaneous access for subsequent queries, reflecting the platform's emphasis on performance optimization and resource efficiency.

Key storage capabilities include:

- **Time-Based Hierarchy**: Implements an intelligent storage structure that mirrors content chronology
  ```
  root/
  ├── {source_name}/          
  │   ├── latest/                                           # folder with latest content
  │   │   └── articles.mgraph.json                          # current feed's articles semantic mgraph
  │   └── {year}/                                           # year 's data
  │       ├── {month}/                                      # month's data
  │       │   ├── {day}/                                    # day  's data
  │       │   │   ├── {hour}/                               # hour 's data
  │       │   │   │   ├── {article_id}                      # article's data
  │       │   │   │   │   ├── article.json                  # article's content
  │       │   │   │   │   └── article.mgraph.json           # article's semantic mgraph       
  │       │   │   │   └── articles.mgraph.json              # hour   's articles semantic mgraph      
  │       │   │   └── articles.mgraph.json                  # day    's articles semantic mgraph    
  │       │   └── articles.mgraph.json                      # month  's articles semantic mgraph    
  │       └── articles.mgraph.json                          # year   's articles semantic mgraph    
  ```

- **Change Set Management**: Creates efficient update mechanisms for evolving knowledge
  - Tracks article additions and removals from RSS feeds
  - Maintains change history through graph versioning
  - Propagates updates across temporal aggregations
  - Preserves historical versions for audit trails

- **Graph Serialization**: Implements the [Mgraph-AI](https://github.com/owasp-sbot/MGraph-AI) package for efficient graph storage
  - Stores semantic graphs in JSON-based format
  - Maintains node and edge relationships
  - Preserves graph metadata and provenance
  - Enables efficient graph merging operations

- **Access Optimization**: Creates multiple access paths for different query patterns
  - Latest Content Access: Sub-25ms response times for current data
  - Historical Queries: Efficient temporal navigation
  - Cross-Source Integration: Fast multi-feed analysis
  - Trend Analysis: Pre-computed temporal views

The storage strategy is tightly integrated with cloud storage (Localstack or S3) native capabilities, exposing files through direct URLs for optimal access performance. This approach enables response times in the 15-25ms range for common queries while maintaining the ability to process more complex historical analyses efficiently.

This architecture supports both cloud and air-gapped deployments through its environment-agnostic design. Whether running in AWS S3, local storage, or custom object stores, the system maintains consistent performance characteristics while adhering to deployment-specific security requirements.

Air-gapped environments will require an extra step to collect the RSS xml feeds and expose them in a location avaible to the data transformation pipeline



### Content Delivery Architecture

The Content Delivery Architecture implements an API-first approach that enables efficient access to the platform's knowledge graphs and processed content. 

By implementing a clear separation between storage and delivery layers, the system achieves remarkable performance characteristics while maintaining the ability to scale dynamically based on demand.

#### Fast API Integration

The Fast API integration layer serves as the primary interface for content access, implementing a comprehensive set of endpoints that expose the platform's capabilities through a clean, performant API. This implementation emphasizes both speed and flexibility, enabling rapid content delivery while maintaining the ability to support complex queries and aggregations.

Key architectural components include:

- **API Endpoint Structure**: Implements a comprehensive RESTful interface
  - Content Access: Direct routes to processed articles and knowledge graphs
  - Temporal Navigation: Endpoints for accessing historical content
  - Graph Operations: Interfaces for knowledge graph queries and updates
  - Health Monitoring: System status and performance metrics
  - Provider Management: LLM configuration and orchestration

- **Performance Optimization**: Creates efficient content delivery paths
  - Direct S3 Integration: Bypasses API server for static content
    ```
    https://{bucket}.s3.{region}.amazonaws.com/
    └── public_data/
        └── {source}/
            └── latest/
                └── article.mgraph.json
    ```
- **Response Time Targets**:
    - 10-30ms for latest content, historical and pre-calculated graphs    
    - 100-200ms for fast api calls



#### Personalization Engine

The Personalization Engine represents a core differentiator of the Cyber Boardroom platform, implementing sophisticated personalization capabilities that bridge the gap between technical cybersecurity content and business stakeholder needs. By leveraging multiple LLMs and advanced knowledge graph processing, the engine creates highly targeted content adaptations while maintaining clear provenance and accuracy.

This engine's architecture reflects the platform's understanding that board members and other stakeholders are highly intelligent and experienced but may lack deep cybersecurity or technical knowledge. 

Rather than simplifying content, the engine focuses on translation and context adaptation, enabling stakeholders to engage with cybersecurity concepts through familiar business frameworks and personal preferences.

##### User Context Integration

The user context integration component implements a comprehensive approach to understanding stakeholder needs and preferences. This goes beyond basic profile information to create a rich understanding of how each user prefers to consume and interact with cybersecurity information.

Key integration capabilities include:

- **Personal Preference Management**: Creates detailed user context profiles
  - **Communication Style Preferences**: Formal, direct, or narrative approaches
  - **Content Depth Requirements**: Level of technical detail desired
  - **Visual vs. Textual Learning**: Preferred information presentation formats
  - **Update Frequency**: Timing and cadence of information delivery

- **Professional Context Mapping**: Understands user's business role and responsibilities
  - **Technical Background**: Current knowledge level and expertise areas
  - **Industry Experience**: Sector-specific understanding and requirements
  - **Decision-Making Role**: Board position and oversight responsibilities
  - **Regulatory Context**: Compliance and governance obligations

- **Resource Optimization**: Aligns content delivery with user constraints
  - **Time Availability**: Adapts content length and detail to user schedule
  - **Priority Management**: Focuses on most relevant information
  - **Meeting Preparation**: Provides context for upcoming decisions
  - **Follow-up Requirements**: Tracks needed actions and updates

##### Content Customization

The content customization component leverages the platform's multi-model LLM architecture to create highly personalized information presentations. This component implements sophisticated prompt engineering that combines user context with cybersecurity content to generate relevant, actionable insights.

Key customization capabilities include:

- **LLM-Powered Adaptation**: Creates personalized content representations
  - **Multi-Model Processing**: Leverages different LLMs for specific aspects of content adaptation
  - **Cultural Intelligence**: Adapts content to user's cultural context
  - **Language Customization**: Supports multiple languages and communication styles
  - **Business Context Integration**: Maps technical concepts to business implications

- **Context-Aware Processing**: Generates relevant summaries and insights
  - **Dynamic Depth Adjustment**: Varies detail based on user needs
  - **Technology Stack Relevance**: Focuses on applicable technologies
  - **Impact Assessment**: Evaluates business implications
  - **Action Item Generation**: Creates specific, actionable recommendations

- **Intelligent Filtering**: Implements sophisticated content prioritization
  - **Relevance Scoring**: Evaluates content importance for each user
  - **Urgency Assessment**: Identifies time-critical information
  - **Duplicate Detection**: Consolidates related content
  - **Thread Tracking**: Maintains narrative continuity across updates

The Personalization Engine's architecture ensures that each user receives a truly customized experience while maintaining the integrity and accuracy of the underlying cybersecurity information. 

This approach enables effective communication across different roles and expertise levels, supporting better cybersecurity decisions through improved understanding and engagement.

## End-to-End Workflow

The End-to-End Workflow demonstrates how The Cyber Boardroom's news feed system implements its architectural principles in practice, creating a seamless pipeline from initial data collection through to personalized content delivery. 

Each stage in the workflow is designed to maintain data integrity while optimizing for both performance and scalability. 

The system leverages the platform's serverless architecture to process cybersecurity news content through a series of discrete, well-defined stages, each building upon the previous stage's output while maintaining clear provenance and enabling efficient error recovery. 

This modular approach ensures reliable operation at scale while facilitating continuous enhancement of individual components.

### 1. RSS Feed Collection

The RSS Feed Collection stage forms the foundation of the platform's data ingestion pipeline, implementing a highly efficient approach to gathering cybersecurity news content at scale. By leveraging the [MyFeeds.ai](https://github.com/the-cyber-boardroom/myfeeds_ai) service architecture, the system maintains consistent data collection while minimizing resource usage and respecting source server limitations. This stage emphasizes reliability and scalability, ensuring a steady flow of current cybersecurity information while maintaining clear provenance and temporal organization.


- [MyFeeds.ai](https://github.com/the-cyber-boardroom/myfeeds_ai) service fetches RSS feeds hourly from cybersecurity news sources
- Raw RSS XML files are stored in S3 buckets using time-based hierarchy
- Only one request per hour is made to each source for scalability
- Files are stored in the format: `{source_name}/{year}/{month}/{day}/{hour}/`

### 2. Initial Processing

The Initial Processing stage transforms raw RSS data into structured, analyzable formats while preserving all original content and metadata. This critical transformation phase leverages the [OSBot Utils](https://github.com/owasp-sbot/OSBot-Utils) API's robust XML processing capabilities to ensure reliable conversion while maintaining strict data integrity. The two-stage approach enables both standardized processing and RSS-specific optimizations, creating a solid foundation for subsequent semantic analysis and knowledge graph generation.

- XML files are converted to JSON format using [OSBot Utils](https://github.com/owasp-sbot/OSBot-Utils) XML/JSON parsing APIs
- Two-stage conversion process:
  1. Pure XML to JSON transformation
  2. RSS-specific JSON conversion considering XML semantics
- Resulting JSON files are stored alongside original XML

### 3. Article Extraction

The Article Extraction stage implements a sophisticated approach to content isolation and management, transforming processed RSS data into discrete, trackable content units. This stage is critical for establishing reliable content tracking and enabling efficient downstream processing. By implementing strong typing and unique identification through the OSBot Utils framework, the system ensures consistent handling of article content while maintaining the relationships and context necessary for knowledge graph generation and personalization.

- Unique IDs are generated for each article using UID3
- [Type_Safe](https://github.com/owasp-sbot/OSBot-Utils/blob/dev/docs/code/osbot_utils/type_safe/Type_Safe.py.md) classes from [OSBot Utils](https://github.com/owasp-sbot/OSBot-Utils) handle strong typing
- Articles are serialized into individual JSON files
- Storage structure preserves article relationships and metadata

### 4. Change Detection

The Change Detection stage represents a critical component in maintaining the platform's knowledge graph accuracy and temporal coherence. By implementing a graph-based tracking system, this stage efficiently manages content evolution while minimizing storage redundancy and computational overhead. The stage's sophisticated change detection process ensures that the platform's knowledge representation remains current and accurate while maintaining a complete historical record of content evolution.

- System maintains change sets through graph-based tracking
- Articles are stored only in the hour they first appear
- Change detection process:
  1. Load article ID graph from latest folder
  2. Compare with new RSS feed
  3. Identify new articles for processing
  4. Track removed articles
  5. Update all relevant graph files

### 5. Semantic Graph Creation

The Semantic Graph Creation stage implements the platform's "LLMs as a Commodity" strategy, leveraging multiple language models to transform processed articles into rich knowledge representations. This stage exemplifies the platform's sophisticated approach to LLM orchestration, where different models are selected based on their specific strengths in semantic analysis and knowledge extraction. By creating hierarchical graph structures at multiple temporal levels, the system enables both immediate access to current insights and deep historical analysis while maintaining clear provenance throughout the knowledge graph.

- LLMs process article content with platform ontology
- Creates semantic knowledge graphs at multiple levels:
  - Individual article graphs
  - Hour/day/month/year consolidated graphs
  - Latest news composite graph
- All graphs maintain source location references

### 6. Fast API Integration

The Fast API Integration stage provides the critical interface layer between the platform's rich knowledge graphs and its various consumption patterns. Following the platform's API-first architecture principles, this stage implements high-performance access patterns that leverage the serverless infrastructure's capabilities while maintaining consistent response times below 25ms for common queries. The design emphasizes direct Cloud Storage (like S3) integration and optimized file access patterns, enabling efficient content delivery across both cloud and air-gapped deployments.

- All functionality exposed through Fast API endpoints
- Direct Cloud Storage file access for optimized delivery
- Latest folder provides quick access to current content

### 7. Cyber Boardroom Integration

The Cyber Boardroom Integration stage represents the culmination of the platform's news feed processing pipeline, where raw cybersecurity content is transformed into personalized, actionable insights. 

This stage leverages the platform's multi-model LLM architecture and sophisticated knowledge graph capabilities to create truly personalized experiences for each user. 

By implementing a comprehensive GraphRAG (Retrieval Augmented Generation) process that combines semantic graphs with rich user context, the system generates content that precisely matches each stakeholder's needs while maintaining the accuracy and provenance of the underlying cybersecurity information. 

This integration demonstrates the platform's core value proposition: transforming complex technical information into business-relevant insights without sacrificing technical accuracy or depth.

1. The Cyber Boardroom Odin bot/agent retrieves semantic graphs
2. User context is integrated:
   - Personal preferences
   - Role requirements
   - Technical background
   - Time availability
3. LLM query combines:
   - Semantic graph
   - User persona
   - Relevant technologies
   - Business context
4. Graph RAG process:
   - Creates knowledge graph of relevant information
   - Retrieves source materials
   - Generates personalized content
5. Quality control LLM verifies output
6. Results show to user
7. Results are saved in user's graph for historical tracking

## Conclusion

The Cyber Boardroom's personalized news feed architecture represents a significant advancement in bridging the gap between technical cybersecurity information and board-level decision-making. 

Through its sophisticated implementation of RSS processing, knowledge graph generation, and LLM orchestration, the system delivers highly personalized content while maintaining strict standards for accuracy and provenance.

Several key innovations distinguish this architecture:

1. The **provider-agnostic LLM approach** treats language models as commodity components, creating value through sophisticated orchestration rather than model development.

2. The **time-based hierarchical storage strategy** optimizes both write performance and read access patterns, enabling sub-25ms response times for common queries.

3. The **personalization engine leverages multiple LLMs** and advanced knowledge graph processing to create targeted content adaptations while maintaining clear provenance.

4. The **deployment-flexible architecture** supports both cloud and air-gapped environments without compromising performance or security.

As cybersecurity continues to demand greater board-level attention, The Cyber Boardroom's architecture provides a scalable foundation for transforming technical information into actionable insights. 

This system demonstrates how sophisticated technical architecture can directly support better business decision-making by making complex cybersecurity information more accessible and actionable for board members and executives.
