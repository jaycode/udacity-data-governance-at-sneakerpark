# Data Governance (at SneakerPark)

## File Descriptions

### `starter-template.pptx`

The presentation file for project submission.

### `sneakerpark-templates.xlsx`

The spreadsheet for project submission.

### `sneakerpark.sql`

The SQL file to populate the database.

### `generate_data_dict.py` and `data_dictionary.csv`

Who got the time to enter the field names manually from `sneakerpark.sql`? Run this Python script to extract the data dictionary from `sneakerpark.sql`. The generated CSV file will overwrite `data_dictionary.csv`.

Only the "Description" column needs to be updated manually, but ChatGPT can help with that.

### `issues.sql`

The queries I used to find data quality issues in the database.

### `download_csv.ipynb`

When working on Udacity Workspace, do the following to download the CSV files of the tables:

1. Click "Start Postgres" and "Init Database".
2. After running `psql` type the following command:

```
ALTER USER postgres WITH PASSWORD 'pass';
```
3. Then upload the notebook `download_csv.ipynb` to the workspace (click on the folder icon on the left part of the workspace to see the file explorer). Run all the code blocks.
4. Download the files in the `data/` directory (refresh the file explorer if needed).

### `dq_report.pbix`

A PowerBI report of the Data Quality dashboard. I use the downloaded CSV files to create it.

### Lucid Chart files

The ERD and MDM files are available here in lucid.app: https://lucid.app/lucidchart/6595f6f2-0cc7-48ff-bd0a-068fa5af85a2/edit?viewport_loc=388%2C7%2C1576%2C1075%2C0_0&invitationId=inv_63e9e009-aa98-410c-81d9-d9f3c4d9979a