# PlateIQ | Virender Bhargav

This README includes instructions for developers and maintainers for this repository.

# 1. Problem Statement
At Plate IQ, we process thousands of customer invoices every day - and invoice digitization is at the center of everything we do.
Customers send in their invoices (PDF files) and the Plate IQ system converts the (unstructured) data from the invoice into a structured format and saves it in an SQL database. At the minimum, this includes the vendor/seller, the purchaser/buyer, the invoice number and date, and each line item mentioned in the invoice. (Here are some examples of invoices on Google Image search​ to help you understand more about the type of information that Invoices generally contain. It is expected that you consider other useful information in your data model). These documents are then processed by our background processing engine using OCR and machine learning (or sometimes manually), structured information is generated ​and validated​,
 
after which the document is marked “digitized” and the structured information is accessible to our customers.
We want to mock this process in this assignment. ​Create a web service with the following requirements​:
API endpoints for the end customer
- To allow a customer to provide a PDF document (invoice) to process
- To allow a customer to track a document’s digitization status
- To allow a customer to retrieve the structured invoice information for a specified
document, if the document status is digitized (simply return mock data in this case)
API endpoints for internal users / other microservices
- To allow a staff member (or another microservice) to manually add digitized / parsed
(​structured​) information for a specific document
- For example, if a staff member views the document and wishes to record in the
Structured data tables that the Invoice Number is INV1234, they should be able
to do so
- It should be possible to add/update more than one field at a time, if the caller
chooses to do so
- It should not be mandatory to update all fields/information in the same call; it
should be possible to independently and partially add/update each piece of
information
- To allow marking a document as “digitized”

# 2. Solution Approach
* User: model(extends Django's AbstractUser) to represent any user who can use the system
* Owner: model to represent Purchaser/Buyer
    * OneToOne Relation with User
    * All fields specific to owner will be added to this model
* Vendor: model to represent Vendor/Seller
    * has OneToOne Relation with User 
    * All fields specific to vendor will be added to this model
    * A vendor is related to one Store
   
* Organization: model to represent any organisation of the system
* Store: Store entity owned by a single Owner
    * has OneToOne Relation with Organization
    * A store has a single Owner
    * ex : MacDonalds/Pizza Hut/Dominoes
* Branch: Branch entity which comes under a single Store
    * has OneToOne Relation with Organization
    * A branch comes under a single Store
    * one store can have multiple branches. Ex: MacD Sector 41 Noida , MacD Sector 50 Noida
    
* Document - model to represent a document that can be uploaded on the system
    * file: to store the uploaded file
    * is_digitized: flag to check if the document has been digitized
    * meta_data: to store json of structured invoice.
    * created_by : user who uploaded the document.
* Invoice - model to represent An invoice registered on the system
    * branch: Branch for which the invoice is to be created
    * vendor: Vendor against whom the invoice is to be created
    * invoice_num: Invoice Number (unique for a given vendor) 
    * date : date of invoice
    * total_amount: total amount of invoice
    * document: document against which this invoice has been created
* InvoiceLineItem : model to represent an item present on single invoice(Association model for Invoice and Item)
    * invoice: associated Invoice
    * item: associated item
    * quantity: quantity ordered
    * price : price of item at time of invoice creation
* Item: model to represent an item that can be present in invoice
    * name: name of item
    * branch: associated branch
    * price: current price of item

# 3. Instructions for Developers

## 3.1 Branches & Environments

### 3.1.1 Branches
    There are 3 main branches namely, master, beta and develop. Other then that you must follow git flow to push your code to develop branch.
    So there are some strict rules when it comes to merging. These rules are given below
        a) You can merge "master" into "beta".
        b) You can merge "beta" into "master" and "develop".
        c) You must have to create apull request to merge code into beta and master branch.

## 3.2 Commit Process

### 3.2.1 Commit Format

Use the multi-line format defined below (do not use `-m` and go through editor):

