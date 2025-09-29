# 📊 Code-to-Diagram Project

**Code-to-Diagram** is an interactive web application that converts source code into visual diagrams. It helps developers, students, and tech enthusiasts understand complex code structures, relationships, and logic flows easily.

## 🚀 Features
✅ Multi-language Support: Supports Python, Java, and C++ for diagram generation.  
✅ Interactive Visualization: Generates flowcharts, class diagrams, and sequence diagrams dynamically.  
✅ Step-by-step Analysis: Breaks down code into logical components with clear visual mapping.  
✅ Export Options: Save generated diagrams as PNG, SVG, or PDF for documentation purposes.  
✅ User-friendly Interface: Upload code files easily and view diagrams with an intuitive React.js interface.  

## 📊 Supported Diagram Types
- Flowcharts: Stepwise execution of code logic.  
- Class Diagrams: Class relationships, inheritance, and methods.  
- Sequence Diagrams: Function calls and execution order.  

## 🖥 System Requirements
- Node.js Version: 16+  
- React Version: 18+  
- Python Version: 3.10+  
- Libraries: react, react-dom, graphviz, d3, axios, flask (or fastapi), numpy, pandas  

## 📂 Project Structure
📂 Code-to-Diagram  
│── backend  
│   │── main.py            # Main backend file  
│   │── requirements.txt   # Python dependencies  
│   │── utils.py           # Helper functions  
│   │── __pycache__  
│       │── main.cpython-313.pyc  
│── frontend  
│   │── src                 # React source code  
│   │── node_modules        # Installed node packages  
│   │── index.html          # Entry HTML file  
│   │── vite.config.js      # Vite configuration  
│   │── package.json        # Node dependencies  
│   │── package-lock.json  
│── .gitignore              # Git ignore rules  
│── README.md               # Project documentation  

## 🔧 Setup & Installation
1. Clone the repository:  
git clone <your-repo-link>  
cd Code-to-Diagram  

2. Setup backend:  
cd backend  
python -m venv venv          # Optional virtual environment  
source venv/bin/activate     # On Windows: venv\Scripts\activate  
pip install -r requirements.txt  
python main.py  

3. Setup frontend:  
cd frontend  
npm install  
npm run dev  

4. Open the app in your browser (http://localhost:5173 by default for Vite).  

## 📜 Usage
1. Upload your source code file (Python, Java, or C++).  
2. Select the type of diagram you want (Flowchart, Class Diagram, Sequence Diagram).  
3. View the generated diagram interactively.  
4. Optionally, export the diagram as PNG, SVG, or PDF.  

## 📦 Example Output
Uploaded File: example.py  
Selected Diagram: Flowchart  
Visualization: Functions, loops, and decision branches dynamically visualized with arrows representing code flow.  

## 🏅 Future Enhancements
- Support for more programming languages (JavaScript, C#, Ruby).  
- Real-time diagram updates while typing code.  
- Add advanced sequence diagrams showing asynchronous calls.  
- Integrate with IDE plugins for instant code-to-diagram generation.  
- Improved UI/UX with dark mode and interactive zoom/pan for diagrams.  

## 🤝 Contributing
Contributions are welcome! Fork the repository, make improvements, and open a pull request.  

## 📧 Contact
Developer: Pavan Kumar  
GitHub: https://github.com/pavan161617  
LinkedIn: https://www.linkedin.com/in/pavan-kumar-b7639125a/  
Email: pavan90990@gmail.com  

⭐ If you find this project useful, please star the repository! ⭐
