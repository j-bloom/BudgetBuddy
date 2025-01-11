# Budget Buddy v2

## How to run this application
- Clone this repo into a directory/folder of your choosing. Preferably somewhere easy to access, run it in your favorite IDE and run the python app.
  - You will need Tesseract OCR and pip installed

# Versions
### v2
- You can also use the link [here](https://drive.google.com/file/d/1oe_4iHYdblln2cCQamoCkjvRXsqG8tAN/view?usp=drive_link) to access a Windows executable.

### v1
- v1 executable can be found [here](https://drive.google.com/file/d/1mq85sGu0TQLGx-VoEKDfbaXUmsESClaO/view?usp=sharing)
  
*Currently the only options to run this app are an exe for Windows and the code being run through an IDE.
  - If you would like to run this app on Linux or Mac, a third party application such as Wine would be necessary.
  - There are plans to compile the application to run on macOS 

## What does this app do?
This is a budgeting application that allows users to enter their spending in several ways.  

![Budget Buddy main screen](https://github.com/user-attachments/assets/cf104f60-a60b-42a3-8590-ed1ab5291ec5)

### Populating budget tables
#### Manually
  - User can manually enter information about a purchase including:
    - Date
    - Store
    - Category (ie, food, health, misc)
    - Entry Type (Expense/Income)
    - Price
    - Description of purchase

  - Dialog for Income/Expense/Edit are all similar. The major differences in them are the categories in the "Category" dropdown
      ![Budget Buddy entry dialog](https://github.com/user-attachments/assets/18979dbe-ca82-4e0d-8dbf-de84ac035151)
      ![Budget Buddy current month table](https://github.com/user-attachments/assets/34a78f86-5c32-48ed-8185-cf6f9aecb5a0)

#### Importing/Exporting
  - CSV 
    - If a user has a budget that they have started in a CSV file, they can import that budget into the current months budget.
    - If a user has the need to share their budget they have the ability to Export the current months budget to a CSV file they can then upload or send to another person.

  - PDF
    - If a user needs to share a monthly budget with someone and requires that the file cannot be modified, the budget can be exported as a PDF.

  - Screenshots
    - If a user has created an entry on a mobile device, they can send it to themselves and import that screenshot  
    <img src="https://github.com/user-attachments/assets/339f92f9-19f2-4170-9f09-56b8739cab28" width="300" height="600" />)

### Multiple Table View
- Multiple tables can be created
  - Users have the option to view previous budgets from prior months.
  - Previous budgets can still be modified and exported if needed
  
![Budget Buddy table search dialog](https://github.com/user-attachments/assets/8c09201b-5da0-4532-b1db-90f5a66cb729)

## Improvements from v1
- Simpler design
  - Income and Expenses are now dialogs rather than their own screens
- Improved sharing
  - Users can now export to a PDF for creating a unmodifiable file
- Better User Experience
  - Users can now create mutliple tables for each month, resulting in better orginization of monthly budgets
  - New tables get dynamically created for the user each month the first time the application is run, resulting in efficiency for the user
  - Users can now edit entries
  - Users can now duplicate entries
  - Filters to navigate table, resulting in time saving searches


## Why this app?
I wrote this application because I wanted to experiment with technologies I haven't had a chance to use, specifically <b>Optical Character Recognition (OCR)</b>.  

I also wanted an application that I could use to track my spending while keeping the information local and offline.  

There are still features and refactoring that are currently being worked on, this is not a finished product.  
However, if you would like to try this out, it is currently in a working state.
