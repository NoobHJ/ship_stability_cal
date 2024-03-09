import React, { useState } from "react";
import "./App.css"; // CSS 파일을 import 합니다.

function App() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    console.log(event.target.files[0]);
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload-stl", {
        method: "POST",
        body: formData,
      });
      // handle response as needed
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1> 선박 계산</h1>
        <div className="background"></div>
        <img src="/logo.svg" className="App-logo" alt="logo" />{" "}
        <h2> 3D cad(.stl) 모델을 업로드 해주세요 </h2>
        <input type="file" accept=".stl" onChange={handleFileChange} />
        <button className="button" onClick={handleSubmit}>
          업로드 및 Hydrostatic Table 만들기
        </button>
      </header>
    </div>
  );
}

export default App;
