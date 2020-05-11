# MOSS-Plagiarism-Checker
Developed for MSRIT's Information Science Department, under the guidance of Dr. Mydhili K Nair. Developed for the course IS6EB1 (Machine Learning)

About the Project
======
The MOSS-Plagiarism-Checker uses the <a href="https://theory.stanford.edu/~aiken/moss/">Stanford MOSS Plagiarism Checker</a> service to perform the following functions: -

1. Download code from specified git repositories of students for a particular assignment
2. Collate the necessary files from all of the students, and send to MOSS for code plagiarism check
3. The report generated by MOSS is used to **generate detailed reports**
4. Finally, the reports are depicted in the form of a **graph to show students who have similar submissions**

Installation / Setup
======
1. Clone the repo to a folder of your choice

2. Install the required python libararies using
``` pip install -r requirements.txt ```

Configurable Parameters
======
Within `config.yml`, a few parameters have to be changed with every new assignment
<ul>
  <li>
    <code>
      name_of_assignment: "Assignment_MLP"
    </code><br>
    The assignment name has to be of the format <i>Assignment_(nameOfAssignment)</i>
  </li>
  <li>
    <code>
      form_responses_csv: "ML GitHub Link (Responses) - Form Responses 1.csv"
    </code><br>
    The CSV file path should be provided. In this example, it is considered that the CSV file is placed in the root directory of the repo
  </li>
  <li>
    <code>
      language: "python"
    </code><br>
    Specifying the coding language of the submissions while submitting to MOSS. Please refer to <a href="https://theory.stanford.edu/~aiken/moss/">documentation</a>
  </li>
  <li>
    <code>
      threshold_percentage: 50
    </code>
    Specify threshold percentage when generating code similarity (plagiarism) reports from MOSS
  </li>
  <li>
    <code>    
      consolidated_report_name: "ConsolidatedReport_Assignment_MLP.xls"
    </code>
    Use this parameter to specify the name of the consolidated report generated for all students
  </li>
</ul>