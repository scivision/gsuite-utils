# gsuite-utils
Scripts handy for admining G Suite domains and organizations


## Intsall

0. If Python isn't installed on your computer, download and install
   [Miniconda](https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
1. download this repository to your computer (either via Git or download and extract the Zip file)
2. setup this program
   ```sh
   cd gsuite-utils
   
   pip install -e .
   ```

## Usage

### Bulk User Add
A certain organization with G Suite "mydomain.org" has an Excel spreadsheet from HR Dept. with certain columns when they add new users in bulk.
G Suite wants a specially formatted CSV file. 

1. convert the HR spreadsheet to G Suite CSV
   ```sh
   python bulk_useradd.py newusers.py newusers.csv mydomain.org
   ```
2. upload `newusers.csv` to G Suite via Bulk User Add on `admin.google.com`
