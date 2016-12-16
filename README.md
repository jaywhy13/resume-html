# Resume

I decided to start maintaining my Resume in HTML and CSS. Feel free to fork the project.

Just edit the HTML, then you need to do two things to get it converted to PDF.

- Run python standalone server to server the HTML pages over port 8000. ``python -m SimpleHTTPServer 8000``
- Install wkhtmltopdf library and run ``wkhtmltopdf http://localhost:8000 resume.pdf``
