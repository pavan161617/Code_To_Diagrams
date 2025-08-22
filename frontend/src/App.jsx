import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import mermaid from "mermaid";

function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [diagramType, setDiagramType] = useState("flowchart"); // flowchart, sequence, statemachine, class
  const [mermaidCode, setMermaidCode] = useState("");
  const diagramRef = useRef(null);

  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, theme: "default" });
  }, []);

  useEffect(() => {
    if (!mermaidCode || !diagramRef.current) return;
    const renderMermaid = async () => {
      try {
        const { svg } = await mermaid.render("diagramSVG", mermaidCode);
        diagramRef.current.innerHTML = svg;
      } catch (e) {
        console.error("Mermaid render error:", e);
        diagramRef.current.innerHTML =
          "<p style='color:red'>Failed to render diagram</p>";
      }
    };
    renderMermaid();
  }, [mermaidCode]);

  const generateDiagram = async () => {
    if (!code) return alert("Enter some code first!");
    try {
      const res = await axios.post("http://127.0.0.1:8000/generate-diagram", {
        code_snippet: code,
        language, // send only what backend expects
      });
      // Pick the selected diagram type from backend response
      const keyMap = {
        flowchart: "flowchart",
        sequence: "sequence",
        statemachine: "statemachine",
        class: "class",
      };
      setMermaidCode(res.data[keyMap[diagramType]]);
    } catch (err) {
      console.error(err);
      alert("Error generating diagram. Check backend logs.");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Code-to-Diagram AI</h1>

      <textarea
        rows="10"
        cols="70"
        placeholder="Paste your code here"
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      <div style={{ margin: "10px 0" }}>
        <label>
          Language:
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            <option value="python">Python</option>
            <option value="java">Java</option>
            <option value="c">C</option>
          </select>
        </label>

        <label style={{ marginLeft: "20px" }}>
          Diagram Type:
          <select
            value={diagramType}
            onChange={(e) => setDiagramType(e.target.value)}
          >
            <option value="flowchart">Flowchart</option>
            <option value="sequence">Sequence Diagram</option>
            <option value="statemachine">State Machine</option>
            <option value="class">UML Class</option>
          </select>
        </label>
      </div>

      <button onClick={generateDiagram}>Generate Diagram</button>

      <div style={{ marginTop: "20px" }}>
        <h3>Diagram:</h3>
        <div ref={diagramRef}></div>
      </div>
    </div>
  );
}

export default App;
