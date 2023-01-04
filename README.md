# YOUR PROJECT TITLE
#### Video Demo:  <https://youtu.be/vZAuovocaqI>
#### Description:
I have created a telegram bot that allows the user to track their expenses.

There are 4 main functions: start, summary, add, new.

/start: starts the bot and gives the user a guide how the other functions work.

/new: Allows the user to create a new spending log to track their expenditure.
    When /new is entered, the bot will prompt the user for a text input, and that text will then be used as the title of the spending log. (function: new)
    When the title is entered, the bot will create a new dictionary in the list of dictionaries "LOGS", and the each dictionary will contain the following keys: Transport, Food, Nutrition, Shopping, Entertainment, Others, Total
    and the keys will all be initalised with a value of 0, and the keys will go on to represent the amount of money the user spends in that category. 
    Afterwards, the bot will return a readback to the user to let the user know he can go /summary to view the newly created spending logs. (function: readback)

/add: Allows the user to add a new expenditure to one of the spending logs
    When /add is entered, the bot will prompt the user to select one of the spending logs that have been created, with a Reply Keyboard. (function: add)
    After the spending log is selected, the bot will store the selection data as a key value pair under context.user_data. Then, the bot will prompt the user to select the category of expenditure, also via a Reply Keyboard. 
    However, if the user inputs a random text input that does not have the same value as the title of any of the spending logs, the bot will end the "conversation" and prompt the user to try again. (function: category) 
    Once the category is selected, the bot will store the selection data as a key value pair under context.user_data. Then the bot will prompt the user to enter the amount spent via text, but entering numbers only. (function: amount)
    Once the amount is entered, the bot will then update the spendings in both the catgeory and the "total", and it will update the user that the spending log has been updated. (function: confirm)

/summary: Allows the user to get an overview of the total amount of money spent in each spending log, and the respective categories.
    When /summary is entered, the bot will prompt the user to select one of the spending logs that have been created, with a Reply Keyboard. (function: summary)
    After the spending log is selected, the bot will store the selection data as a key value pair under context.user_data. Then, the bot will prompt the user to select the category of expenditure to view, also via a Reply Keyboard. 
    However, if the user inputs a random text input that does not have the same value as the title of any of the spending logs, the bot will end the "conversation" and prompt the user to try again.(function: categorysum) 
    Once the category is selected, the bot will store the selection data as a key value pair under context.user_data. The bot will then make use of the stored selections to give the user an update of how much has been spent in the form of a formatted string. (function: end)

/cancel: Allows the user to end the "conversation" at any point in time after initiating any of the 3 commands above.
    When /cancel is entered, the bot will terminate the conversation, and update the user that the cancellation has been processed, allowing the user to initiate a new command.
