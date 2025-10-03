from typing import Final

MAKING_STRUCTURE_SYSTEM_PROMPT: Final[str] = """
### Task Description
Your task has TWO STAGES:

**STAGE 1: VALIDATION CHECK**
Before processing, you MUST check if the provided text meets these criteria:
- Contains actual conversational text between two humans
- Has clear turn-taking pattern (speaker alternation)
- Is NOT: auto-replies, voicemail, system messages, placeholders, monologues

If the text fails validation, respond with: {"status": "invalid", "reason": "clear explanation"}

**STAGE 2: INTELLIGENT DIALOGUE SEGMENTATION**
Only for valid dialogues, segment into "client" and "manager" roles using DOMAIN-SPECIFIC PATTERNS.

### DOMAIN-SPECIFIC ROLE IDENTIFICATION

**MANAGER (Operator) Speech Patterns:**
- GREETINGS: "Добрый день/вечер", "Здравствуйте", "Служба дезинфекции", "Меня зовут [имя]"
- COMPANY INTRODUCTION: "Наша компания", "Мы предоставляем", "Имеем лицензию"
- QUESTIONING: "Подскажите, как вас зовут?", "От кого требуется обработка?", "Сколько комнат?", "Вы в городе или области?"
- PRICE DISCUSSION: "Стоимость составляет", "Рассчитаю стоимость", "У нас есть скидки"
- PROCEDURAL INFO: "Гарантия до одного года", "Мастер приедет", "Заключаем договор"
- REASSURANCE: "Я понимаю", "Сейчас все объясню", "Давайте уточним детали"
- CALL TO ACTION: "Когда вам удобно?", "Запишем вас на обработку", "Подтвердите время"

**CLIENT Speech Patterns:**
- PROBLEM STATEMENT: "У нас появились тараканы/клопы/грызуны", "Нужно избавиться от насекомых"
- PRICE QUESTIONS: "Сколько стоит?", "Это дорого", "У других дешевле"
- PROCEDURAL QUESTIONS: "Как проходит обработка?", "Что нужно подготовить?", "Какие препараты?"
- DOUBTS: "Я подумаю", "Надо посоветоваться", "А вы гарантируете результат?"
- OBJECTIONS: "Зачем вам имя?", "К чему столько вопросов?", "Мне сразу назовите цену"
- LOGISTICS: "Когда можете приехать?", "А вы работаете в нашем городе?", "Сколько длится обработка?"
- PERSONAL INFO: "Меня зовут [имя]", "Я из [город]", "У меня квартира/дом"

### CONTEXT-AWARE SEGMENTATION RULES

1. **SPEAKER ALTERNATION**: Dialogue should alternate between roles (client → manager → client → manager)
2. **CONTINUITY DETECTION**: If one speaker asks a question, the next speaker typically answers it
3. **QUESTION-RESPONSE PATTERN**: Question → Answer pairs help identify role transitions
4. **DOMAIN CONTEXT**: Use pest control domain knowledge to predict speaker roles

### COMMON SEGMENTATION MISTAKES TO AVOID
- ❌ DON'T merge multiple turns from same speaker
- ❌ DON'T split natural speech into artificial fragments  
- ❌ DON'T ignore question-answer logical flow
- ❌ DON'T assign role based solely on single words

### Output Structure
**CRITICAL FORMAT REQUIREMENTS:**
- Output MUST be valid JSON parseable by json.loads()
- NO extra newlines within JSON
- NO trailing commas
- String values properly escaped

For valid dialogues ONLY:
[{"role": "client", "text": "Full client statement"}, {"role": "manager", "text": "Complete manager response"}]

For invalid dialogues:
{"status": "invalid", "reason": "clear explanation"}

### Examples

**Valid Dialogue Example:**
Input: "Добрый день! У нас в квартире завелись тараканы." "Здравствуйте! Служба дезинфекции, меня зовут Анна. Подскажите, как вас зовут?" "Меня зовут Ирина. Скажите, сколько будет стоить обработка?" "Ирина, стоимость зависит от площади квартиры. Подскажите, сколько у вас комнат?"

Output: [{"role": "client", "text": "Добрый день! У нас в квартире завелись тараканы."}, {"role": "manager", "text": "Здравствуйте! Служба дезинфекции, меня зовут Анна. Подскажите, как вас зовут?"}, {"role": "client", "text": "Меня зовут Ирина. Скажите, сколько будет стоить обработка?"}, {"role": "manager", "text": "Ирина, стоимость зависит от площади квартиры. Подскажите, сколько у вас комнат?"}]

**What NOT to do:**
❌ WRONG: Splitting natural speech: [{"role": "client", "text": "Добрый день!"}, {"role": "client", "text": "У нас в квартире завелись тараканы."}]
✅ CORRECT: Keep complete thoughts together

### Important
- ALWAYS validate first, then segment
- Use DOMAIN PATTERNS for accurate role assignment
- Maintain natural speech boundaries
- Preserve question-answer logical flow
"""

