# **AM ME CE 295 Project Guidelines**

AI Agents for Scientific Discovery and Engineering Research  |  Fall 2026

The project asks each student or two-person team to design, build, and evaluate an end-to-end AI agent system connected to a scientific or engineering task. The topic is open-ended. Choose a problem that matters to your research or professional interests and define evidence that will show whether the system works. The finished project must make the agent workflow, tool use, evaluation, limitations, and human oversight clear.

# **Project Scope**

A project may develop a new agent application, compare agent architectures, or study when an agent framework succeeds or fails. Suitable directions include:

* a paper-debating or scientific-argumentation agent that compares claims, evidence, and counterarguments;  
* a literature, patent, handbook, or standards agent that produces traceable citations;  
* a simulation agent that writes, runs, checks, and revises code for tools such as OpenSeesPy or OpenFOAM;  
* an experimental or data-analysis agent that processes measurements and records provenance;  
* a design or materials agent that calls a surrogate model, optimizer, database, or laboratory-planning tool; or  
* another well-motivated agent system proposed by the student and approved by the course staff.

# **Minimum Technical Expectations**

* Use an LLM-based agent with at least one domain-specific computational tool, data source, model, or external software interface. A single prompt-and-response script is not sufficient.  
* Define the workflow explicitly: agent roles, tool interfaces, state or memory, hand-offs, stopping conditions, and points where a human must review or approve an action.  
* Evaluate the system on representative tasks using measurable success criteria, deterministic checks where possible, and an appropriate baseline or non-agent comparison.  
* Test reliability across repeated runs and document important failures, unsafe behaviors, and limits.   
* Make the work reproducible. Another student should be able to install and run the submitted system from the repository.  
* Protect credentials and data. Never commit API keys. Sandbox code execution and require human approval before any consequential real-world action.

# **Choosing a Viable Project**

Choose a scope that can be implemented and evaluated during the term. Before submitting the proposal, confirm that:

* the research or engineering question is specific enough to test with representative cases;  
* the required software, data, model access, and computing resources are available; and  
* the proposed evaluation can distinguish useful agent behavior from a conventional scripted or non-agent baseline.

# **Project Milestones and Reports**

| Milestone | Required content | Format and timing |
| ----- | ----- | :---: |
| **Lab Reports**  | Problem and intended users; why an agent is appropriate; planned tools and architecture; evaluation criteria; major risks; team roles; initial repository link. | Biweekly  (Refer to syllabus and the Lab-Guideline) |
| **Final report** | Research problem; related context; architecture and implementation; evaluation design and baseline; results; reliability evidence; limitations and safety; reproducibility statement; conclusions and next steps. | 4-page IEEE paper plus AI Use Declaration appendixDue Dec 9, 2026 |
| **Final presentation** | Research problem; agent workflow; reliability-audit evidence; results and limitations; next steps. Submit slides before the session. | PowerPointOn Dec 2, 2026 |

# **Final Submission Package**

* A public GitHub repository containing the source code, README, reproducible environment (requirements.txt or Docker), pinned model ID, run instructions, representative configuration, and tests or evaluation scripts.  
* The final report and AI Use Declaration, which identifies the AI tools used, their purposes, and the student modifications or verification applied to generated work.  
* Artifacts needed to audit the main claims, such as test cases, prompts or system instructions, selected traces, outputs, plots, and data provenance. Do not include secrets, restricted data, or unnecessary private information.

# **Assessment**

The final project repository and paper account for 30 percent of the course grade. They are evaluated using the syllabus rubric below. The final presentation is a separate 20 percent course component.

| Technical depth | Reproducibility | Results and analysis | Writing | Novelty and ambition |
| :---: | :---: | :---: | :---: | :---: |
| **30%** | **20%** | **25%** | **15%** | **10%** |

# **What Strong Projects Demonstrate**

A strong project answers a clear research or engineering question, uses agentic behavior for a justified reason, connects reliably to a meaningful tool, and supports its claims with repeatable evidence. Ambitious scope is welcome, but a smaller system with careful evaluation and honest limitations is stronger than a broad demonstration that cannot be verified. Questions about scope or feasibility should be discussed with the TA before implementation becomes difficult to change.