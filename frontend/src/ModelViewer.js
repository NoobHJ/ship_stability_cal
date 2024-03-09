import React from "react";
import { useLoader } from "@react-three/fiber";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";

function ModelViewer({ stlUrl }) {
  stlUrl = "../../backend/uploaded_stl_files/test1.stl";
  const { nodes } = useLoader(STLLoader, stlUrl);

  return (
    <mesh>
      <primitive object={nodes} />
    </mesh>
  );
}

export default ModelViewer;
