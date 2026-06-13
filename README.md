# capstone

## SmartCRM: Customer Relationship Management System

## Project Overview & Intent
SmartCRM is a full-stack, enterprise-ready web application engineered to solve real-world operational bottlenecks for growing small businesses. The system provides a centralized platform to organize customer data, track sales leads and deals, log communication history and track every task associated with an individual deal. 

## Why I Built It
I built this CRM project to solve a real-world business operational challenge for small businesses. Many small businesses struggle to manage customer data from lead stage to deal closure and often relying on scattered and unorganized spreadsheets that lack real-time monitoring, structured relationships, or communication logs. 
The intention is to challenge myself by building an operational enterprise grade solution. This project allowed me to implement complex data modeling, manage multi-layered relational databases, handle secure user permissions, and write highly responsive JavaScript to optimize administrative workflows.

## Distinctiveness 
#This CRM application is entirely distinct from all previous projects assigned in this course. It moves away from trivial social media interactions or consumer e-commerce systems, operating instead as a complex, data-driven Business-to-Business (B2B) application:
**Unlike Project 1 (Wiki):** The project does not focus on Markdown file conversion or basic encyclopedia routing. It is a highly dynamic, relational transactional engine.
**Unlike Project 2 (Commerce):** The project focuses on long-term B2B (Business-to-Business) relationships, complex data tracking, and dashboard summary while moving away from consumer e-commerce structures like bidding and auction logic.
**Unlike Project 3 (Mail):** While Project 3 handled a single type of messaging model, this CRM architecture manages leads, activities, distinct business/deal accounts, and task historical record.
**Unlike Project 4 (Network):** The project goes beyond a simple social media timeline. It implements role-based permission, tracks numeric monetary and deal stages, and features status histories rather than basic text posts and "likes".

## Complexity 
The system's engineering depth is demonstrated through several critical layers that ensure security, speed, and structural integrity:
** Relational Database Model:** Built with Django, the database handles asymmetric relationships, Cascading deletions, and explicit lookup foreign keys (User, Role, Lead, Deal, Activity and Task).
** Asynchronous AJAX Actions:** The UI leverages JavaScript fetch API calls to transition sales leads through Kanban steps, add interactive call notes, and update statuses instantaneously without forcing full page reloads.
** Granular Access Control:**  Data queries are filtered dynamically in Django views so team members see only their assigned or logged clients, while managers retain full global view over the corporate sales funnel.
**Front-end Responsiveness:** Custom CSS structures ensure that large interactive tables and detailed analytical layouts remain clean on both mobile and desktop screens.

##  File Structure and Written Code Descriptions
This section lists and explains the specific purpose of the files written for this application.

### Backend Architecture (`smartcrm/`)
**smartcrm /models.py**: Contains the application database architecture. This includes the User model, Lead model (business entities), the Deal model (tracking pipeline metrics and stages), the Activities model (storing timestamped communication logs) and the Task (storing timestamped to-do logs).
*smartcrm/views.py: This controls the core back-end server logic of the application. It contains python views for handling user authentication, deal/pipeline stage changes, RESTful API endpoints for asynchronous JavaScript components, and authorization enforcement rules.
*smartcrm/urls.py: This maps the application endpoints. It defines paths for user entry points, individual dynamic lead and deal profiles, API routes for data fetching, and dashboard generation views.
*smartcrm/serializer.py: This acts as the vital bridge between my database and the frontend of the application. It converts complex Django QuerySets and Model instances into native Python primitives.
*smartcrm/forms.py: This manages user input collection, validation, and database storage for server-rendered web pages. It automatically handles CSRF (Cross-Site Request Forgery) protection to prevent malicious data injections into my CRM database.
*Smartcrm/admin.py: This configures and controls the internal management dashboard used by managers, and administrators to assign roles and oversee data.

### Static Assets (`smartcrm/static/`)
**`smartcrm/js/`**: This handles the interactive UI lifecycle. This file captures client-side events, tracks toggles, and initiates asynchronous HTTP requests via the Fetch API to save or update records in the background.
**`smartcrm/css/`**: This manages styling of the font and overall look of the application.

## Template Architecture (`smartcrm/templates/smartcrm/`) 
The interface layer is split into specialized HTML views that extend a common layout. This holds the UI layout templates of the application:
**`layout.html`**: The base shell for the entire web application. It includes global metadata, imports required stylesheet files, establishes navigation menus that adapt to a user's permission level, and mounts shared JavaScript modules.
**`index.html`**: The central operational dashboard. It provides a visual summary of the sales funnel, aggregate pipeline values, urgent tasks, and recent activity updates to keep users aligned on priorities.
*lead_detail.html`**: This shows the individual lead details, new log activity, and a historical timeline of logged activities.
**`lead.html`**:  Renders a comprehensive overview of all registered prospects, incorporating sorting parameters, pagination tools, and filtering fields to navigate large volumes of contacts efficiently. 
**`add_lead.html`**: A clean workspace containing the validated creation form used to parse, clean, and register new customer entries into the core database.
**`deal_detail.html`**: This shows the profile of the deal. This also features the deal status update as well as the adding of task to the deal.
**`deals_list.html`**: Displays categorized sales deals using toggleable UI tabs. Users can switch views between active open cycles, won accounts, and lost opportunities to inspect performance.
**`task_detail.html`**: This features the task form for an individual deal. Each task will be submitted and be transferred to the task dashboard.
**`task_dashboard.html`**: The central interface for task management. It organizes action items into toggleable tabs for pending and completed tasks, enabling teams to track outstanding deliverables.

## Tech Stack Used
* Backend:  Django (Python)
* Frontend: JavaScript, HTML5, CSS3 / Bootstrap
* Database: SQLite (Development)

## Installation and Execution Guide
Ensure you have Python 3 installed on your local environment.

# Step-by-Step Execution
1. Clone the project repository:
   ```bash
   git clone < https://github.com/sammyades/capstone.git >
   cd <capstone>
   ```
2. Perform database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Create an administrative user (Optional but recommended.
  python manage.py createsuperuse

4. Start the local development server:
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0` to test and utilize the CRM system.
