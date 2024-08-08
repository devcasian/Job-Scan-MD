# Job Scan MD

Job Scan MD is a web application that scrapes job listings from [rabota.md](http://rabota.md "rabota.md") based on user-provided keywords. It presents the results in a sortable, easy-to-read table format.

## Features

- Web interface for entering job search keywords
- Scrapes multiple pages of job listings from rabota.md
- Displays results sorted by company name
- Responsive design for various screen sizes

## Future Plans

- Integration with Telegram for job notifications

## Installation

1. Clone the repository:
```git clone https://github.com/devcasian/Job-Scan-MD```
2. Go to folder:
```cd Job-Scan-MD```
3. Create a virtual environment and activate it:
```venv\Scripts\activate```
4. Install the required packages:
```pip install -r requirements.txt```

## Usage

1. Run the Flask application:
```python app.py```
2. Open a web browser and navigate to `http://127.0.0.1:5000/`

3. Enter a keyword in the search box and click Search

4. View the results in the table, sorted by company name

## Project Structure

- `app.py`: Main Flask application file
- `templates/`: Contains HTML templates
- `index.html`: Home page with search form
- `results.html`: Results page displaying job listings
- `static/`: Contains static files
- `style.css`: CSS styles for the web interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
