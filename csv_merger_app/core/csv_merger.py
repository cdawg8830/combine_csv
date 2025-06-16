import pandas as pd
import os

class CSVMerger:
    @staticmethod
    def merge_files(file_paths, output_path):
        error_report = []
        dataframes = []
        headers_set = set()
        all_columns = set()
        
        for path in file_paths:
            try:
                df = pd.read_csv(path)
                dataframes.append(df)
                headers = tuple(df.columns)
                headers_set.add(headers)
                all_columns.update(df.columns)
            except Exception as e:
                error_report.append(f"Error reading {os.path.basename(path)}: {e}")
        
        if len(headers_set) > 1:
            error_report.append("Warning: Not all files have matching headers. Columns will be unioned and missing values filled with blanks.")
        
        # Reindex all dataframes to union of columns
        all_columns = list(all_columns)
        for i, df in enumerate(dataframes):
            dataframes[i] = df.reindex(columns=all_columns)
        
        try:
            merged = pd.concat(dataframes, ignore_index=True)
            merged.to_csv(output_path, index=False)
            return True, '\n'.join(error_report)
        except Exception as e:
            error_report.append(f"Error during merging or saving: {e}")
            return False, '\n'.join(error_report) 