MAKING_STRUCTURE_USER_PROMPT: Final[str] = """
Analyze the following conversation from pest control service and segment into client-manager dialogue.

Apply DOMAIN-SPECIFIC rules:
- Manager: introduces company, asks structured questions, discusses pricing, provides guarantees
- Client: describes pest problems, asks about cost/procedure, expresses concerns/doubts

Maintain NATURAL SPEECH BOUNDARIES - don't split complete thoughts.

Conversation to analyze:
{text}

Output MUST be clean JSON without extra formatting.
"""

MAKING_ANALYZES_SYSTEM_PROMPT: Final[str] = """
You are a professional conversation quality analyst for a call center. Your expertise is in analyzing sales and service calls against predefined scripts with high semantic accuracy.

**CRITICAL ANALYSIS METHODOLOGY:**

1. **COMPREHENSIVE SCRIPT ANALYSIS:** You MUST analyze EVERY script element:
   - For EACH stage: analyze ALL script blocks and ALL predefined objections
   - For EACH objection in the script: check if it was raised by client AND how operator handled it
   - Never skip or omit any script elements from analysis

2. **OBJECTION PROCESSING RULES:**
   - If client raised an objection from script → `"client_raised": true` + analyze operator's response
   - If objection exists in script but wasn't raised → `"client_raised": false` + `"compliance_percentage": 0`
   - Include ALL script objections in output, even with 0% compliance
   - Calculate compliance based on semantic match to script's suggested response

3. **COMPLIANCE CALCULATION:**
   - Stage percentage = (Number of semantically matched script blocks / Total script blocks) × 100
   - Overall percentage = Average of ALL stage percentages
   - Consider partial matches (e.g., 50% for incomplete coverage)

4. **STRICT DATA ADHERENCE:**
   - Analyze ONLY information present in conversation
   - Use exact field names and structure from required JSON format
   - Output MUST be complete - never skip fields or arrays

**ABSOLUTE OUTPUT RULES:**
- Output ONLY valid JSON without any additional text
- Include ALL script objections in analysis, not just raised ones
- Follow exact JSON structure - no field modifications
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

structure_text = {
  "transcription": [
    {
      "role": "client",
      "text": "Здравствуйте. А я звоню по телефону Дмитрий. Всё верно. Меня зовут Алёна. Вас как зовут?"
    },
    {
      "role": "manager",
      "text": "Меня Евгения. Евгения. Я слушаю. Какой у вас вопрос?"
    },
    {
      "role": "client",
      "text": "Ваша служба занимается, да, уничтожением грызунов?"
    },
    {
      "role": "manager",
      "text": "Грызуны, насекомые, да, всё верно. Устранение неприятного запаха."
    },
    {
      "role": "client",
      "text": "А вот как это фактически будет?"
    },
    {
      "role": "manager",
      "text": "Я вам сейчас всё объясню. Скажите, пожалуйста, требуется вам от грызунов обработка, верно?"
    },
    {
      "role": "client",
      "text": "Да. В квартире, в тесном доме?"
    },
    {
      "role": "manager",
      "text": "В квартире, к сожалению. У нас на первом этаже стали делать ремонт в магазине. Поработали всю домю. Вот теперь у нас распространились грызуны. Евгения, скажите, пожалуйста, в квартире сколько комнат у вас?"
    },
    {
      "role": "client",
      "text": "Две комнаты."
    },
    {
      "role": "manager",
      "text": "Наблюдаете по всей площади?"
    },
    {
      "role": "client",
      "text": "Не поняла."
    },
    {
      "role": "manager",
      "text": "Наблюдаете везде? Продвигаете?"
    },
    {
      "role": "client",
      "text": "Нет, нет, нет. К сожалению, только к счастью, в прихожей и на кухне."
    },
    {
      "role": "manager",
      "text": "Всё хорошо. Знаете, я сама раскладывала, и сейчас их нет. И даже еда, которая лежит, у меня из-за травы. Покусана. Но я на этом не останавливаюсь."
    },
    {
      "role": "client",
      "text": "Ну, правильно, лучше сразу себя обезопасить и забыть вообще про это."
    },
    {
      "role": "manager",
      "text": "Всё верно. Так, скажите, пожалуйста, находитесь в городе?"
    },
    {
      "role": "client",
      "text": "Да, да, в городе на Краматорской."
    },
    {
      "role": "manager",
      "text": "Всё хорошо. Здесь все животные с вами проживают?"
    },
    {
      "role": "client",
      "text": "Нет, ни животных, ничего, я одна."
    },
    {
      "role": "manager",
      "text": "Евгения, скажите, пожалуйста, возможность на 2-3 часа будет покинуть квартиру после обработки?"
    },
    {
      "role": "client",
      "text": "Конечно, будет."
    },
    {
      "role": "manager",
      "text": "Всё хорошо. Сейчас я вас ориентирую по стоимости. Смотрите, как происходит данная процедура. Мастер к вам приезжает, заключает с вами договор на обработку. В договоре указана у нас гарантия, чем сделали и как сделали. Гарантию предоставляем мы до года. Мастер обработку сделал, вы закрыли квартиру на 2-3 часа. Потому что методы обработки, они разные. Бывает мелкодисперсное распыление, бывает обработка генератором тумана. Ну и также имеется гранулированная обработка. То есть непосредственно метод подбирают для вас мастер на месте. Уже после осмотра. Так, скажите пожалуйста, пенсионеркой являетесь?"
    },
    {
      "role": "client",
      "text": "Да, да."
    },
    {
      "role": "manager",
      "text": "Хорошо, так, хорошо. Хорошо. И это даже хорошо, потому что для пенсионеров у нас сейчас в данный момент скидки идут. Поэтому это хорошо."
    },
    {
      "role": "client",
      "text": "Ясно, ясно, я поняла."
    },
    {
      "role": "manager",
      "text": "Так, смотрите, по стоимости обработка с учетом скидки будет 3200 рублей полностью вся квартира."
    },
    {
      "role": "client",
      "text": "Ясно. Я буду согласна, потому что я не сплю даже по ночам."
    },
    {
      "role": "manager",
      "text": "Ну я представляю вас. Скажите пожалуйста, мастера, когда вы готовы будете принять будние, выходные?"
    },
    {
      "role": "client",
      "text": "Мне все равно, я не работаю."
    },
    {
      "role": "manager",
      "text": "Так, смотрите, на завтра на 11 часов удобно вам будет?"
    },
    {
      "role": "client",
      "text": "Вы знаете, мне лучше попозже, потому что я с утра пью лекарства. Как раз вот до обеда практически, до обеда. А потом после обеда в любое время."
    },
    {
      "role": "manager",
      "text": "Так, смотрите, могу вам предложить 13.30, могу вам предложить 14.30."
    },
    {
      "role": "client",
      "text": "Давайте в 14.30."
    },
    {
      "role": "manager",
      "text": "В 14.30, хорошо. Адрес можно ваш, пожалуйста? Краматорская 3?"
    },
    {
      "role": "client",
      "text": "Краматорская. 23."
    },
    {
      "role": "manager",
      "text": "Дополнительный номер для связи будет для мастера или только по этому номеру звонить?"
    },
    {
      "role": "client",
      "text": "Только по этому номеру звонить. Нет, только по этому, только по этому."
    },
    {
      "role": "manager",
      "text": "Все, хорошо, назначаем с вами мастера на завтра на 14.30."
    },
    {
      "role": "client",
      "text": "Но он только еще посмотрит, а потом уже другое время будет."
    },
    {
      "role": "manager",
      "text": "Нет, нет, нет, он уже завтра будет у вас проводить обработку."
    },
    {
      "role": "client",
      "text": "Ну ясно, ясно. Я хочу подготовиться, все убрать, чтобы у меня все было более-менее закрыто."
    },
    {
      "role": "manager",
      "text": "Ну вот как раз у вас пока будет время потихонечку, не торопясь."
    },
    {
      "role": "client",
      "text": "Да, в 14.30, спасибо."
    },
    {
      "role": "manager",
      "text": "Да, все верно. Спасибо."
    },
    {
      "role": "client",
      "text": "А вы это, станопедстанция, да?"
    },
    {
      "role": "manager",
      "text": "Да, все верно."
    },
    {
      "role": "client",
      "text": "Да, все верно. Тогда веры больше, если это станопедстанция."
    },
    {
      "role": "manager",
      "text": "Всего доброго, ожидайте, пожалуйста."
    }
  ]
}

MAKING_ANALYZES_USER_PROMPT: Final[str] = """
Perform COMPREHENSIVE semantic analysis of the client-manager conversation against the provided script.

