import { useState } from "react";

import Annotate from "./Annotate";
import ColorPicking from "./ColorPicking";
import RetrainorDownload from "./RetrainorDownload";
import Upload from "./Upload";

const Select = () => {
  const [selected, setSelected] = useState("Upload");

  const handleSetectedRadio = (e: string) => {
    setSelected(e);
  };

  return (
    <div className="select" style={{ textAlign: "center" }}>
      <h1>Retrain & Uploading new training data</h1>
      <div
        className="select_block"
        style={{ textAlign: "left", paddingLeft: "35%" }}
      >
        <h3>Select</h3>
        <ul className="select">
          <input
            type="radio"
            id="upload"
            name={selected}
            value="Upload"
            defaultChecked={true}
            onClick={(e) => handleSetectedRadio(e.currentTarget.value)}
          />
          <label htmlFor="upload">Upload</label>
          <br />
          <input
            type="radio"
            id="retrain"
            name={selected}
            value="Retrain"
            onClick={(e) => handleSetectedRadio(e.currentTarget.value)}
          />
          <label htmlFor="retrain">Retrain</label>
          <br />
          <input
            type="radio"
            id="download"
            name={selected}
            value="Download"
            onClick={(e) => handleSetectedRadio(e.currentTarget.value)}
          />
          <label htmlFor="download">Download</label>
          <br />
          <input
            type="radio"
            id="annotate"
            name={selected}
            value="Annotate"
            onClick={(e) => handleSetectedRadio(e.currentTarget.value)}
          />
          <label htmlFor="annotate">Annotate</label>
          <br />
          <input
            type="radio"
            id="color_picking"
            name={selected}
            value="color_picking"
            onClick={(e) => handleSetectedRadio(e.currentTarget.value)}
          />
          <label htmlFor="color_picking">Color picking</label>
          <br />
        </ul>
        <div>
          {selected === "Upload" ? (
            <Upload />
          ) : selected === "Retrain" ? (
            <RetrainorDownload isDownload={false} />
          ) : selected === "Download" ? (
            <RetrainorDownload isDownload={true} />
          ) : selected === "Annotate" ? (
            <Annotate />
          ) : selected === "color_picking" ? (
            <ColorPicking />
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default Select;
