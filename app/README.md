# Agentic Risk Capability Framework - Streamlit Application

This Streamlit application provides an interactive interface for assessing risks and controls for agentic AI applications using the Agentic Risk Capability Framework (ARC). The application provides a comprehensive risk assessment tool for agentic AI systems.

## Project Structure

```
app/
├── app.py                 # Main Streamlit application
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic data models
├── utils/
│   ├── __init__.py
│   ├── data_loader.py     # Data loading utilities
│   ├── llm_utils.py       # LLM API utilities
│   ├── session_utils.py   # Session state management
│   └── export_utils.py    # Word document export
├── sample_data.yaml       # Sample application data
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
└── README.md             # This file
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file in the parent directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   Or copy the example environment file:
   ```bash
   cp env.example .env
   ```
   Then edit `.env` and add your OpenAI API key.

3. **Data Files**:
   Ensure the following YAML files exist in the `../data/` directory:
   - `capabilities.yaml` - Defines capabilities and their categories
   - `risks.yaml` - Contains all risks with descriptions and associated controls
   - `controls.yaml` - Defines all available controls
   - `baseline.yaml` - Lists baseline categories that apply to all applications

## Running the Application

```bash
streamlit run app.py
```

Open your browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`).

## Deploying to Airbase 

Because the application requires the data files, the following commands must be run from the root directory. 

```
airbase link
airbase container deploy
airbase container deploy
```

## Features

### 1. Application Assessment
- Input form for application details:
  - Application description and purpose
  - Components description (technical architecture, tools, MCP servers, integrations, data flows)
  - Data classification (Public/Open, Internal, Confidential, Restricted)
  - Deployment type (SaaS, Custom, Platform)
  - Human in the loop description
  - Public facing status
  - Criticality level (Low, Medium, High, Critical)
  - PII data usage
- Auto-fill with sample data via "Try Sample" button
- AI-generated comprehensive description using LiteLLM
- Editable description with real-time updates

### 2. Capability Identification
- AI-driven capability analysis based on application details
- Interactive capability selection with checkboxes
- Category-based organization (Cognitive, Interaction, etc.)
- Capability descriptions displayed alongside IDs and names
- Baseline risks section (collapsed by default, all selected)
- Seamless transition to risk assessment

### 3. Risk Assessment
- **Application Summary**: Expandable summary of application details and identified capabilities
- **Capability-Specific Risks**: Collapsible section showing risks specific to selected capabilities, organized by category
- **Baseline Risks**: Collapsible section showing all baseline risks organized by category (LLM, Instructions, Tools, Memory, Agentic Architecture, Roles and Access Controls, Monitoring and Traceability)
- Contextualized risk analysis for each risk based on your application
- Editable likelihood and impact scores (1-5 scale)
- Color-coded risk indicators (🟢 Very Low, 🟡 Low, 🟠 Medium, 🔴 High, 🔴 Very High)
- Reasoning fields for both likelihood and impact scores
- Threshold-based filtering for controls (default: likelihood ≥ 4, impact ≥ 4)

### 4. Controls & Mitigation
- High-priority risk controls based on threshold settings
- Risk listing with contextualization
- Control details with descriptions
- Implementation status tracking with editable text boxes
- Default implementation text: "I did not implement this control. I accept all residual risk."
- Two-column layout: control information and implementation status
- Comprehensive Word document export with all assessment details

## Usage Workflow

1. **Complete the Application Assessment**: Fill out the form on the first page with details about your agentic AI application, or use the "Try Sample" button for quick testing
2. **Review Generated Description**: The AI will generate a comprehensive description of your application based on your inputs
3. **Edit if Needed**: Click the "Edit" button to modify the generated description before proceeding
4. **Continue to Capability Identification**: Click "Continue to Capability Identification" to proceed
5. **Review AI Analysis**: Review the AI's reasoning for capability identification
6. **Select Capabilities**: Choose or modify the capabilities that apply to your application
7. **Continue to Risk Assessment**: Click "Continue to Risk Assessment" to proceed
8. **Review Risk Analysis**: The AI will contextualize all risks to your specific application
9. **Adjust Scores**: Edit likelihood and impact scores and reasoning for each risk
10. **Set Control Thresholds**: Adjust the likelihood and impact thresholds to determine which risks require controls
11. **Continue to Controls**: Review and document control implementations
12. **Export Assessment**: Use the "Export Assessment" button to generate a Word document with all assessment details

## Architecture

The application follows a modular architecture:

- **Models (`models/schemas.py`)**: Pydantic schemas for data validation and structured LLM outputs
- **Utils**: Reusable utility functions
  - `data_loader.py`: Loads YAML data files with error handling
  - `llm_utils.py`: Handles LiteLLM API calls for capability analysis, risk assessment, and description generation
  - `session_utils.py`: Centralized session state management
  - `export_utils.py`: Word document generation for assessment export
- **Main App (`app.py`)**: Streamlit UI, page routing, and user interaction

## API Integration

The application uses LiteLLM to integrate with various LLM providers. By default, it uses GPT-4o-mini, but you can modify the model in the `get_llm_capability_analysis`, `get_llm_risk_analysis`, and `get_application_description` functions in `utils/llm_utils.py`.

## Error Handling

Comprehensive error handling is implemented throughout:
- File I/O operations with specific error messages
- LLM API calls with fallback handling
- Data validation using Pydantic models
- User input validation
- Missing data detection and warnings

## Session State Management

Centralized session state management with:
- Consistent key usage via `SessionKeys` class
- Default value initialization
- State validation
- Helper functions for complex state updates

## Customization

You can customize the application by:
- Modifying the data files (`../data/*.yaml`) to add new capabilities, risks, or controls
- Changing the LLM model used for analysis in `utils/llm_utils.py`
- Adjusting the UI layout and styling in `app.py`
- Adding new assessment questions in the application assessment form
- Modifying theme colors in `.streamlit/config.toml`

## Troubleshooting

- **No AI Analysis**: If the AI analysis doesn't work, check your API key in the `.env` file and internet connection
- **Missing Data**: Ensure all YAML files are present in the `../data/` directory
- **Performance Issues**: The application caches data for better performance, but you may need to restart if you modify the data files
- **Environment Variables**: Make sure your `.env` file is in the parent directory and contains a valid `OPENAI_API_KEY`
- **Button Colors**: Primary buttons should appear blue based on the theme configuration in `.streamlit/config.toml`
