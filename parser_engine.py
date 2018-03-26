def parse_string(string_to_parse):
# Questions to answer

# helper definitions
# ===========================================
   def find(word,array_of_sentences):
      questions = []
      for sentences in array_of_sentences:
         if word in sentences:
               questions.append(sentences)
      return questions



   def analyse(question,identifier,specific_identifier):
   # print(question)
      question_parts = []
      while len(question) > 255:
      # print("question = " + question)
         question_parts.append(question[:255])
         question = question[255:]
      responses = []
      for part in question_parts:
         responses.append(client.message(part))
   # print(responses)
      positive_responses = [i for i in syn["may"]]
      negative_responses = [i for i in syn["not"]]
   # print(response["entities"])
   # print(response["entities"]["intent"])
      all_values = []
      for response in responses:
         if "intent" in response["entities"]:
            for i in response["entities"]["intent"]:
               all_values.append(i["value"])
   # print(positive_responses)
   # print(negative_responses)
      result = 2 * len(list(filter(lambda x: x in positive_responses,all_values)))\
            - 1.5 * len(list(filter(lambda x: x in negative_responses,all_values)))\
            + len(list(filter(lambda x: x not in positive_responses or negative_responses,all_values)))
      print(result)
      if result > questions[identifier][specific_identifier]:
         questions[identifier][specific_identifier] = result

   # print("=================")


   def wordcount(sentence):
       return len(sentence.split(' '))
# ===========================================
   questions = {   "rights":   {
                                "surrender":0,
                                "guarantee":0,
                                "litigate":0
                            },
                "data":     {
                                "asset":0,
                                "authority":0,
                                "create":0
                            },
                "terms":    {
                                "change":0,
                                "notify":0
                            },
                "retain":   {
                                "terminate":0,
                                "retain":0,
                                "license":0
                            }
                            }
   import re
   from wit import Wit
   client = Wit("SOCU7BOASMBY5TC44U7C3GK44GFSHDXV")

# definitions
   syn = {
    "may":["may","can","will","do"],
    "authority":["authority","authorites","government","regulatory bodies"],
    "surrender":["surrender","abandon","abdicate","give up","relinquish"],
    "breach":["breach","nonfulfillment"],
    "create":["create","generate"],
    "ownership":["ownership","proprietary","hold rights"],
    "notify":["notify","alert","announce","warn"],
    "user":["user","account","you","your"],
    "data":["data","content","information"],
    "license":["license","authorisation","consent","permit"],
    "asset":["asset"],
    "retain":["retain","conserve","keep","preserve","reserve","save","store","include"],
    "features":["features","functionalities"],
    "terms":["terms","terms and condtions"],
    "company":["us","we","company","affiliate","associate","institution","partner","successor","third party","third parties"],
    "rights":["rights","claim","priviledge"],
    "change":["change","modify","revise","tweak"],
    "not":["not","dont","not allowed","not permitted","restricted"],
    "litigate":["litigate","courts","dispute","jurisdiction","sue"],
    "terminate":["terminate","annul","disconitnue","cease","delete","halt","remove"],
    "share":["share","distribute"],
    "guarantee":["guarantee","assure","assurance","promise"],
    "give":["give","grant"]
    }

# getting document ready for parsing
# ================================================
   terms_conditions_file = open("tandc","r")
   terms_conditions_file.seek(0)
   terms_conditions = terms_conditions_file.read()
   sentences = list(map(lambda x: x.strip(),terms_conditions.split(".")))
   sentences = list(filter(lambda x: wordcount(x) >= 7,sentences))
   plausible_questions = []
   actual_questions = []
# finding important sentences
   for identifier in questions.keys() :
      plausible_questions = []
      for synonyms in syn[identifier]:
         plausible_questions += find(synonyms,sentences)
      plausible_questions = set(plausible_questions)

      for question in plausible_questions:
         for specific_identifier in questions[identifier].keys():
            for synonyms in syn[specific_identifier]:
               actual_questions += find(synonyms,plausible_questions)

   actual_questions = set(actual_questions)
   for question in actual_questions:
   # print("********\n" + str(actual_questions) + "*********\n")
      analyse(question,identifier,specific_identifier)
# print(questions)

   return "\
Rights:\n\
\n\
- Do you give up on rights? {}\n\
- Are you gaurenteed functionality? {}\n\
- Is the jurisdiction specific? {}\n\
\n\
========================================\n\
# Who can see your data?:\n\
\n\
- Is your data a business asset? {}\n\
- How do services deal with government requests? {}\n\
- Does the company own the content you generate on the service? {}\n\
\n\
========================================\n\
# Changes to terms:\n\
\n\
- Changes to the Terms are possible? {}\n\
- Are users notified when terms change? {}\n\
\n\
=======================================\n\
# Control of your data:\n\
\n\
- Do they keep the data? {}\n\
- To avoid lock-in and stay in control {}\n\
- Can you control your privacy? {}\n\
\n\
====================='''.format(
questions["rights"]["surrender"] >=1,
questions["rights"]["guarantee"] >=1,
questions["rights"]["litigate"] >=1,
questions["data"]["asset"] >=1,
questions["data"]["authority"] >=1,
questions["data"]["create"] >=1,
questions["terms"]["change"] >=1,
questions["terms"]["notify"] >=1,
questions["retain"]["terminate"] >=1,
questions["retain"]["retain"] >=1,
questions["retain"]["license"] >=1)

print(parse_string("abc"))
