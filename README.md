# database-code

## About

This repository archives code and intermediate data files used for cleaning, parsing, modifying, and loading data into the London Stage Database between 2013 and 2019. 
This code represents a phase of the project's development and is no longer in use.

The sequence of Python files transforms the data from the London Stage Information Bank into a relational database. The resulting text files were supplemented with OCRed data collected from HathiTrust copies of the [*The London stage, 1660-1800*](https://catalog.hathitrust.org/Record/000200105) by Emma Hallock.

Those interested in the London Stage Database project in its *current form* can search the database on the [project website](https://londonstagedatabase.uoregon.edu/) or download the [underlying SQL database](https://github.com/LondonStageDB/data/releases). 

## Files

### Documentation
* `Process_of_Cleaning_and_Loading_London_Data.txt` 
    - This README documents the steps required for taking input files recovered from Lawrence through the various parsing and data cleanup programs.  
* `London_ERD_Diagram_September_26_2018.pdf` 
    - a proposed entity-relationship diagram mapping the relationship between
    tables in the SQL version of the LSDB. 
    - these constraints were not formalized in the database table definitions at the time

### Code

* `NPK_date_conversion_with_comments.py`
    - Corrects NPK dates for the London Stage Project text files
* `ocr_fix_2-21-18_with_comments.py`
    - Corrects OCR text in London Stage Project text files
* `LondonLoadDatabaseMayOthersZ.py`
    - Cleans London Stage Project text files in preparation for insertion in to a SQL database as tables
* `LondonFormatEverythingMay112019.py`
    - Processing pipeline used to construct `modified_everything_07-03-19_withOrigDataHathiFixed.txt`
* `Ladder.py` 
    - Populates the performance date ladder in the SQL database.

### Data
* `data/LondonFinal.txt`
    - The 2019 final version of the London Stage Project in `.txt` form, used to construct the SQL database
    - Migrated from the LondonStageDB/data repository in 2025
* `data/modified_everything_07-03-19_withOrigDataHathiFixed.txt`
    - An intermediate stage in the project with OCRed data from HathiTrust versions of the *The London stage, 1660-1800*
    - Migrated from the LondonStageDB/data repository in 2025
*  `data/2015_concatenated_LSP_files_from_Lawrence.txt`
    - A 2015 file of concatenated entries recovered from the London Stage Information Bank
    - Migrated from the LondonStageDB/data repository in 2025

### Works Table Development
A folders of plain-text notes, `.docx` files, and intermediate `.xlsx` spreadsheets
documenting the development of the Works table by Emma Hallock in 2019.

This folder was archived in 2025.

#### Documentation
* `works/A Guide to the Works Table EH 4.1.19`
* `works/A Guide to the Works Table EH 4.1.19.docx`

#### Notes
* `works/Authors Researched Log EH 4.1.19`
* `works/Authors Researched Log EH 4.1.19.docx`
* `works/Notes for 1670-1700 EH 4.1.19` 
* `works/Notes for 1670-1700 EH 4.1.19.docx`
* `works/Notes for 1700-1720 EH 4.1.19`
*  `works/Notes for 1700-1720 EH 4.1.19.docx`
* `works/Notes for 1720-1800 EH 4.1.19`
* `works/Notes for 1720-1800 EH 4.1.19.docx`

#### Spreadsheets
* `works/Works Table Final EH 3.15.19 MB 6.19.19.xlsx`
* `works/Works Table Final EH 3.15.19 MB 6.26.19.xlsx`
* `works/Works Table Final EH 3.15.19.xlsx`
    