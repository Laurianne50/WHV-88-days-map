Aim of the code: create a map of Australian cities in which  Working Holiday Visa (WHV) holders can work towards their 88 days.

Context: In Australia, Working Holiday Visa holders need to work 88 days during their first year to be able to renew their visa towards a second year. Work need to be undertaken in specific geographical areas and fields of work. Explanations are provided on the website of the Australian Government [here](https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/work-holiday-417/specified-work) and the map generated in this project is based on these information.  

The map is directly accessible in your browser using [this link](https://laurianne50.github.io/WHV-88-days-map/2026_map_whv.html)

README is in progress

# Step 1
Clone this Git repository.

# Step 2
Create and activate your conda environment
    ```shell
    conda env create -f environment_conda.yml
    ```

# Step 3
Run Processing_of_raw_data.py --> will produce file "Data_postcode_whv.csv"

# Step 4
Run Map_generation.ipynb within Jupyter Notebook --> notebook is made to produce the map as a HTML file
