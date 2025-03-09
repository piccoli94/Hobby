from pdfrw import PdfReader, PdfWriter, PdfDict

# Define the path to the input and output PDF files
input_pdf_path = 'Scheda Hope v.2 edit.pdf'
output_pdf_path = 'output.pdf'

# Define the data to fill in the PDF form
data = {
    '(Text1)': 'Danilo',
    # Add more fields as needed
}

# Read the input PDF
template_pdf = PdfReader(input_pdf_path)

# Iterate through the pages and fill the form fields
for page in template_pdf.pages:
    annotations = page.Annots
    if annotations:
        i=0
        for annotation in annotations:
            field = annotation
            field_name = field.T
            print(f"{field_name} \n")
            field.update(
                PdfDict(V=str(i)) )
            i=i+1            
#            if field_name in data.keys():
#                field.update(
#                    PdfDict(V=data[field_name])
#                )

# Write the filled PDF to the output file
PdfWriter().write(output_pdf_path, template_pdf)

print(f'Filled PDF saved to {output_pdf_path}')