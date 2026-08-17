You are the lead product-research and systems-analysis agent for an individual submission to the Hack2Skill UniHack challenge:

**“AI-Powered Product Intelligence for Industrial Commerce.”**

Your job in this task is **MODULE 1 ONLY: PROBLEM AND DOMAIN UNDERSTANDING**.

You are NOT being asked to build the application yet.

You must act as a senior AI product architect, industrial-data analyst, and hackathon evaluator simultaneously.

## CHALLENGE

Industrial manufacturers manage large amounts of product information across:

* company websites
* product pages
* PDF datasheets
* technical manuals
* catalogs
* specification sheets
* images
* diagrams
* tables
* digital assets
* other fragmented product sources

Transforming this fragmented and often incomplete information into accurate, structured, consistent, validated, and commerce-ready product intelligence is difficult and time-consuming.

The challenge asks participants to build an AI-powered solution that can automate:

1. creation of product intelligence from limited product information
2. enrichment of product information
3. validation of product information

The challenge specifically encourages approaches including:

* AI agents
* RAG
* knowledge graphs
* document intelligence
* vision-language models
* human-in-the-loop workflows

Expected outcomes include:

* generate structured product intelligence from limited inputs
* improve product data quality and consistency
* validate and enrich information with traceable outputs
* scale efficiently across large product catalogs

## PRIMARY OBJECTIVE

Do deep analysis and produce a **technology-independent problem specification** that will become the foundation for every later module.

Do NOT jump to implementation.

Do NOT decide that RAG, agents, vector databases, knowledge graphs, or any other technology must be used unless the analysis proves that they are necessary.

We are building this as a serious real-world AI product, not a superficial “LLM generates JSON” demo.

## RESEARCH RULES

Research the problem thoroughly using reliable sources available to you.

Prioritize:

1. official Hack2Skill challenge information
2. manufacturer/product-data documentation
3. industrial/e-commerce product-information standards
4. authoritative technical documentation
5. credible industry research
6. established commerce/product-information terminology

Do not invent facts.

Separate:

* verified facts
* reasonable assumptions
* proposed design decisions

Cite important external claims.

Do not spend time researching unrelated AI technologies yet.

## QUESTIONS YOU MUST ANSWER

### 1. What exactly is “Product Intelligence”?

Define it specifically for this challenge.

Do not give a generic AI definition.

Explain what information belongs inside an industrial product intelligence record.

Break it into categories such as, where appropriate:

* identity
* classification
* technical specifications
* physical attributes
* materials
* dimensions
* performance
* operating conditions
* applications
* compatibility
* certifications
* safety
* commercial attributes
* media/digital assets
* relationships to other products
* provenance/evidence
* quality/confidence information

Do not assume these exact categories are final. Determine the correct model from research.

### 2. Who are the users?

Identify realistic actors in the ecosystem.

For example, consider:

* manufacturer/product-data teams
* catalog managers
* technical teams
* e-commerce teams
* distributors
* procurement teams
* reviewers/approvers

For each user, identify:

* what information they have
* what they need
* what is painful today
* what errors are costly
* what they expect from our system

### 3. What goes into the system?

Define realistic input scenarios.

Include:

* complete inputs
* incomplete inputs
* conflicting inputs
* messy PDFs
* scanned PDFs
* images
* tables
* diagrams
* website information
* partial specifications
* duplicate information
* inconsistent units
* inconsistent terminology

Identify the minimum viable input required for the system to produce useful output.

### 4. What must come out?

Define the ideal output.

Describe both:

A. the machine-readable structured product representation

B. the human-facing product intelligence/review experience

The output must be more than a JSON object.

Explain what makes an output:

* structured
* useful
* trustworthy
* commerce-ready
* traceable

### 5. What does “limited product information” actually mean?

Analyze this phrase carefully.

Give concrete examples of:

* extremely limited input
* partially sufficient input
* rich input

Explain what the system may safely infer, enrich, normalize, retrieve, or propose in each situation.

Clearly distinguish:

**FACT**
directly supported by evidence

**NORMALIZED FACT**
same fact expressed in a standardized representation

**DERIVED VALUE**
computed from known evidence

**ENRICHED VALUE**
obtained from additional trustworthy sources

**INFERENCE**
AI-generated interpretation that is not directly established

This distinction is extremely important for later validation.

### 6. What can go wrong?

Build a detailed failure taxonomy.

Include:

