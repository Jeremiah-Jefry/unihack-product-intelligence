# Research Sources

> **Status:** Complete  
> **Module:** 1 — Problem & Domain Understanding  
> **Purpose:** Document all external sources consulted during Module 1, categorized by reliability and relevance.

---

## 1. Source Categories

| Category | Reliability | Use in this project |
|----------|------------|-------------------|
| **Primary — Official challenge** | Highest | Defines the problem we must solve |
| **Primary — Company documentation** | High | Defines the business context (Unilog) |
| **Industry standards** | High | Defines product data models and classification |
| **Industry research / Analysis** | Medium-High | Defines real-world challenges and best practices |
| **Vendor documentation** | Medium | Describes existing solutions and approaches |
| **Blog / Opinion** | Lower | Provides context and examples; not authoritative |

---

## 2. Primary Sources — Challenge Definition

### 2.1 Hack2Skill UniHack Challenge

- **URL:** https://hack2skill.com/event/unilog2026
- **What:** Official challenge page for UniHack
- **Key information:** Challenge is an AI innovation hackathon by Unilog x Hack2skill. Participants build prototype solutions for Unilog's content and commerce challenges.
- **Date accessed:** August 2026

### 2.2 LinkedIn Announcement (Hack2skill)

- **URL:** https://www.linkedin.com/posts/hack2skill_unilog-unilogcorp-aihackathon-activity-7488146056929648640-Qi7W
- **What:** Official announcement of UniHack challenge
- **Key information:** "The challenge: turn minimal product information — a manufacturer part number, a brand, one line of description — into rich, structured, commerce-ready product intelligence."
- **Encouraged approaches:** AI agents, multi-agent systems, RAG, knowledge graphs, document intelligence, vision-language models, confidence scoring
- **Timeline:** Registrations & submissions July 29 – August 23, 2026
- **Date published:** August 3, 2026

### 2.3 Resquare LinkedIn Post

- **URL:** https://www.linkedin.com/posts/resquare_hackathon-unihack-unilog-ai-hackathon-2026-activity-7490448157785423872-CLCo
- **What:** Additional details about the challenge
- **Key information:** Prize pool ₹5,00,000. Top performers considered for internships/PPOs at Unilog. Teams of 1-4, fully virtual. IP rights of winning solutions transfer to Unilog.
- **Date published:** August 4, 2026

---

## 3. Primary Sources — Company Context (Unilog)

### 3.1 Unilog Corporate Website

- **URL:** https://www.unilogcorp.com/
- **What:** Unilog's main website describing their products and services
- **Key information:** "AI-Native B2B Product Content and Commerce." CX1 Platform includes PIM, Product Content, eCommerce. 10M+ actively managed SKUs. Over 2,000 manufacturer data feeds. Verticals: HVAC, electrical, plumbing, industrial supply, construction.
- **Date accessed:** August 2026

### 3.2 CX1 Product Content

- **URL:** https://www.unilogcorp.com/platform/product-content/
- **What:** Description of Unilog's product content solution
- **Key information:** "A continuously updated B2B product content subscription that keeps your catalog enriched and current." AI agents inside CX1 Platform. Content sourced from direct relationships with nearly 2,000 manufacturers.
- **Date accessed:** August 2026

### 3.3 CX1 Product Content Services

- **URL:** https://www.unilogcorp.com/platform/product-content/content-services/
- **What:** Custom content creation and enrichment services
- **Key information:** Custom product creation and enrichment to any data standard, taxonomy, or format. Image processing, data standardization, supplier onboarding.
- **Date accessed:** August 2026

### 3.4 CX1 Content Subscription

- **URL:** https://www.unilogcorp.com/platform/product-content/content-subscription/
- **What:** Content subscription service details
- **Key information:** "10M+ enriched products. Over 2,000 manufacturer data feeds." Each enriched product follows consistent taxonomy and data structure. Multiple layers of data: ERP data → manufacturer feeds → manufacturer website → third-party sites.
- **Date accessed:** August 2026

### 3.5 CX1 Sigma Platform

- **URL:** https://www.unilogcorp.com/platform/cx1-sigma/
- **What:** Unilog's newest AI commerce platform
- **Key information:** "First self-composing, self-healing AI commerce platform." Includes Catalog Agents for managing and enriching product data. Merchandising Agents for bundling and cross-sells.
- **Date accessed:** August 2026

### 3.6 Unilog Blog — AI in Workflows

