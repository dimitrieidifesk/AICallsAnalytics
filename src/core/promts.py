from typing import Final

MAKING_STRUCTURE_SYSTEM_PROMT: Final[str] =  """
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
MAKING_STRUCTURE_USER_PROMT: Final[str] = "Provide the segmented version of the following dialogue in the specified JSON format: {text}."

raw_transcript = '''
        Здравствуйте, это служба дезинфекции, вы нам звонили недавно.
        Я еще не решила, я перезвоню. А подскажите, что смущает, может могу помочь чем-то?
        Нет, не надо. Хорошо, тогда ждем звонка. Перекопать ведь надо, надо перекопать. Зачем?
        Сначала обычно обработку проводят, избавляются, а потом уже перекапывают. Да? Ну да, как можно скорее. Ну как определимся, так вам перезвони
        м телефончиком. По этому телефону звонить? Ну да, конечно, можете нам сюда звонить. Ага, хорошо, хорошо. Всего доброго.
        Как определимся, так сразу позвоним вам. Вы приезжаете и обрабатываете всю территорию, да? Да, конечно, сколько надо, столько и обработаем.
        А гарантия есть какая, что их не будет? Да, конечно, у нас гарантия до года, фактически мастер пропишет на месте.
        То есть либо год, либо больше будет. Ага, вы где находитесь, вы какая станция? Служба дезинфекции, мы в Липецке находимся, еще в нескольких городах у 
        нас отделение есть. А, у вас во всех отделениях, во всех городах. Хорошо, две с половиной тысячи, да?
        Так, у вас указано три тысячи за пять соток, да, верно? Вы звонили две с половиной, сказать.
        Так, ну давайте сейчас разговор закончим, я проверю, какую стоимость вам называли до этого. Послушаю диалог.
        Ага, ладно, ладно, ладно, мы перезвоним. Ждем, да, тогда. Хорошо, хорошо. Всего доброго. До свидания.
        ''' # Исключительно для тестов и экномии поинтов на запросы