* hallucination
* incorrect extraction
* table-reading errors
* OCR errors
* unit conversion errors
* conflicting sources
* outdated information
* duplicate products
* wrong product/model association
* missing fields
* ambiguous terminology
* unsupported enrichment
* false confidence
* incorrect categorization
* incorrect relationships

Explain the consequences of each.

### 7. What does “validation” mean?

Do NOT interpret validation as simply asking an LLM:

“Is this correct?”

Define a serious validation framework.

Consider:

* schema validation
* type validation
* unit validation
* range validation
* cross-field consistency
* source verification
* cross-source agreement
* contradiction detection
* freshness
* provenance
* confidence
* human review

Identify which validations can be automated and which may require human approval.

### 8. What does “traceable output” mean?

Define exactly what evidence should be attached to a generated product attribute.

For example, investigate concepts such as:

* source document
* source URL
* page
* section
* table
* extracted passage
* image region
* timestamp
* transformation performed
* confidence
* validation state

Do not finalize the schema yet, but identify the required provenance concepts.

### 9. What does “commerce-ready” mean?

Define the characteristics of a product record that is genuinely ready for downstream commerce/catalog usage.

Distinguish:

* technical completeness
* content completeness
* consistency
* discoverability
* standardization
* trustworthiness
* approval status

Do not equate “commerce-ready” with “good marketing copy.”

### 10. What does scale mean?

Interpret “scale across large product catalogs.”

Identify the dimensions of scale:

* number of products
* number of source documents
* document size
* multimodal inputs
* processing throughput
* latency
* storage
* retrieval
* model cost
* reprocessing
* updates
* human review workload

Do not design the scalable architecture yet. Just define the requirements it will eventually need to satisfy.

## COMPETITIVE / NOVELTY ANALYSIS

Study the obvious naive approaches:

1. simple LLM extraction
2. PDF → JSON
3. basic RAG chatbot
4. generic AI agent
5. OCR + LLM
6. vector search + LLM

Explain why each is insufficient for this challenge.

Then identify opportunities for a genuinely stronger solution.

Focus on the problem and differentiators, not technology hype.

## CREATE A REQUIREMENTS MATRIX

Produce a table containing:

Requirement
Why it matters
Input
Expected behavior
Failure risk
Validation need
Priority

Classify each requirement as:

* P0 — absolutely required
* P1 — important
* P2 — enhancement

## DEFINE SUCCESS

Propose measurable evaluation dimensions.

At minimum investigate:

* extraction accuracy
* completeness
* consistency
* validation accuracy
* contradiction detection
* evidence coverage
* unsupported-claim rate
* hallucination rate
* human-review rate
* processing time
* cost per product
* scalability

Do not invent fake benchmark numbers.

Instead define what should be measured and later establish targets.

## PRODUCE AN “OUT OF SCOPE FOR NOW” SECTION

Explicitly list things we should NOT build in Module 1.

This prevents premature engineering.

## FINAL DELIVERABLES

Create the following files in the repository:

`docs/module-01-problem-definition.md`

`docs/domain-model.md`

`docs/requirements.md`

`docs/risks-and-failure-modes.md`

`docs/evaluation-framework.md`

Also create:

`docs/research-sources.md`

The files must be consistent with one another.

Do not duplicate large sections unnecessarily.

## QUALITY BAR

The result must be good enough that another senior engineer could read these documents and design the architecture without misunderstanding the business problem.

The result must also be understandable by me as a beginner working on this project.

For every major technical concept, explain:

**what it means → why it matters → example → implication for our product**

Avoid unnecessary jargon.

## CRITICAL CONSTRAINTS

* Do not write application code.
* Do not select the final tech stack.
* Do not create the final architecture.
* Do not prematurely introduce frameworks.
* Do not fabricate benchmark results.
* Do not claim something is solved merely because an LLM can generate an answer.
* Do not treat generated information as factual unless evidence supports it.
* Do not hide uncertainty.
* Do not optimize for buzzwords.
* Optimize for correctness, explainability, reliability, and eventual scalability.

## WORKING METHOD

Before writing the final documents:

1. inspect the repository
2. inspect `AGENTS.md`
3. research the challenge and domain
4. reason through the problem
5. identify contradictions or ambiguities in the challenge
6. formulate the problem model
7. write the documents
8. cross-check all documents for consistency
9. perform a final quality review

At the end, provide:

### MODULE 1 COMPLETION REPORT

Include:

* what was established
* major insights
* major assumptions
* unresolved questions
* risks discovered
* what Module 2 should address
* files created
* sources used

Most importantly:

**Do not start Module 2.**

Stop after Module 1 and wait for further orchestration instructions.