- **URL:** https://www.unilogcorp.com/resources/blog-posts/ai-belongs-in-your-workflows-not-on-your-to-do-list/
- **What:** Unilog's perspective on AI in B2B commerce
- **Key information:** "AI can help enrich and standardize product content faster, but only when paired with strong governance, quality controls, and centralized product data management." Alternate part numbers, manufacturer terminology, industry shorthand are contributors to poor data quality.
- **Date published:** May 22, 2026

---

## 4. Industry Standards — Product Data and Classification

### 4.1 ETIM International — Classification

- **URL:** https://www.etim-international.com/classification/
- **What:** ETIM classification standard for technical products
- **Key information:** ETIM provides a classification model for technical products with uniform structuring, data-entry, and exchange format. Classes with defined features and controlled value lists. Covers electrical, HVAC, building technology. 5,500+ classes.
- **Date accessed:** August 2026

### 4.2 UNSPSC — United Nations Standard Products and Services Code

- **URL:** https://www.undp.org/unspsc
- **What:** Global multi-sector classification standard
- **Key information:** Five-level hierarchical classification. Used for spend analysis, procurement optimization, e-commerce. No attribute model — code only.
- **Date accessed:** August 2026

### 4.3 eCl@ss vs UNSPSC vs ETIM Comparison

- **URL:** https://getclaro.ai/resources/comparisons/etim-vs-unspsc-vs-eclass/
- **What:** Detailed comparison of major classification standards
- **Key information:** ETIM strongest in electrical/HVAC with typed attributes. UNSPSC strongest in procurement/spend analysis, no attributes. eCl@ss strongest in industrial/engineering with deep property dictionary. Most distributors need multiple standards.
- **Date published:** June 10, 2026

### 4.4 GS1 GPC Standards

- **URL:** https://www.gs1.org/standards/gpc/access-gpc-works
- **What:** GS1 Global Product Classification
- **Key information:** Four-level hierarchy (segment, family, class, brick). Designed for GS1 GDSN data synchronization. Consumer goods focus.
- **Date accessed:** August 2026

### 4.5 Product Taxonomy Standards Overview

- **URL:** https://wisepim.com/guides/product-taxonomy
- **What:** Comprehensive comparison of product taxonomy standards
- **Key information:** ETIM 5,500+ categories, 3 levels, strongest in electrical. UNSPSC ~100,000 categories, 4 levels, strongest in procurement. eCl@ss 45,000+ categories, industrial focus. GS1 GPC ~40,000 categories, consumer goods.
- **Date published:** March 4, 2026

### 4.6 Product Classification System Standards

- **URL:** https://www.atropim.com/en/blog/product-classification-system
- **What:** Overview of classification standards for PIM
- **Key information:** ETIM dominant for electrical product data exchange in Europe. eCl@ss broader scope across industrial B2B. UNSPSC used in procurement and supply chain. Many companies need more than one standard.
- **Date accessed:** August 2026

---

## 5. Industry Research — Product Data Challenges

### 5.1 Manufacturing PIM Implementation Challenges

- **URL:** https://www.credencys.com/blog/top-7-manufacturing-pim-implementation-challenges/
- **What:** Analysis of PIM challenges in manufacturing
- **Key information:** Inconsistent attribute names, missing values, duplicate SKUs, conflicting hierarchies. "Bad data in means bad data out." Missing or incomplete specs, outdated information, duplicates across systems.
- **Date published:** November 17, 2025

### 5.2 PIM for Manufacturing (Inriver)

- **URL:** https://www.inriver.com/resources/pim-for-manufacturing/
- **What:** Comprehensive guide to PIM in manufacturing
- **Key information:** "Almost 70% of manufacturers say data quality and integration problems are their biggest obstacle." Product data scattered across ERPs, supplier spreadsheets, shared drives. Product and operational data living across disconnected systems creates compounding errors.
- **Date published:** April 6, 2026

### 5.3 The Expedition: Manufacturer's Guide to Getting Product Data Right

- **URL:** https://www.b2bea.org/insights-advice/the-expedition-a-manufacturers-guide-to-getting-product-data-right
- **What:** Deep analysis of manufacturer data challenges
- **Key information:** Knowledge exists in engineering documentation, CAD files, legacy ERP systems, institutional memory. "None of it was ever organized for external consumption." Before syndicating structured content, you must have structured content to syndicate.
- **Date published:** June 30, 2026

### 5.4 Two Different Problems: Manufacturers vs Distributors

