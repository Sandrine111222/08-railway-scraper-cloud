# Description 📊




This project creates a real-world data pipeline that fetches train departure data from the [iRail API](https://docs.irail.be/), normalizes it, and stores it in a SQL database — all deployed using Microsoft Azure.


---

# Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Dataset](#dataset)  
- [Building the SQL pipeline](#building-the-sql-pipeline)   
- [Creating visuals in PowerBI](#creating-visuals-in-powerbi)
- [Deployment to Azure] (#deployment-to-azure)
- [Project Structure](#project-structure)   


---

# Project Overview

This project is structured in three progressive levels:

- 🟢 Setting up the core functionality — fetch and store data via Azure Portal using Azure Functions and Azure SQL Database
- 🟡 Adding automation (scheduling), build a live dashboard (e.g., Power BI), and enable data refresh.
- 🔴 Exploring full DevOps integration — CI/CD pipelines, scripting with Azure CLI, Docker deployment, and cloud-native infrastructure as code.

Due to license restictions in Azure (multiple accounts which cannot be deleted), another approach was chosen based on CSV file creation 
using VSCode and Python. Uploading to GitHub allowed deployment to Azure. 


---

# Features

Taking the project to production-grade deployment using DevOps practices and cloud scripting.


---

# Dataset

The raw dataset is structured as CVS files stocked in a CVS storage.



  
  
---

# Building the SQL pipeline


## Key steps

1. **Cleaning of the data**  
   - Put everything in English only.
   - Correct spelling mistakes.
   - Group into smaller amount of subcategories per table.
   - Handle "zero" and "NULL". 

2. **Answer 10 questions**  
   - Key business questions:
      1. What is the price distribution of menu items?
      2. What is the distribution of restaurants per location?
      3. Which are the top 10 pizza restaurants by rating?
      4. Map locations offering kapsalons (or your favorite dish) and their average price.

   - Open ended questions:

      1. Which restaurants have the best price-to-rating ratio?
      2. Where are the delivery ‘dead zones’—areas with minimal restaurant coverage?
      3. How does the availability of vegetarian and vegan dishes vary by area?
      4. Identify the **World Hummus Order (WHO)**; top 3 hummus serving restaurants.
      5. What are the top 10 restaurants for deserts?
      6. What are the 10 worst restaurants?
    
   - SQL queries have been optimized for speed and readability.

3. **Store in CSV files**  
   - CSV files circumvent SQLite extension issues and PowerBI restrictions.

---

# Creating visuals in PowerBI


- Maps, tables, bar charts are made accordingly to the desired question.
  


---


# Project Structure

```bash
delivery-market-analysis/
│
├──cleaned_db.sql
├──ER_schema_takeaway.png
├──pipeline_sql.py
├──README.md
├──Top 10 pizzas.pbix
├──csv_exports
│    └──best_value_restaurants.csv
│    └──delivery_dead_zones.csv
│    └──kapsalon_map.csv
│    └──price_distribution.csv
│    └──restaurants_per_city.csv
│    └──top_10_pizza_restaurants.csv
│    └──veg_vegan_distribution.csv
│    └──world_hummus_order.csv
└── venv/  
     

---


This project is part of AI & Data Science Bootcamp training at **`</becode>`** and it written by :

- Sandrine Herbelet  [LinkedIn](https://www.linkedin.com/in/) | [Github](https://github.com/Sandrine111222)# 🚆 Azure Train Data Project with iRail API






## 🧠 Project Vision

Using the [iRail API](https://docs.irail.be), your mission is to create a **live, cloud-native dashboard** that gives insight into train operations in Belgium. You'll gather real-time public transport data, structure and store it in the cloud, and visualize it in a way that's useful and meaningful.

You're encouraged to bring **your own ideas and creativity**. The iRail API offers a variety of data: live departures, delays, connections, train routes, and more. Your final dashboard should **tell a story**, answer real-world questions, or help someone make smarter decisions about train travel.

## 💡 Example Use Cases to Consider Early

These are some potential directions your dashboard could take. Pick one early to help you decide:

- **Live Departure Board**: Show current or recent train departures for a selected station
- **Delay Monitor**: Track which stations or trains experience the most delays over time
- **Route Explorer**: Let users check travel time and transfer info between two cities
- **Train Type Distribution**: Visualize where and how different train types (IC, S, etc.) operate
- **Peak Hour Analysis**: Show how train traffic and delays vary by time of day or week
- **Real-Time Train Map** (advanced): Plot moving trains with geolocation



## 🟢 Must-Have: Azure Function Pipeline via Azure Portal

### Objective  
Use the Azure **web portal** (no CLI) to deploy a **Python Azure Function** that fetches live train data and inserts it into an **Azure SQL Database**.

### Azure Services Used

| Azure Service              | Purpose                                       |
|---------------------------|-----------------------------------------------|
| Azure Function App (Python) | Run data ingestion logic as a serverless app |
| Azure SQL Database         | Store normalized train data                   |
| Azure Storage Account      | Dependency for Function App                  |
| App Service Plan (Consumption) | Host the Function with autoscaling      |

### Steps

1. **Create Azure SQL Database** via the portal:
   - Use the “Create a resource” wizard
   - Set up firewall to allow external IP
   - Note the connection string for later use

2. **Create an Azure Function App**:
   - Use “Python 3.10” as the runtime
   - Deploy an HTTP-triggered function using the web editor
   - Use environment variables for credentials (in App Settings)

3. **Implement the logic** to:
   - Call the iRail API (`/liveboard` or /`connections`)
   - Normalize the JSON using Python libraries (e.g., pandas)
   - Connect and write to Azure SQL

4. **Test the Function** directly from the portal and verify that the data appears in your SQL table.

### Deliverables

- ✅ Deployed Azure Function (HTTP endpoint)
- ✅ Azure SQL DB with at least one filled table
- ✅ Documentation (README) describing your process
  
## 🟡 Nice-to-Have: Automation, Power BI, and Scheduling

### Objective  
Extend the project by automating data ingestion and building live dashboards.

### Additions

1. **Scheduled Data Fetching**
   - Add a **Timer Trigger** to your Function App
   - Fetch new data every hour (or another interval)
   - Ensure duplicate entries are handled in your SQL table

2. **Live Power BI Dashboard**
   - Connect **Power BI Service (online)** to Azure SQL
   - Create visuals: bar charts, line graphs (e.g., trains per hour)
   - Publish and embed the dashboard (optional)

3. **Improved Data Schema**
   - Normalize additional fields like platform, status, vehicle type
   - Use proper SQL data types: `DATETIME`, `INT`, `VARCHAR`

4. **Logging & Monitoring**
   - Use Azure Application Insights for runtime metrics and error tracking
   - Log custom events in your Function

## 🔴 Hardcore Level: CI/CD, Azure CLI, and DevOps Automation




### Advanced Features

1. **CI/CD Pipeline**  
   - Automate building, testing, and deploying your Function App and infrastructure.  
   - Use GitHub Actions or Azure DevOps Pipelines for repeatable, reliable delivery.

2. **Infrastructure as Code with Terraform**  
   - Define and provision Azure resources declaratively using Terraform configs.  
   - Enables version-controlled, repeatable infrastructure deployments integrated into your pipeline.

3. **Azure CLI and Scripting Automation**  
   - Write Python or shell scripts to automate Azure resource management and configuration tasks.  
   - Useful for custom setup steps not covered by Terraform or CI/CD tools.

4. **Authentication and Security Best Practices**  
   - Implement Managed Identities to avoid hardcoded secrets.  
   - Secure Function endpoints with OAuth, API keys, or Azure AD integration.

5. **Containerization with Docker**  
   - Package your Azure Function or pipeline code in Docker containers.  
   - Deploy containers to Azure Container Registry and run via Azure Functions Premium Plan or Azure Container Apps.


## 📝 Evaluation Criteria

| Category                      | Must-Have | Nice-to-Have | Hardcore Level     |
|------------------------------|--------------|----------------------|----------------------------|
| Function App is deployed     | ✅            | ✅                    | ✅                          |
| SQL DB contains live data    | ✅            | ✅                    | ✅                          |
| Code structure and clarity   | Basic        | Good abstraction     | Modular, reusable          |
| Automation & scheduling      | ❌            | ✅                    | ✅ with pipeline automation |
| Dashboard                    | ❌            | ✅ Power BI Live      | ✅ Auto-refresh + embed     |
| Deployment strategy          | Manual       | Partial scripts      | Full CI/CD pipeline         |
| Use of environment configs   | Basic         | Partial              | Secrets vault or managed ID|


## ✅ Submission Checklist

- [ ] GitHub repo with all source code and README
- [ ] Screenshot of Function App test run
- [ ] Screenshot of SQL data table
- [ ] If applicable, link to Power BI dashboard
- [ ] (Optional) CI/CD pipeline config and diagram


## 🔚 Final Notes

- Focus first on getting your **Function App to insert real data**
- Treat each level as an **independent milestone**


                     +--------------------+
                     |  iRail API         |
                     |  (Live Departures) |
                     +---------+----------+
                               |
                               v
                     +--------------------+
                     | Python Azure       |
                     | Function / Local   |
                     | Pipeline Script    |
                     +---------+----------+
                               |
     -----------------------------------------------------------
     |           |              |             |               |
     v           v              v             v               v
+-----------+ +-----------+ +-----------+ +-----------+ +-----------+
| Live      | | Delay     | | Train     | | Peak      | | Route &   |
| Departures| | Monitor   | | Type Dist | | Hour      | | Map       |
| CSV       | | CSV       | | CSV       | | Analysis  | | CSV       |
+-----------+ +-----------+ +-----------+ +-----------+ +-----------+
     |           |              |             |               |
     -----------------------------------------------------------
                               |
                               v
                     +--------------------+
                     | Power BI / Excel   |
                     | Dashboards &       |
                     | Visualizations     |
                     +--------------------+
Flow Description

iRail API:

Source of all live train data (station, time, delay, platform, train type, route, coordinates)

Python Azure Function / Local Pipeline:

Fetches, normalizes, and appends the data into CSVs

Handles all 6 analysis modules in one run

CSV Outputs:

live_departures.csv → Live Departure Board

delay_monitor.csv → Delays over time

train_type_distribution.csv → IC, S, etc. breakdown

peak_hour_analysis.csv → Departures and delays by hour/day

route_explorer.csv → Route + transfer info

train_map.csv → Geolocation for moving train map

Power BI / Excel:

Reads CSVs for dashboards

Can refresh every 5–15 minutes based on Azure Function schedule

✅ Optional DevOps/Deployment Additions

CI/CD with GitHub Actions: automatically push to Azure Functions when code is updated

Dockerize the pipeline for local reproducibility

Infrastructure as Code: ARM templates or Terraform to set up Function App, Storage, Timer, and Data directories

Monitoring & Alerts: Azure Application Insights can log errors or failed API calls
