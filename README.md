# database-code

## About

This repository archives code and intermediate data files used for cleaning, parsing, modifying, and loading data into the London Stage Database between 2013 and 2019. 
This code represents a phase of the project's development and is no longer in use.

The sequence of Python files transforms the data from the London Stage Information Bank into a relational database. The resulting text files were supplemented with OCRed data collected from HathiTrust copies of the [*The London Stage, 1660-1800*](https://catalog.hathitrust.org/Record/000200105) by Mattie Burkert and Lauren Liebe.

Those interested in the London Stage Database project in its *current form* can search the database on the [project website](https://londonstagedatabase.uoregon.edu/) or download the [underlying SQL database](https://github.com/LondonStageDB/data). 

## Files

### Documentation
* `Process_of_Cleaning_and_Loading_London_Data.txt` 
    - This README documents the steps required for taking input files recovered from Lawrence
      through the various parsing and data cleanup programs.  
* `London_ERD_Diagram_September_26_2018.pdf` 
    - An entity-relationship diagram created by Todd Hugie, mapping implicit relationships
      between tables in the SQL version of the LSDB.
    - These relationships were not implemented as formal database constraints at the time.
      Doing so was unnecessary as that version of the database was not designed for ongoing,
      active modification outside of the initial funded period of performance. 
    - Constraints were added in 2025 to support resumption of active development work.

### Code

* `NPK_date_conversion_with_comments.py`
    - Corrects NPK dates for the London Stage Project text files.
* `ocr_fix_2-21-18_with_comments.py`
    - Corrects OCR text in London Stage Project text files.
* `LondonLoadDatabaseMayOthersZ.py`
    - Cleans London Stage Project text files in preparation for insertion in to a SQL database as tables.
* `LondonFormatEverythingMay112019.py`
    - Processing pipeline used to construct `modified_everything_07-03-19_withOrigDataHathiFixed.txt`
* `Ladder.py` 
    - Populates the performance date ladder in the SQL database.

### Data
* `data/LondonFinal.txt`
    - The 2019 final version of the London Stage Project in `.txt` form, used to construct the SQL database.
    - Migrated from the LondonStageDB/data repository in 2025.
* `data/modified_everything_07-03-19_withOrigDataHathiFixed.txt`
    - An intermediate stage in the project with OCRed data from HathiTrust versions of the *The London stage, 1660-1800*.
    - Migrated from the LondonStageDB/data repository in 2025.
*  `data/2015_concatenated_LSP_files_from_Lawrence.txt`
    - A 2015 file of concatenated entries recovered from the London Stage Information Bank.
    - Migrated from the LondonStageDB/data repository in 2025.

### Works Table Development
A folder of plain-text notes, `.docx` files, and intermediate `.xlsx` spreadsheets
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
    
### London Stage Database PDF Splitting
This folder contains the scripts and intermediate JSON files to slice the original PDFs by date and key the slices to events in the database.

This folder was archived in 2025.

#### Documentation
* `pdf_split/README.md`
    - Documents the Javascript files and intermediate inputs used to generate split PDFs.

#### Code

* `pdf_split/ImportToDB.js`
* `pdf_split/PDF2JSON.js`
* `pdf_split/SplitPDF.js` 
* `pdf_split/webpack.config.js`
* `pdf_split/ZDPDFSplit.js`
* `pdf_split/ZeroDates.js`
* `pdf_split/ZeroDatesFilenames.js`

#### Data

* `pdf_split/pages/dates-final_1659-1700.json`	
* `pdf_split/pages/dates-final_1729-1736.json`	
* `pdf_split/pages/dates-final_1755-1767.json`	
* `pdf_split/pages/dates-final_1783-1792.json`
* `pdf_split/pages/dates-final_1700-1717.json`	
* `pdf_split/pages/dates-final_1736-1747.json`	
* `pdf_split/pages/dates-final_1767-1776.json`	
* `pdf_split/pages/dates-final_1792-1800.json`
* `pdf_split/pages/dates-final_1717-1729.json`	
* `pdf_split/pages/dates-final_1747-1755.json`	
* `pdf_split/pages/dates-final_1776-1783.json`	
* `pdf_split/pages/zero-dates-filenames.json`
* `pdf_split/dates/working-dates_1659-1700.json`	
* `pdf_split/dates/working-dates_1729-1736.json`
* `pdf_split/dates/working-dates_1755-1767.json`	
* `pdf_split/dates/working-dates_1783-1792.json`
* `pdf_split/dates/working-dates_1700-1717.json`	
* `pdf_split/dates/working-dates_1736-1747.json`	
* `pdf_split/dates/working-dates_1767-1776.json`	
* `pdf_split/dates/working-dates_1792-1800.json`
* `pdf_split/dates/working-dates_1717-1729.json`	
* `pdf_split/dates/working-dates_1747-1755.json`	
* `pdf_split/dates/working-dates_1776-1783.json`