```
[<task-id>] <task-summary>
<blank line>
- <commit description line 1>
- <commit description line 2>
- <commit description line 3>
```

In the header line `<task-id>` is the JIRA task id, and `<task-summary>` is the JIRA task summary.

**NOTE**: The blank line is important. That's what makes git know that you have a header line.

Also, optionally, you may include lines using the [smart commit syntax](https://confluence.atlassian.com/bitbucket/processing-jira-software-issues-with-smart-commit-messages-298979931.html) in your summary.

### 3.2.2 Pre-commit checks

1. Run `coverage run ./manage.py test` to run Django tests and ensure no errors
2. Run `cov-check.sh` to check code coverage and ensure it give a pass message

### 3.2.3 commit and Merge

1. `$ git add <your files..>`
2. `$ git commit` to create a commit
3. `$ git pull --rebase` to get changes from repository.
4. In case the above steps gives you any conflicts:
    1. Resolve the conflicted files by manually inspecting
    2. `git add` all conflicted files resolved manually by you
    3. `$ git rebase --continue` to tell git that you have resolved the conflicts. This may ask you to create another commit.

### 3.2.4 Push to remote

```
$ git push
```

## 2.3 Coding Standards

### 2.3.1 Python

#### 2.3.1.1 Coding Standards

We would follow the following standards:

- [PEP8](https://www.python.org/dev/peps/pep-0008/)
- [PEP257](https://www.python.org/dev/peps/pep-0257/)

Additionally, look at this [presentation](http://python.net/~goodger/projects/pycon/2007/idiomatic/presentation.html)


# 4. Development Environment Setup

## 4.1 Ubuntu 16.04

### 4.1.1 Download and Installation

-Suggested OS is Ubuntu 16.04. Install python3.7 before proceeding further: https://tecadmin.net/install-python-3-6-ubuntu-linuxmint/

### 4.1.2 How to setup new development workspace
    a) create a directory let say "plateiq-backend"
    b) run "cd path_to_directory"
    c) run "sudo apt-get install python3-venv"
    d) run "python3 -m venv ."
    e) run "git init"
    f) run "git remote add origin your_repo_path_url"
    g) run "git fetch --all"
    h) run "git checkout develop"
    i) run "git pull origin develop"
    j) run "source bin/activate"
    k) run "pip install -r requirements.txt"
    l) run "cp sample-file.env .env" and change env variable values accordingly
    m) run "mkdir log". This directory will used to store app logs.
    n) run "cd src"
    0) run "python manage.py runserver 0.0.0.0:8000"

# 5. Developer:
    a) Virender Bhargav (raif.viren@gmail.com)

# 6 Tech Stack:
    In this project we are using
        a) Django 3.0.7 with python 3.7.5
        b) postgresql with psycopg2
        c) EC2 of AWS for servers
        d) RDS for postgresql deployment

    
# 7. How to run test cases:
1. Run `coverage run ./manage.py test` to run Django tests and ensure no errors
2. Run `cov-check.sh` to check code coverage and ensure it give a pass message


# 8. Work Flow:
1. Create a store using "/api/v1/stores/" POST API
2. Create a branch for store created above by using "/api/v1/branches/" POST API
3. To allow a customer to provide a PDF document (invoice) to process
    * Upload the pdf document using "/api/v1/documents/" POST API
4. To track a document’s digitization status or to retrieve the structured invoice information
    * Get Document Details using "api/v1/documents/<document_id>" GET API
    * meta_data field contains structured invoice information
5. To manually add digitized  information for a specific document 
    * Create a invoice for given branch and document by using "/api/v1/invoices/" POST API
6. To add/update more than one field at a time
    * Update Invoice using "/api/v1/invoices/<invoice_id>" PUT API
7. To mark a document as “digitized”
    * Update Document using  "api/v1/documents/<document_id>" PUT API

# 9. Postman Collection:
https://www.getpostman.com/collections/822b4e0c266facb800f2 