- **URL:** https://www.b2bea.org/insights-advice/two-different-problems-why-the-pim-decision-looks-nothing-alike-for-manufacturers-and-distributors
- **What:** Analysis of distinct challenges for manufacturers vs distributors
- **Key information:** Manufacturer problem = excavation (knowledge exists but isn't structured). Distributor problem = normalization (heterogeneous incoming data from hundreds of suppliers). "Pipe diameter" vs "nominal size" vs "NB" — different terms for same concept.
- **Date published:** June 30, 2026

### 5.5 PIM Challenges: Implementation, Scalability

- **URL:** https://www.atropim.com/en/blog/pim-challenges
- **What:** Common PIM implementation challenges
- **Key information:** "The same product may exist three times with different SKUs, missing dimensions, and conflicting descriptions." 47% of newly created data records contain at least one critical error (citing MIT Sloan). Only 3% of companies' data meets basic quality standards (citing Harvard Business Review).
- **Date published:** April 10, 2026

### 5.6 Product Data Governance

- **URL:** https://www.atropim.com/en/blog/product-data-governing
- **What:** Product data governance for manufacturers and distributors
- **Key information:** "Gartner estimates that poor data quality costs organizations an average of $12.9 million per year." A mid-sized industrial equipment company might manage 50,000 SKUs, each with dozens of technical attributes.
- **Date accessed:** August 2026

---

## 6. Industry Research — AI and Product Data

### 6.1 State of Product Data in MRO & Industrial (2026)

- **URL:** https://www.anglera.com/blog/mro-industrial-state
- **What:** Current state of industrial product data challenges
- **Key information:** "94% [of B2B buyers] used AI somewhere in their most recent purchase process." "54% using AI tools specifically for product research." Manual re-keying runs 30-45 minutes per SKU. Grainger's CEO pointed to "core product and customer information assets" as foundation for AI.
- **Date published:** April 25, 2026

### 6.2 Industrial Distributor Product Data: 7 Patterns

- **URL:** https://startwithdata.co.uk/insight/product-data-industrial-distributors-7-patterns/
- **What:** Common patterns in industrial distributor data problems
- **Key information:** "Every manufacturer ships data in a different format, using different attribute names, different units of measurement, and different interpretations of what a specification means." One distributor had products arriving in "over forty distinct formats." "Attribute coverage varied from complete and accurate through to a part number and a price with nothing else attached."
- **Date published:** June 25, 2026

### 6.3 Building an Attribute Schema for MRO & Industrial

- **URL:** https://www.anglera.com/blog/mro-industrial-attributes
- **What:** Why attribute schema design matters for MRO products
- **Key information:** "A maintenance planner shopping for a replacement pillow block bearing doesn't type 'heavy-duty bearing for tough conditions.' They type a bore diameter, a housing style, and a locking method." "A part can be filed in exactly the right category and still be functionally invisible, because the category node has no opinion on the feature-level fields a buyer filters by."
- **Date published:** April 22, 2026

### 6.4 AI Catalog Enrichment Needs Production Architecture

- **URL:** https://getclaro.ai/resources/articles/ai-catalog-enrichment-production-architecture/
- **What:** Why AI catalog enrichment needs more than a demo pipeline
- **Key information:** "The demo proves that AI can generate enriched product content. The production system decides whether enriched data is accurate, governed, repeatable, cost-effective, and safe enough to write back into the catalog." Three controls: confidence score, provenance to exact evidence, reviewable/reversible write-back.
- **Date published:** July 13, 2026

### 6.5 AI in Service of Data Quality (Claro)

- **URL:** https://getclaro.ai/resources/articles/ai-in-service-of-data-quality/
- **What:** Using AI to improve data quality with governance
- **Key information:** Brickworks used AI agents to recommend missing master-data values, with SMEs validating before application. "Agents proposed missing values, and accountable people approved them." Three controls: confidence score, provenance, reviewable/reversible write-back.
- **Date published:** July 27, 2026

### 6.6 PDF Product Data Enrichment (Trustana)

- **URL:** https://www.trustana.com/resources/blog/pdf-product-data-enrichment-source
- **What:** Using PDFs as product data enrichment source
- **Key information:** "A single PDF page may contain 20 to 30 products. One file may represent hundreds of SKUs." Trustana claims "95 percent or higher accuracy" for PDF attribute extraction. Processing of 100+ product catalogs, 200+ pages per file.
- **Date accessed:** August 2026

### 6.7 Process Data Sheets with AI (Konfuzio)

- **URL:** https://konfuzio.com/en/process-data-sheet-with-ki/
- **What:** AI processing of technical data sheets
- **Key information:** "Countless product series that are sold in various versions, individual measured values, test standards and certifications — all in different documents and layouts." Technical data sheets contain "specifications on material and processing properties as well as test standards."
- **Date published:** April 16, 2026

---

## 7. Industry Research — Data Quality

### 7.1 Product Data Quality: Six Dimensions

- **URL:** https://startwithdata.co.uk/insight/product-data-quality-how-to-measure-it-and-what-good-looks-like/
- **What:** Framework for measuring product data quality
- **Key information:** Six dimensions: Completeness, Accuracy, Consistency, Timeliness, Validity, Channel Readiness. Passing benchmarks: 95% weighted completeness for ecommerce, 97% accuracy on critical attributes, 90% consistency against controlled vocabulary. Example scorecard from 60,000 SKU industrial distributor.
- **Date published:** June 11, 2026

### 7.2 GS1 US National Data Quality Playbook

- **URL:** https://documents.gs1us.org/adobe/assets/deliver/urn%3Aaaid%3Aaem%3A6760371b-06fd-4b68-b278-7629a57d8d7e/GS1-US-National-Data-Quality-Playbook.pdf
- **What:** GS1's framework for product data quality
- **Key information:** Data quality = "consistent, complete, accurate, standards-based, timely data." Data quality = "electronic data exchanged equals physical data." Framework includes data governance, education/training, and attribute audit.
- **Date accessed:** August 2026

### 7.3 Product Data Validation in PIM (AtroPIM)

- **URL:** https://www.atropim.com/en/blog/product-data-validation
- **What:** Comprehensive guide to product data validation
- **Key information:** "47% of newly created data records contain at least one critical error that impacts downstream processes" (citing MIT Sloan). "Only 3% of companies' data meets basic quality standards" (citing Harvard Business Review). Validation layers: format, completeness, channel-specific, cross-field.
- **Date accessed:** August 2026

### 7.4 Product Content Audit for Industrial Catalogs (Claro)

- **URL:** https://getclaro.ai/resources/articles/product-content-audit-industrial-catalogs/
- **What:** Seven-dimension audit framework for industrial catalogs
- **Key information:** Seven dimensions: Product Identity, Classification, Attribute Schema, Completeness, Consistency, Provenance, Activation. "A missing lifestyle image is cosmetic. A missing pressure rating on a pressure component is structural."
- **Date published:** July 13, 2026

### 7.5 Industrial Catalog Readiness Gap (Claro)

- **URL:** https://getclaro.ai/resources/articles/industrial-catalog-readiness-gap-ebook/
- **What:** Why industrial catalogs fail for AI and procurement
- **Key information:** "A human can interpret an image, description, and PDF. A machine needs technical attributes, operating limits, compatibility, certifications, identifiers, and source-backed values." Pre-PIM layer resolves identity, maps categories, extracts values, normalizes terminology, validates results, routes exceptions.
- **Date published:** July 13, 2026

---

## 8. Summary of Key Research Findings

### 8.1 Problem Scale

- Industrial product data is scattered across dozens of systems per manufacturer
- Distributors receive data from hundreds of suppliers in different formats
- Manual re-keying runs 30-45 minutes per SKU
- 70% of manufacturers cite data quality as their biggest obstacle (Deloitte)
- Poor data quality costs $12.9M/year on average (Gartner)

### 8.2 Data Quality Reality

- 47% of new data records contain at least one critical error (MIT Sloan)
- Only 3% of companies' data meets basic quality standards (Harvard Business Review)
- A single distributor may receive products in 40+ distinct formats
- Attribute coverage varies from "complete and accurate" to "part number and price with nothing else"

### 8.3 Market Context

- 94% of B2B buyers used AI in their most recent purchase process (Forrester 2026)
- 54% use AI specifically for product research
- Grainger's CEO credits "core product and customer information assets" as foundation for AI
- AI answer engines pull from whichever source has specs in clean, structured format

### 8.4 Classification Standards

- ETIM: 5,500+ classes, strongest in electrical/HVAC, has typed attributes
- eCl@ss: 45,000+ classes, industrial focus, deep property dictionary
- UNSPSC: ~100,000 codes, procurement focus, no attribute model
- Most distributors need multiple standards simultaneously

### 8.5 AI Enrichment Best Practices

- Production enrichment needs batch architecture, validation, taxonomy fit, and write-back controls
- Three controls separate evidence-backed proposal from faster guessing: confidence score, provenance, reviewable/reversible write-back
- AI should propose; humans should approve
- Identity resolution must happen before enrichment
- Validate values before approval

---

*All sources were accessed in August 2026. URLs should be verified before citing in external communications.*
