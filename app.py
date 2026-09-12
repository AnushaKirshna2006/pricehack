from flask import Flask, render_template, request
from scraper import scrape_amazon_product

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    product_data = None
    error_message = None

    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                product_data = scrape_amazon_product(url)
                if not product_data:
                    error_message = "Failed to scrape the product. It might be a CAPTCHA page or an invalid URL."
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
        else:
            error_message = "Please enter a valid Amazon URL."

    return render_template("index.html", product=product_data, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