**COMPREHENSIVE ANALYSIS REQUIREMENTS:**

1. **ANALYZE ALL SCRIPT ELEMENTS:**
   - Process EVERY stage and EVERY objection from the script benchmark
   - For each stage: evaluate ALL script text blocks and ALL predefined objections
   - Never omit any script elements from the analysis

2. **DETAILED OBJECTION ANALYSIS:**
   - For EACH objection in script: check if client raised it in conversation
   - If raised: analyze operator's response against script's suggested response
   - If not raised: include with `"client_raised": false` and `"compliance_percentage": 0`
   - Include ALL script objections in the final output array

3. **STAGE COMPLIANCE EVALUATION:**
   - Break down each stage into semantic blocks from script text
   - Check which blocks were covered by operator's speech
   - Calculate percentage based on covered blocks vs total blocks

4. **UNSCRIPTED OBJECTIONS:**
   - Identify ANY client objections not present in the script
   - Add them to unscripted_objections with exact client text

**CONVERSATION DATA:**
{structure_text}

**SCRIPT DATA (ANALYSIS BENCHMARK):**
{analysis_benchmark}

**CRITICAL OUTPUT INSTRUCTIONS:**
- You MUST output COMPLETE JSON with ALL script objections included
- You MUST NOT skip any objections from the script benchmark
- You MUST maintain exact field structure and data types
- For unraised objections: use `"client_raised": false` and `"compliance_percentage": 0`

**REQUIRED JSON OUTPUT FORMAT:**
{REQUIRED_JSON_OUTPUT_FORMAT}
"""