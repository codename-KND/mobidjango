import pdfkit

class Report:
    def __init__(self):
        self.columns = []
        self.display_names = []
        self.data = None
        self.title = ''
        self.logo_location = ''
        self.address = ''
    
    def pdf_generator(self):
        table_rows = []
        for item in self.data:
            table_columns = []
            for column in self.columns:
                column_value = item.get(column, '')  # Get the value of the column from the item dictionary
                table_columns.append(f'<td>{column_value}</td>')
            table_row = ''.join(table_columns)
            table_rows.append(f'<tr>{table_row}</tr>')
        table_html = ''.join(table_rows)

        html = f'''
        <html>
        <head>
        </head>
        <body>
            <h1>{self.title}</h1>
            <p>{self.address}</p>
            <img src="{self.logo_location}" alt="Logo">
            <table>
                <tr>
                    {"".join(f"<th>{display_name}</th>" for display_name in self.display_names)}
                </tr>
                {table_html}
            </table>
        </body>
        </html>
        '''

        options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',
        }

        # Generate PDF and return as string
        pdf_string = pdfkit.from_string(html, False, options=options)
        return pdf_string
