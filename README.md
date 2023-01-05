# CI/CD with Azure Pipelines
 
 This is a sample pipeline on Azure DevOps pipeline.
 The piepline utilizes data from a sample API (TOMTOM Traffic data for 3 regions)
 
 Azure pipelines enables the use of variables to store credentials and ultiumately utilize them in script to be run in the pipeline 
 these credentials are stored as enviroment variables and can be called in scripts where needed.
 
 ![image](https://user-images.githubusercontent.com/66565804/210675116-333fe3f2-bb00-40b6-a181-e98b5afaf962.png)


 A python script 'TomTom_Traffic_Data.py' which extracts data from the API and uploads the data to a Azure blob in a container.
 This upload processes is facilitated by Azure blob storage modules.
 To set up connectivity to blob storage, a storage account name and a storage account key are needed. 
 This can be found in the network & security tab of the storage account on Azure portal.

Azure pipeline provides an Analytics tab where detailed information about the pipeline runs can be found.

![image](https://user-images.githubusercontent.com/66565804/210675298-30073769-c211-48f0-893b-a030f0de2932.png)


![image](https://user-images.githubusercontent.com/66565804/210675462-de1a629e-7e96-4875-9047-cd82d37adf6c.png)


Azure pipelines also provides options to set up scheduled runs for pipelines. 
This can be done either in the yaml file of the pipeline of by using the UI.

