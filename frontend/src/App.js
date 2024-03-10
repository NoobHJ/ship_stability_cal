import React, { useState } from "react";
import "./App.css";
import { Canvas } from "@react-three/fiber";
import ModelViewer from "./ModelViewer";

function App() {
  const [file, setFile] = useState(null);
  const [stlUrl, setStlUrl] = useState(null);
  const [serverMessage, setServerMessage] = useState(""); // 서버로부터 받은 메시지 상태 추가

  const handleFileChange = (event) => {
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
      const data = await response.json();
      setStlUrl(data.stlUrl);
      setServerMessage(data.message);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Hydrostatic Table</h1>
        <div className="background"></div>
        <img src="/logo.svg" className="App-logo" alt="logo" />
        <h2>3D cad(.stl) 모델을 업로드 해주세요</h2>
        <input type="file" accept=".stl" onChange={handleFileChange} />
        <button className="button" onClick={handleSubmit}>
          업로드 및 Hydrostatic Table 만들기
        </button>
        <h4>업로드 후 30초 정도 로딩이 필요합니다</h4>
      </header>
      <div className="server-message">{serverMessage}</div>
      <Canvas style={{ width: "100%", height: "500px" }}>
        {stlUrl && <ModelViewer stlUrl={stlUrl} />}
      </Canvas>
    </div>
  );
}

export default App;
