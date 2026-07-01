# ADR: Selecting best LLM serving layer to enable AI for all intelligent apps and operations- Amazon Bedrock
 STATUS: Accepted
 DECIDERS: Sahil M - Principal Architect
 DATE: 06-22-2026
 SUPERCEDES:

## 1. Context and Problem Statement:
Our product teams are rapidly spinning up feature prototypes that require LLM access for text summarization, design prototyping and Retrieval augmented generation, and code testing etc. Currently the teams are managing their own API keys to enable this integration. 
This fragmented approach introduces data access and privacy risks, cyber security risks, and increased maintenance and build costs. enabling a single standard layer to serve these models will enable us to deliver cost optimized standard rack to build and maintain these features. to enable speed and minimize risks, we need a standard model serving layer which can be maintained by our Global technology infrastructure and monitoring teams.

## 2. Decision Drivers:
a. Compliance and Data privacy: Customer data must never be used to train models. the platform must provide guarantees for SOC and other compliances.
b. Cost: The platform should provide a way to optimize on cost, enable feature delivery keeping the cost in control.
c. Operational simplicity: platform must be easy to maintain and allow quick feature delivery without feature teams worrying about how the models are maintained.
d. Model Flexibility: Provide for a way to choose model best suited to the usecase. cheaper, smaller for simple tasks and frontier for complex tasks.
e. network security: the traffic must remain within our VPC whenever possible. provide enough cyber controls against new threats like prompt injection etc.

## 3. Options considered: 
1. AWS Bedrock: serverless models.
2. OpenAPI direct integration
3. Deploying OSS models internally
4. Google cloud/Microsoft cloud

## 4. Evaluation of options:
1. AWS Bedrock:
    - Description: A fully managed and serverless AWS service which offers API access to foundational models from providers like Anthropic, OpenAI etc and open source providers like Deepseek, Qwen etc.
    - Pro:
        - Zero infrastructure management cost for Models
        - Platform familiarity and maturity: the teams are already using aws services like ecs etc which makes adoption and maintenance easier.
        - Wide Range of models: Allows integration with a range frontier and OSS models allowing separate priced offerings for each usecase
        - usage based pricing: Simple widely advertized pricing model based on token usage.
    - Cons:
        - Vendor lockin: Deepens our dependence on Amazon and that is against multicloud resiliency options
        - Resiliency: models offering differs in some regions making resiliency difficult.











