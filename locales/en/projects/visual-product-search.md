## Goal

Help staff at home improvement stores (Home Centers) match an unfamiliar screw, nut or washer to verifiable candidates in the manufacturer's product catalog. The difficulty was both distinguishing similar specifications and reducing the number of specialist attributes staff had to enter.

I was responsible for application development and delivery spanning algorithms, frontend, backend and hierarchical account management. I also compared approaches and used a Claude prototype to explore how an agent could simplify in-store queries. In phase one, I developed recognition and matching algorithms and the backend for a product-matching web application. Phase two expanded the APIs, frontend, backend and account management, followed by exploration of interactions between a language model and catalog tools.

Query records also give the manufacturer signals about demand: what users searched for, which specifications they selected and which candidates appeared. Combining those records with sales, inventory and lead times is a potential subsequent use.

## Inputs

Inputs included part photographs, reference objects where measurement was needed, real catalog part numbers and specifications, and attributes selected by users or inferred by a model. Most products lacked photographs, so the approach could not assume a complete product image library.

Shape, dimensions, thread pitch, material and surface treatment have different levels of visual observability. Uncertainty should remain explicit for attributes that a photo cannot reliably establish. Precise dimensional matching requires additional capture conditions, measurement or human verification.

## User flow

In the existing application, users selected attributes and took a guided photograph. The system detected and segmented the part, converted image measurements using a reference object, estimated thread pitch, and combined measurements with catalog specifications to return candidates. Query history and administrative exports supported review and analysis.

To reduce input effort, I tested another interaction through a Claude Skill: the model inferred attributes from a photo, requested additional views when necessary, called Python tools to filter a CSV catalog, and presented the top three candidates with explanations. If no candidates matched, it could adjust filters and query again.

This was a demonstration prototype. Model API integration was staged after customer approval. Vector retrieval over specification text was a separate design option, distinct from the demonstrated CSV tool workflow.

## Outputs

Algorithm work included detection and segmentation experiments, PCA-based in-plane alignment, reference-based scale conversion, DFT-based thread-pitch estimation and specification matching. Engineering deliverables included the product-matching web application, a FastAPI/PostgreSQL backend, APIs, frontend pages, hierarchical account management, query history and exports for store staff and manufacturer administrators.

The model-related work produced a Claude Skill prototype and code for attribute message construction, enum validation and handling low-confidence fields. The model handled visual semantics and interaction; catalog tools supplied product records; measurement and user verification supplied precise specifications.

## Scope

Candidate recommendations assist lookup; a photograph cannot always uniquely identify a part. PCA only corrects in-plane orientation. Reference-based measurement remains sensitive to perspective, resolution and relative position. A relative matching score is not a probability that a purchase is correct.

Results on controlled samples do not establish in-store performance across an expanded catalog. The Skill demonstration was not a production web agent, and queries are not purchases. Supply-chain analysis remains a direction for further work with query data, without quantified supply-chain benefits to date.

## Acceptance criteria

Validation requires fixed catalog versions, test images and reference products. Checks should separately cover measurement error, candidate hits, input effort and completion time, and handling of no-match results and poor images. Engineering checks should confirm query permissions, history and traceability.

## Iteration

I first reduced “identify every part” to “find verifiable candidates,” using catalog retrieval and geometry for the parts that could be established reliably. When customer feedback highlighted interaction complexity, I reframed the question around reducing manual attribute selection and used a Skill to test the division of work between model and tools. Working backward from real part numbers and result verification shaped interfaces, data and capture requirements. Effective components could then become reusable attribute schemas, tools and evaluation methods.
