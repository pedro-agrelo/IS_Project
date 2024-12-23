# Contents
- [Overview](#overview)  
- [What is Projecta?](#what-is-projecta)  
- [Target Audience](#target-audience)  
- [About this User Guide](#about-this-user-guide)  
- [Getting Started with Projecta](#getting-started-with-projecta)  
- [Main Features](#main-features)  
- [Side Menu](#side-menu)  
- [Importing a File Section](#importing-a-file-section)  
- [Spreadsheet Section](#spreadsheet-section)  
- [Variables Section](#variables-section)  
- [Missing Data Section](#missing-data-section)  
- [Model graph section](#model-graph-section)  
- [Model information section](#model-information-section)  
- [Model description section](#model-description-section)  
- [Prediction section](#prediction-section)  
- [Downloading Projecta](#downloading-projecta)  
- [Installing Projecta](#installing-projecta)  
- [Using Projecta](#using-projecta)  
- [Importing Files](#importing-files)  
- [Preprocessing Data](#preprocessing-data)  
- [Selecting the Variables](#selecting-the-variables)  
- [Handling Missing Data](#handling-missing-data)  
- [Creating a Linear Regression Model](#creating-a-linear-regression-model)  
- [Predicting data](#predicting-data)  
- [License Information](#license-information)  
- [Contacting Our Team](#contacting-our-team)  

## Overview
This ReadMe file is a user guide for our new release software—Projecta. You can download the software from our GitHub repository. The software is lightweight and compatible with only personal computers. However, Projecta can work on the following platforms:
- MacOS
- Windows
- Linux

## What is Projecta?
Projecta is software that predicts information using the linear regression model. It works with any type of variable.

## Target Audience
Projecta aims to reach professional and academic audiences in any sector that needs to work on projecting data based on historical information.

## About this User Guide
This user guide walks users through the software's functioning, covering its primary and advanced functionalities and providing step-by-step instructions.

## Getting Started with Projecta
The Getting Started section will help you understand the software, including:
- the software’s features, 
- the user interface with specific explanations, and 
- how to download and install the software.

## Main Features
Projecta predicts a variable's value based on other variables' values. The software features include:
- Allow you to add a description if you need it for other purposes of presentation or input to other documentation.
- Save the model to review next time.
- Create a new separate file with prediction data.

The user interface contains three main screens:

| Stages                          | Screen               | Details                                                                                     |
|----------------------------------|----------------------|---------------------------------------------------------------------------------------------|
| Import a database file          | Welcome screen       | - software’s file formats.                                                                  |
| Adjust and collect data before creating a linear model | Preprocessing data screen | - A spreadsheet section. <br> - The entry columns section to select values of entry variables that you use to predict. <br> - The target column section to select a variable that you want to predict its value. <br> - Handle missing data section to process the empty cells before the prediction stage. <br> **Note**: The software cannot predict data if the spreadsheet has empty cells. <br> - Create a linear model button. |
| Create a model or load a model  | Linear model screen  | - Graph section with a regression line in a coordinate plane having two axes: the horizontal and vertical axes with actual data. <br> - Model information section with formula, training MAE, and test MAE. <br> - Prediction results section. <br> - Description section to enter the description of your model. <br> - Buttons to save the description and model. |

**Table 1**: A list of the screens in order when users predict data and the details of those screens.

## Side Menu
You can use the side menu to:
- Create a New Model
- Load a Model
- Read the User Guide

You can access it by clicking the three-line button. See **Figure 1**.

![sidemenu](https://github.com/user-attachments/assets/2b254745-4f1b-4fef-9c89-71c9e6a05afa)
**Figure 1**. Side menu.

## Importing a File Section
You can import a database file to create a new model or load a saved model. You can import a file from:
- The side menu. See **Figure 2**.
- The built-in section in the main interface. See **Figure 3**.

![figure2](https://github.com/user-attachments/assets/e31376a6-8e9d-48dd-afeb-e28ff0b8acd8)

**Figure 2**. Importing a File initial interface. 

![figure3](https://github.com/user-attachments/assets/2c22804c-8bb0-46ad-a496-af5c439fe2cd)
 
**Figure 3**. Importing a File main interface.

## Spreadsheet Section
This section contains all the granular data from the imported file. The interface shows the specific values in columns and rows. The software only predicts numerical values. See **Figure 4**.

![figure4](https://github.com/user-attachments/assets/ec540ed9-4d66-4c6d-8894-ab589bee4ab6)

**Figure 4**. Spreadsheet section.

## Variables Section
This section includes:
- Entry columns — the independent variables selection section—you can select the columns for the input variable(s).
- Target column — the dependent variable selection (target) section—you can select the column for the output value. The software will create a model with the prediction data in the target column.

See **Figure 5**.

![figure5](https://github.com/user-attachments/assets/78e17586-c425-4e6b-88c1-6125de912e1b)


**Figure 5**. Variables selection section.

## Handle Missing Data Section
The handle Missing Data section has a dropdown list that contains options to handle empty cells with no value, such as “n/a,” “na,” “non,” and “nan.” The software offers different options:

| Options                    | Functions                                                                 |
|----------------------------|---------------------------------------------------------------------------|
| Remove rows                | To delete the entire row that contains the empty cell(s).                |
| Fill with mean             | To fill all empty cells with the mean of the remaining cells’ column values. |
| Fill with median           | To fill all empty cells with the median of the remaining cells’ column values. |
| Fill with constant value   | To fill all empty cells throughout the row with a specific value. You must manually enter the constant value. |

**Table 2**: Options in the Handle Missing Data dropdown list.  
See **Figure 6**.

![figure6](https://github.com/user-attachments/assets/87a53bd1-f33a-406c-b6f8-e635d086460e)

**Figure 6**. Missing data section.

![figure7](https://github.com/user-attachments/assets/df3d17ca-70c8-48e3-854b-d1bf4395e35b)

**Figure 7**. : Handle Missing Data options in the dropdown list.

## Model graph section
This section shows the graph with a regression line in a two-axis coordinate plane; see 

![figure8](https://github.com/user-attachments/assets/38fb816e-abc9-4d1b-90b5-d31d4994a831)

- The Y-axis represents the target column.
- The X-axis represents the entry column.

**Figure 8**: Model graph section.

## Model information section
This section shows the statistical data about the model:
- The linear regression formula is an equation that contains factors representing the turnout in the data prediction. This equation adjusts to the principle:
  - `y = mx + b`

  | Factors | Meanings           |
  |---------|--------------------|
  | y       | the dependent variable |
  | x       | the independent variable |
  | m       | the regression coefficient |
  | b       | the error term |

  **Table 3**: Factors in the linear regression formula.
- The Training Mean Absolute Error (Training MAE) evaluates the performance of a machine learning model on the training dataset.
- The Test Mean Absolute Error (Test MAE) estimates different test datasets that the model does not recognize as usual during the training.
- The R² is a coefficient to predict future outcomes. The coefficient determines the quality of the model in replicating the results and the proportion of variation in the outcomes that the model can explain.

See **Figure 9**.

![figure9](https://github.com/user-attachments/assets/a19d93e1-362d-4944-ba1c-3c7b48e46685)

**Figure 9**: Model information section.

## Model Description section
You can add a description related to the model. See **Figure 10**.  

![figure10](https://github.com/user-attachments/assets/c2112f66-2081-4649-ba71-42b873395c33)

**Figure 10**: Model Description section.

## Prediction section
In this section, you can enter a value for the independent variable and get a predicted value—dependent variable. See **Figure 11**.

![figure11](https://github.com/user-attachments/assets/5a16e8ab-3865-4acd-a99b-8cd2bfce5983)

**Figure 11**. Prediction section.

## Downloading Projecta
You can download Projecta from our GitHub repository.  
To download Projecta:
1. Select Code to view the download options.  
   The Local dropdown menu opens.

![figure12](https://github.com/user-attachments/assets/828ef898-cce0-4884-bd68-042a987ed75a)

   **Figure 12**: The Local dropdown menu from the GitHub repository.
3. Select Download ZIP to download the software.

## Installing Projecta
You must extract the ZIP file to install the software.  
To Install Projecta:

1. Navigate to the folder you extracted from the ZIP file.
2. Enter in the cmd `pip install -r requirements.txt` to install the dependencies.  
   **Note**: Check the requirements for Python from `requirements.txt`.
3. Double-click the `Interface.py` to open the file and then run this file.

## Using Projecta
In this section, we guide you through the execution process. The four main stages:
1. Importing a file.
2. Preprocessing data.
   - Selecting the input variables.
   - Handling missing data.
3. Creating a linear regression model.
4. Predicting data.

## Importing Files
Projecta can import from local storage various database file formats: 
- CSV
- Microsoft Excel
- SQLite

To import a file from the side menu:
1. Select New Model in the side menu. See **Figure 2**.  
   The Select File dialog window opens.


   **Figure 12**: Select File dialog window.
2. Navigate to the folder you need to import the file from.
3. Select the file you need to import.
4. Select Open to import the file.  
   The spreadsheet appears in the input variable interface. See **Figure 4**


#### To Import a File from the Main Interface
1. Select **New Model** in the side menu. See **Figure 3**.  
   The **Select File** dialog window opens. See **Figure 13**.
   ![figure13](https://github.com/user-attachments/assets/00189b2d-2c5b-4896-ae83-a286626f9f2e)  
3. Navigate to the folder you need to import a file from.  
4. Select the file you need to import.  
5. Click **Open** to import the file.

## Preprocessing Data
After importing a database file, you can select the variables to create the model.

### Selecting the Variables
Projecta needs one or more variables (column headers of the spreadsheet) as input to predict a target variable. You must select both the **entry** and the **target** columns.

#### To Select the Entry Variables:
1. Select **Single Selection** or **Multiple Selection** in the **Entry Columns** section.  
2. Scroll to the list of variables.  
3. Select the variable(s). See **Figure 14**.

![figure14](https://github.com/user-attachments/assets/99b50a6d-6010-4429-8c6e-2262d1530a11)
     
   **Note:** A **Single Selection** is only for one variable. A **Multiple Selection** is for two or more variables. For multiple selections, you can select the multiple entry columns you need.

#### To Select a Target:
1. Scroll to the list in the **Target Column** section.  
2. Select the target. See **Figure 15**
   ![figure15](https://github.com/user-attachments/assets/8d6bfb49-5935-4f22-9d8e-88e465ec017b) 
3. Select **Confirm columns selection**.  
   A **Success dialog** window opens. See **Figure 16**.
   ![figure16](https://github.com/user-attachments/assets/b6ca335c-477b-465b-9342-d30c4bf4ee23)
4. Select **OK** to close the Success dialog window.  
   The software selects your entry and target columns.  
   **Note:** To change the variables, you must import a file again.

## Handling Missing Data
You must handle empty cells before creating a linear regression model. The software cannot predict data if your entry and target columns have empty cells. See **Selecting the Variables** to work on the missing data section.  
Projecta has four strategies to handle missing data:  
- Remove rows  
- Fill with Mean  
- Fill with Median  
- Fill with Constant Value. See **Table 2**.  
You should highlight the empty cells in your spreadsheet before you decide which strategy to use to handle the missing data.

### To Display the Empty Cells
**Note:** You must select the Entry and Target columns to see the empty cells. See **Selecting the Variables**.  
1. Select **Show Empty Cells** in the **Handle Missing Data** section.  
   The empty cells appear in red in the spreadsheet section. See **Figure 17**.  
2. Scroll through the spreadsheet section to see all empty cells.

   ![figure17](https://github.com/user-attachments/assets/2b6c2270-5be6-46f6-80b9-4a01c45bfef2)

### To Select a Strategy for Missing Data
1. Select the dropdown list in the **Handle Missing Data** section. See **Figure 18**.

![figure18](https://github.com/user-attachments/assets/a00af08f-295b-46da-a067-396fe6605c5f)
   
2. Select the action you want to apply to the empty cells. See **Table 2**.  
   The software applies the strategy for both entry and target variables.  
   **Note:** Enter a value in the constant value box if you select **Fill with Constant Value**. See **Figure 19**.
![figure19](https://github.com/user-attachments/assets/86b7e677-5585-4783-9a0a-279022a3df63)
3. Select **Apply**.  
   The **Success dialog** window opens. See **Figure 20**.

![figure20](https://github.com/user-attachments/assets/bec059de-a3b1-43eb-b2ae-3f6e3a6f4193)
   
4. Select **OK** to confirm the strategy and close the dialogue window.  
   The software applies the strategy and closes the dialogue window.

## Creating a Linear Regression Model
The software creates a linear regression model in a graph after you complete the preprocessing stage. See **Preprocessing Data**.  
You can add descriptions for each linear model to help you navigate and find the model you saved next time.

### To Create a Linear Regression Model:
1. Preprocess data.  
   a. Select the Entry and Target columns.  
   b. Select a strategy for missing data cells.  
2. Select **Create Linear Model**.  
   The linear model screen appears. See **Figure 7**.

### To Save the Linear Model Description:
1. Enter the description of the model in the description box.  
2. Select **Save Description** to save the description into the model.  
   The software adds the model description you just saved. See **Figure 9**.  
   **Note:** You can enter a new description and select **Save Description** anytime to update the model description.

### To Save the Linear Regression Model:
1. Select **Save Model**.  
   The **Save Model** dialog window opens. See **Figure 21**.

![figure21](https://github.com/user-attachments/assets/55867132-a747-4963-afaf-b573e7f55afe)
   
2. Navigate to the folder you want to save the model.  
3. Enter the model’s name in the file name box.  
4. Select **Save** to save the model.  
   **Note:** You can use Notepad to open the saved model.  
   The **Success dialog** window opens. See **Figure 22**.  
5. Select **OK** to close the Success dialog window. See **Figure 22**.

   ![figure22](https://github.com/user-attachments/assets/cf54a678-c437-483e-87c4-b3adca6ff2d8)

## Predicting Data
After creating a model, you can get a target value with your specific entry value. See **Creating a Linear Regression Model**.

### To Predict Data:
1. Enter a value in the **Entry Column** box. See **Figure 10**.  
2. Select **Predict**.  
   The new value appears in the **Prediction** field. See **Figure 23**.

   ![figure23](https://github.com/user-attachments/assets/52fefd97-9faf-49fa-b116-e76e5af5be9b)

## Getting Help
You can select the **User Guide** from the side menu to get help. The **User Guide** provides step-by-step instructions to:
- Create a new model.
- Load a saved model.

### To Read the User Guide:
1. Select the side menu.  
2. Select the **User Guide**. See **Figure 24**.  
   The software shows the User Guide.

   ![figure24](https://github.com/user-attachments/assets/3cc5899a-6076-475d-83b7-6a08af70c825)

## License Information
Copyright© 2024 Projecta.  
Our team grants permission, free of charge, to any person obtaining a copy of this software and associated documentation files to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and sublicense. We permit the following conditions:
- All copies or substantial portions of the Software must include the above copyright notice and this permission notice.  
- We provide the software "as is” without warranty of any kind. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of tort or arising from out of or in connection with the software or the use of the software.

## Projecta GitHub Repository
[https://github.com/pedro-agrelo/IS_Project](https://github.com/pedro-agrelo/IS_Project)

## Developed by:
- Diego Lopez Gonzalez
- Sergio Pérez Vilar
- Santiago Brunet Muñiz
- Pedro José Agrelo Márquez
- Hugo Garabatos Díaz

## Written by:
- Eduardo Talledo
- Mai Dang

## Contacting Our Team
Project Link: [https://github.com/pedro-agrelo/IS_Project](https://github.com/pedro-agrelo/IS_Project)

## Contributors
**Software Developers:**
- Diego Lopez Gonzalez
- Sergio Pérez Vilar
- Santiago Brunet Muñiz
- Pedro José Agrelo Márquez
- Hugo Garabatos Díaz

**Technical Documentation Writers:**
- Eduardo Talledo
- Mai Dang

