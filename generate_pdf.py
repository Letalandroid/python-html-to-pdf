# pip3 install weasyprint

from weasyprint import HTML
import io
import re
from flask import Flask, Response, request

app = Flask(__name__)

def is_valid_html(content: str) -> bool:
  """Validates that the given string contains basic HTML structure."""
  content = content.strip()
  # Check for at least one HTML tag (opening or closing)
  return bool(re.search(r'<[a-zA-Z][^>]*>', content))

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
  try:
    html_content = request.get_data(as_text=True)

    if not html_content or not html_content.strip():
      return {"error": "Request body is empty. Please provide HTML content."}, 400

    if not is_valid_html(html_content):
      return {"error": "Invalid content. The body must contain valid HTML."}, 400

    pdf_buffer = io.BytesIO()

    HTML(string=html_content).write_pdf(target=pdf_buffer)

    pdf_byte_string = pdf_buffer.getvalue()
    pdf_buffer.close()

    response = Response(pdf_byte_string, content_type="application/pdf")
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"

    return response
  except Exception as e:
    return {"error": f"PDF generation failed: {str(e)}"}, 500

if __name__ == "__main__":
  app.run(debug=True)