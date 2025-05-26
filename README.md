# Repository Overview

This repository is a multi-project workspace featuring advanced AI agent systems, automated data/documentation tools, and specialized integrations for content and data analysis. Each project is described below:

---

## 1. Blogpost Crew (crewai agents project)

**Purpose**:  
An automated, multi-agent AI system built using the [crewAI](https://crewai.com) framework. The goal is to generate high-quality, research-based financial blog content by orchestrating specialized agents in collaborative workflows.

**Project Scope**:
- **Agents**:  
  - *Market News Monitor*: Analyzes real-time financial news for relevant trends.
  - *Data Analyst*: Processes and synthesizes market data into actionable insights.
  - *Content Creator*: Crafts engaging content based on research and data.
  - *Quality Assurance*: Reviews and refines the final content for accuracy and brand alignment.

- **Tools & Resources Used**:  
  - `crewAI` platform for multi-agent orchestration  
  - Agents and tasks are configured in YAML files for flexibility (`src/blogpost/config/agents.yaml`, `src/blogpost/config/tasks.yaml`)
  - Tools like SerperDevTool (for web search), ScrapeWebsiteTool, WebsiteSearchTool
  - Main orchestration logic in `src/blogpost/crew.py` and `src/blogpost/main.py`

- **Prompts & Workflow**:  
  The system is prompt-driven, with agents collaborating in a chain to monitor news, analyze data, create content, and ensure QA. Output is typically a detailed `report.md` on financial topics.

- **How to Run**:  
  - Install dependencies using UV or pip.
  - Set up your API keys in `.env`.
  - Edit YAML files for custom agents/tasks.
  - Run:  
    ```
    crewai run
    ```
  - The system will generate a research-based blog/report.

---

## 2. Kaggle API Dataset Documentation Tool

**Purpose**:  
A project (in the `kaggle-api/` directory) focused on automatic dataset description and documentation using Kaggle's API.  
**Scope**:  
- Automates fetching dataset metadata, sample data, and descriptive statistics from Kaggle.
- Intended to streamline the creation of dataset READMEs or documentation for data science projects.

---

## 3. Weather Project (Agent Integration Example)

**Purpose**:  
Located in the `weather/` directory, this project demonstrates the use of Claude desktop client integration with an MCP server.

**Scope**:  
- Likely involves retrieving or processing weather data, possibly using agent-based automation.
- Integrates with external AI clients or services.
---

## 4. Gradio Letter Counter & MCP Server (`server.py`)

**Purpose & Scope**:  
A standalone Python application that:
- Provides a Gradio web interface for counting occurrences of a letter in a text.
- Launches an MCP server alongside the web UI.
- Useful as a simple demonstration of Gradio + MCP integration.

**How it works**:  
- Enter text and the target letter in the web UI.
- The app returns the count of that letter.
- The MCP server is enabled by default for agent integration.

---

## Additional Notes

- For more details on each project, check inside the respective directories for additional documentation or code.
- The `src/blogpost/config/agents.yaml` and `src/blogpost/config/tasks.yaml` files provide detailed agent roles, goals, and task descriptions for the crewAI-based blogpost project.
---
