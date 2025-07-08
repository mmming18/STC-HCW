import pandas as pd
import re


def process_excel_file(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Create a new DataFrame to store the results
    results = []

    # Process each row starting from the second row (index 1)
    for idx, row in df.iloc[1:].iterrows():
        # Get values from columns A, B, C, D, E
        col_a = row.iloc[0] if not pd.isna(row.iloc[0]) else ""
        col_b = row.iloc[1] if not pd.isna(row.iloc[1]) else ""
        col_c = row.iloc[2] if not pd.isna(row.iloc[2]) else ""
        col_d = row.iloc[3] if not pd.isna(row.iloc[3]) else ""
        col_e = row.iloc[4] if len(row) > 4 and not pd.isna(row.iloc[4]) else ""

        if pd.isna(col_e) or col_e == "":
            # If column E is empty, just add the row as is
            results.append({
                df.columns[0]: col_a,
                df.columns[1]: col_b,
                df.columns[2]: col_c,
                df.columns[3]: col_d,
                df.columns[4]: col_e
            })
        else:
            # Split column E by numbered items (e.g., "(1)", "(2)", etc.)
            # Use a regular expression to match numbered items
            items = re.findall(r'\(\d+\)[^()]*(?=\(\d+\)|$)', str(col_e))

            # If no items were found, add the row as is
            if not items:
                results.append({
                    df.columns[0]: col_a,
                    df.columns[1]: col_b,
                    df.columns[2]: col_c,
                    df.columns[3]: col_d,
                    df.columns[4]: col_e
                })
            else:
                # Create a new row for each split item
                for item in items:
                    results.append({
                        df.columns[0]: col_a,
                        df.columns[1]: col_b,
                        df.columns[2]: col_c,
                        df.columns[3]: col_d,
                        df.columns[4]: item.strip()
                    })

    # Convert the results to a DataFrame
    result_df = pd.DataFrame(results)

    # Save the result to a CSV file
    result_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"Processed {len(results)} rows and saved to {output_file}")



# Example usage
if __name__ == "__main__":
    input_file = "风险防控.xlsx"  # Replace with your input file path
    output_file = "风险防控.csv"  # Replace with your desired output file path
    process_excel_file(input_file, output_file)
