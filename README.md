# Python vs. Typescript Competitive Code Improvement Agents

Idea: Generative Adversarial Coding Agents for fun and profit (and to win a hackathon today!)
Core: Setup two agents (or two multi-agent flows) that write matching code in another language, then improve it such that it runs better and is more readable than the others'. One is Typescript, one is Python

## Potential Practical Value of the Project:
1. Solve polyglot AI development ecosystem in a creative way
2. Better code in both
3. Fun to watch the coding battles
4. See which can be optimized maximally in different vectors

## Hackathon Requirements:
1. Multi-agent: At least two agents
2. Multi-modal: At least 2 modes of agents (text + image)

## Draft Ideas

### Multi-modal possibilities:
1. Interpretive art about the code & evaluation
2. Score card?
3. Code shaming image gen
4. Image gen of the repo structure or app idea
5. Image recognition of app diagram into code in one of the languages


## Evaluation of Code:
1. Readability:
	1. Primary: Human-in-the-loop, LLM-as-judge
	2. Secondary: token and word count, reading coherency (via recall tests)
2. Maintainability
	1. Primary: Human-in-the-loop, LLM-as-judge
	2. Secondary: minimal LoC, minimal deps, tests, types, folder structure, shared code, up-to-date human and agent docs
3. Latest tools
	1. Primary: HitL, LLMaJ, Newness of lib, rate of GH stars
	2. Secondary: the vibe factor
4. Enjoyability of Docs:
	1. Primary: HitL, vibes
	2. Secondary: LLMaJ for deep funability analysis
5. Performance & Security (I guess...give it the smallest model)
	1. Primary: LLMaJ w/ web search for perf and security
	2. Secondary: Run (execute) it a bunch of times


## Killer bits for winning the hackathon:
1. Entertainment value
2. "Wow" factor demo of practical use case
3. Pretty score card


## AGENTS

### CORE AGENTS
1. Orchestrator - knows the whole deal
2. Shared Knowledge & Context grounder
3. Python Architect
4. Typescript Architect
5. Polyglot Architect
6. Python Coder
7. Typescript Coder
---
### EVAL AGENTS
1. Eval Orchestrator
2. LLMaJ
3. Python judges
	1. Readability
	2. Maintainability
	3. Latest hotness
	4. Enjoyability of Docs
	5. Security & Performance
	6. Snarky comment about how it would be horribly implemented in TS (using cliche criticisms of TS/JS code and community) + image gen prompt
4. TS judges
	1. Readability
	2. Maintainability
	3. Latest hotness
	4. Enjoyability of Docs
	5. Security & Performance
	6. Snarky comment about how it would be horribly implemented in TS (using cliche criticisms of python code and community) + image gen prompt
5. Scorer
---
### IMAGE AGENTS
1. Interpretive Art of expected code + eval - "How it started / How it's going"
2. Code shaming
<!-- 3. Architecture image
4. How we think the app looks in prod
5. Recognize images of what I want -->


## IMPLEMENTATION OF AGENTS

### Orchestrator
1. Take code,
2. route python code to TS agent, route TS to python
3. Loop `n` number of times
4. Return the code in schema
(without an agent, we then pass to the evaluator)

### Domain Language Multi-Agents Flow

1. Take in {LANGUAGE_FROM} code
2. {LANGUAGE_FROM_AGENT} - Describe what's going on in the {LANGUAGE_FROM} code
3. {POLYGLOT_AGENT} Identify how to convert it
4. {PA}Identify gotchas in converting it (if any)
5. {LT_ARCHITECT} - Plan best implementation (to hand to coding agent)
6. {LT_CODER} Code the implementation
7. {LT_ARCHITECT} Review the implementation
8. {PA} Review the implementation and compare to {LF} code
9. Log & Pass back to Orchestrator

### Eval Agent Orchestrator Flow
1. Take in the generated and original code
2. Pass the python and typescript to respective eval agents (Readability, Maintainability, Latest hotness tools, enjoyability of docs, security & performance)
3. Await results
4. Summarize results
5. Give a super good looking results file that we'll put in a nice UI

### Image Agents Flow
1. Take in generated descriptions of code and evals
2. Generate an image of Code
3. Generate an image of the eval results
4. generate images from the python agent and typescript agent image gen prompts
