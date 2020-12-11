# -*- coding: utf-8 -*-
# import pdfkit
# from html2pdf import HTMLToPDF
from xhtml2pdf import pisa  # ==0.2.4
# https://github.com/xhtml2pdf/xhtml2pdf


def render_pdf(html_str=None, file_name='pdf.pdf'):
    with open(file_name, 'w+b') as pdf_file:
        pisaStatus = pisa.CreatePDF(html_str, dest=pdf_file)
        if pisaStatus.err:
            return 'We had some errors with code %s <pre>%s</pre>' % (pisaStatus.err, html_str)


if __name__ == '__main__':
    html_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8" />
        </head>
        <body>
            <h1>HROne Payslip</h1>
            <h2>Basic Info</h2>
            <table border='1' cellpadding='5'>
                <tr><th align='left' width='200px'>Username</th><td>Tom</td></tr>
                <tr><th align='left'>Employer</th><td>HRTwo</td></tr>
                <tr><th align='left'>Period</th><td>2020-10</td></tr>
            </table>
            <br /><br />
            <h2>Salary Info</h2>
            <table border='1' cellpadding='5'>
                <tr>
                    <th align='left' width='200px'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Category1</th>
                    <td>
                        Basic Salary: 1000 <br />
                        Peformance Salary: 2000
                    </td>
                </tr>
                <tr>
                    <th align='left'>Social Insurance</th>
                    <td>
                        Pension: 800 <br />
                        House Fund: 600
                    </td>
                </tr>
                <tr>
                    <th align='left'>Net Salary</th>
                    <td>
                        Net Salary: 800
                    </td>
                </tr>
            </table>
        </body>
        </html>
    """
    file_name = 'test.pdf'

    # pisa.showLogging()
    render_pdf(html_str, file_name)

    pass

