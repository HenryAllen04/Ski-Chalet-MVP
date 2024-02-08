Ski Chalet MVP
What can this project do?
- Reccomend restaurants with maps API
- Tell User what lifts are open and closed
- answer genral inquiries from a KB

How to run?
1) Run the code inside of a REPL
2) Check the Voiceflow code is published to the latest Version
3) Go to infalyzetech.com and click on the chat bubble in the bottom right

Steps to go from MVP to Solution
1) Fintune KB 
2) Decide whether to host it inside of Voiceflow or Inside the REPL (where it is now) - this decision needs to be made to further the implementation of a KB loop,

      if the KB is in VF:
            - The KB loop will be easier to implement
            - The KB might not be as accurate (look into some RAG techniques with VF)
            - Will probably have to move alot of assistance API code into VF to accompany the KB properly

      if the KB is in REPL:
            - The KB loop will be very hard to implement, it will have to be hardcoded and we will have to use langchain to tell whether the user has asked a Q the Kb knows in order to initiate the KB loop steps
            - The KB will be a stronger
