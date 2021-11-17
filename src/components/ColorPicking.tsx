import { useState } from "react";
import AddNewProduct from "./AddNewProduct";
import ColorDetection from "./ColorDetection";

const ColorPicking = () => {
  const [option, setOption] = useState("color");

  const handleOptionRadio = (e: string) => {
    setOption(e);
  };

  return (
    <div>
      <h3>Choose an option</h3>
      <ul className="select">
        <input
          type="radio"
          id="color"
          name={option}
          value="color"
          defaultChecked={true}
          onClick={(e) => handleOptionRadio(e.currentTarget.value)}
        />
        <label htmlFor="color">Color Code Extraction</label>
        <br />
        <input
          type="radio"
          id="add"
          name={option}
          value="add"
          onClick={(e) => handleOptionRadio(e.currentTarget.value)}
        />
        <label htmlFor="add">Add New Product</label>
      </ul>
      <div>{option === "color" ? <ColorDetection /> : <AddNewProduct />}</div>
    </div>
  );
};

export default ColorPicking;
