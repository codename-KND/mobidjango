import base64
from pathlib import Path

from weasyprint import HTML, CSS

"""
    The report class enables you to create simple tabular pdf
    Before using it, you are required to install wasyprint using 
    
    -> pip install weasyprint
    
    ---------------------------Usage--------------------------------
    1. Create an object of the class. e.g pdf_gen = Report()
    2. Give the object the columns to reference e.g pdf_gen.columns = ['first_name','second_name']
    3. Give the object how you want your column headers to appear e.g pdf_gen.display_names = ['First Name', 'Second Name']
    4. Give the object the data to use e.g pdf_gen.data = Students.objects.all()
    5. Give the object a title for your report e.g pdf_gen.title = "A report of all students"
    6. OPTIONAL: you can give the class a logo location. e.g pdf_gen.logo_location = '/students/static/students/images/image.png'
        make sure to start with a slash. The directory must start from your app.
    7. OPTIONAL: you can give an address for your company. To end line use \n. e.g pdf_gen.address = 'Student app\nNairobi' 
    8. Mandatory: call the pdf_generator method and equate it to a variable of your choice e.g pdf_string = pdf_gen.pdf_generator()
    9. Pass the pdf_string to the context e.g return render(request, 'home.html', context={'pdf_strint': pdf_string} ).
    10. In the html file, create an iframe element and give it src to be your context key. e.g 
                <iframe src={{pdf_string}} width=1000 height = 700> 
"""


class Report:
    def __init__(self, data=None, display_names=None, title: str = "", columns=None, address=''):
        self.address = address
        self.logo_directory = None
        if columns is None:
            columns = []
        if display_names is None:
            display_names = []
        if data is None:
            data = []

        self.data = data
        self.display_names = display_names
        self.columns = columns
        self.title = title

    def pdf_generator(self):
        columns: list = self.columns
        title: str = self.title
        display_names: list = self.display_names
        query_set = self.data

        if len(display_names) != len(columns):
            raise ValueError("Columns and display names should match")

        # Generate the header
        header = ""
        index = 0
        for name in display_names:
            header += f'<th align="left">{name}</th>'
            index += 1

        # Generate rows
        table_rows = ""
        counter = 0
        for each in query_set:
            try:
                Ken = getattr(each, 'user')
                print(getattr(Ken, 'password'))
                data_dict: dict = each.__dict__
            except:
                data_dict = each

            color = "#ffffff" if counter % 2 != 0 else "#C5C5C5"
            single_row = f'<tr style="background-color: {color}">'
            for column in columns:
                if len(column.split('.')) <= 1:
                    col_data = str(data_dict.get(column)).capitalize()
                else:
                    index = 0
                    dt = each
                    fields = column.split('.')
                    for element in fields:
                        dt = getattr(dt, element)
                    col_data = dt

                single_row += f"<td>{col_data}</td>"

            single_row += '</tr>'
            table_rows += single_row
            counter += 1

        # Load the logo
        logo_image = ''

        if self.logo_directory:
            with open(str(Path(__file__).resolve().parent.parent) + self.logo_directory, "rb") as image2string:
                converted_string = base64.b64encode(image2string.read())
                img_src = converted_string.decode('utf-8')
                logo_image = f'<img src ="data:image/{self.logo_directory.split(".")[-1]};base64,{img_src}">'
        if self.address:
            self.address = self.address.replace('\n', '<br>', 10)

        html_string = """
                    <div class="header">
                        <div>{logo}</div>
                        <div>{address}</div>
                    </div>
                    <h2>{title}</h2>
                   
                   <table border="1" align="center">
                       <thead>
                           <tr>
                               {header}
                           </tr>
                       </thead>
                       <tbody>
                           {rows}
                       </tbody>
                   </table>

                   """.format(header=header, rows=table_rows, title=title.upper(), logo=logo_image,
                              address=self.address)

        styles = """
            .header{
                display: flex;
                justify-content: space-between;
                height: 100px;
            }
            .header div{
                height: 100px;
            }
            img{
                width: 100px;
                position: relative;
                top: -30px;
            }
            h2{
                text-align: center;
                color: indigo;
            }
            table{
                border: 1px solid black;
                border-collapse: collapse;
                width: 100%;
            }
            tr, td, th{
                border: 1px solid black;
                max-width: 50%;
            }
        """

        html = HTML(string=html_string)

        pdf = html.write_pdf(stylesheets=[CSS(string=styles)])

        base64_bytes = base64.b64encode(pdf)
        base64_string = base64_bytes.decode('utf-8')
        return 'data:application/pdf;base64,' + base64_string
