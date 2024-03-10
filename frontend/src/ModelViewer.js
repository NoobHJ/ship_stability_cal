import React, { Suspense, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import { useLoader } from "@react-three/fiber";

function STLViewer({ url }) {
  const stl = useLoader(STLLoader, url);

  return (
    <mesh>
      <primitive object={stl} />
      <meshStandardMaterial color={"gray"} />
    </mesh>
  );
}

function ModelViewer() {
  const [fileUrl, setFileUrl] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setFileUrl(url);
    }
  };
  return (
    <>
      <input type="file" onChange={handleFileChange} />
      <Canvas camera={{ position: [0, 0, 100], fov: 70 }}>
        <Suspense fallback={null}>
          {fileUrl && <STLViewer url={fileUrl} />}
        </Suspense>
        <ambientLight intensity={0.5} />
        <directionalLight position={[0, 0, 5]} />
      </Canvas>
    </>
  );
}

export default ModelViewer;
