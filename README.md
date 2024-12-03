# Streamlit-Starter

A scalable, modular, and extensible boilerplate for building Streamlit applications with support for **routing**, **URL parameters**, and reusable **components**.

---

## Features

- **Modular Architecture**: Organized file structure for easy development and scaling.
- **Routing with URL Parameters**: Navigate between pages using query parameters (e.g., `?page=home`).
- **Reusable Components**: Centralized components like navigation bars and sidebars.
- **Decorators**: Easily add logging, authentication, and other reusable logic.
- **Custom Styling**: Support for custom CSS through the `static/` folder.
- **Scalability**: Designed to grow with your application needs.

---

## Directory Structure

```plaintext
streamlit_app/
├── app.py                  # Main entry point for the Streamlit app
├── pages/
│   ├── __init__.py
│   ├── home.py             # Home page logic
│   ├── about.py            # About page logic
│   ├── dashboard.py        # Dashboard logic
├── components/
│   ├── __init__.py
│   ├── navbar.py           # Navigation bar component
│   ├── sidebar.py          # Sidebar component
│   ├── footer.py           # Footer component
├── utils/
│   ├── __init__.py
│   ├── decorators.py       # Common decorators (auth, logging, etc.)
│   ├── helpers.py          # Helper functions
│   ├── url_manager.py      # URL parameter handling
├── static/
│   ├── styles.css          # CSS styles (if needed)
├── data/
│   ├── sample_data.json    # Example data storage
├── config.py               # Configuration file
└── requirements.txt        # Python dependencies
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/streamlit-starter.git
   cd streamlit-starter
   ```

2. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## Usage

### Adding Pages
1. Create a new file under `pages/` (e.g., `example.py`).
2. Add a `render()` function in the new page file:
   ```python
   import streamlit as st

   def render():
       st.title("Example Page")
       st.write("Content for your new page.")
   ```
3. Add the page to the navbar in `components/navbar.py`:
   ```python
   options = {
       "Home": "home",
       "About": "about",
       "Dashboard": "dashboard",
       "Example": "example"
   }
   ```

### URL Parameters
- The app uses query parameters for routing.
- Example: `http://localhost:8501/?page=dashboard` will load the `dashboard` page.

### Custom Decorators
- Add reusable decorators in `utils/decorators.py` for tasks like authentication or logging:
   ```python
   def sample_decorator(func):
       def wrapper(*args, **kwargs):
           # Add custom logic here
           return func(*args, **kwargs)
       return wrapper
   ```

### Styling
- Add custom CSS to `static/styles.css` and include it in the app:
   ```python
   st.markdown('<style>' + open('static/styles.css').read() + '</style>', unsafe_allow_html=True)
   ```

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/new-feature
   ```
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

[Your Name](https://github.com/yourusername)  
Feel free to reach out for suggestions, improvements, or general feedback!

---

Happy Streamlit-ing! 🚀