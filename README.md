# CSV File Merger GUI for macOS

A user-friendly macOS application for merging multiple CSV files with a simple drag-and-drop interface, error reporting, and progress feedback.

## Features
- Drag-and-drop CSV file/folder selection
- Merge 80-200+ CSV files efficiently
- Manual output filename specification
- Progress bar during merging
- Error reporting (per file/row, plain text)
- Simple data preview
- Clean, modern UI (powered by 21st dev magic)

## Requirements
- macOS (tested on Monterey and later)
- Python 3.9+
- [PyQt5](https://pypi.org/project/PyQt5/) or [PyQt6](https://pypi.org/project/PyQt6/)
- [pandas](https://pypi.org/project/pandas/)

## Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/combine_csv.git
   cd combine_csv
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
- Run the app locally:
  ```sh
  python main.py
  ```
- Drag and drop your CSV files or folders into the window.
- Specify the output filename and start merging.
- View error reports and preview merged data.


## License
MIT 
