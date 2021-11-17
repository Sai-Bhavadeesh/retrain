import { useState } from "react";
import { Dropdown } from "react-bootstrap";

const ColorDetection = () => {
  const [selectedStore, setSelectedStore] = useState("Select Store ID");
  const [selectedWarmer, setSelectedWarmer] = useState("Select Warmer");
  const [selectedFile, setSelectedFile] = useState("Select File");
  const [selectedImage, setSelectedImage] = useState("Select Image");

  const handleStoreDropDown = (e: string) => {
    setSelectedStore(e);
  };

  const handleWarmerDropDown = (e: string) => {
    setSelectedWarmer(e);
  };

  const handleFileDropDown = (e: string) => {
    setSelectedFile(e);
  };

  const handleImageDropDown = (e: string) => {
    setSelectedImage(e);
  };

  return (
    <div>
      <h3>Color detection of sizzli box</h3>
      <h5>Choose store ID</h5>
      <Dropdown>
        <Dropdown.Toggle
          variant="success"
          id="dropdown-basic"
          style={{ backgroundColor: "grey" }}
        >
          {selectedStore}
        </Dropdown.Toggle>
        <Dropdown.Menu>
          <Dropdown.Item onClick={() => handleStoreDropDown("Store 1")}>
            Store 1
          </Dropdown.Item>
          <Dropdown.Item onClick={() => handleStoreDropDown("Store 2")}>
            Store 2
          </Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
      {selectedStore !== "Select Store ID" ? (
        <div>
          <h5>Choose the Warmer</h5>
          <Dropdown>
            <Dropdown.Toggle
              variant="success"
              id="dropdown-basic"
              style={{ backgroundColor: "grey" }}
            >
              {selectedWarmer}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.Item onClick={() => handleWarmerDropDown("Warmer 1")}>
                Warmer 1
              </Dropdown.Item>
              <Dropdown.Item onClick={() => handleWarmerDropDown("Warmer 2")}>
                Warmer 2
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
          <div>
            {selectedWarmer !== "Select Warmer" ? (
              <div>
                <h5>Choose the file to collect images</h5>
                <Dropdown>
                  <Dropdown.Toggle
                    variant="success"
                    id="dropdown-basic"
                    style={{ backgroundColor: "grey" }}
                  >
                    {selectedFile}
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                    <Dropdown.Item onClick={() => handleFileDropDown("File 1")}>
                      File 1
                    </Dropdown.Item>
                    <Dropdown.Item onClick={() => handleFileDropDown("File 2")}>
                      File 2
                    </Dropdown.Item>
                  </Dropdown.Menu>
                </Dropdown>
                <div>
                  {selectedFile !== "Select File" ? (
                    <div>
                      {" "}
                      <h5>Choose an Image</h5>
                      <Dropdown>
                        <Dropdown.Toggle
                          variant="success"
                          id="dropdown-basic"
                          style={{ backgroundColor: "grey" }}
                        >
                          {selectedImage}
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                          <Dropdown.Item
                            onClick={() => handleImageDropDown("Image 1")}
                          >
                            Image 1
                          </Dropdown.Item>
                          <Dropdown.Item
                            onClick={() => handleImageDropDown("Image 2")}
                          >
                            Image 2
                          </Dropdown.Item>
                        </Dropdown.Menu>
                      </Dropdown>
                    </div>
                  ) : null}
                </div>
              </div>
            ) : null}
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default ColorDetection;