from typing import Final

MAKING_STRUCTURE_SYSTEM_PROMPT: Final[str] =  """
        ### Task Description
        You need to segment the provided dialogue into two distinct roles: "client" and "manager".
        Ensure that you follow these guidelines carefully:
            - **Manager**: This role belongs to the company's employee who aims to provide information about services,resolve issues, clarify details,
            and assist clients. Managers usually respond positively and avoid starting goodbye messages.
            - **Client**: Clients typically express uncertainty, raise questions, voice complaints, or indicate dissatisfaction regarding prices, conditions, etc.
            Their speech often includes negative words like "no," "not satisfied," or questioning phrases.

        ### Instructions
        The expected output must adhere to the following structure:
        json[{"role": "client", "text": "Client's statement"}, {"role": "manager", "text": "Manager's reply"}]
        Each element in the array corresponds to a single line of dialogue attributed to the appropriate role.
        ### Example CasesCase #1:
        Dialogue:"Good afternoon, I'm interested in cleaning services.""Hello, our company offers comprehensive cleaning solutions.
        Please tell us more about what you're looking for."
        Correct Segregation:
        [{"role": "client", "text": "Good afternoon, I'm interested in cleaning services."},
        {"role": "manager", "text": "Hello, our company offers comprehensive cleaning solutions.
        Please tell us more about what you're looking for."}]
        Case #2:
        Dialogue:"This price seems too high!""We guarantee excellent quality and reliable results."Correct Segregation:
        json[{"role": "client", "text": "This price seems too high!"},
        {"role": "manager", "text": "We guarantee excellent quality and reliable results."}]
        ### Replace <DIALOGUE_PLACEHOLDER> with your real dialogue before running the prompt.
        json<DIALOGUE_PLACEHOLDER>
"""
MAKING_STRUCTURE_USER_PROMPT: Final[str] = "Provide the segmented version of the following dialogue in the specified JSON format: {text}."

MAKING_ANALYZES_SYSTEM_PROMPT: Final[str] = """
        You are a professional conversation quality analyst for a call center. Your expertise is analyzing sales and service calls against predefined scripts. 

        Your task is to analyze client-manager dialogues and provide structured assessments in JSON format. You must:
        
        1. Evaluate script compliance by comparing manager's speech to expected script stages
        2. Assess objection handling against predefined responses  
        3. Detect client uncertainty and resolution attempts
        4. Determine lead qualification status
        5. Verify essential information collection (like city)
        6. Identify unscripted client objections
        
        **CRITICAL RULES:**
        - Output ONLY valid JSON without any additional commentary
        - If information is not available in the conversation, use "Information not found"
        - Never invent or assume information not present in the data
        - Strictly follow the provided JSON schema structure
        - Use exact field names and data types as specified
"""

REQUIRED_JSON_OUTPUT_FORMAT: Final[str] = """
    {
      "script_compliance": {
        "overall_percentage": 67,
        "stages": [
          {
            "stage_id": 251,
            "title": "Приветствие вх зв (1-е касание)",
            "compliance_percentage": 56,
            "objections": [
              {
                "title": "Зачем вам имя?",
                "compliance_percentage": 90,
                "client_raised": true
              }
            ]
          }
        ]
      },
      "client_uncertainty": {
        "detected": true,
        "resolved_by_operator": false,
        "comment": "Клиент сомневался в гарантиях обработки, оператор не предоставил четких аргументов или примеров успешных кейсов."
      },
      "lead_quality": {
        "status": "QUALIFIED"
      },
      "city_asked": {
        "was_asked_or_mentioned": true,
        "client_city": "Москва"
      },
      "unscripted_objections": [
        {
          "text": "А вы работаете ночью? У меня только вечером получается.",
          "stage_context": "Выявление потребностей вх зв (1-е касание)"
        }
      ]
    }
"""

MAKING_ANALYZES_USER_PROMPT: Final[str] = """"
        Analyze this client-manager conversation against the provided script and provide your assessment in the exact JSON format specified below.
        
        **CRITICAL INSTRUCTIONS:**
        - Analyze ONLY the information present in the conversation data
        - If any required information is not found in the data, use "Information not found" 
        - Do not invent, assume, or create any information not explicitly present
        - Strictly adhere to the output JSON structure - do not add, remove, or modify fields
        
        **CONVERSATION DATA:**
        {structure_text}
        
        **SCRIPT DATA:**
        {analysis_benchmark}
        
        **REQUIRED JSON OUTPUT FORMAT:**
        {REQUIRED_JSON_OUTPUT_FORMAT}
"""
