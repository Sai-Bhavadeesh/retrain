import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import Loader from "react-loader-spinner";
import DownloadService from "../services/DownloadService";
import RetrainService from "../services/RetrainService";

const RetrainorDownload = (props: any) => {
  const [label, setLabel] = useState("None");
  const [weights, setWeights] = useState("");
  const [epochs, setEpochs] = useState(0);
  const [busy, setBusy] = useState(false);
  const textRef = React.createRef<HTMLInputElement>();
  const numberRef = React.createRef<HTMLInputElement>();

  const handleTextInput = () => {
    setWeights(textRef.current?.value ?? "");
  };

  const handleNumberInput = () => {
    setEpochs(parseInt(numberRef.current?.value ?? "0"));
  };

  const handleLabelRadio = (e: string) => {
    setLabel(e);
  };

  const callRetrainModel = async () => {
    if (label !== "None") {
      setBusy(true);
      await RetrainService(label, label, weights, epochs);
      setBusy(false);
    }
  };

  const callDownloadModel = async () => {
    if (label !== "None") {
      setBusy(true);
      await DownloadService(label);
      setBusy(false);
    }
  }

  return (
    <div>
      {busy ? (
        <div>
          <Loader type="ThreeDots" color="Grey" />{" "}
        </div>
      ) : (
        <div>
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
          </ul>
          {props.isDownload ? (
            <Form style={{ paddingRight: "35%" }}>
              <Button
                variant="primary"
                type="submit"
                onClick={callDownloadModel}
              >
                Download Zip
              </Button>
            </Form>
          ) : (
            <Form style={{ paddingRight: "35%" }}>
              <Form.Group className="mb-3" controlId="weights">
                <Form.Label>Weight Name</Form.Label>
                <Form.Control
                  ref={textRef}
                  type="text"
                  placeholder="Enter weights name"
                  onChange={handleTextInput}
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="epochs">
                <Form.Label>Number of epochs</Form.Label>
                <Form.Control
                  ref={numberRef}
                  type="number"
                  placeholder="Enter number of epochs"
                  onChange={handleNumberInput}
                />
              </Form.Group>
              <Button
                variant="primary"
                type="submit"
                onClick={callRetrainModel}
              >
                Re-Train
              </Button>
            </Form>
          )}
        </div>
      )}
    </div>
  );
};

export default RetrainorDownload;
