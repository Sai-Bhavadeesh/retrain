import { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import Loader from "react-loader-spinner";
import UploadService from "../services/UploadService";

const Upload = () => {
  const imageFileTypes = ["JPG", "PNG", "JPEG"];
  const [imageFile, setImageFile] = useState();
  const annotationFileTypes = ["PLAIN", "XML"];
  const [annotationFile, setAnnotationFile] = useState();
  const [label, setLabel] = useState("None");
  const [busy, setBusy] = useState(false);

  const handleImageChange = (file: any) => {
    setImageFile(file);
  };

  const handleAnnotationChange = (file: any) => {
    setAnnotationFile(file);
  };

  const handleLabelRadio = async (e: string) => {
    setLabel(e);
    if (label !== "None") {
      setBusy(true);
      await UploadService(imageFile, annotationFile, label);
      setBusy(false);
    }
  };

  return (
    <div>
      {busy ? (
        <div>
          <Loader type="ThreeDots" color="Grey" />{" "}
        </div>
      ) : (
        <div>
          <h3 style={{ marginTop: 20, marginBottom: 20 }}>Upload image</h3>
          <FileUploader
            handleChange={handleImageChange}
            name="image"
            types={imageFileTypes}
            maxSize={200}
            onTypeError={(err: any) => console.log(err)}
            onSizeError={(file: any) => console.log(file)}
          />
          <h3 style={{ marginTop: 20, marginBottom: 20 }}>
            Upload Annotations
          </h3>
          <FileUploader
            handleChange={handleAnnotationChange}
            name="annotation"
            types={annotationFileTypes}
            maxSize={200}
            onTypeError={(err: any) => console.log(err)}
            onSizeError={(file: any) => console.log(file)}
          />
          {annotationFile !== undefined && imageFile !== undefined ? (
            <div style={{ marginTop: 20, marginBottom: 20 }}>
              <h3>Select Label</h3>
              <ul className="select">
                <input
                  type="radio"
                  id="None"
                  name={label}
                  value="None"
                  defaultChecked={true}
                  onClick={(e) => handleLabelRadio(e.currentTarget.value)}
                />
                <label htmlFor="None">None</label>
                <br />
                <input
                  type="radio"
                  id="burrito"
                  name={label}
                  value="burrito"
                  onClick={(e) => handleLabelRadio(e.currentTarget.value)}
                />
                <label htmlFor="burrito">Burrito</label>
                <br />
                <input
                  type="radio"
                  id="sizzli_top"
                  name={label}
                  value="sizzli_top"
                  onClick={(e) => handleLabelRadio(e.currentTarget.value)}
                />
                <label htmlFor="sizzli_top">Sizzli Top</label>
                <br />
                <input
                  type="radio"
                  id="sizzli_bottom"
                  name={label}
                  value="sizzli_bottom"
                  onClick={(e) => handleLabelRadio(e.currentTarget.value)}
                />
                <label htmlFor="sizzli_bottom">Sizzli Bottom</label>
                <br />
                <input
                  type="radio"
                  id="yolo_can"
                  name={label}
                  value="yolo_can"
                  onClick={(e) => handleLabelRadio(e.currentTarget.value)}
                />
                <label htmlFor="yolo_can">Yolo Can</label>
                <br />
                <input
                  type="radio"
                  id="yolo_empty"
                  name={label}
                  value="yolo_empty"
                  onClick={(e) => handleLabelRadio(e.currentTarget.value)}
                />
                <label htmlFor="yolo_empty">Yolo Empty</label>
                <br />
                <input
                  type="radio"
                  id="hashbrown-yolo"
                  name={label}
                  value="hashbrown-yolo"
                  onClick={(e) => handleLabelRadio(e.currentTarget.value)}
                />
                <label htmlFor="hashbrown-yolo">Hashbrown Yolo</label>
                <br />
              </ul>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
};

export default Upload;
